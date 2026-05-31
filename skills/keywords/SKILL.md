---
name: keywords
description: Recherche de mots-clés et clustering via DataForSEO Labs — idées, requêtes liées, suggestions, volumes, difficulté et intention, regroupés en clusters thématiques actionnables. À utiliser quand l'utilisateur veut explorer un univers de mots-clés, trouver des opportunités, ou construire un plan de contenu autour d'un sujet. Invocable via /rankpulse:keywords.
---

# Rankpulse — Keyword Research + Clustering

Explore l'univers d'un mot-clé seed et le structure en clusters exploitables pour une stratégie de contenu.

## Prérequis
- Credentials DataForSEO configurés (`/rankpulse:setup`).

## Paramètres (langage naturel)
- **keyword** (requis) : le mot-clé seed.
- **locale** : pays/langue (défaut `France / fr`) → `location_name` + `language_code`.
- **depth** : `quick` (idées + volumes), `standard` (défaut : idées + related + suggestions), `deep` (+ difficulté + intention).

## Procédure

1. **Coût.** Les endpoints Labs coûtent ~$0.01–0.05 selon le volume de résultats. Annoncer le coût estimé avant un `deep`.

2. **Collecter** selon la profondeur :
   - Idées : `mcp__dataforseo__dataforseo_labs_google_keyword_ideas`
   - Requêtes liées : `mcp__dataforseo__dataforseo_labs_google_related_keywords`
   - Suggestions longue traîne : `mcp__dataforseo__dataforseo_labs_google_keyword_suggestions`
   - Volumes/CPC : présents dans les retours Labs, sinon `mcp__dataforseo__kw_data_google_ads_search_volume`
   - (deep) Difficulté : `mcp__dataforseo__dataforseo_labs_bulk_keyword_difficulty` ; Intention : `mcp__dataforseo__dataforseo_labs_search_intent`

3. **Dédupliquer et enrichir** : fusionner les sources, retirer les doublons, garder pour chaque mot-clé volume, CPC, (deep) difficulté et intention.

4. **Clusteriser** par proximité sémantique / intention partagée. Pour chaque cluster :
   - thème, intention dominante, volume cumulé,
   - mots-clés pivots (fort volume / difficulté raisonnable),
   - opportunités longue traîne (faible difficulté, intention claire).

5. **Livrable** (français par défaut, sinon `--lang`) :
   - Tableau par cluster (thème, volume cumulé, intention, top mots-clés).
   - 5 à 10 opportunités prioritaires (bon ratio volume/difficulté).
   - Suggestion de structure de contenu (page pilier + articles satellites) si pertinent.

## Ne pas faire
- Ne pas générer le contenu rédigé — ce n'est pas le rôle de Rankpulse (passer le relais à un plugin de rédaction).
- Ne pas dépasser la profondeur demandée pour limiter le coût.
