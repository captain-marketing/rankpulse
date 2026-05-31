---
name: content-gap
description: Analyse les mots-clés sur lesquels un concurrent se classe mais pas le domaine cible (gap analysis), et identifie les opportunités de contenu à fort potentiel. À utiliser quand l'utilisateur veut comprendre pourquoi un concurrent le surpasse, trouver des sujets de contenu manquants, ou prioriser sa stratégie éditoriale face à la concurrence. Invocable via /rankpulse:content-gap.
---

# Rankpulse — Content Gap Analysis

Identifie les opportunités de contenu que le concurrent exploite et que le domaine cible manque.

## Prérequis
- Credentials DataForSEO configurés (`/rankpulse:setup`).

## Paramètres (langage naturel)
- **domain** (requis) : domaine cible.
- **vs** (requis) : domaine concurrent (1 à 3 domaines).
- **locale** : pays/langue (défaut `France / fr`).
- **focus** : `gaps` (défaut — mots-clés du concurrent absents de la cible) ou `overlap` (mots-clés communs, positions comparées).

## Procédure

1. **Coût.** DataForSEO Labs coûte ~$0.02–0.10 selon la taille des domaines. Annoncer avant de lancer.

2. **Récupérer les mots-clés classés** :
   - Domaine cible : `mcp__dataforseo__dataforseo_labs_google_ranked_keywords` (top 1000 positions)
   - Chaque concurrent : idem

3. **Intersection / gap** via `mcp__dataforseo__dataforseo_labs_google_domain_intersection` : obtenir les mots-clés communs (avec positions comparées) et les exclusifs par domaine.

4. **Analyser les gaps** (mots-clés où le concurrent se classe, pas le domaine cible) :
   - Filtrer par volume ≥ 100 et difficulté raisonnable.
   - Regrouper par intention (informationnelle, commerciale, transactionnelle).
   - Identifier les clusters thématiques non couverts vs sous-couverts (page existe mais mal classée).

5. **Analyser les overlaps** (si `focus=overlap`) :
   - Mots-clés communs où le concurrent est mieux classé : pourquoi ? (autorité ? contenu plus complet ? backlinks ?)

6. **Livrable** (français par défaut, sinon `--lang`) :
   - **Top gaps** : tableau (mot-clé, volume, difficulté, position concurrent) trié par opportunité.
   - **Clusters manquants** : thèmes entiers absents du domaine cible.
   - **Pages à créer** vs **pages à améliorer** : distinction claire.
   - 5 à 10 priorités actionnables ordonnées par ROI estimé (volume × difficulté inversée).

## Ne pas faire
- Ne pas générer le contenu des articles — Rankpulse identifie les gaps, la rédaction est déléguée.
- Ne pas comparer plus de 3 concurrents simultanément (coût et lisibilité).
- Ne pas inclure les mots-clés branded du concurrent dans les recommandations.
