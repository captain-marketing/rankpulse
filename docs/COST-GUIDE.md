# Guide des coûts API DataForSEO

Rankpulse suit les coûts en temps réel et vous avertit quand votre budget mensuel est atteint. Ce guide détaille le coût par endpoint et les bonnes pratiques pour maîtriser les dépenses.

## Coûts par commande

| Commande | Endpoints utilisés | Coût estimé par appel |
|---|---|---|
| `/rankpulse:serp` | SERP Organic Live Advanced | $0.002 – $0.006 |
| `/rankpulse:keywords` (quick) | Labs Keyword Ideas | ~$0.010 |
| `/rankpulse:keywords` (standard) | + Related + Suggestions | ~$0.025 |
| `/rankpulse:keywords` (deep) | + Bulk Difficulty + Intent | ~$0.060 |
| `/rankpulse:backlinks` (quick) | Backlinks Summary | ~$0.010 |
| `/rankpulse:backlinks` (standard) | + Referring Domains + Anchors | ~$0.030 |
| `/rankpulse:audit` (Tier 0) | On-Page Instant + Lighthouse | ~$0.015 |
| `/rankpulse:content-gap` | Domain Intersection + Ranked Keywords | ~$0.040 |
| `/rankpulse:aeo` (par moteur) | LLM Mentions + ChatGPT Scraper | $0.050 – $0.200 |
| `/rankpulse:track snapshot` (par mot-clé) | SERP Organic Live Advanced | $0.002 – $0.006 |
| `/rankpulse:audit-full` (agent complet) | Combinaison de 4–5 appels | $0.10 – $0.25 |
| `/rankpulse:brief` (agent) | SERP + Keywords + Gap | ~$0.08 |
| `/rankpulse:watch` (agent) | SERP × N + Backlinks + Gap | $0.05 – $0.15 |

> Les coûts DataForSEO sont facturés en USD, prélevés sur votre solde de compte. Ils varient selon le volume de résultats demandés.

## ⚠️ API Backlinks — engagement minimum requis

L'API Backlinks DataForSEO nécessite un **engagement minimum de $100/mois** souscrit séparément. Sans cet abonnement, toute requête backlinks renvoie une erreur `40204`.

- Les skills `/rankpulse:backlinks` et `/rankpulse:watch` fonctionnent en mode dégradé sans backlinks (positions SERP et gap analysis disponibles, profil de liens indisponible).
- Pour activer : contacter DataForSEO support et demander l'accès Backlinks API.
- Alternative gratuite pour estimer l'autorité : Ahrefs Free (Ahrefs.com → Free Backlink Checker).

## Endpoints les plus coûteux

**À surveiller particulièrement :**

1. **AEO / LLM Mentions** — $0.05 à $0.20 par requête/moteur. Utiliser `--engines chatgpt` en ciblé plutôt que `--engines all`.
2. **Keywords deep** — Le mode `deep` enchaîne 4 endpoints. Sur une liste de 50 mots-clés, comptez $2–4.
3. **Backlinks sur gros domaines** — Les referring domains et anchors sur les domaines avec des millions de backlinks peuvent renvoyer de gros volumes.

## Suivi des coûts en temps réel

Rankpulse enregistre chaque coût réel (champ `cost` des réponses DataForSEO) dans `~/.config/rankpulse/usage.log` :

```json
{"ts": "2026-05-30T10:00:00+00:00", "tool": "mcp__dataforseo__serp_organic_live_advanced", "cost": 0.003}
```

En fin de session, le coût du mois est affiché automatiquement.

## Configurer un budget mensuel

```bash
echo '{ "monthly_usd": 50 }' > ~/.config/rankpulse/budget.json
chmod 600 ~/.config/rankpulse/budget.json
```

Rankpulse affiche un avertissement dès que le budget est atteint (sans bloquer).

## Bonnes pratiques

**Réduire les coûts :**
- Utiliser `depth=quick` pour l'exploration initiale, `standard` ou `deep` uniquement pour les sujets validés.
- Pour le tracking, limiter à 10–15 mots-clés prioritaires par domaine.
- Sur l'AEO, tester un moteur à la fois avant de lancer `--engines all`.
- Éviter les snapshots manuels répétés — laisser l'automatisation hebdomadaire faire le travail.

**Estimation avant un gros appel :**
Les skills affichent le coût estimé avant toute requête > $0.01. Une confirmation est demandée au-dessus de $0.50.

## Budget mensuel recommandé

| Profil | Usage typique | Budget suggéré |
|---|---|---|
| Découverte / test | Quelques analyses par semaine | $10–20/mois |
| Consultant solo | 5–10 domaines suivis, audits réguliers | $30–60/mois |
| Agence (10+ clients) | Audits full + tracking intensif + AEO | $100–200/mois |
