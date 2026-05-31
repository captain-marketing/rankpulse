---
name: aeo
description: Analyse la visibilité d'une marque ou d'un domaine dans les réponses des LLMs (ChatGPT, Gemini, Perplexity, etc.) via DataForSEO AI Optimization. Mesure les mentions, les positions dans les citations, et compare avec les concurrents. Invocable via /rankpulse:aeo.
---

# Rankpulse — AEO (AI Engine Optimization)

Mesure la présence d'une marque dans les réponses générées par les LLMs — la nouvelle frontière du référencement.

## Prérequis
- Credentials DataForSEO configurés (`/rankpulse:setup`).
- Note de coût : les endpoints AI Optimization sont parmi les plus coûteux de DataForSEO (~$0.05–0.20 par requête). Toujours annoncer le coût avant d'exécuter.

## Paramètres (langage naturel)
- **brand** (requis) : nom de la marque ou domaine à analyser (ex. `Captain Marketing` ou `captainmarketing.io`).
- **engines** : LLMs à interroger (défaut : tous disponibles). Options : `chatgpt`, `gemini`, `perplexity`, `claude`, ou `all`.
- **keywords** : liste de requêtes sur lesquelles tester la visibilité (ex. `"consultant marketing IA,agence marketing digital"`). Si absent, utiliser les 5 requêtes principales issues de `track` ou `keywords`.
- **compare** : marque concurrente optionnelle.
- **lang** : langue (défaut `fr`).

## Procédure

1. **Récupérer les modèles disponibles** via `mcp__dataforseo__ai_optimization_llm_models` pour confirmer quels LLMs sont accessibles.

2. **Annoncer le coût estimé** : X requêtes × Y moteurs × ~$0.05–0.20 = total estimé. Demander confirmation si > $0.50.

3. **Rechercher les mentions** pour chaque keyword via `mcp__dataforseo__ai_opt_llm_ment_search`. Paramètres : `keyword`, `language_code`, filtre sur `brand`.

4. **Métriques agrégées** via `mcp__dataforseo__ai_opt_llm_ment_agg_metrics` : taux de mention global, position moyenne dans les citations, fréquence par moteur.

5. **Top domaines cités** (concurrence indirecte AEO) via `mcp__dataforseo__ai_opt_llm_ment_top_domains` : qui est systématiquement cité à la place de la marque ?

6. **Si `--compare` fourni** : `mcp__dataforseo__ai_opt_llm_ment_cross_agg_metrics` pour la comparaison directe des deux marques.

7. **Optionnel — ChatGPT en direct** : si `chatgpt` dans les engines, `mcp__dataforseo__ai_optimization_chat_gpt_scraper` pour une réponse live à une requête clé.

## Livrable (français par défaut)

**Rapport AEO — [BRAND]**

**Visibilité globale**
- Taux de mention : X% des requêtes testées contiennent une référence à [brand]
- Position moyenne dans les citations : X/N sources citées
- Moteurs les plus favorables : [classement]

**Par mot-clé**
| Requête | Mentionné | Moteurs | Position moy. |
|---|---|---|---|
| [kw] | ✅/❌ | GPT, Gemini | X |

**Concurrents qui vous supplantent dans les LLMs**
| Domaine | Taux citation | Gap vs [brand] |
|---|---|---|

**Recommandations AEO**
1. Contenu à créer/optimiser pour augmenter les citations (basé sur les requêtes à 0%)
2. Formats préférés des LLMs pour ce secteur (listes, définitions, comparatifs)
3. Sources à cibler pour l'authority building LLM (sites souvent cités dans les réponses)

## Ne pas faire
- Ne pas lancer tous les engines sur toutes les requêtes sans confirmation du coût.
- Ne pas interpréter une absence de mention comme une erreur — c'est une opportunité.
