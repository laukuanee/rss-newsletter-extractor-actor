# Marketplace Listing Draft

## Product Name

RSS and Newsletter Page Extractor Actor

## Short Description

Find RSS, Atom, JSON feed links, and likely newsletter/archive update links from public pages.

## Longer Description

This Actor helps content ops, monitoring, research, and automation workflows discover feed URLs and update links from public blogs, changelogs, newsletter archives, and release pages. Provide public page URLs or saved HTML and receive normalized feed URLs, likely update-item links, duplicate removal, and per-page extraction stats.

## Key Features

- Detects declared RSS, Atom, and JSON feed metadata.
- Extracts likely newsletter, archive, changelog, release, update, issue, article, and post links.
- Normalizes relative links into absolute URLs.
- Removes duplicate feed and item URLs.
- Returns compact actor-style JSON with page-level stats.
- Keeps scope to public pages and user-supplied HTML.

## Differentiator

Many feed tools either require manual lookup or try to crawl too broadly. This MVP is deliberately narrow: feed discovery plus conservative update-link extraction from public pages, which reduces support burden and account-risk while still solving a repeated monitoring problem.

## Pricing Draft

- Free/evaluation: small page batches.
- Starter: scheduled checks for a modest number of public pages.
- Bulk/monitoring: higher page limits and historical change exports.

Public pricing and any support/availability claims need approval before marketplace publication.
