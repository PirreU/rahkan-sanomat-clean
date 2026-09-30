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
    fi_path = os.path.join(BASE_DIR, "data", "stories_fi.json")
    if os.path.exists(fi_path):
        stories = json.load(open(fi_path, encoding="utf-8"))
        for i, s in enumerate(stories):
            if not s.get("headline_fi") or s["headline_fi"] == s.get("headline"):
                en_title = s.get("headline", "")
                print(f"[{i+1}/{len(stories)}] Translating: {en_title[:50]}...")
                s["headline_fi"] = translate_text(en_title, "fi")
                time.sleep(0.3)
        json.dump(stories, open(fi_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("All stories fully translated!")

if __name__ == "__main__":
    main()
