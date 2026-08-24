---
name: bug report
about: A source broke, dates look wrong, or the collector failed
labels: bug
---

**Source affected**
e.g. coex, kintex, luma-seoul — or "all"

**Command run**
```
python3 skills/tech-event-scout/scripts/collect.py --start YYYYMMDD --end YYYYMMDD
```

**Expected vs actual**
What you expected, what you got (paste a few output lines).

**Site change? (optional)**
Venue/portal sites quietly change query params. If you inspected the page and spotted a
renamed parameter or new calendar URL, note it here — it speeds up the fix a lot.
