# tech-event-scout

AI·테크 행사를 찾아 주는 멀티호스트 에이전트 플러그인. 코엑스·킨텍스 달력과 AWS, Google
Cloud, OpenAI, Anthropic, Groq 같은 주요 플랫폼의 공식 페이지를 직접 확인해서, 놓치기 쉬운
컨퍼런스와 전시·서밋 일정을 한눈에 정리해 줍니다.

[English README](README.en.md) · [수집 소스 리스트](docs/sources.md)

## 어떤 걸 찾아주나요?

- **클라우드**: AWS Summit Seoul, re:Invent, Google Cloud Next
- **AI 플랫폼**: Anthropic(Claude), OpenAI DevDay, Google(Gemini), Groq
- **국내 행사**: AI Summit Seoul & Expo, 공공 AI 박람회, 산업AI EXPO — 코엑스·키텍스 중심
- **그 밖에**: 해커톤, CFP(발표자 모집), 각종 AI 서밋

검색에만 의존하지 않고 공식 리스트 페이지를 우선 확인하는 게 이 플러그인의 특징이에요.
그래서 결과가 빠르고, 지나가버린 행사를 예정인 것처럼 잘못 안내하는 일도 덜합니다.

전체 수집 소스와 조회 패턴은 [docs/sources.md](docs/sources.md)에서 확인하세요.

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

## 라이선스

MIT
