import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("rss_newsletter_extractor", ROOT / "rss_newsletter_extractor.py")
extractor = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["rss_newsletter_extractor"] = extractor
SPEC.loader.exec_module(extractor)


SAMPLE_HTML = """<!doctype html>
<html>
  <head>
    <title>Example Updates</title>
    <link rel="alternate" type="application/rss+xml" title="RSS" href="/feed.xml">
    <link rel="alternate" type="application/atom+xml" href="https://example.com/atom.xml">
  </head>
  <body>
    <a class="post-card" href="/updates/launch"> Launch notes </a>
    <a href="/newsletter/june">June newsletter</a>
    <a href="/about">About</a>
    <a href="/updates/launch">Duplicate Launch notes</a>
  </body>
</html>"""


class RssNewsletterExtractorTests(unittest.TestCase):
    def test_extracts_declared_feeds_and_likely_items(self):
        result = extractor.extract_from_html("https://example.com/blog", SAMPLE_HTML)

        self.assertEqual(result["source_url"], "https://example.com/blog")
        self.assertEqual(
            [feed["url"] for feed in result["feeds"]],
            ["https://example.com/feed.xml", "https://example.com/atom.xml"],
        )
        self.assertEqual(
            [item["url"] for item in result["items"]],
            ["https://example.com/updates/launch", "https://example.com/newsletter/june"],
        )
        self.assertEqual(result["stats"]["duplicate_links_removed"], 1)

    def test_run_actor_accepts_inline_html_pages(self):
        payload = {
            "pages": [
                {
                    "url": "https://example.com/blog",
                    "html": SAMPLE_HTML,
                }
            ]
        }

        result = extractor.run_actor(payload)

        self.assertEqual(result["page_count"], 1)
        self.assertEqual(result["total_feeds"], 2)
        self.assertEqual(result["total_items"], 2)
        self.assertEqual(result["pages"][0]["stats"]["links_seen"], 4)

    def test_run_actor_rejects_missing_pages(self):
        with self.assertRaises(ValueError) as context:
            extractor.run_actor({})

        self.assertIn("pages", str(context.exception))


if __name__ == "__main__":
    unittest.main()
