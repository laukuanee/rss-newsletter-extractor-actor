# Actor Contract Draft

## Input

```json
{
  "pages": [
    {
      "url": "https://example.com/blog",
      "html": "<html>optional saved HTML for testing or offline runs</html>"
    }
  ]
}
```

Fields:

- `pages`: required non-empty array.
- `url`: required public page URL.
- `html`: optional page HTML. If omitted, the local MVP fetches the public URL with a timeout and byte limit.

## Output

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
        }
      ],
      "items": [
        {
          "url": "https://example.com/updates/launch",
          "title": "Launch notes",
          "score": 1
        }
      ],
      "stats": {
        "links_seen": 3,
        "feeds_found": 1,
        "items_found": 1,
        "duplicate_links_removed": 0
      }
    }
  ]
}
```

## Error Cases

- Missing or empty `pages`.
- Page item without `url`.
- Non-HTML response when fetching a URL.
- Page larger than the configured byte limit.
- Network timeout or fetch failure.

## Future Actor Packaging

- Map `pages` to Apify input schema.
- Emit each feed and item as dataset records.
- Add optional depth-1 follow-up discovery for archive pages only.
- Add a scheduled-monitoring variant after the baseline actor is reliable.
