# Terminal Demo Capture

## Test Suite

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.030s

OK
```

## Sample Output

```json
{
  "page_count": 1,
  "total_feeds": 2,
  "total_items": 2,
  "pages": [
    {
      "source_url": "https://example.com/blog",
      "feeds": [
        {
          "url": "https://example.com/feed.xml",
          "type": "rss",
          "title": "RSS"
        },
        {
          "url": "https://example.com/atom.xml",
          "type": "atom",
          "title": "atom"
        }
      ],
      "items": [
        {
          "url": "https://example.com/updates/launch",
          "title": "Launch notes",
          "score": 2
        },
        {
          "url": "https://example.com/newsletter/june",
          "title": "June newsletter",
          "score": 1
        }
      ],
      "stats": {
        "links_seen": 4,
        "feeds_found": 2,
        "items_found": 2,
        "duplicate_links_removed": 1
      }
    }
  ]
}
```

## Apify-Style Dataset Records

```jsonl
{"record_type": "feed", "source_url": "https://example.com/blog", "title": "RSS", "type": "rss", "url": "https://example.com/feed.xml"}
{"record_type": "feed", "source_url": "https://example.com/blog", "title": "atom", "type": "atom", "url": "https://example.com/atom.xml"}
{"record_type": "item", "score": 2, "source_url": "https://example.com/blog", "title": "Launch notes", "url": "https://example.com/updates/launch"}
{"record_type": "item", "score": 1, "source_url": "https://example.com/blog", "title": "June newsletter", "url": "https://example.com/newsletter/june"}
```
