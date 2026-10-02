#!/usr/bin/env bash
# WorldWire pipeline: collect RSS -> merge -> cluster -> translate top stories -> done
# NO_PRE_TRANSLATE=1 : skip mass title translation (rate-limit friendly)
set -e
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$ROOT_DIR/data"
mkdir -p "$DATA_DIR"

echo "=== $(date -Is) pipeline start ==="
python3 scripts/collect_rss.py
DATA_DIR="$DATA_DIR" python3 - <<'EOF'
import json, os
DATA = os.environ["DATA_DIR"]
rss = os.path.join(DATA, "rss_matches.jsonl")
combined = os.path.join(DATA, "combined_matches.jsonl")
rows = []
if os.path.exists(rss):
    with open(rss, encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
with open(combined, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"combined: {len(rows)}")
EOF
export NO_PRE_TRANSLATE=1
DATA_DIR="$DATA_DIR" python3 scripts/cluster_translate.py --translate
echo "=== $(date -Is) pipeline done ==="