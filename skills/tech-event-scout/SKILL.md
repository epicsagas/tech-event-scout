---
name: tech-event-scout
description: >-
  AI/테크 행사·컨퍼런스 정보 수집. AWS, GCP, Anthropic(Claude), OpenAI, Google Gemini,
  Groq 등 AI 플랫폼 행사와 서밋, 코엑스(COEX)·키텍스(KINTEX) 등 국내외 행사 일정·등록·CFP 정보를
  수집·요약할 때 사용.
---

# tech-event-scout

AI/테크 행사 정보 수집 에이전트. **검색보다 공식 리스트 페이지 직접 패치(WebFetch)가 우선** —
토큰 절약·속도·정확도 모두 유리. 웹 검색은 아래 소스에 없는 행사만 보조용으로.

## 검증된 소스 리스트 (직접 패치 대상)

| 소스 | 리스트 페이지 | 비고 |
|------|--------------|------|
| 코엑스 달력 | `https://www.coex.co.kr/event/exhibitions-calendar/` | 월 단위 달력. 국내 AI 행사 대부분 여기서 1차 확인 |
| 킨텍스 달력 | `https://www.kintex.com/web/ko/event/clist.do` | JS 렌더링이라 패치 결과 날짜가 어긋날 수 있음 — 날짜·행사명 교차 확인 필수 |
| AI Summit Seoul | `https://www.aisummit.co.kr/` | 국내 최대 AI 컨퍼런스. 매년 8월 셋째 주 코엑스 (2026: 8/19-21) |
| AWS 이벤트 | `https://aws.amazon.com/ko/events/` | AWS Summit Seoul은 매년 5월 코엑스. re:Invent는 12월 |
| Google Cloud Next | `https://www.googlecloudevents.com/next-vegas` | 매년 4월 라스베이거스 |
| OpenAI DevDay | `https://openai.com/devday/` | 매년 가을 (2026: 9/29 예정) |
| Anthropic | `https://www.anthropic.com/events` | 수시 확인 필요 |
| Groq | `https://groq.com/events/` | 공식 일정 공개가 늦는 편 |

## 연간 주기 참고 (2026년 기준 검증값)

| 행사 | 시기 | 장소 |
|------|------|------|
| Google Cloud Next | 4월 | 라스베이거스 |
| AWS Summit Seoul | 5월 (2026: 5/20-21) | 코엑스 |
| 공공 AI 박람회 | 6월 | 킨텍스 |
| AI Summit Seoul & Expo | 8월 셋째 주 (2026: 8/19-21) | 코엑스 |
| OpenAI DevDay | 9월 말 | 샌프란시스코 |
| 산업AI EXPO | 10월 (2026: 10/21-23) | 킨텍스 |
| AWS re:Invent | 12월 (2026: 12/1-5) | 라스베이거스 |

## 워크플로우

1. **범위 확정**: 주제·기간·지역 미지정 시 되묻기. 기본값: 오늘부터 3개월, 국내+주요 글로벌.
2. **1차 수집**: 위 소스 테이블에서 기간에 해당하는 페이지를 WebFetch. 코엑스·킨텍스 달력은
   국내 행사 파악의 출발점.
3. **보조 검색**: 소스에 없는 행사(Gemini 관련, 해커톤, CFP)만 WebSearch.
4. **검증**: 행사별 공식 페이지에서 일정·장소·등록 확인. 블로그 2차 인용만으로 확정 금지.
5. **중복 제거·출력**: 아래 포맷. 종료된 행사 제외, CFP 마감 임박 순 별도 섹션.

## 출력 포맷

| 행사명 | 주최 | 일정 | 장소 | 등록 | CFP | 링크 | 출처 |

- 일정: `2026-09-17 ~ 09-18`. 미확정이면 `(미정)`.
- 비공식 소스면 표기. 답변에 기준일 명시 (예: "2026-08-24 기준").

## 함정

- **연도 착오**: 검색 결과에 과거 회차가 섞임. 과거 대형 행사(예: AI Summit 2026 = 8/19-21 종료)를
  예정처럼 보고하지 말 것.
- **킨텍스 달력 JS**: 패치 시 날짜-행사 매핑이 어긋나는 경우 확인됨. 인접 행사 날짜로 재확인.
- **조기 종료된 주간**: 8월 말 코엑스는 자율주행/EV·제약바이오 위주 — AI 순수 행사 없을 수 있음.
  "해당 기간 AI 행사 없음"도 유효한 결과.
