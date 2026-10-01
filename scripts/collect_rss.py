#!/usr/bin/env python3
import feedparser
import json
import os
import time
import datetime
from zoneinfo import ZoneInfo

FEEDS = {
    "Deutsche Welle": "https://rss.dw.com/rdf/rss-en-all",
    "France 24": "https://www.france24.com/en/rss",
    "Euronews": "https://www.euronews.com/rss?format=rss",
    "Politico Europe": "https://www.politico.eu/feed/",
    "Eurotopics": "https://www.eurotopics.net/export/en/rss.xml"
}

KEYWORDS = ['riot', 'protest', 'eu commission', 'age verification', 'politics', 'political', 'strike', 'regulation', 'digital', 'police', 'demonstration', 'parliament', 'law', 'court', 'election', 'migrant', 'immigration', 'asylum', 'refugee', 'maahanmuutto', 'turvapaikka', 'trump', 'tariff', 'war', 'russia', 'ukraine', 'israel', 'gaza', 'energy', 'economy', 'climate', 'environment', 'health', 'technology', 'science', 'culture', 'sports', 'entertainment', 'business', 'finance', 'education', 'security', 'defense', 'diplomacy', 'human rights', 'humanitarian', 'crime', 'corruption', 'terror', 'attack', 'incident', 'disaster', 'accident', 'disinformation', 'fake news', 'media', 'journalism', 'art', 'music', 'film', 'literature', 'society', 'community', 'government', 'policy', 'reform', 'innovation', 'infrastructure', 'transportation', 'agriculture', 'trade', 'industry', 'manufacturing', 'tourism', 'environmental', 'sustainability', 'climate change', 'global warming', 'pollution', 'waste', 'recycling', 'renewable energy', 'nuclear', 'fossil fuels', 'oil', 'gas', 'coal', 'electricity', 'water', 'food', 'agriculture', 'farming', 'fisheries', 'forestry', 'biodiversity', 'ecosystem', 'wildlife', 'conservation', 'protection', 'endangered species', 'climate action', 'climate summit', 'climate agreement', 'climate policy', 'climate finance', 'climate adaptation', 'climate mitigation', 'climate resilience', 'climate vulnerability', 'climate impact', 'climate risk', 'climate change', 'climate crisis', 'climate emergency', 'climate urgency', 'climate action', 'climate justice', 'climate leadership', 'climate innovation', 'climate technology', 'climate science', 'climate research', 'climate education', 'climate awareness', 'climate communication', 'climate advocacy', 'climate activism', 'climate movement', 'climate campaign', 'climate protest', 'climate strike', 'climate march', 'climate rally', 'climate demonstration', 'climate action', 'climate change', 'climate crisis', 'climate emergency', 'climate urgency', 'climate action', 'climate justice', 'climate leadership', 'climate innovation', 'climate technology', 'climate science', 'climate research', 'climate education', 'climate awareness', 'climate communication', 'climate advocacy', 'climate activism', 'climate movement', 'climate campaign', 'climate protest', 'climate strike', 'climate march', 'climate rally', 'climate demonstration']

DATA_DIR = os.path.expanduser("~/multiperspective-news/data")
OUT_MATCHES = os.path.join(DATA_DIR, "rss_matches.jsonl")
HELSINKI_TZ = ZoneInfo("Europe/Helsinki")

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    matches = []
    
    for source, url in FEEDS.items():
        try:
            d = feedparser.parse(url)
            for entry in d.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "#")
                
                pub_parsed = entry.get("published_parsed", entry.get("updated_parsed", None))
                if pub_parsed:
                    # Convert UTC time struct to Helsinki time
                    utc_dt = datetime.datetime(*pub_parsed[:6], tzinfo=datetime.timezone.utc)
                    helsinki_dt = utc_dt.astimezone(HELSINKI_TZ)
                    pub = helsinki_dt.strftime("%Y-%m-%d %H:%M:%S")
                    timestamp = utc_dt.timestamp()
                else:
                    helsinki_dt = datetime.datetime.now(HELSINKI_TZ)
                    pub = helsinki_dt.strftime("%Y-%m-%d %H:%M:%S")
                    timestamp = time.time()
                
                # if not KEYWORDS or any(kw in combined_text for kw in KEYWORDS):
                if True:
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
            
    # Sort strictly by underlying Unix timestamp descending (preserves sorting)
    matches.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

    with open(OUT_MATCHES, "w", encoding="utf-8") as f:
        for m in matches:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
            
    stories_path = os.path.join(DATA_DIR, "stories.json")
    stories = [{"headline": m["title"], "summary": m["summary"], "link": m["link"], "source": m["source"], "pub": m["published"], "timestamp": m["timestamp"]} for m in matches]
    json.dump(stories, open(stories_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            
    print(f"Collected and sorted {len(matches)} articles with Helsinki timestamps.")

if __name__ == "__main__":
    main()
