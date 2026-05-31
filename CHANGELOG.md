# Changelog

Toutes les modifications notables de Rankpulse sont documentées ici.
Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

---

## [1.0.0] — 2026-05-30

### Ajouté

**Skills (10)**
- `setup` — Configuration credentials DataForSEO + budget mensuel + test connexion
- `google-setup` — Wizard Service Account / OAuth pour GSC (Tier 1) et GA4 (Tier 2)
- `serp` — Analyse SERP Google/Bing/YouTube : top 10, SERP features, intention dominante
- `keywords` — Keyword research + clustering (quick / standard / deep)
- `backlinks` — Profil de liens : autorité, spam score, ancres, comparaison concurrent
- `audit` — Audit 3 couches : technique DataForSEO + visibilité GSC + performance GA4
- `content-gap` — Gap analysis concurrentiel : mots-clés absents, clusters manquants
- `aeo` — AI Engine Optimization : visibilité marque dans les LLMs (ChatGPT, Gemini…)
- `track` — Suivi positions SQLite local avec automatisation hebdomadaire (launchd/cron)
- `dashboard` — Dashboard HTML standalone : courbes SVG, alertes, résumé coûts

**Agents (3)**
- `seo-auditor` — Audit complet scoré 0-100 : SERP + backlinks + audit + gap en séquence
- `brief-factory` — Brief éditorial SEO : SERP → keywords → gap → structure complète
- `competitor-watcher` — Veille comparée : positions, backlinks, gaps, alertes delta

**Commands (3)**
- `audit-full` — Déclenche l'agent `seo-auditor`
- `brief` — Déclenche l'agent `brief-factory`
- `watch` — Déclenche l'agent `competitor-watcher`

**Infrastructure**
- MCP DataForSEO `v2.9.4` épinglé via launcher sécurisé (`mcp-launch.sh`)
- Credentials via `~/.config/rankpulse/credentials.env` (0600) — jamais dans le repo
- Field filtering natif : `DATAFORSEO_SIMPLE_FILTER=true` côté serveur MCP
- Hooks `PreToolUse` + `PostToolUse` + `SessionEnd` pour suivi coûts en temps réel
- `cost-tracker.py` : lit le coût réel des réponses DataForSEO, log JSONL, alerte budget
- `gsc_client.py` + `ga4_client.py` : clients Python Tier 1/2 (Service Account ou OAuth)
- `dashboard-generator.py` : HTML standalone, SVG inline, zéro dépendance externe
- `snapshot.sh` : snapshots SQLite via launchd/cron (remplace le hook Schedule inexistant)

**Documentation**
- `docs/SETUP.md`, `docs/GOOGLE-SETUP.md`, `docs/COMMANDS.md`
- `docs/COST-GUIDE.md`, `docs/DASHBOARD.md`
- `tests/test-connections.sh`, `tests/test-google-apis.sh`
