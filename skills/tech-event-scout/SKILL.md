---
name: tech-event-scout
description: >-
  AI/테크 행사·컨퍼런스 정보 수집 (AI event & conference scout). AWS, GCP, Anthropic(Claude),
  OpenAI, Google Gemini, Groq 등 AI 플랫폼 행사와 서밋, 코엑스(COEX)·키텍스(KINTEX) 등
  국내외 행사 일정·등록·CFP 정보를 수집·요약. Use when the user asks about upcoming AI/tech
  events, conferences, summits, expos, registration deadlines, or CFPs.
---

# tech-event-scout

AI/tech event intelligence agent. **Fetch official list pages directly (WebFetch) before searching** —
better token cost, speed, and accuracy. Web search only for gaps the sources below don't cover.

**Language rule**: reply in the language the user asked in (default: Korean).

## Sources

### Venues (paginated lists with date queries)

| Source | URL pattern | Pagination / query |
|------|--------------|------|
| COEX | `https://www.coex.co.kr/event/full-schedules/?var_page=1&search_start_date=YYYY.MM.DD&search_end_date=YYYY.MM.DD&list_type=LIST` | date range + `var_page` |
| KINTEX | `https://www.kintex.com/web/ko/event/list.do?searchType=&searchStartMon=YYYYMM&searchEndMon=YYYYMM&searchStartDt=&searchEndDt=` | month range |
| BEXCO | `https://www.bexco.co.kr/kor/CMS/EventScheduleMgr/list.do?robot=Y&mCode=MN214&page=1` | `page` (Busan) |

### Platforms & flagship events

| Source | URL | Notes |
|------|--------------|------|
| AWS events | `https://aws.amazon.com/ko/events/` | Hub has no dates — fetch the specific event page (e.g. `aws.amazon.com/events/reinvent/`) |
| Google Cloud events | `https://cloud.google.com/events` | Filter state lives in URL (`?ser=...`); fall back to WebSearch if filters don't apply |
| Anthropic events | `https://www.anthropic.com/events#events` | Small, check quickly |
| OpenAI events | `https://devday.openai.com/` | DevDay site (was 403-prone under openai.com/devday/). DevDay Exchanges (Seoul, Tokyo, etc.) announced here |
| Groq | `https://groq.com/events/` | Dates published late |
| Google Cloud Next | `https://www.googlecloudevents.com/next-vegas` | Every April, Las Vegas |
| World Summit AI | `https://worldsummit.ai/` | Every October, Amsterdam |
| AI Summit Seoul | `https://www.aisummit.co.kr/` | 3rd week of August, COEX |
| Industrial AI EXPO | `https://industrialaiexpo.or.kr/` | Every October, KINTEX |

### Aggregators (Korean community events)

| Source | URL | Notes |
|------|--------------|------|
| onoffmix | `https://www.onoffmix.com/event/main?s=<keyword>` | `s=` keyword query |
| Event-us | `https://event-us.kr/` | Dev community events |
| Luma Seoul | `https://luma.com/seoul` | Meetup calendar; JS — API/render fallbacks above |
| Dev-Event | `https://github.com/brave-people/Dev-Event` | Events + CFPs, continuously updated |
| dev-conf-replay | `https://github.com/hibuz/dev-conf-replay` | Past-edition archive — annual-cycle inference |
| SLEXN events | `https://www.slexn.com/events/` | Conferences + webinars (AI/ML, DevOps, testing). Secondary — cross-check before adopting |

## Annual cycle reference (verified 2026 values)

| Event | Timing | Location |
|------|------|------|
| Google Cloud Next | April | Las Vegas |
| AWS Summit Seoul | May (2026: 5/20-21) | COEX |
| Public AI Expo | June | KINTEX |
| AI Summit Seoul & Expo | 3rd week of August (2026: 8/19-21) | COEX |
| OpenAI DevDay | Late September (2026: 9/29, Fort Mason; apps closed; free keynote livestream; DevDay Exchange Seoul TBD) | San Francisco |
| AI Festa | Early October (2026: 10/6-8) — MSICT AI Week official, free | COEX Hall C |
| KES (한국전자전) | Mid October (2026: 10/13-16) | COEX Hall A/B, kes.org |
| World Summit AI | Early October (2026: 10/7-8, World AI Week 10/5-9) | Amsterdam |
| Industrial AI EXPO | October (2026: 10/21-23) | KINTEX |
| AIoT Korea | Early November (2026: 11/3-6) | COEX |
| AWS re:Invent | Late Nov–early Dec (2026: 11/30-12/4) | Las Vegas |
| Softwave | Early December (2026: 12/2-4) | COEX |

