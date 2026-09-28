#!/usr/bin/env python3
from translatepy import Translator
import json
import os
import time

def translate_text(text, target="fi"):
    try:
        translator = Translator()
        return translator.translate(text, target).result or text
    except Exception:
        return text

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sp = os.path.join(BASE_DIR, "data", "stories.json")
    fi_path = os.path.join(BASE_DIR, "data", "stories_fi.json")
    if os.path.exists(sp):
        stories = json.load(open(sp, encoding="utf-8"))
        stories.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        
        # Load existing translations if available to avoid re-translating old stories
        existing_fi = {}
        if os.path.exists(fi_path):
            try:
                for s in json.load(open(fi_path, encoding="utf-8")):
                    if s.get("link") and s.get("headline_fi"):
                        existing_fi[s["link"]] = s["headline_fi"]
            except Exception:
                pass

        for s in stories:
            link = s.get("link")
            en_title = s.get("headline", "")
            if link in existing_fi:
                s["headline_fi"] = existing_fi[link]
            else:
                print(f"Translating: {en_title[:40]}...")
                s["headline_fi"] = translate_text(en_title, "fi")
                time.sleep(0.3)

        json.dump(stories, open(fi_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("Successfully translated all stories.")

if __name__ == "__main__":
    main()
