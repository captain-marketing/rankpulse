#!/usr/bin/env bash
# Vérifie les connexions Google Search Console (Tier 1) et GA4 (Tier 2).
# Lit les credentials depuis ~/.config/rankpulse/google-api.json.
set -euo pipefail

GOOGLE_CONFIG="${HOME}/.config/rankpulse/google-api.json"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)/scripts"

# --- Prérequis ---
if [ ! -f "$GOOGLE_CONFIG" ]; then
  echo "❌ google-api.json introuvable." >&2
  echo "   Lance /rankpulse:google-setup pour configurer l'accès Google." >&2
  exit 1
fi

if ! python3 -c "import googleapiclient" 2>/dev/null; then
  echo "⚠️  Dépendances Python manquantes. Installation..." >&2
  pip3 install -q -r "${SCRIPT_DIR}/requirements.txt"
fi

SITE_URL=$(python3 -c "import json,sys; c=json.load(open('$GOOGLE_CONFIG')); print(c.get('site_url',''))")
GA4_ID=$(python3 -c "import json,sys; c=json.load(open('$GOOGLE_CONFIG')); print(c.get('ga4_property_id',''))")

if [ -z "$SITE_URL" ]; then
  echo "❌ site_url manquant dans google-api.json." >&2
  exit 1
fi

# --- Test Tier 1 : GSC ---
echo "→ Test Tier 1 — Google Search Console (${SITE_URL})…"
GSC_OUTPUT=$(python3 "${SCRIPT_DIR}/gsc_client.py" --url "${SITE_URL}" --days 7 2>/tmp/gsc_err.txt || true)

if echo "$GSC_OUTPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(1 if 'error' in d else 0)" 2>/dev/null; then
  echo "✅ Tier 1 (GSC) : connexion OK"
  if command -v jq >/dev/null 2>&1; then
    echo "   Clics (7j) : $(echo "$GSC_OUTPUT" | jq -r '.search_analytics.total_clicks // "n/a"')"
    echo "   Impressions : $(echo "$GSC_OUTPUT" | jq -r '.search_analytics.total_impressions // "n/a"')"
  fi
else
  ERR=$(echo "$GSC_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('error','inconnue'))" 2>/dev/null || cat /tmp/gsc_err.txt)
  echo "❌ Tier 1 (GSC) : erreur — $ERR" >&2
  echo "   Vérifie : email du Service Account ajouté à GSC ? site_url exact ?" >&2
fi

# --- Test Tier 2 : GA4 ---
if [ -z "$GA4_ID" ]; then
  echo "ℹ️  Tier 2 (GA4) non configuré (ga4_property_id absent). Tier 1 uniquement."
  exit 0
fi

echo "→ Test Tier 2 — Google Analytics 4 (property ${GA4_ID})…"
GA4_OUTPUT=$(python3 "${SCRIPT_DIR}/ga4_client.py" --days 7 2>/tmp/ga4_err.txt || true)

if echo "$GA4_OUTPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(1 if 'error' in d else 0)" 2>/dev/null; then
  echo "✅ Tier 2 (GA4) : connexion OK"
  if command -v jq >/dev/null 2>&1; then
    echo "   Sessions organiques (7j) : $(echo "$GA4_OUTPUT" | jq -r '.total_organic_sessions // "n/a"')"
  fi
else
  ERR=$(echo "$GA4_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('error','inconnue'))" 2>/dev/null || cat /tmp/ga4_err.txt)
  echo "❌ Tier 2 (GA4) : erreur — $ERR" >&2
  echo "   Vérifie : email du Service Account ajouté à la propriété GA4 ? ga4_property_id correct ?" >&2
fi
