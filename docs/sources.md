# Collection Sources / 수집 소스 리스트

Full source table with query patterns and per-venue detail-link extraction rules lives in
[`skills/tech-event-scout/SKILL.md`](../skills/tech-event-scout/SKILL.md). This page is the
human-readable list of every site the skill queries.

## Venues (paginated lists, date queries)

| Venue | List page | Query |
|-------|-----------|-------|
| COEX (코엑스, Seoul) | https://www.coex.co.kr/event/full-schedules/ | `search_start_date`/`search_end_date` (YYYY.MM.DD) + `var_page`, `list_type=LIST` |
| KINTEX (킨텍스, Goyang) | https://www.kintex.com/web/ko/event/list.do | `searchStartDt`/`searchEndDt` (YYYY-MM-DD) + `pageIndex` |
| BEXCO (벡스코, Busan) | https://www.bexco.co.kr/kor/CMS/EventScheduleMgr/list.do?robot=Y&mCode=MN214 | `page` |

Detail links: COEX → "홈페이지 바로가기" on the venue detail page · KINTEX → homepage URL in the
detail body · BEXCO → "참가 안내" link.

## Platforms & flagship events

| Source | Page |
|-------|------|
| AWS events | https://aws.amazon.com/ko/events/ |
| AWS re:Invent | https://aws.amazon.com/events/reinvent/ |
| Google Cloud events | https://cloud.google.com/events |
| Google Cloud Next | https://www.googlecloudevents.com/next-vegas |
| Anthropic events | https://www.anthropic.com/events |
| OpenAI DevDay | https://devday.openai.com/ (DevDay + DevDay Exchanges incl. Seoul) |
| Groq events | https://groq.com/events/ |
| World Summit AI | https://worldsummit.ai/ |
| AI Summit Seoul | https://www.aisummit.co.kr/ |
| 산업AI EXPO | https://industrialaiexpo.or.kr/ |

## Korean community aggregators

| Source | Page |
|-------|------|
| onoffmix | https://www.onoffmix.com/ (`?s=<keyword>` search) |
| Event-us | https://event-us.kr/ |
| Luma (Seoul) | https://luma.com/seoul |
| Dev-Event (brave-people) | https://github.com/brave-people/Dev-Event |
| dev-conf-replay (hibuz) | https://github.com/hibuz/dev-conf-replay |
| SLEXN events | https://www.slexn.com/events/ (conferences + webinars; secondary — cross-check before adopting) |