## Workflow

1. **Scope**: if topic, period, or region is unspecified, ask. Defaults: 3 months from today, domestic + major global.
2. **Run the collector first** (deterministic, near-zero tokens):
   `python3 skills/tech-event-scout/scripts/collect.py [--start YYYYMMDD --end YYYYMMDD] [name=url ...]`
   Fetches server-rendered sources (SLEXN, Dev-Event, onoffmix by default), keyword-filters, emits
   compact JSON. Read that JSON instead of WebFetching these pages.
3. **WebFetch only what the script can't do**: JS-rendered venue lists (COEX/KINTEX/BEXCO — build the
   date-query URLs from the source table, walk pagination), platform event pages (AWS/GCP/Anthropic/
   OpenAI), and Luma (`luma.com/seoul`). Batch these in one parallel round.

   JS-rendering fallback ladder, cheapest first — plain WebFetch often fails on these:
   a. **JSON API**: many sites serve the list from an open endpoint (`/api/...`, `.json`) — probe with
      curl before rendering anything; parse in the collector script or read directly.
   b. **Obscura headless**: `obscura-fetch` skill renders JS and returns text/links.
   c. **Selenium/Playwright**: last resort for sites blocking headless fetches.
4. **Keyword filter** (already applied by the script; apply manually to WebFetch results) — keep titles
   matching: AI, 인공지능, GPT, LLM, 생성형, 테크, IT, SW/소프트웨어, 개발, 컨퍼런스, 세미나,
   웨비나/웹비나, 밋업, 보안, 클라우드, 데이터, 로봇, 자율주행, AIoT, 해커톤, CFP. Online webinars
   count — don't drop them for being virtual. Drop the rest (art fairs, bio/pharma, education expos
   unless AI-tagged).
5. **Detail-link extraction** — link the event's own official page, never the list/calendar page:
   - COEX: venue detail page → "홈페이지 바로가기" link
   - KINTEX: detail page → homepage URL in body (plain URL text)
   - BEXCO: "참가 안내" link
   - Aggregators: detail page → official/homepage link if present, else the detail page itself
6. **Supplementary search**: only for gaps (Gemini-specific, hackathons, CFPs not in aggregators).
7. **Verification**: confirm date, venue, registration on the official page. Never finalize on
   secondhand blog citations alone.
8. **Dedupe & output**: format below. Exclude ended events; imminent CFP/registration deadlines in a
   separate section.

## Output format

| Event | Organizer | Dates | Venue | Registration | CFP | Link | Source |

- Dates: `2026-09-17 ~ 09-18`; unconfirmed: `(TBD)`.
- Link: event's own detail/official page.
- Mark unofficial sources. State the as-of date (e.g. "as of 2026-08-24").

## Pitfalls

- **Year confusion**: search results mix past editions. Never report a past event (AI Summit 2026 =
  ended 8/19-21) as upcoming. re:Invent: 2025=12/1-5, 2026=11/30-12/4.
- **Venue calendar date errors**: COEX listed the ended AI Summit at 9/19-21 instead of 8/19-21;
  KINTEX JS rendering shifts date-event mapping. Always cross-check against the organizer's site.
- **Deadline drift**: registration/CFP deadlines close while pages stay live (DevDay 2026 apps
  closed before the 9/17 published deadline). Re-verify deadline status, not just the date.
- **Late-August COEX weeks**: autonomous driving/EV and pharma-bio dominate — pure AI events may not
  exist. "No AI events in this period" is a valid result.
- **Token budget**: batch venue + platform fetches in one parallel round; WebFetch caches 15 min, so
  re-checking the same URL in one run is free — across runs, skip re-fetching pages already verified
  this session.
