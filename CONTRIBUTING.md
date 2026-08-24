# Contributing

## Adding a source

The whole collector is a declarative registry — a new source is usually one dict entry
in `skills/tech-event-scout/scripts/collect.py`:

```python
{"name": "example", "kind": "anchors", "url": "https://example.com/events/"},
```

1. **Check renderability first**: `curl -sL -A "Mozilla/5.0" <url> | grep -c <event-path>`.
   If the event list is in the raw HTML, it can be code-collected. If not, add it with
   `"js": True` so it becomes a WebFetch stub.
2. **Find the real query params**: inspect the page's `<form>` hidden inputs and JS setters —
   not the URL you see in the browser. (KINTEX ignores `searchStartMon`; only
   `searchStartDt/searchEndDt` work.)
3. **Reuse a parser kind** (`anchors`, `md-links`, `aws-json`, `coex-card`, `kintex-card`,
   `bexco-card`, `luma-json`) or add a small `parse_<name>` function and register it in
   `PARSERS`.
4. **Verify**: `python3 skills/tech-event-scout/scripts/collect.py --start <YYYYMMDD> --end <YYYYMMDD>`
   and check the new source appears with sane titles/dates/links.

## Updating SKILL.md

When a source's site changes (params renamed, calendar moves), update both
`skills/tech-event-scout/SKILL.md` and `docs/sources.md` in the same commit — they must
not drift apart.

## Commit style

Conventional Commits (`feat:`, `fix:`, `docs:`, `perf:` …), subject ≤50 chars, body
wrapped at 72. `--no-verify` is not allowed.

## Issues

Bug reports should include: the source name, the exact command run, and a few lines of
the output. Date-format regressions (a venue suddenly returning 0 events) are usually a
site-side param change — say so if you spotted it.
