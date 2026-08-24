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
better token cost, speed, and accuracy. Use web search only for events not covered by the sources below.

**Language rule**: always reply to the user in the language the user asked in (default: Korean).

## Verified sources (fetch directly)

| Source | List page | Notes |
|------|--------------|------|
| COEX full schedules | `https://www.coex.co.kr/event/full-schedules/?var_page=1&search_start_date=2026.08.24&search_end_date=2026.09.24&list_type=LIST` | LIST type with date query + `var_page` pagination. First stop for most Korean AI events |
| KINTEX list | `https://www.kintex.com/web/ko/event/list.do?searchType=&searchStartMon=202608&searchEndMon=202608&searchStartDt=&searchEndDt=` | Month-range query (`searchStartMon`/`searchEndMon`). JS-rendered; dates may shift — cross-check |
| BEXCO list | `https://www.bexco.co.kr/kor/CMS/EventScheduleMgr/list.do?robot=Y&mCode=MN214&page=2` | `page` pagination. Busan venue |
| AI Summit Seoul | `https://www.aisummit.co.kr/` | Korea's largest AI conference. 3rd week of August, COEX (2026: 8/19-21) |
| AWS events | `https://aws.amazon.com/ko/events/` | No specific dates listed — fetch `aws.amazon.com/events/reinvent/` directly |
| Google Cloud Next | `https://www.googlecloudevents.com/next-vegas` | Every April, Las Vegas |
| OpenAI DevDay | `https://openai.com/devday/` | WebFetch gets 403 — use announcement post `openai.com/index/devday-<year>/` or WebSearch |
| Anthropic | `https://www.anthropic.com/events` | Check frequently |
| Groq | `https://groq.com/events/` | Official dates are published late |
| World Summit AI | `https://worldsummit.ai/` | World's largest global AI conference. Every October, Amsterdam |
| Industrial AI EXPO | `https://industrialaiexpo.or.kr/` | Korea's flagship industrial-AI expo. Every October, KINTEX |
| SLEXN H2 roundup | `https://www.slexn.com/major-domestic-and-international-ai-conferences-in-the-second-half-of-2026/` | Annual domestic+global list, secondary source. Re-search with the year swapped. Adopt only after cross-checking the official site |
| AWS events | `https://aws.amazon.com/ko/events/` | No dates on the hub — fetch the specific event page (e.g. re:Invent) |
| Google Cloud events | `https://cloud.google.com/events` | Filter UI state is in the URL (`?ser=...`); use WebSearch if filters don't apply |
| Anthropic events | `https://www.anthropic.com/events#events` | Check frequently |
| OpenAI events | `https://academy.openai.com/public/events` | DevDay page gets 403 on WebFetch |
| Event-us | `https://event-us.kr/` | Korean dev community events |
| onoffmix | `https://www.onoffmix.com/event/main?s=%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A0%20ai%20chatgpt%20%EC%B1%97gpt` | Korean event aggregator; `s=` keyword query |
| Luma Seoul | `https://luma.com/seoul` | Community/tech meetups, Seoul calendar |
| dev-conf-replay | `https://github.com/hibuz/dev-conf-replay` | Korean dev conference replay archive — past editions for annual-cycle inference |
| Dev-Event | `https://github.com/brave-people/Dev-Event` | Korean dev events/CFP aggregator, updated continuously |

## Annual cycle reference (verified 2026 values)

| Event | Timing | Location |
|------|------|------|
| Google Cloud Next | April | Las Vegas |
| AWS Summit Seoul | May (2026: 5/20-21) | COEX |
| Public AI Expo | June | KINTEX |
| AI Summit Seoul & Expo | 3rd week of August (2026: 8/19-21) | COEX |
| OpenAI DevDay | Late September (2026: 9/29, application deadline 9/17) | San Francisco |
| World Summit AI | Early October (2026: 10/7-8, World AI Week 10/5-9) | Amsterdam |
| Industrial AI EXPO | October (2026: 10/21-23) | KINTEX |
| AIoT Korea | Early November (2026: 11/3-6) | COEX |
| AWS re:Invent | Late Nov–early Dec (2026: 11/30-12/4) | Las Vegas |
| Softwave | Early December (2026: 12/2-4) | COEX |

## Workflow

1. **Scope**: if topic, period, or region is unspecified, ask. Defaults: 3 months from today, domestic + major global.
2. **Primary collection**: WebFetch the venue list pages with the target date range as query params
   (COEX `search_start_date`/`search_end_date`, KINTEX `searchStartMon`/`searchEndMon`), walking each
   `var_page`/`page`/pagination until the range is covered. Then keyword-filter the list (AI, 인공지능,
   테크, IT, 소프트웨어, 보안, 개발, 클라우드, 데이터, 로봇 …) — drop everything else.
3. **Detail-link extraction** — link the event's own official page, never the venue list/calendar page:
   - COEX: open the event's venue detail page, take the "홈페이지 바로가기" link
   - KINTEX: open the detail page, take the homepage URL shown in the body (plain URL text)
   - BEXCO: take the "참가 안내" link
   - Aggregators (onoffmix, Event-us, Luma, GitHub lists): open the event detail page and take its
     official/homepage link if present; otherwise link the detail page itself
4. **Supplementary search**: only for events missing from the sources (Gemini-related, hackathons, CFPs).
5. **Verification**: confirm date, venue, registration on each event's official page. Never finalize on
   secondhand blog citations alone.
6. **Dedupe & output**: use the format below. Exclude ended events; list imminent CFP deadlines in a
   separate section.

## Output format

| Event | Organizer | Dates | Venue | Registration | CFP | Link | Source |

- Dates: `2026-09-17 ~ 09-18`. If unconfirmed: `(TBD)`.
- Link: the event's own detail/official page, never the calendar or list page it was found on.
- Mark unofficial sources. State the as-of date in the answer (e.g. "as of 2026-08-24").

## Pitfalls

- **Year confusion**: search results mix past editions. Never report a past major event (e.g. AI Summit
  2026 = ended 8/19-21) as upcoming.
- **KINTEX calendar JS**: fetched date-to-event mapping can be off. Recheck against adjacent event dates.
- **COEX calendar date errors**: ended events have appeared under wrong months (2026: AI Summit, ended
  8/19-21, was listed at 9/19-21). Always cross-check calendar dates against the organizer's official site.
- **re:Invent year confusion**: 2025=12/1-5, 2026=11/30-12/4 — verify the edition year before reporting.
- **Late-August COEX weeks**: dominated by autonomous driving/EV and pharma-bio — pure AI events may not
  exist. "No AI events in this period" is a valid result.
