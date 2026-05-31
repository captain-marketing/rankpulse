---
name: setup
description: Configure et teste les credentials DataForSEO de Rankpulse. À utiliser quand l'utilisateur veut connecter son compte DataForSEO, définir un budget API mensuel, ou vérifier que la connexion fonctionne. Invocable via /rankpulse:setup.
---

# Rankpulse — Setup DataForSEO

Configure les identifiants DataForSEO de façon sécurisée et vérifie la connexion.

## Règles de sécurité (non négociables)
- Les secrets ne sont JAMAIS écrits dans le repo, ni affichés en clair, ni mis dans `.mcp.json`.
- Ils vont uniquement dans `~/.config/rankpulse/credentials.env` avec permissions `0600`.
- Ce fichier est lu par `scripts/mcp-launch.sh` au lancement du serveur MCP.

## Procédure

1. **Récupérer les identifiants.** Demander à l'utilisateur son `DATAFORSEO_USERNAME` (login API) et son `DATAFORSEO_PASSWORD`. Ne jamais les afficher après saisie.

2. **Écrire le fichier de credentials** (`~/.config/rankpulse/credentials.env`) :
   ```
   DATAFORSEO_USERNAME=<login>
   DATAFORSEO_PASSWORD=<password>
   ```
   Puis : `mkdir -p ~/.config/rankpulse && chmod 700 ~/.config/rankpulse && chmod 600 ~/.config/rankpulse/credentials.env`.

3. **Budget mensuel (optionnel).** Proposer de définir un plafond. Si accepté, écrire `~/.config/rankpulse/budget.json` :
   ```json
   { "monthly_usd": 25 }
   ```
   Le hook `cost-tracker.py` avertira quand ce seuil est atteint.

4. **Tester la connexion** en lançant `bash "${CLAUDE_PLUGIN_ROOT}/tests/test-connections.sh"`.
   Ce script vérifie l'authentification contre `/v3/appendix/user_data` et affiche le solde du compte.

5. **Important :** après une première configuration, le serveur MCP `dataforseo` doit être (re)chargé pour prendre en compte les credentials. Indiquer à l'utilisateur de redémarrer la session si les outils `mcp__dataforseo__*` ne répondent pas.

## Sortie attendue
Confirmation que la connexion fonctionne, le solde DataForSEO restant, et le budget configuré le cas échéant. Langue : français par défaut.
