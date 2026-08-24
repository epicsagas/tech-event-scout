#!/usr/bin/env python3
"""tech-event-scout aggregator.

Architecture: declarative source registry (domain model per site) -> one adapter
pipeline (fetch -> parse -> normalize -> filter -> dedupe) -> compact summary.
LLM consumes the summary + the flagged JS-only stubs, then synthesizes.

Usage: collect.py [--start YYYYMMDD] [--end YYYYMMDD] [--all-json] [name=url ...]
"""
import argparse
import html as htmlmod
import json
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) tech-event-scout/0.3"}

# ---------------------------------------------------------------- domain model
# kind: parser id (see PARSERS). js: True means plain HTTP gets no event data —
# the stub is emitted for the agent to WebFetch/render instead.
SOURCES = [
    # aggregators & platforms, no date params
    {"name": "slexn",      "kind": "anchors",    "url": "https://www.slexn.com/events/", "path": "/event/"},
    {"name": "dev-event",  "kind": "md-links",   "url": "https://raw.githubusercontent.com/brave-people/Dev-Event/master/README.md"},
    {"name": "onoffmix",   "kind": "anchors",    "url": "https://www.onoffmix.com/event/main?s=%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5", "path": "/event/"},
    {"name": "onoffmix-dev","kind": "anchors",   "url": "https://www.onoffmix.com/event/main?s=%EA%B0%9C%EB%B0%9C%EC%9E%90", "path": "/event/"},
    {"name": "luma-seoul", "kind": "luma-json",  "url": "https://luma.com/seoul"},
    {"name": "aws-summits","kind": "aws-json",   "url": "https://aws.amazon.com/events/summits/"},
    # venues, date-parameterized
    {"name": "coex",   "kind": "coex-card",  "dates": "dot",    "paginate": True,
     "url": "https://www.coex.co.kr/event/full-schedules/?var_page={page}&search_start_date={start}&search_end_date={end}&list_type=LIST"},
    {"name": "kintex", "kind": "kintex-card", "dates": "ym", "paginate": True,
     "url": "https://www.kintex.com/web/ko/event/list.do?searchType=&searchStartMon={start}&searchEndMon={end}&searchStartDt=&searchEndDt=&pageIndex={page}"},
    {"name": "bexco",  "kind": "bexco-card", "url": "https://www.bexco.co.kr/kor/CMS/EventScheduleMgr/list.do?robot=Y&mCode=MN214&page=1"},
    # JS-only: codebase can't fetch; emit stub for LLM follow-up
    {"name": "event-us",   "js": True, "url": "https://event-us.kr/"},
    {"name": "anthropic",  "js": True, "url": "https://www.anthropic.com/events"},
    {"name": "gcp",        "js": True, "url": "https://cloud.google.com/events"},
    {"name": "openai-devday", "js": True, "url": "https://devday.openai.com/"},
]

KEYWORDS = [
    "AI", "인공지능", "GPT", "LLM", "생성형", "테크", "tech", "IT", "SW", "소프트웨어",
    "개발", "컨퍼런스", "세미나", "웨비나", "웹비나", "밋업", "보안", "시큐리티",
    "클라우드", "데이터", "로봇", "자율주행", "AIoT", "해커톤", "DevOps", "전자전",
    "summit", "conference", "webinar", "hackathon", "meetup", "security",
]
# ponytail: \b on ASCII tokens stops SPYAIR→"AI" false hits; Korean needs no boundary
_KO = [k for k in KEYWORDS if re.search(r"[가-힣]", k)]
_EN = [k for k in KEYWORDS if k not in _KO]
KEY_RE = re.compile(r"\b(?:" + "|".join(map(re.escape, _EN)) + r")|" + "|".join(map(re.escape, _KO)),
                    re.IGNORECASE)

# -------------------------------------------------------------------- fetching
def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", "replace")

def clean(s: str) -> str:
    return htmlmod.unescape(s).strip()

