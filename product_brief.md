# Product Brief: RSS and Newsletter Page Extractor Actor

## Target User

People who monitor public blogs, changelogs, newsletters, and archive pages but need clean feed URLs or normalized update links without building a custom scraper for every site.

## Problem

Many public sites expose RSS, Atom, or JSON feeds in page metadata, but users often miss them. Newsletter archive pages also contain update links that are useful for monitoring, research, or content ops, but the page structure varies by provider.

## MVP Promise

Submit public page URLs or saved HTML and receive:

1. declared RSS, Atom, or JSON feed URLs;
2. likely newsletter/archive/update item links;
3. normalized absolute URLs;
4. duplicate removal;
5. a compact JSON report per page.

## Differentiator

The first version focuses on feed discovery and conservative link extraction rather than broad crawling. That keeps support burden low and avoids authenticated/private data risk.

## First Publish Path

Apify Actor is the natural first marketplace because the utility is input-page-to-dataset shaped and can later add schedules/monitoring.

## Risk Boundary

Only public pages or user-supplied HTML are in scope. The actor should not bypass paywalls, login walls, CAPTCHAs, robots restrictions, or platform access controls.
