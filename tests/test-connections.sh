#!/usr/bin/env bash
# Vérifie l'authentification DataForSEO et affiche le solde du compte.
# Lit les credentials depuis ~/.config/rankpulse/credentials.env (ou l'environnement).
set -euo pipefail

CREDS="${HOME}/.config/rankpulse/credentials.env"
if [ -f "$CREDS" ]; then
  set -a; . "$CREDS"; set +a
fi

if [ -z "${DATAFORSEO_USERNAME:-}" ] || [ -z "${DATAFORSEO_PASSWORD:-}" ]; then
  echo "❌ Credentials manquants. Lance /rankpulse:setup." >&2
  exit 1
fi

echo "→ Test d'authentification DataForSEO…"
HTTP=$(curl -s -o /tmp/rankpulse_user_data.json -w "%{http_code}" \
  --user "${DATAFORSEO_USERNAME}:${DATAFORSEO_PASSWORD}" \
  "https://api.dataforseo.com/v3/appendix/user_data")

if [ "$HTTP" != "200" ]; then
  echo "❌ Échec HTTP $HTTP. Vérifie le login/password (DATAFORSEO_USERNAME / DATAFORSEO_PASSWORD)." >&2
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  STATUS=$(jq -r '.status_message' /tmp/rankpulse_user_data.json)
  BALANCE=$(jq -r '.tasks[0].result[0].money.balance // "n/a"' /tmp/rankpulse_user_data.json)
  echo "✅ Connexion OK — $STATUS"
  echo "   Solde restant : \$${BALANCE}"
else
  echo "✅ Connexion OK (HTTP 200). Installe 'jq' pour afficher le solde."
fi
