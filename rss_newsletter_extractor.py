#!/usr/bin/env python3
"""Extract RSS/feed links and likely newsletter/archive items from public pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen


FEED_TYPES = {
    "application/rss+xml": "rss",
    "application/atom+xml": "atom",
    "application/feed+json": "json-feed",
    "application/json": "json",
}
ITEM_HINTS = (
    "post",
    "article",
    "archive",
    "newsletter",
    "issue",
    "update",
    "changelog",
    "release",
)


class PublicPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.feeds: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self._active_link: dict[str, str] | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "link":
            rel = attributes.get("rel", "").lower()
            mime_type = attributes.get("type", "").lower()
            href = attributes.get("href", "")
            if "alternate" in rel and href and mime_type in FEED_TYPES:
                self.feeds.append(
                    {
                        "url": href,
                        "type": FEED_TYPES[mime_type],
                        "title": clean_text(attributes.get("title", "")),
                    }
                )
        elif tag.lower() == "a" and attributes.get("href"):
            self._active_link = {
                "url": attributes["href"],
                "class": attributes.get("class", ""),
                "rel": attributes.get("rel", ""),
            }
            self._text_parts = []

    def handle_data(self, data: str) -> None:
        if self._active_link is not None:
            self._text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._active_link is not None:
            link = dict(self._active_link)
            link["text"] = clean_text(" ".join(self._text_parts))
            self.links.append(link)
            self._active_link = None
            self._text_parts = []


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def absolute_url(base_url: str, href: str) -> str:
    return urljoin(base_url, href)


def score_item(link: dict[str, str]) -> int:
    haystack = " ".join([link.get("url", ""), link.get("text", ""), link.get("class", ""), link.get("rel", "")]).lower()
    return sum(1 for hint in ITEM_HINTS if hint in haystack)


def dedupe_by_url(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    duplicates = 0
    for row in rows:
        url = row["url"]
        if url in seen:
            duplicates += 1
            continue
        seen.add(url)
        deduped.append(row)
    return deduped, duplicates


def extract_from_html(source_url: str, html: str) -> dict[str, Any]:
    parser = PublicPageParser()
    parser.feed(html)

    feeds = [
        {
            "url": absolute_url(source_url, feed["url"]),
            "type": feed["type"],
            "title": feed["title"] or feed["type"],
        }
        for feed in parser.feeds
    ]
    feeds, duplicate_feeds = dedupe_by_url(feeds)

    item_candidates: list[dict[str, Any]] = []
    for link in parser.links:
        score = score_item(link)
        if score <= 0:
            continue
        item_candidates.append(
            {
                "url": absolute_url(source_url, link["url"]),
                "title": link["text"] or absolute_url(source_url, link["url"]),
                "score": score,
            }
        )
    items, duplicate_items = dedupe_by_url(item_candidates)

    return {
        "source_url": source_url,
        "feeds": feeds,
        "items": items,
        "stats": {
            "links_seen": len(parser.links),
            "feeds_found": len(feeds),
            "items_found": len(items),
            "duplicate_links_removed": duplicate_feeds + duplicate_items,
        },
    }


def fetch_public_page(url: str, timeout_seconds: int = 10, max_bytes: int = 1_000_000) -> str:
    request = Request(url, headers={"User-Agent": "UtilityToUsageRSSExtractor/0.1 (+public feed discovery)"})
    with urlopen(request, timeout=timeout_seconds) as response:
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type and "application/xhtml" not in content_type:
            raise ValueError(f"Unsupported content type for {url}: {content_type or 'unknown'}")
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError(f"Page exceeds {max_bytes} byte limit: {url}")
    return data.decode("utf-8", errors="replace")


def run_actor(payload: dict[str, Any]) -> dict[str, Any]:
    pages = payload.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("Input must include a non-empty pages array")

    results: list[dict[str, Any]] = []
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("url"), str):
            raise ValueError("Each page must include a url")
        url = page["url"]
        html = page.get("html")
        if html is None:
            html = fetch_public_page(url)
        if not isinstance(html, str):
            raise ValueError(f"Page html must be text for {url}")
        results.append(extract_from_html(url, html))

    return {
        "page_count": len(results),
        "total_feeds": sum(len(page["feeds"]) for page in results),
        "total_items": sum(len(page["items"]) for page in results),
        "pages": results,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Actor-style JSON input file")
    parser.add_argument("--out", required=True, help="Output JSON path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = run_actor(payload)
    except Exception as exc:
        print(f"rss-newsletter-extractor error: {exc}", file=sys.stderr)
        return 1

    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
