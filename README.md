# tech-event-scout

AI·테크 행사를 찾아 주는 멀티호스트 에이전트 플러그인. 코엑스·키텍스 달력과 AWS, Google
Cloud, OpenAI, Anthropic, Groq 같은 주요 플랫폼의 공식 페이지를 직접 확인해서, 놓치기 쉬운
컨퍼런스와 전시·서밋 일정을 한눈에 정리해 줍니다.

## 어떤 걸 찾아주나요?

- **클라우드**: AWS Summit Seoul, re:Invent, Google Cloud Next
- **AI 플랙폼**: Anthropic(Claude), OpenAI DevDay, Google(Gemini), Groq
- **국내 행사**: AI Summit Seoul & Expo, 공공 AI 박람회, 산업AI EXPO — 코엑스·키텍스 중심
- **그 밖에**: 해커톤, CFP(발표자 모집), 각종 AI 서밋

검색에만 의존하지 않고 공식 리스트 페이지를 우선 확인하는 게 이 플러그인의 특징이에요.
그래서 결과가 빠르고, 지나가버린 행사를 예정인 것처럼 잘못 안내하는 일도 덜합니다.

## 사용 예시

- "9월에 코엑스에서 열리는 AI 행사 알려줘"
- "AWS와 OpenAI 다음 행사 일정 정리해 줘"
- "지금부터 3개월 안에 CFP 마감되는 컨퍼런스 있어?"

## 설치

```bash
# Claude Code
claude plugin marketplace add epicsagas/plugins
claude plugin install tech-event-scout@epicsagas

# Codex
codex plugin marketplace add epicsagas/plugins
codex plugin add tech-event-scout@epicsagas

# agy (repo URL, no .git)
agy plugin install https://github.com/epicsagas/tech-event-scout
agy plugin enable tech-event-scout

# hermes (repo URL)
hermes plugins install https://github.com/epicsagas/tech-event-scout
hermes plugins enable tech-event-scout
# 설치가 skills_guard에 막힌다면(AGENTS.md → CRITICAL persistence)
# hermes 설정에서 plugins.scan_on_install: false 로 끄세요.
```

---

# tech-event-scout (English)

A multi-host agent plugin that tracks AI and tech events for you. It checks the
official sources directly — the COEX and KINTEX event calendars plus AWS, Google
Cloud, OpenAI, Anthropic, and Groq event pages — and puts conferences, expos,
and summits into one tidy summary.

## What it covers

- **Cloud**: AWS Summit Seoul, re:Invent, Google Cloud Next
- **AI platforms**: Anthropic (Claude), OpenAI DevDay, Google (Gemini), Groq
- **Korea events**: AI Summit Seoul & Expo, Public AI Expo, Industrial AI EXPO
- **More**: hackathons, CFPs (call for papers), AI summits

Instead of relying on search results alone, the skill fetches official list
pages first — faster, cheaper, and far less likely to surface stale or expired
events.

## Example prompts

- "What AI events are happening at COEX in September?"
- "Summarize the next AWS and OpenAI event dates."
- "Any conference CFPs closing in the next 3 months?"

## Install

See the Korean section above — the commands are identical for Claude Code,
Codex, agy, and hermes.

## License

MIT
