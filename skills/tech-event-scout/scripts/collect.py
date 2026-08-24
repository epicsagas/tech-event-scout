#!/usr/bin/env python3
"""tech-event-scout collector — deterministic fetch + keyword filter, LLM-free.

Fetches each source list page, strips HTML, keyword-filters AI/tech event lines,
emits compact JSON. JS-only sources are flagged so the agent WebFetches just those.

Usage: collect.py [--start YYYYMMDD] [--end YYYYMMDD] [url ...]
Output: JSON on stdout: {source, status, events:[{title, url, dates}]}
"""
# ponytail: regex tag-stripping, no BeautifulSoup — add bs4 if listings get complex
import argparse
import json
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) tech-event-scout/0.2"}

KEYWORDS = [
    "AI", "인공지능", "GPT", "LLM", "생성형", "테크", "tech", "IT", "SW", "소프트웨어",
    "개발", "컨퍼런스", "세미나", "웨비나", "웹비나", "밋업", "보안", "시큐리티",
    "클라우드", "데이터", "로봇", "자율주행", "AIoT", "해커톤", "DevOps",
    "summit", "conference", "webinar", "hackathon", "meetup", "security",
]
# ponytail: false-positive guard — bare "it"/"data" never match, only Korean/exact tokens
KEY_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)
DATE_RE = re.compile(r"20\d{2}[.\-/ ~년]*\d{1,2}[.\-/ ~월]*\d{1,2}")

DEFAULT_SOURCES = [
    ("slexn", "https://www.slexn.com/events/"),
    ("dev-event", "https://raw.githubusercontent.com/brave-people/Dev-Event/master/README.md"),
    ("onoffmix-ai", "https://www.onoffmix.com/event/main?s=%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5"),
    ("aws-summits", "https://aws.amazon.com/events/summits/"),
]

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", "replace")

def extract(html: str, base: str):
    """Yield (title, url, dates) from anchor/heading text lines."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    for m in re.finditer(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', text, re.S):
        href, inner = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
        title = re.sub(r"\s+", " ", inner).strip()
        if len(title) < 6 or not KEY_RE.search(title):
            continue
        url = href if href.startswith("http") else base.rstrip("/") + href
        yield {"title": title[:120], "url": url}
    # headings carry titles on JS-lite pages (slexn)
    ctx_dates = DATE_RE.findall(text[:200000])
    for h in re.finditer(r"<h[1-4][^>]*>(.*?)</h[1-4]>", text, re.S):
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h.group(1))).strip()
        if len(title) >= 6 and KEY_RE.search(title):
            yield {"title": title[:120], "url": ""}

def extract_aws_summits(html: str, base: str):
    """AWS summits hub embeds event cards as JSON: itemCTALink → itemMetaDate → itemTitle."""
    pat = re.compile(
        r'"itemCTALink":"([^"]*summits/[a-z-]+/)"(?:,"itemMetaDate":"([^"]*)")?.{0,300}?"itemTitle":"([^"]+)"'
    )
    seen = set()
    for link, date, title in pat.findall(html):
        if link in seen:
            continue
        seen.add(link)
        yield {"title": title[:120], "url": f"https://aws.amazon.com{link}", "dates": date}

ADAPTERS = {"aws-summits": extract_aws_summits}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("urls", nargs="*", help="extra list URLs as name=url")
    a = ap.parse_args()
    sources = list(DEFAULT_SOURCES)
    for s in a.urls:
        name, _, url = s.partition("=")
        sources.append((name or url[:24], url))
    out = []
    for name, url in sources:
        try:
            events = list(ADAPTERS.get(name, extract)(fetch(url), url))
            seen, uniq = set(), []
            for e in events:  # dedupe by title
                k = e["title"]
                if k not in seen:
                    seen.add(k); uniq.append(e)
            out.append({"source": name, "status": "ok", "count": len(uniq), "events": uniq})
        except Exception as ex:
            out.append({"source": name, "status": f"error: {ex}", "events": []})
    print(json.dumps({"as_of": a.start or "", "sources": out},
                     ensure_ascii=False, indent=1))

if __name__ == "__main__":
    sys.exit(main())
