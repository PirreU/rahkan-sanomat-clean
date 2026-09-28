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
        # Sort descending by pub
        stories.sort(key=lambda x: x.get("pub", ""), reverse=True)
        for i, s in enumerate(stories):
            en_title = s.get("headline", "")
            if i < 15:
                s["headline_fi"] = translate_text(en_title, "fi")
            else:
                s["headline_fi"] = en_title
        json.dump(stories, open(fi_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("Successfully generated translated and sorted stories_fi.json")

if __name__ == "__main__":
    main()
