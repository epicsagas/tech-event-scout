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
| COEX calendar | `https://www.coex.co.kr/event/exhibitions-calendar/` | Monthly calendar. First stop for most Korean AI events |
| KINTEX calendar | `https://www.kintex.com/web/ko/event/clist.do` | JS-rendered; dates may shift when fetched — cross-check date and event name |
| AI Summit Seoul | `https://www.aisummit.co.kr/` | Korea's largest AI conference. 3rd week of August, COEX (2026: 8/19-21) |
| AWS events | `https://aws.amazon.com/ko/events/` | No specific dates listed — fetch `aws.amazon.com/events/reinvent/` directly |
| Google Cloud Next | `https://www.googlecloudevents.com/next-vegas` | Every April, Las Vegas |
| OpenAI DevDay | `https://openai.com/devday/` | WebFetch gets 403 — use announcement post `openai.com/index/devday-<year>/` or WebSearch |
| Anthropic | `https://www.anthropic.com/events` | Check frequently |
| Groq | `https://groq.com/events/` | Official dates are published late |
| World Summit AI | `https://worldsummit.ai/` | World's largest global AI conference. Every October, Amsterdam |
| Industrial AI EXPO | `https://industrialaiexpo.or.kr/` | Korea's flagship industrial-AI expo. Every October, KINTEX |
| SLEXN H2 roundup | `https://www.slexn.com/major-domestic-and-international-ai-conferences-in-the-second-half-of-2026/` | Annual domestic+global list, secondary source. Re-search with the year swapped. Adopt only after cross-checking the official site |

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
2. **Primary collection**: WebFetch the source table pages covering the period. COEX/KINTEX calendars
   are the starting point for domestic events.
3. **Supplementary search**: only for events missing from the sources (Gemini-related, hackathons, CFPs).
4. **Verification**: confirm date, venue, registration on each event's official page. Never finalize on
   secondhand blog citations alone.
5. **Dedupe & output**: use the format below. Exclude ended events; list imminent CFP deadlines in a
   separate section.

## Output format

| Event | Organizer | Dates | Venue | Registration | CFP | Link | Source |

- Dates: `2026-09-17 ~ 09-18`. If unconfirmed: `(TBD)`.
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
