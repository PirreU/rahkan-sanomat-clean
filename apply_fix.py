from pathlib import Path

root = Path(__file__).resolve().parent


def replace(file_rel, old, new):
    path = root / file_rel
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Pattern not found in {file_rel}")
    path.write_text(text.replace(old, new), encoding="utf-8")


# Fix collect_rss.py
replace(
    "scripts/collect_rss.py",
    "import feedparser\nimport json\nimport os\nimport time\nimport datetime\nfrom zoneinfo import ZoneInfo\n\nFEEDS = {\n",
    "import feedparser\nimport json\nimport os\nimport time\nimport datetime\nfrom pathlib import Path\nfrom zoneinfo import ZoneInfo\n\nREPO_ROOT = Path(__file__).resolve().parent.parent\nDATA_DIR = REPO_ROOT / \"data\"\n\nFEEDS = {\n",
)

replace(
    "scripts/collect_rss.py",
    "DATA_DIR = os.path.expanduser(\"~/multiperspective-news/data\")\nOUT_MATCHES = os.path.join(DATA_DIR, \"rss_matches.jsonl\")\nHELSINKI_TZ = ZoneInfo(\"Europe/Helsinki\")\n",
    "OUT_MATCHES = DATA_DIR / \"rss_matches.jsonl\"\nHELSINKI_TZ = ZoneInfo(\"Europe/Helsinki\")\n",
)

# Fix cluster_translate.py
replace(
    "scripts/cluster_translate.py",
    "import feedparser\nimport json\nimport os\nimport time\nfrom email.utils import parsedate_to_datetime\nfrom datetime import datetime\n\nDATA_DIR = os.path.expanduser(\"~/multiperspective-news/data\")\nMATCHES = os.path.join(DATA_DIR, \"rss_matches.jsonl\")\n",
    "import feedparser\nimport json\nimport os\nimport time\nfrom email.utils import parsedate_to_datetime\nfrom datetime import datetime\nfrom pathlib import Path\n\nREPO_ROOT = Path(__file__).resolve().parent.parent\nDATA_DIR = REPO_ROOT / \"data\"\nMATCHES = DATA_DIR / \"rss_matches.jsonl\"\n",
)

replace(
    "scripts/cluster_translate.py",
    "    os.makedirs(DATA_DIR, exist_ok=True)\n    with open(os.path.join(DATA_DIR, \"stories.json\"), \"w\", encoding=\"utf-8\") as f:\n        json.dump(stories, f, ensure_ascii=False, indent=2)\n        \n    with open(os.path.join(DATA_DIR, \"stories_fi.json\"), \"w\", encoding=\"utf-8\") as f:\n        json.dump(stories_fi, f, ensure_ascii=False, indent=2)\n",
    "    DATA_DIR.mkdir(parents=True, exist_ok=True)\n    with open(DATA_DIR / \"stories.json\", \"w\", encoding=\"utf-8\") as f:\n        json.dump(stories, f, ensure_ascii=False, indent=2)\n\n    with open(DATA_DIR / \"stories_fi.json\", \"w\", encoding=\"utf-8\") as f:\n        json.dump(stories_fi, f, ensure_ascii=False, indent=2)\n",
)

# Fix pipeline.sh
replace(
    "scripts/pipeline.sh",
    "set -e\ncd \"$(dirname \"$0\")/..\"\n\necho \"=== $(date -Is) pipeline start ===\"\npython3 scripts/collect_rss.py\npython3 - <<'EOF'\nimport json, os\nDATA = os.path.expanduser(\"~/multiperspective-news/data\")\nrss = os.path.join(DATA, \"rss_matches.jsonl\")\ncombined = os.path.join(DATA, \"combined_matches.jsonl\")\nrows = []\nif os.path.exists(rss):\n    with open(rss, encoding=\"utf-8\") as f:\n        rows = [json.loads(l) for l in f if l.strip()]\nwith open(combined, \"w\", encoding=\"utf-8\") as f:\n    for r in rows:\n        f.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\nprint(f\"combined: {len(rows)}\")\nEOF\nexport NO_PRE_TRANSLATE=1\npython3 scripts/cluster_translate.py --translate\necho \"=== $(date -Is) pipeline done ===\"",
    "set -e\nROOT_DIR=\"$(cd \"$(dirname \"$0\")/..\" && pwd)\"\nDATA_DIR=\"$ROOT_DIR/data\"\nmkdir -p \"$DATA_DIR\"\n\necho \"=== $(date -Is) pipeline start ===\"\npython3 scripts/collect_rss.py\nDATA_DIR=\"$DATA_DIR\" python3 - <<'EOF'\nimport json, os\nDATA = os.environ[\"DATA_DIR\"]\nrss = os.path.join(DATA, \"rss_matches.jsonl\")\ncombined = os.path.join(DATA, \"combined_matches.jsonl\")\nrows = []\nif os.path.exists(rss):\n    with open(rss, encoding=\"utf-8\") as f:\n        rows = [json.loads(l) for l in f if l.strip()]\nwith open(combined, \"w\", encoding=\"utf-8\") as f:\n    for r in rows:\n        f.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\nprint(f\"combined: {len(rows)}\")\nEOF\nexport NO_PRE_TRANSLATE=1\nDATA_DIR=\"$DATA_DIR\" python3 scripts/cluster_translate.py --translate\necho \"=== $(date -Is) pipeline done ===\"",
)

print("Fix applied successfully.")
