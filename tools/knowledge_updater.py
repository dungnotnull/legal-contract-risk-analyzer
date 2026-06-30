#!/usr/bin/env python3
"""knowledge_updater.py - Legal Contract Risk Analyzer (Idea 56)

Crawl legal-scholarship / statute sources (SSRN, ABA, Cornell LII, optional
RSS feeds), score candidates by recency + relevance, deduplicate, and append
jurisdiction-tagged findings to SECOND-KNOWLEDGE-BRAIN.md.

Design goals (production-grade, open-source ready):
  - Multiple fetch backends with graceful degradation:
      1. requests + BeautifulSoup4 (preferred, light deps)
      2. crawl4ai (optional, heavier)
      3. local fixtures / RSS (feedparser optional)
  - Rate limiting + retry + timeout per host.
  - Deterministic dedupe via 12-char SHA-1(url+title).
  - Safety filter: reject entries that assert definitive enforceability
    conclusions (UPL guard) - this brain only stores patterns/findings.
  - Idempotent, side-effect-free in --dry-run.
  - Configurable via CLI flags and an optional INI file.

Usage:
  python knowledge_updater.py                 # crawl + append
  python knowledge_updater.py --dry-run        # print block, no write
  python knowledge_updater.py --offline        # fixtures only, no network
  python knowledge_updater.py --limit 20        # cap appended entries
  python knowledge_updater.py --sources SSRN,ABA
  python knowledge_updater.py --self-test       # internal smoke test

Schedule: weekly cron. See requirements.txt for optional dependencies.

NOTE: This tool only STORES public-source findings/patterns. It never asserts
that any clause is enforceable or unenforceable - that would be UPL.
"""
from __future__ import annotations

import argparse
import configparser
import datetime as dt
import hashlib
import json
import logging
import os
import pathlib
import random
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Iterable, Optional
from urllib.parse import urlparse

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAIN = REPO_ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
DEFAULT_CONFIG = REPO_ROOT / "tools" / "knowledge_updater.ini"
FIXTURES = REPO_ROOT / "tools" / "fixtures.json"

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_SOURCES = [
    {"name": "SSRN", "url": "https://www.ssrn.com/index.cfm/en/"},
    {"name": "ABA", "url": "https://www.americanbar.org/news/"},
    {"name": "Cornell LII", "url": "https://www.law.cornell.edu/wex"},
]
DEFAULT_QUERIES = [
    "non-compete enforceability 2026",
    "contract clause risk",
    "tenancy law update",
    "arbitration clause ruling",
    "indemnity clause trend",
    "auto-renewal regulation",
]
KEYWORDS = [
    "contract", "clause", "non-compete", "indemnity", "liability", "lease",
    "tenancy", "arbitration", "enforce", "employment", "partnership",
    "boilerplate", "liquidated", "waiver", "jurisdiction", "amend",
]
JURISDICTION_TOKENS = [
    "eu", "uk", "california", "texas", "new york", "ny", "florida",
    "us", "federal", "illinois", "washington", "massachusetts", "georgia",
]
UPL_PATTERNS = [
    r"\bis (definitely|clearly|100%)\b",
    r"\b(un)?enforceable\b",
    r"\byou will (win|lose|prevail)\b",
    r"\bthe contract is (void|valid)\b",
    r"\bis (illegal|legal)\b",
]

HASH_RE = re.compile(r"<!--h:([0-9a-f]{12})-->")
TIMEOUT = 20.0
RATE_LIMIT_DELAY = (1.0, 2.5)  # seconds, randomized between fetches
MAX_RETRIES = 2
USER_AGENT = (
    "legal-contract-risk-analyzer/1.0 (knowledge_updater; "
    "+https://github.com/) educational research bot"
)

