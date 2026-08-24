# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-24

### Added
- Multi-host plugin (Claude Code, Codex, agy, hermes) with `tech-event-scout` skill
- `collect.py` deterministic aggregator: declarative source registry → one adapter pipeline
- Adapters: COEX (date query + pagination), KINTEX (`searchStartDt` + `pageUnit=30`),
  BEXCO (`schStartDate` + pages), AWS Summits (embedded JSON), SLEXN, Dev-Event,
  onoffmix (2 keyword queries), Luma Seoul (`__NEXT_DATA__`)
- Date-window, keyword (word-boundary, ko/en), and dedupe filters in code
- JS-only sources (Event-us, Anthropic, OpenAI DevDay) emitted as WebFetch stubs
- Verified annual-cycle reference table and Korean venue pitfall notes
- Marketplace listing in [epicsagas/plugins](https://github.com/epicsagas/plugins)
