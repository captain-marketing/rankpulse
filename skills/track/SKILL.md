---
name: track
description: Déclare les domaines et mots-clés à surveiller dans Rankpulse, prend des snapshots de positions et gère la base de suivi locale. Propose l'automatisation hebdomadaire via launchd (macOS) ou cron. Invocable via /rankpulse:track.
---

# Rankpulse — Suivi de positions

Gère la base de suivi locale (`~/.config/rankpulse/tracking.db`) et les snapshots de positions.

## Prérequis
- Credentials DataForSEO configurés (`/rankpulse:setup`).
- Python 3 + module `sqlite3` (stdlib — aucune dépendance externe).

## Sous-commandes

### `add` — Ajouter un domaine et ses mots-clés
```
/rankpulse:track add <domain> --keywords "kw1,kw2,kw3" [--locale "France / fr"]
```

1. Ouvrir (ou créer) `~/.config/rankpulse/tracking.db` avec ce schéma :
```sql
CREATE TABLE IF NOT EXISTS domains (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS keywords (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain_id INTEGER REFERENCES domains(id) ON DELETE CASCADE,
  keyword TEXT NOT NULL,
  locale TEXT DEFAULT 'France',
  language TEXT DEFAULT 'fr',
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER REFERENCES keywords(id) ON DELETE CASCADE,
  taken_at TEXT NOT NULL,
  position INTEGER,
  url TEXT,
  title TEXT
);
```
2. Insérer le domaine (ou ignorer si déjà présent) puis les mots-clés.
3. Prendre un premier snapshot immédiat : appeler le skill `serp` pour chaque mot-clé et stocker les résultats dans `snapshots`. Signaler les mots-clés pour lesquels la page du domaine n'apparaît pas dans le top 20.
4. **Proposer l'automatisation** : si `launchd` est disponible (macOS), proposer de créer un plist dans `~/Library/LaunchAgents/io.rankpulse.snapshot.plist` qui lance `scripts/snapshot.sh` chaque lundi matin à 8h. Attendre confirmation avant d'écrire.

### `list` — Voir les domaines et mots-clés suivis
```
/rankpulse:track list [--domain <domain>]
```
Afficher un tableau : domaine, mots-clés, date du dernier snapshot, dernières positions connues.

### `remove` — Supprimer un domaine ou un mot-clé
```
/rankpulse:track remove <domain> [--keyword <kw>]
```
Supprimer le domaine entier (+ mots-clés + snapshots en cascade) ou un mot-clé spécifique.

### `snapshot` — Snapshot manuel immédiat
```
/rankpulse:track snapshot [--domain <domain>]
```
Prendre un snapshot de position pour tous les mots-clés trackés (ou d'un domaine seul). Appeler `serp` pour chaque mot-clé et upsert dans `snapshots`. Afficher un résumé des positions avant/après.

## Gestion des coûts
Chaque snapshot consomme 1 appel SERP par mot-clé (~$0.002–0.006 chacun). Avant de lancer un snapshot massif (> 10 mots-clés), afficher le coût estimé total et demander confirmation.

## Sortie attendue
Confirmation des mots-clés ajoutés, premier snapshot pris, coût consommé, et instruction claire pour activer ou non l'automatisation hebdomadaire. Français par défaut.
