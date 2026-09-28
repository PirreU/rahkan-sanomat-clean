#!/usr/bin/env python3
import feedparser
import json
import os
import time
from email.utils import parsedate_to_datetime
from deep_translator import GoogleTranslator
from datetime import datetime

DATA_DIR = os.path.expanduser("~/multiperspective-news/data")
MATCHES = os.path.join(DATA_DIR, "rss_matches.jsonl")

def parse_pub_dt(p_str):
    if not p_str:
        return datetime.min
    try:
        dt = parsedate_to_datetime(p_str)
        return dt.replace(tzinfo=None)
    except:
        return datetime.min

def format_pub(dt):
    if dt == datetime.min:
        return "Recent"
    return dt.strftime("%Y-%m-%d %H:%M")

def main():
    rows = []
    if os.path.exists(MATCHES):
        with open(MATCHES, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
    
    rows.sort(key=lambda x: parse_pub_dt(x.get("published", "")), reverse=True)
    
    stories = []
    for r in rows:
        title = r.get("title", "")
        pub_raw = r.get("published", "")
        dt = parse_pub_dt(pub_raw)
        pub_formatted = format_pub(dt)
        
        stories.append({
            "headline": title,
            "headline_fi": title,
            "link": r.get("link", "#"),
            "source": r.get("source", "Unknown"),
            "pub": pub_formatted,
            "_dt": dt.isoformat()
        })
    
    stories_fi = []
    translator = GoogleTranslator(source='auto', target='fi')
    
    # Only translate top 15 stories to avoid rate limits and timeouts
    for i, s in enumerate(stories):
        s_fi = s.copy()
        if i < 15:
            try:
                translated = translator.translate(s["headline"])
                if translated:
                    s_fi["headline_fi"] = translated
                else:
                    s_fi["headline_fi"] = s["headline"]
            except Exception as e:
                print(f"Translation failed: {e}")
                s_fi["headline_fi"] = s["headline"]
            time.sleep(1.0)
        else:
            s_fi["headline_fi"] = s["headline"]
        
        s.pop("_dt", None)
        s_fi.pop("_dt", None)
        stories_fi.append(s_fi)

    for s in stories:
        s.pop("_dt", None)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "stories.json"), "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(DATA_DIR, "stories_fi.json"), "w", encoding="utf-8") as f:
        json.dump(stories_fi, f, ensure_ascii=False, indent=2)
        
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
