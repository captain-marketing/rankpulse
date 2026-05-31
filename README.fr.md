# Rankpulse

**Couche données SEO en temps réel pour Claude Code.** Propulsé par DataForSEO, Google Search Console et Google Analytics 4.

SERP · Keywords · Backlinks · Audit technique · Content Gap · AEO · Dashboard de positions — avec suivi des coûts API en temps réel.

---

## Fonctionnalités

| Skill | Commande | Ce que ça fait |
|---|---|---|
| Setup | `/rankpulse:setup` | Configure les credentials DataForSEO + budget mensuel |
| SERP | `/rankpulse:serp` | Analyse Google/Bing/YouTube : top 10, features, intention |
| Keywords | `/rankpulse:keywords` | Research + clustering thématique (volume, difficulté, intention) |
| Backlinks | `/rankpulse:backlinks` | Profil de liens, spam score, comparaison concurrent |
| Audit | `/rankpulse:audit` | Audit technique + on-page (3 couches : DataForSEO + GSC + GA4) |
| Content Gap | `/rankpulse:content-gap` | Mots-clés du concurrent absents de votre domaine |
| AEO | `/rankpulse:aeo` | Visibilité de votre marque dans les LLMs (ChatGPT, Gemini…) |
| Track | `/rankpulse:track` | Suivi de positions hebdomadaire en SQLite local |
| Dashboard | `/rankpulse:dashboard` | Rapport HTML interactif standalone (zéro serveur) |

**Agents orchestrés :**
- `/rankpulse:audit-full <domain>` — Audit complet scoré 0-100 + plan d'action
- `/rankpulse:brief <keyword>` — Brief éditorial SEO complet prêt à utiliser
- `/rankpulse:watch <domain> --vs <competitor>` — Veille concurrentielle comparée

---

## Installation

```
/plugin install github:captain-marketing/rankpulse
```

Puis configurer les credentials :
```
/rankpulse:setup
```

---

## Prérequis

- **Claude Code** (CLI ou desktop)
- **Compte DataForSEO** — [dataforseo.com](https://dataforseo.com) · ~$5 de crédit pour démarrer
- **Python 3** — pour les scripts et les clients Google (Phase 4+)
- **Node.js + npx** — pour le serveur MCP DataForSEO

**Google APIs (optionnel) :**
- Service Account GCP pour Google Search Console (Tier 1)
- + GA4 Property ID pour Google Analytics 4 (Tier 2)

---

## Démarrage rapide

```
# 1. Configurer DataForSEO
/rankpulse:setup

# 2. Analyser une SERP
/rankpulse:serp "marketing automation" --locale "France / fr"

# 3. Rechercher des mots-clés
/rankpulse:keywords "marketing automation" --depth standard

# 4. Auditer une page
/rankpulse:audit https://votre-site.com/votre-page

# 5. Tracker des positions
/rankpulse:track add votre-site.com --keywords "kw1,kw2,kw3"
/rankpulse:dashboard
```

---

## Système de tiers Google

Rankpulse est **100 % fonctionnel sans aucun credential Google** (Tier 0). Les tiers suivants sont des enrichissements optionnels :

| Tier | Prérequis | Ce que ça débloque |
|---|---|---|
| 0 | DataForSEO uniquement | Tout (SERP, keywords, backlinks, audit technique, gap) |
| 1 | + Google Search Console | Indexation réelle, impressions, CTR, position réelle |
| 2 | + GA4 Property ID | Sessions organiques, conversions, engagement |

---

## Sécurité et confidentialité

- Credentials **jamais** dans le repo — stockés dans `~/.config/rankpulse/` en `0600`
- Données de suivi **100 % locales** (SQLite, aucune transmission externe)
- Coûts API **lus dans les réponses** DataForSEO (pas estimés), loggés localement

---

## Documentation

- [Guide de configuration DataForSEO](docs/SETUP.md)
- [Guide Google APIs (GSC + GA4)](docs/GOOGLE-SETUP.md)
- [Référence des commandes](docs/COMMANDS.md)
- [Guide des coûts](docs/COST-GUIDE.md)
- [Guide du dashboard](docs/DASHBOARD.md)

---

## Auteur

**Stéphane Truphème** · [Captain Marketing](https://captainmarketing.io)

Ce plugin est **indépendant** de DataForSEO, Google et Anthropic.

---

## Licence

MIT — voir [LICENSE](LICENSE)
