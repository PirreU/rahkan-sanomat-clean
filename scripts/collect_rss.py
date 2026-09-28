#!/usr/bin/env python3
import feedparser
import json
import os
import time
import datetime

FEEDS = {
    "Deutsche Welle": "https://rss.dw.com/rdf/rss-en-all",
    "France 24": "https://www.france24.com/en/rss",
    "Euronews": "https://www.euronews.com/rss?format=rss",
    "Politico Europe": "https://www.politico.eu/feed/",
    "Eurotopics": "https://www.eurotopics.net/export/en/rss.xml"
}

KEYWORDS = ['riot', 'protest', 'eu commission', 'age verification', 'politics', 'political', 'strike', 'regulation', 'digital', 'police', 'demonstration', 'parliament', 'law', 'court', 'election', 'migrant', 'immigration', 'asylum', 'refugee', 'maahanmuutto', 'turvapaikka', 'trump', 'tariff', 'war', 'russia', 'ukraine', 'israel', 'gaza', 'energy', 'economy']

DATA_DIR = os.path.expanduser("~/multiperspective-news/data")
OUT_MATCHES = os.path.join(DATA_DIR, "rss_matches.jsonl")

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    matches = []
    
    for source, url in FEEDS.items():
        try:
            d = feedparser.parse(url)
            print(f"Fetched {len(d.entries)} entries from {source}")
            for entry in d.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "#")
                
                pub_parsed = entry.get("published_parsed", entry.get("updated_parsed", None))
                if pub_parsed:
                    pub = time.strftime("%Y-%m-%d %H:%M:%S", pub_parsed)
                    timestamp = time.mktime(pub_parsed)
                else:
                    pub = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    timestamp = time.time()
                
                combined_text = (title + " " + summary).lower()
                if not KEYWORDS or any(kw in combined_text for kw in KEYWORDS):
                    matches.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "source": source,
                        "published": pub,
                        "timestamp": timestamp
                    })
        except Exception as e:
            print(f"Error parsing {source}: {e}")
            
    matches.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

    with open(OUT_MATCHES, "w", encoding="utf-8") as f:
        for m in matches:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
            
    stories_path = os.path.join(DATA_DIR, "stories.json")
    stories = [{"headline": m["title"], "summary": m["summary"], "link": m["link"], "source": m["source"], "pub": m["published"], "timestamp": m["timestamp"]} for m in matches]
    json.dump(stories, open(stories_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            
    print(f"Collected and sorted {len(matches)} articles by true timestamp.")

if __name__ == "__main__":
    main()
