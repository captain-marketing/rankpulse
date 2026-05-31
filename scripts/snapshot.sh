#!/usr/bin/env bash
# Prend un snapshot de positions pour tous les mots-clés trackés dans tracking.db.
# Conçu pour être appelé par launchd / cron (snapshot hebdomadaire automatique)
# ou manuellement via /rankpulse:track snapshot.
#
# Dépendances : sqlite3, curl, python3 (stdlib uniquement).
set -euo pipefail

DB="${HOME}/.config/rankpulse/tracking.db"
CREDS="${HOME}/.config/rankpulse/credentials.env"
LOG="${HOME}/.config/rankpulse/snapshot.log"
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Charger les credentials DataForSEO
if [ -f "$CREDS" ]; then
  set -a; . "$CREDS"; set +a
fi
: "${DATAFORSEO_USERNAME:?DATAFORSEO_USERNAME manquant — lance /rankpulse:setup}"
: "${DATAFORSEO_PASSWORD:?DATAFORSEO_PASSWORD manquant — lance /rankpulse:setup}"

if [ ! -f "$DB" ]; then
  echo "[$NOW] tracking.db introuvable — aucun mot-clé tracké. Lance /rankpulse:track add." | tee -a "$LOG"
  exit 0
fi

DOMAIN_FILTER="${1:-}"

# Récupérer les mots-clés à snapshotter
if [ -n "$DOMAIN_FILTER" ]; then
  QUERY="SELECT k.id, k.keyword, k.locale, k.language FROM keywords k JOIN domains d ON k.domain_id = d.id WHERE d.domain = '${DOMAIN_FILTER}';"
else
  QUERY="SELECT k.id, k.keyword, k.locale, k.language FROM keywords k;"
fi

KEYWORDS=$(sqlite3 "$DB" "$QUERY" 2>/dev/null || true)

if [ -z "$KEYWORDS" ]; then
  echo "[$NOW] Aucun mot-clé à snapshotter." | tee -a "$LOG"
  exit 0
fi

TOTAL=0
ERRORS=0

while IFS='|' read -r KW_ID KEYWORD LOCALE LANGUAGE; do
  [ -z "$KW_ID" ] && continue

  # Appel DataForSEO SERP (Organic Live Advanced)
  PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps([{
  'keyword': sys.argv[1],
  'location_name': sys.argv[2],
  'language_code': sys.argv[3],
  'depth': 20,
  'device': 'desktop'
}]))
" "$KEYWORD" "$LOCALE" "$LANGUAGE" 2>/dev/null)

  HTTP_CODE=$(curl -s -o /tmp/rankpulse_snap.json -w "%{http_code}" \
    --user "${DATAFORSEO_USERNAME}:${DATAFORSEO_PASSWORD}" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" 2>/dev/null || echo "000")

  if [ "$HTTP_CODE" != "200" ]; then
    echo "[$NOW] ERREUR HTTP $HTTP_CODE pour : $KEYWORD" | tee -a "$LOG"
    ERRORS=$((ERRORS + 1))
    continue
  fi

  # Parser la réponse et extraire position + URL pour les domaines trackés
  python3 - "$KW_ID" "$NOW" "$DB" <<'PYEOF'
import json, sqlite3, sys

kw_id = int(sys.argv[1])
taken_at = sys.argv[2]
db_path = sys.argv[3]

with open('/tmp/rankpulse_snap.json') as f:
    data = json.load(f)

# Récupérer le domaine associé au keyword
conn = sqlite3.connect(db_path)
row = conn.execute(
    "SELECT d.domain FROM domains d JOIN keywords k ON k.domain_id = d.id WHERE k.id = ?",
    (kw_id,)
).fetchone()
if not row:
    conn.close()
    sys.exit(0)

domain = row[0].lower().rstrip('/')
items = []
try:
    items = data['tasks'][0]['result'][0]['items'] or []
except (KeyError, IndexError, TypeError):
    pass

position = None
url = None
title = None
for item in items:
    if item.get('type') != 'organic':
        continue
    item_domain = (item.get('domain') or '').lower()
    if domain in item_domain or item_domain in domain:
        position = item.get('rank_absolute')
        url = item.get('url')
        title = item.get('title')
        break

conn.execute(
    "INSERT INTO snapshots (keyword_id, taken_at, position, url, title) VALUES (?, ?, ?, ?, ?)",
    (kw_id, taken_at, position, url, title)
)
conn.commit()
conn.close()
PYEOF

  TOTAL=$((TOTAL + 1))
  echo "[$NOW] Snapshot OK : $KEYWORD" >> "$LOG"

done <<< "$KEYWORDS"

echo "[$NOW] Snapshot terminé — $TOTAL mots-clés traités, $ERRORS erreur(s)." | tee -a "$LOG"
