# RSS and Newsletter Page Extractor Actor

Status: local MVP seed.

This utility is the second build candidate from the Utility-to-Usage scanner after the CSV cleanup tool reached a live deployment.

## Product Shape

Discover feed and update links from public pages by:

- finding declared RSS, Atom, and JSON feed metadata;
- extracting likely newsletter, archive, changelog, release, and update links;
- normalizing relative URLs into absolute URLs;
- removing duplicates;
- returning actor-style JSON output.

## Run

Run the extractor CLI:

```powershell
C:\Users\lauku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\rss_newsletter_extractor.py --input .\samples\input.json --out .\samples\output.json
```

Run the Apify-style local entrypoint:

```powershell
C:\Users\lauku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\main.py
```

That writes newline-delimited records to `storage/datasets/default/records.jsonl`.

## Test

```powershell
C:\Users\lauku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest discover -s .\tests
```

## Publish Path

- First target: Apify Actor.
- Later variant: hosted monitor that runs scheduled checks and emits changed feeds/items.

Apify packaging files included:

- `apify.json`
- `INPUT_SCHEMA.json`
- `Dockerfile`
- `main.py`

## Risk Boundary

This MVP uses public pages or user-supplied HTML only. It does not handle logins, paywalls, CAPTCHAs, private data, or platform evasion.
