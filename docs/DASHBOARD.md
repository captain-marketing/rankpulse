# Guide du dashboard de positions

Le dashboard Rankpulse est un rapport HTML standalone généré localement — zéro serveur, zéro dépendance externe, zéro transmission de données.

## Démarrage rapide

```
# 1. Ajouter un domaine et ses mots-clés à suivre
/rankpulse:track add captainmarketing.io --keywords "marketing IA,consultant marketing IA,agence marketing digital"

# 2. Générer et ouvrir le dashboard
/rankpulse:dashboard
```

## Workflow complet

### Étape 1 — Déclarer les mots-clés

```
/rankpulse:track add <domain> --keywords "kw1,kw2,kw3"
```

- Le premier `add` prend un snapshot immédiat de toutes les positions (coût : ~$0.003 par mot-clé).
- Le skill propose d'activer le snapshot automatique hebdomadaire via `launchd` (macOS).

**Conseil :** limiter à 10–15 mots-clés par domaine pour maîtriser les coûts. Privilégier les mots-clés sur lesquels vous avez déjà une position dans les 50 premiers résultats.

### Étape 2 — Consulter les mots-clés suivis

```
/rankpulse:track list
/rankpulse:track list --domain captainmarketing.io
```

### Étape 3 — Générer le dashboard

```
/rankpulse:dashboard
/rankpulse:dashboard --domain captainmarketing.io
/rankpulse:dashboard --period 8w
/rankpulse:dashboard --domain captainmarketing.io --period 90d --output ~/Desktop/seo-report.html
```

Le fichier HTML est ouvert automatiquement dans votre navigateur par défaut.

## Contenu du dashboard

### Vue d'ensemble
- En-tête : domaine(s) suivi(s), période, date de génération
- Résumé des coûts DataForSEO du mois en cours

### Tableau par domaine
| Colonne | Description |
|---|---|
| Mot-clé | La requête trackée |
| Position actuelle | Dernière position connue dans le top 20 Google |
| Meilleure | Meilleure position historique sur la période |
| Tendance | Badge coloré ▲ (gain) / ▼ (perte) / = (stable) si delta > 3 |
| Évolution | Courbe SVG inline des positions semaine par semaine |

### Alertes visuelles
- 🟢 **Gain ≥ 3 positions** — badge vert
- 🔴 **Perte ≥ 3 positions** — badge rouge
- **Hors top 20** — indiqué en gris italique (la page n'apparaît pas dans les 20 premiers résultats)

## Automatisation hebdomadaire

Après le premier `/rankpulse:track add`, le skill propose de créer un agent launchd sur macOS :

```xml
<!-- ~/Library/LaunchAgents/io.rankpulse.snapshot.plist -->
<!-- Exécute snapshot.sh chaque lundi à 08:00 -->
```

Pour activer manuellement sur macOS :
```bash
# Créer le plist (demander à /rankpulse:track de le générer)
launchctl load ~/Library/LaunchAgents/io.rankpulse.snapshot.plist
```

Sur Linux (cron) :
```bash
# Ajouter via crontab -e
0 8 * * 1 /path/to/rankpulse/scripts/snapshot.sh >> ~/.config/rankpulse/snapshot.log 2>&1
```

## Stockage des données

| Fichier | Contenu | Taille typique |
|---|---|---|
| `~/.config/rankpulse/tracking.db` | Snapshots SQLite | ~2 Mo (12 mois × 20 mots-clés) |
| `~/.config/rankpulse/snapshot.log` | Log des snapshots automatiques | < 100 Ko |
| `~/.config/rankpulse/dashboard.html` | Dernier rapport généré | ~30–100 Ko |

Toutes les données restent 100 % locales. Aucune transmission externe.

## Réinitialiser le suivi

```
/rankpulse:track remove captainmarketing.io
```
Supprime le domaine, ses mots-clés et tous ses snapshots de la base.