# --------------------------------------------------------------------- parsers
# Each parser: (html, base) -> [{title, url, dates}] — keyword filter applied by
# the pipeline, parsers stay pure extractors.
def parse_anchors(html, base):
    """Generic: <a> text lines (slexn, onoffmix)."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    for m in re.finditer(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', text, re.S):
        href, inner = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
        title = re.sub(r"\s+", " ", inner).strip()
        if len(title) >= 6:
            yield {"title": title, "url": href if href.startswith("http") else base.rstrip("/") + href}

def parse_md_links(html, base):
    """Markdown lists (Dev-Event raw README)."""
    for m in re.finditer(r"\[[^\]]{6,}\]\((https?://[^)]+)\)", html):
        title, url = m.group(0)[1:m.group(0).index("]")], m.group(1)
        yield {"title": title, "url": url}

def parse_aws_json(html, base):
    """AWS summits hub embedded cards: itemCTALink -> itemMetaDate -> itemTitle."""
    pat = re.compile(r'"itemCTALink":"([^"]*summits/[a-z-]+/)"(?:,"itemMetaDate":"([^"]*)")?.{0,300}?"itemTitle":"([^"]+)"')
    for link, date, title in pat.findall(html):
        yield {"title": title, "url": f"https://aws.amazon.com{link}", "dates": date}

def parse_coex(html, base):
    """COEX BlogEventItem cards: link / -tit / -date."""
    for m in re.finditer(r"<a[^>]+href='(https://www\.coex\.co\.kr/exhibitions/[^']+)'[^>]*>.*?"
                         r"BlogEventItemCont-tit'>([^<]+)</h4>.*?BlogEventItemCont-date'>([^<]*)<",
                         html, re.S):
        url, title, dates = m.groups()
        yield {"title": clean(title), "url": url.split("?")[0], "dates": clean(dates)}

def parse_kintex(html, base):
    """KINTEX fnView cards: item-subject / item-date."""
    for m in re.finditer(r"fnView\('\./view\.do',\s*(\d+)\);.*?"
                         r'class="item-subject">([^<]+)</div>.*?class="item-date">([^<]*)<',
                         html, re.S):
        eid, title, dates = m.groups()
        yield {"title": clean(title), "url": f"https://www.kintex.com/web/ko/event/view.do?seq={eid}",
               "dates": clean(dates)}

def parse_bexco(html, base):
    """BEXCO EventList cards: event_seq link, text = 상세보기 상태 카테고리 제목 기간 장소."""
    for m in re.finditer(r'<a href="(/kor/CMS/EventScheduleMgr/view\.do[^"]+event_seq=\d+)">(.*?)</a>', html, re.S):
        href, inner = m.groups()
        text = clean(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner)))
        dm = re.search(r"(20\d{2}-\d{2}-\d{2}\s*~\s*20\d{2}-\d{2}-\d{2})", text)
        title = re.sub(r"^(상세보기\s*)?(진행중|종료)?\s*\S{1,4}\s+", "", text.split("~")[0]).strip()
        yield {"title": title, "url": "https://www.bexco.co.kr" + href,
               "dates": dm.group(1) if dm else ""}

def parse_luma(html, base):
    """Luma city page: __NEXT_DATA__ embeds events[].event {name, start_at, url}."""
    m = re.search(r'id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        return
    d = json.loads(m.group(1))
    for ev in d["props"]["pageProps"]["initialData"]["data"]["events"]:
        e = ev["event"]
        yield {"title": e.get("name", ""), "url": f"https://luma.com/{e.get('url', e.get('api_id', ''))}",
               "dates": e.get("start_at", "")[:10]}

PARSERS = {"anchors": parse_anchors, "md-links": parse_md_links, "aws-json": parse_aws_json,
           "coex-card": parse_coex, "kintex-card": parse_kintex, "bexco-card": parse_bexco,
           "luma-json": parse_luma}

# ------------------------------------------------------------------ aggregator
def build_urls(src, start, end):
    """Fill url template with date params per site's format."""
    fmt = {"dot": lambda s: f"{s[:4]}.{s[4:6]}.{s[6:]}" if s else "",
           "ym":  lambda s: s[:6] if s else ""}.get(src.get("dates"))
    if "{" not in src["url"]:
        return [src["url"]]
    if src.get("paginate"):
        return [src["url"].format(page=p, start=fmt(start), end=fmt(end)) for p in range(1, 6)]
    return [src["url"].format(start=fmt(start), end=fmt(end))]

DATE_RE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})|(20\d{2})\.(\d{2})\.(\d{2})|(20\d{2})[./](\d{1,2})[./](\d{1,2})")

def event_date(e):
    """First YYYY-MM-DD found in dates field or title; None if absent."""
    m = DATE_RE.search(e.get("dates", "") + " " + e["title"])
    if not m:
        return None
    g = [x for x in m.groups() if x]
    return "".join(g[:3]) if len(g) >= 3 else None

def collect(src, start, end):
    """One adapter pass: fetch pages -> parse -> keyword filter -> date filter -> normalize."""
    events, seen = [], set()
    for url in build_urls(src, start, end):
        try:
            parsed = list(PARSERS[src["kind"]](fetch(url), url))
        except Exception as ex:
            return {"source": src["name"], "status": f"error: {ex}", "events": []}
        if src.get("paginate") and not parsed:  # COEX: stop at first empty page
            break
        for e in parsed:
            t = clean(re.sub(r"\s+", " ", e["title"]))[:120]
            if t in seen or not KEY_RE.search(t) or "종료된" in t:
                continue
            if src.get("path") and src["path"] not in e["url"]:
                continue  # keep only event-detail paths (drops category nav links)
            d = event_date(e)
            if d and start and end and not (start <= d <= end):  # outside window
                continue
            seen.add(t)
            e["title"], e["url"] = t, e["url"][:160]
            events.append(e)
    return {"source": src["name"], "status": "ok", "count": len(events), "events": events}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end"); ap.add_argument("--all-json", action="store_true")
    ap.add_argument("extra", nargs="*", help="name=url overrides / additions")
    a = ap.parse_args()
    sources = list(SOURCES)
    for s in a.extra:
        name, _, url = s.partition("=")
        sources = [x for x in sources if x["name"] != name] + [
            {"name": name, "kind": "anchors", "url": url}]
    out = [collect(s, a.start or "", a.end or "") for s in sources if not s.get("js")]
    stubs = [{"source": s["name"], "fetch": s["url"]} for s in sources if s.get("js")]
    if a.all_json:
        print(json.dumps({"collected": out, "js_stubs": stubs}, ensure_ascii=False, indent=1))
        return
    # compact summary — the only part the LLM needs to read
    print(f"# collected {a.start or '-'} .. {a.end or '-'}")
    for s in out:
        print(f"\n[{s['source']}] {s['status']}" + (f" ({s['count']})" if s.get("count") else ""))
        for e in s["events"]:
            print(f"- {e.get('dates','') or '-'} | {e['title']} | {e['url']}")
    print("\n# js-only (WebFetch these):")
    for s in stubs:
        print(f"- {s['source']}: {s['fetch']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
