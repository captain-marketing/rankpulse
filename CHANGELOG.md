# Changelog

All notable changes to Rankpulse are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

> 🇫🇷 [Version française](CHANGELOG.fr.md)

---

## [1.0.0] — 2026-05-30

### Added

**Skills (10)**
- `setup` — DataForSEO credentials configuration + monthly budget + connection test
- `google-setup` — Service Account / OAuth wizard for GSC (Tier 1) and GA4 (Tier 2)
- `serp` — SERP analysis Google/Bing/YouTube: top 10, SERP features, dominant intent
- `keywords` — Keyword research + clustering (quick / standard / deep)
- `backlinks` — Link profile: authority, spam score, anchors, competitor comparison
- `audit` — 3-layer audit: technical DataForSEO + GSC visibility + GA4 performance
- `content-gap` — Competitive gap analysis: missing keywords, missing clusters
- `aeo` — AI Engine Optimization: brand visibility in LLMs (ChatGPT, Gemini…)
- `track` — Local SQLite position tracking with weekly automation (launchd/cron)
- `dashboard` — Standalone HTML dashboard: inline SVG curves, alerts, cost summary

**Agents (3)**
- `seo-auditor` — Full domain audit scored 0-100: SERP + backlinks + audit + gap in sequence
- `brief-factory` — SEO editorial brief: SERP → keywords → gap → complete structure
- `competitor-watcher` — Comparative intelligence: positions, backlinks, gaps, delta alerts

**Commands (3)**
- `audit-full` — Triggers the `seo-auditor` agent
- `brief` — Triggers the `brief-factory` agent
- `watch` — Triggers the `competitor-watcher` agent

**Infrastructure**
- DataForSEO MCP `v2.9.4` pinned via secure launcher (`mcp-launch.sh`)
- Credentials via `~/.config/rankpulse/credentials.env` (0600) — never in the repo
- Native field filtering: `DATAFORSEO_SIMPLE_FILTER=true` on the MCP server side
- `PreToolUse` + `PostToolUse` + `SessionEnd` hooks for real-time cost tracking
- `cost-tracker.py`: reads actual cost from DataForSEO responses, logs JSONL, budget alert
- `gsc_client.py` + `ga4_client.py`: Python Tier 1/2 clients (Service Account or OAuth)
- `dashboard-generator.py`: standalone HTML report, inline SVG, no external dependencies
- `snapshot.sh`: SQLite snapshots via launchd/cron (replaces the non-existent Schedule hook)

**Documentation**
- `docs/SETUP.md`, `docs/GOOGLE-SETUP.md`, `docs/COMMANDS.md`
- `docs/COST-GUIDE.md`, `docs/DASHBOARD.md`
- `tests/test-connections.sh`, `tests/test-google-apis.sh`
- Full bilingual documentation (English + French)
