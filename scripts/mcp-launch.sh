#!/usr/bin/env bash
# Launcher du MCP server DataForSEO.
# Rôle : faire le pont entre les credentials stockés sur disque (0600) et les
# variables d'environnement attendues par le serveur MCP, AVANT de l'exécuter.
# Évite tout secret dans le repo ou dans .mcp.json.
set -euo pipefail

CREDS="${HOME}/.config/rankpulse/credentials.env"

# Charge les credentials s'ils existent (sinon on suppose qu'ils sont déjà
# dans l'environnement, ex. CI / Cowork).
if [ -f "$CREDS" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$CREDS"
  set +a
fi

: "${DATAFORSEO_USERNAME:?DATAFORSEO_USERNAME manquant — lance /rankpulse:setup}"
: "${DATAFORSEO_PASSWORD:?DATAFORSEO_PASSWORD manquant — lance /rankpulse:setup}"

# Version épinglée (reproductibilité). Mettre à jour volontairement, jamais @latest.
exec npx -y dataforseo-mcp-server@2.9.4
