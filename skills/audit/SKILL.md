---
name: audit
description: Audit technique et on-page d'une URL via DataForSEO (Tier 0), enrichi par Google Search Console (Tier 1) et Google Analytics 4 (Tier 2) si configurés. Produit un score global 0-100 et des recommandations priorisées par impact réel. À utiliser quand l'utilisateur veut auditer une page ou un domaine, diagnostiquer un problème de référencement, ou obtenir un rapport d'optimisation actionnable. Invocable via /rankpulse:audit.
---

# Rankpulse — Audit On-Page + Technique

Audit en 1 à 3 couches selon les credentials disponibles. Tier 0 fonctionne sans aucun accès Google.

## Prérequis
- **Tier 0** : Credentials DataForSEO uniquement (`/rankpulse:setup`). Toujours disponible.
- **Tier 1** : Google Search Console configuré (`/rankpulse:google-setup`). Optionnel.
- **Tier 2** : GA4 configuré (`/rankpulse:google-setup`). Optionnel.

## Paramètres (langage naturel)
- **url** (requis) : URL complète à auditer (ex. `https://captainmarketing.io/marketing-ia`).
- **tier** : forcer `0`, `1`, ou `2`. Par défaut : utilise le tier maximum disponible.
- **lang** : langue du rapport (défaut `fr`).

## Procédure

### Tier 0 — Analyse technique DataForSEO

1. **Récupérer le contenu de la page** via `mcp__dataforseo__on_page_instant_pages`. Extraire : balises SEO (title, meta description, H1-H3), texte principal, liens internes/externes.

2. **Analyse Lighthouse** via `mcp__dataforseo__on_page_lighthouse` : Core Web Vitals (LCP, CLS, FID/INP), performance, accessibilité.

3. **Analyse SERP de l'URL** (optionnel, si keyword fourni) : `mcp__dataforseo__serp_organic_live_advanced` pour voir la position actuelle.

4. **Scoring Tier 0** sur 40 points :
   - Technique : vitesse, Core Web Vitals, mobile-friendly (15 pts)
   - On-page : title, meta, H1, structure contenu, densité mots-clés (15 pts)
   - Liens : internes, externes, brisés (10 pts)

### Tier 1 — Enrichissement GSC (si configuré)

5. **Appeler** `scripts/gsc_client.py` en sous-processus avec l'URL et les credentials `~/.config/rankpulse/google-api.json`.

6. **Données récupérées** : statut d'indexation, impressions/clics/CTR/position moyenne sur 90 jours, mots-clés qui apportent du trafic, URL Inspection (canonique, couverture, problèmes).

7. **Scoring Tier 1** : +30 points supplémentaires (visibilité réelle dans Google).

### Tier 2 — Enrichissement GA4 (si configuré)

8. **Appeler** `scripts/ga4_client.py` en sous-processus avec l'URL et le GA4 Property ID.

9. **Données récupérées** : sessions organiques, taux d'engagement, pages par session, conversions canal organique, répartition mobile/desktop.

10. **Scoring Tier 2** : +30 points supplémentaires (performance business réelle).

### Score global et livrable

11. **Score final** : total pondéré sur 100. Seuils : 0-40 critique / 41-65 à améliorer / 66-85 bon / 86-100 excellent.

12. **Livrable** (français par défaut) :
    - Score global + décomposition par couche disponible.
    - Tableau des problèmes critiques (bloquants SEO).
    - Recommandations priorisées par impact (Quick Wins → Chantiers longs).
    - Si Tier 1/2 : croisement visibilité × performance (ex. : « forte impression, CTR faible → problème de title/meta »).

## Ne pas faire
- Ne pas signaler l'absence de Tier 1/2 comme une erreur — indiquer clairement ce qu'un tier supplémentaire apporterait.
- Ne pas auditer un domaine entier en une passe (hors agent `seo-auditor`) — une URL à la fois.
- Ne pas halluciner de métriques GSC/GA4 si les scripts renvoient une erreur ; afficher l'erreur et proposer le diagnostic.
