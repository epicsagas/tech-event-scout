# tech-event-scout (English)

A multi-host agent plugin that tracks AI and tech events for you. It checks the
official sources directly — the COEX and KINTEX event calendars plus AWS, Google
Cloud, OpenAI, Anthropic, and Groq event pages — and puts conferences, expos,
and summits into one tidy summary.

[한국어 README](README.md) · [Collection sources](docs/sources.md)

## What it covers

- **Cloud**: AWS Summit Seoul, re:Invent, Google Cloud Next
- **AI platforms**: Anthropic (Claude), OpenAI DevDay, Google (Gemini), Groq
- **Korea events**: AI Summit Seoul & Expo, Public AI Expo, Industrial AI EXPO
- **More**: hackathons, CFPs (call for papers), AI summits

Instead of relying on search results alone, the skill fetches official list
pages first — faster, cheaper, and far less likely to surface stale or expired
events. The full source list and query patterns live in
[docs/sources.md](docs/sources.md).

## Example prompts

- "What AI events are happening at COEX in September?"
- "Summarize the next AWS and OpenAI event dates."
- "Any conference CFPs closing in the next 3 months?"

## Install

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
# If skills_guard blocks the install (AGENTS.md → CRITICAL persistence),
# disable plugins.scan_on_install in hermes config.
```

## License

MIT
