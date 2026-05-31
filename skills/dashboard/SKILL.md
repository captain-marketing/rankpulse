---
name: dashboard
description: Génère un rapport HTML interactif standalone des positions trackées et l'ouvre dans le navigateur. Lit la base tracking.db locale, produit un fichier HTML auto-contenu (zéro dépendance externe) avec courbes d'évolution, alertes et résumé de coûts. Invocable via /rankpulse:dashboard.
---

# Rankpulse — Dashboard Positions

Génère le rapport HTML de suivi des positions à partir de la base locale.

## Prérequis
- Mots-clés trackés (`/rankpulse:track add` doit avoir été exécuté).
- Python 3 + module `sqlite3` (stdlib).
- `~/.config/rankpulse/tracking.db` doit exister et contenir au moins un snapshot.

## Paramètres (langage naturel)
- **domain** : filtrer sur un domaine spécifique (défaut : tous les domaines trackés).
- **period** : fenêtre d'affichage — `4w`, `8w`, `12w` (défaut) ou `90d`, `180d`.
- **output** : chemin de sortie du fichier HTML (défaut : `~/.config/rankpulse/dashboard.html`).

## Procédure

1. **Vérifier les données** : confirmer que `tracking.db` existe et contient des snapshots. Si vide ou absent, rediriger vers `/rankpulse:track add`.

2. **Prendre un snapshot à la volée** si le dernier en base date de plus de 7 jours (sauf si `--no-snapshot` passé). Appeler `scripts/snapshot.sh` en sous-processus.

3. **Générer le dashboard** en appelant `scripts/dashboard-generator.py` avec les paramètres :
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/dashboard-generator.py" \
     --domain "<domain ou vide>" \
     --period "<period>" \
     --output "<output>"
   ```

4. **Ouvrir dans le navigateur** :
   - macOS : `open <output>`
   - Linux : `xdg-open <output>`

5. **Confirmer** : afficher le chemin du fichier généré, le nombre de mots-clés affichés, la plage de dates couverte, et le coût DataForSEO du mois en cours (depuis `usage.log`).

## Contenu du dashboard HTML généré
- En-tête : domaine(s) suivi(s), période, date de génération
- Courbes SVG inline par mot-clé : évolution de position semaine par semaine
- Tableau récap : position actuelle, meilleure position, tendance (▲/▼/=)
- Alertes : gains/pertes > 3 positions en rouge/vert
- Section coûts : dépenses DataForSEO du mois, projection mensuelle
- Pied de page : date du prochain snapshot automatique (si launchd actif)

## Sortie attendue
Confirmation que le fichier est généré et ouvert. Français par défaut.
