---
name: serp
description: Analyse la SERP Google (et Bing/YouTube) pour un mot-clé via DataForSEO — positions organiques, SERP features, intention dominante et opportunités. À utiliser quand l'utilisateur veut voir qui se classe sur une requête, analyser une page de résultats, ou comprendre le paysage concurrentiel d'un mot-clé. Invocable via /rankpulse:serp.
---

# Rankpulse — Analyse SERP

Analyse en direct une page de résultats de recherche et la transforme en lecture actionnable.

## Prérequis
- Credentials DataForSEO configurés (`/rankpulse:setup`). Si les outils `mcp__dataforseo__*` sont indisponibles, renvoyer vers le setup.

## Paramètres (langage naturel)
- **keyword** (requis) : la requête à analyser.
- **locale** : pays/langue (défaut `France / fr`). Mapper vers `location_name` + `language_code` DataForSEO.
- **device** : `desktop` (défaut) ou `mobile`.
- **moteur** : `google` (défaut), `bing` ou `youtube`.

## Procédure

1. **Coût.** L'appel SERP Live Advanced coûte ~$0.002–0.006. Si le mot-clé fait partie d'un lot (> 10 requêtes), prévenir du coût cumulé avant de lancer.

2. **Récupérer la SERP** via `mcp__dataforseo__serp_organic_live_advanced` (ou `serp_youtube_organic_live_advanced` pour YouTube). Passer `keyword`, `location_name`, `language_code`, `device`. Demander assez de profondeur pour couvrir le top 10–20.

3. **Analyser** et produire :
   - **Top 10 organique** : position, domaine, titre, URL, type de résultat.
   - **SERP features présentes** : featured snippet, People Also Ask, images, vidéos, local pack, AI Overview… (signalent l'intention et les formats à viser).
   - **Intention dominante** : informationnelle / commerciale / transactionnelle / navigationnelle, déduite des résultats et des features.
   - **Diversité concurrentielle** : marques vs éditeurs vs places de marché ; un domaine domine-t-il plusieurs positions ?
   - **Opportunités** : featured snippet capturable, PAA à adresser, formats sous-exploités, intention mal couverte par les pages en place.

4. **Livrable** (français par défaut, sinon `--lang`) : tableau du top 10 + synthèse intention + 3 à 5 recommandations priorisées. Rester concis ; ne pas recracher le JSON brut.

## Ne pas faire
- Ne pas inventer de positions : si DataForSEO ne renvoie pas un résultat, le dire.
- Ne pas multiplier les appels (un par locale/device demandé), pour maîtriser le coût.