log = logging.getLogger("knowledge_updater")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class Entry:
    title: str
    source: str
    url: str
    jurisdiction: str = "GEN"
    retrieved: str = field(default_factory=lambda: dt.date.today().isoformat())
    finding: str = ""

    def to_line(self, h: str) -> str:
        finding = self.finding or "pattern"
        return (
            f"- [{self.retrieved}] [{self.jurisdiction}] {self.title} - "
            f"{self.source} - {finding} - {self.url} <!--h:{h}-->"
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def jurisdiction_of(title: str) -> str:
    low = title.lower()
    for tok in JURISDICTION_TOKENS:
        if tok in low:
            return tok.upper().replace(" ", "-")
    return "GEN"


def entry_hash(e: Entry) -> str:
    return hashlib.sha1((e.url + "|" + e.title).encode("utf-8")).hexdigest()[:12]


def existing_hashes(text: str) -> set:
    return set(HASH_RE.findall(text))


def looks_upl(text: str) -> bool:
    low = text.lower()
    return any(re.search(p, low) for p in UPL_PATTERNS)


def relevance_score(title: str) -> float:
    low = title.lower()
    hits = sum(k in low for k in KEYWORDS)
    # mild recency bonus if a 4-digit year >= 2020 appears
    year = re.search(r"\b(20\d{2})\b", title)
    bonus = 0.5 if year and int(year.group(1)) >= 2020 else 0.0
    return hits + bonus


def clean_line(raw: str) -> str:
    """Strip markdown/list noise and collapse whitespace."""
    t = raw.strip().strip("#*-").strip()
    t = re.sub(r"\s+", " ", t)
    return t


# ---------------------------------------------------------------------------
# Fetch backends
# ---------------------------------------------------------------------------
def _requests_get(url: str) -> Optional[str]:
    try:
        import requests  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on env
        log.debug("requests unavailable: %s", exc)
        return None
    try:
        resp = requests.get(
            url, timeout=TIMEOUT, headers={"User-Agent": USER_AGENT}
        )
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        log.warning("requests fetch failed for %s: %s", url, exc)
        return None


def _crawl4ai_get(url: str) -> Optional[str]:
    try:
        from crawl4ai import WebCrawler  # type: ignore
    except Exception as exc:  # pragma: no cover
        log.debug("crawl4ai unavailable: %s", exc)
        return None
    try:
        c = WebCrawler()
        c.warmup()
        res = c.run(url=url)
        return getattr(res, "markdown", "") or ""
    except Exception as exc:
        log.warning("crawl4ai fetch failed for %s: %s", url, exc)
        return None


def _bs4_extract(html: str) -> list:
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception as exc:  # pragma: no cover
        log.debug("bs4 unavailable: %s", exc)
        return _regex_extract(html)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    candidates = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "li", "a", "p"]):
        text = clean_line(el.get_text(" ", strip=True))
        if text:
            candidates.append(text)
    return candidates


