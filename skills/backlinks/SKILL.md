---
name: backlinks
description: Analyse le profil de backlinks d'un domaine via DataForSEO — résumé d'autorité, domaines référents, ancres, spam score, et comparaison optionnelle avec un concurrent. À utiliser quand l'utilisateur veut auditer la qualité des liens entrants d'un site, identifier des opportunités de link building, ou comparer deux profils de liens. Invocable via /rankpulse:backlinks.
---

# Rankpulse — Analyse Backlinks

Audite le profil de liens entrants d'un domaine et identifie les opportunités et risques.

## Prérequis
- Credentials DataForSEO configurés (`/rankpulse:setup`).

## Paramètres (langage naturel)
- **domain** (requis) : domaine cible (ex. `captainmarketing.io`).
- **compare** : domaine concurrent optionnel pour une comparaison côte à côte.
- **depth** : `quick` (résumé seul) ou `standard` (défaut : résumé + referring domains + ancres).

## Procédure

1. **Coût.** Les endpoints backlinks coûtent ~$0.01–0.05 selon le volume. Annoncer avant un appel `standard` sur un gros domaine.

2. **Récupérer les données** selon la profondeur :
   - Résumé : `mcp__dataforseo__backlinks_summary` (autorité de domaine, total backlinks, domaines référents, spam score)
   - Domaines référents : `mcp__dataforseo__backlinks_referring_domains` (top domaines, leur autorité, type de lien follow/nofollow)
   - Ancres : `mcp__dataforseo__backlinks_anchors` (ancres les plus fréquentes et leur densité)
   - Si `--compare` fourni : `mcp__dataforseo__backlinks_domain_intersection` pour les domaines référents communs/exclusifs

3. **Analyser** :
   - **Autorité** : score de domaine, ratio follow/nofollow, diversité des domaines référents.
   - **Qualité** : spam score moyen, domaines référents de haute autorité vs faible.
   - **Ancres** : distribution naturelle (marque, URL, générique, exact-match) ou sur-optimisation.
   - **Si comparaison** : qui a l'avantage en volume et qualité, quels domaines référents le concurrent a-t-il que la cible n'a pas (opportunités de link building).

4. **Livrable** (français par défaut, sinon `--lang`) :
   - Tableau récap : score de domaine, backlinks totaux, domaines référents uniques, spam score.
   - Top 10 domaines référents (autorité + type).
   - Distribution des ancres + alerte si over-optimisation détectée.
   - 3 à 5 recommandations priorisées (liens à obtenir, risques à corriger).
   - Si comparaison : tableau différentiel + opportunités spécifiques.

## Ne pas faire
- Ne pas recracher l'intégralité du JSON brut — synthétiser.
- Ne pas effectuer plusieurs appels `referring_domains` avec pagination sur `quick`.