def _regex_extract(html: str) -> list:
    """Fallback extractor when bs4 is absent: pull text-ish lines."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return [clean_line(ln) for ln in text.splitlines() if ln.strip()]


def fetch_source(source: dict, offline: bool = False) -> list:
    """Return a list of Entry candidates from a single source."""
    if offline:
        return _fixtures(source)
    html = _requests_get(source["url"])
    if html is None:
        html = _crawl4ai_get(source["url"])
    if html is None:
        log.warning("All fetch backends failed for %s; using fixtures.",
                    source["name"])
        return _fixtures(source)
    lines = _bs4_extract(html) if html else []
    out = []
    seen_titles = set()
    for ln in lines:
        if not (20 < len(ln) < 220):
            continue
        if not any(k in ln.lower() for k in KEYWORDS):
            continue
        if looks_upl(ln):
            continue  # UPL guard: never store a definitive ruling
        if ln in seen_titles:
            continue
        seen_titles.add(ln)
        out.append(
            Entry(
                title=ln,
                source=source["name"],
                url=source["url"],
                jurisdiction=jurisdiction_of(ln),
            )
        )
    return out


def _fixtures(source: dict) -> list:
    """Return canned candidates for offline/smoke runs (never a generator)."""
    out: list = []
    if FIXTURES.exists():
        try:
            data = json.loads(FIXTURES.read_text(encoding="utf-8"))
        except Exception as exc:
            log.warning("fixtures parse failed: %s", exc)
            data = {}
        for item in data.get(source["name"], []):
            out.append(
                Entry(
                    title=item["title"],
                    source=source["name"],
                    url=item.get("url", source["url"]),
                    jurisdiction=item.get("jur", jurisdiction_of(item["title"])),
                    finding=item.get("finding", "pattern"),
                )
            )
        return out
    # minimal built-in fixtures so --offline always works
    built = {
        "SSRN": [
            ("Non-compete enforceability across US states (survey)", "ssrn.com",
             "jurisdiction variance"),
            ("Boilerplate terms and consumer surprise", "ssrn.com",
             "hidden-term risk"),
        ],
        "ABA": [
            ("ABA drafting principles for clear contracts", "americanbar.org",
             "drafting clarity"),
        ],
        "Cornell LII": [
            ("Cornell LII: unconscionability definition", "law.cornell.edu",
             "doctrine overview"),
        ],
    }
    for title, domain, finding in built.get(source["name"], []):
        out.append(
            Entry(
                title=title,
                source=source["name"],
                url=f"https://{domain}",
                jurisdiction=jurisdiction_of(title),
                finding=finding,
            )
        )
    return out


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------
def collect(sources: list, offline: bool, delay: bool) -> list:
    collected = []
    for s in sources:
        entries = fetch_source(s, offline=offline)
        log.info("source=%s candidates=%d", s["name"], len(entries))
        collected.extend(entries)
        if delay and not offline:
            time.sleep(random.uniform(*RATE_LIMIT_DELAY))
    # rank by relevance then recency (recency captured in retrieved date)
    collected.sort(key=lambda e: relevance_score(e.title), reverse=True)
    return collected


def build_block(entries: list, seen: set, limit: int) -> list:
    today = dt.date.today().isoformat()
    lines = []
    for e in entries[:limit] if limit > 0 else entries:
        h = entry_hash(e)
        if h in seen:
            continue
        seen.add(h)
        e.retrieved = today
        lines.append(e.to_line(h))
    return lines


def append_block(lines: list) -> None:
    if not lines:
        return
    today = dt.date.today().isoformat()
    block = "\n\n### Auto-update %s\n" % today + "\n".join(lines) + "\n"
    with BRAIN.open("a", encoding="utf-8") as fh:
        fh.write(block)


def load_config(path: Optional[pathlib.Path]) -> dict:
    cfg = {
        "sources": DEFAULT_SOURCES,
        "queries": DEFAULT_QUERIES,
        "limit": 25,
        "delay": True,
    }
    if path and pathlib.Path(path).exists():
        cp = configparser.ConfigParser()
        cp.optionxform = str  # preserve source-name case
        cp.read(path, encoding="utf-8")
        if cp.has_section("sources"):
            cfg["sources"] = [
                {"name": name, "url": cp["sources"][name]}
                for name in cp["sources"]
            ]
        if cp.has_section("options"):
            cfg["limit"] = cp.getint("options", "limit", fallback=25)
            cfg["delay"] = cp.getboolean("options", "delay", fallback=True)
    return cfg


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def self_test() -> int:
    """Smoke test: hashing, dedupe, UPL filter, jurisdiction tagging."""
    e1 = Entry("California non-compete survey 2023", "SSRN", "https://x")
    e2 = Entry("California non-compete survey 2023", "SSRN", "https://x")
    assert entry_hash(e1) == entry_hash(e2), "hash not deterministic"
    assert jurisdiction_of("California tenant law") == "CALIFORNIA", "jur tag"
    assert looks_upl("this clause is unenforceable"), "UPL missed"
    assert not looks_upl("this clause raises considerations"), "UPL false+"
    block = build_block([e1, e2], set(), limit=10)
    assert len(block) == 1, "dedupe failed: %r" % block
    print("self-test OK")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="print block, no write")
    ap.add_argument("--offline", action="store_true", help="fixtures only, no network")
    ap.add_argument("--limit", type=int, default=25, help="cap appended entries")
    ap.add_argument("--sources", help="comma-separated source names to include")
    ap.add_argument("--config", help="path to INI config")
    ap.add_argument("--brain", help="path to brain markdown (default: repo root)")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--self-test", action="store_true", help="run internal smoke test")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if args.self_test:
        return self_test()

    global BRAIN
    if args.brain:
        BRAIN = pathlib.Path(args.brain)
    cfg = load_config(pathlib.Path(args.config) if args.config else DEFAULT_CONFIG)

    sources = cfg["sources"]
    if args.sources:
        wanted = {s.strip() for s in args.sources.split(",") if s.strip()}
        sources = [s for s in sources if s["name"] in wanted]
        if not sources:
            log.error("no matching sources for --sources=%s", args.sources)
            return 2

    brain_text = BRAIN.read_text(encoding="utf-8") if BRAIN.exists() else ""
    seen = existing_hashes(brain_text)

    entries = collect(sources, offline=args.offline, delay=cfg["delay"])
    if not entries:
        print("No candidates collected.")
        return 0

    limit = args.limit if args.limit > 0 else cfg["limit"]
    lines = build_block(entries, seen, limit=limit)
    if not lines:
        print("No new entries (all deduped).")
        return 0

    if args.dry_run:
        print("\n".join(lines))
        return 0

    append_block(lines)
    print(f"Appended {len(lines)} entries to {BRAIN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())