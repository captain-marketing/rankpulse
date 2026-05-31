# Rankpulse

<p align="center">
  <img src="https://raw.githubusercontent.com/captain-marketing/rankpulse/main/docs/banner.svg" alt="Rankpulse banner" width="100%">
</p>

**Real-time SEO data layer for Claude Code.** Powered by DataForSEO, Google Search Console, and Google Analytics 4.

SERP · Keywords · Backlinks · Technical Audit · Content Gap · AEO · Position Dashboard — with real-time API cost tracking.

> 🇫🇷 [Version française](README.fr.md)

---

## Features

| Skill | Command | What it does |
|---|---|---|
| Setup | `/rankpulse:setup` | Configure DataForSEO credentials + monthly budget |
| SERP | `/rankpulse:serp` | Google/Bing/YouTube analysis: top 10, SERP features, intent |
| Keywords | `/rankpulse:keywords` | Keyword research + thematic clustering (volume, difficulty, intent) |
| Backlinks | `/rankpulse:backlinks` | Link profile, spam score, competitor comparison |
| Audit | `/rankpulse:audit` | Technical + on-page audit (3 layers: DataForSEO + GSC + GA4) |
| Content Gap | `/rankpulse:content-gap` | Competitor keywords absent from your domain |
| AEO | `/rankpulse:aeo` | Brand visibility in LLMs (ChatGPT, Gemini…) |
| Track | `/rankpulse:track` | Weekly position tracking in local SQLite |
| Dashboard | `/rankpulse:dashboard` | Standalone interactive HTML report (no server required) |

**Orchestrated agents:**
- `/rankpulse:audit-full <domain>` — Full SEO audit scored 0-100 + action plan
- `/rankpulse:brief <keyword>` — Complete SEO editorial brief ready to use
- `/rankpulse:watch <domain> --vs <competitor>` — Comparative competitive intelligence

---

## Installation

```
/plugin install github:captain-marketing/rankpulse
```

Then configure credentials:
```
/rankpulse:setup
```

---

## Requirements

- **Claude Code** (CLI or desktop)
- **DataForSEO account** — [dataforseo.com](https://dataforseo.com) · ~$5 credit to get started
- **Python 3** — for scripts and Google clients (Tier 1+)
- **Node.js + npx** — for the DataForSEO MCP server

**Google APIs (optional):**
- GCP Service Account or OAuth client for Google Search Console (Tier 1)
- + GA4 Property ID for Google Analytics 4 (Tier 2)

---

## Quick Start

```
# 1. Configure DataForSEO
/rankpulse:setup

# 2. Analyze a SERP
/rankpulse:serp "marketing automation" --locale "United States / en"

# 3. Keyword research
/rankpulse:keywords "marketing automation" --depth standard

# 4. Audit a page
/rankpulse:audit https://your-site.com/your-page

# 5. Track positions
/rankpulse:track add your-site.com --keywords "kw1,kw2,kw3"
/rankpulse:dashboard
```

---

## Google Tier System

Rankpulse is **100% functional without any Google credentials** (Tier 0). The following tiers are optional enhancements:

| Tier | Requirements | What it unlocks |
|---|---|---|
| 0 | DataForSEO only | Everything (SERP, keywords, backlinks, technical audit, gap) |
| 1 | + Google Search Console | Real indexation, impressions, CTR, actual position |
| 2 | + GA4 Property ID | Organic sessions, conversions, engagement |

---

## Security & Privacy

- Credentials **never** in the repo — stored in `~/.config/rankpulse/` with `0600` permissions
- Tracking data **100% local** (SQLite, no external transmission)
- API costs **read from DataForSEO responses** (not estimated), logged locally

---

## Documentation

- [DataForSEO Setup Guide](docs/SETUP.md)
- [Google APIs Guide (GSC + GA4)](docs/GOOGLE-SETUP.md)
- [Commands Reference](docs/COMMANDS.md)
- [Cost Guide](docs/COST-GUIDE.md)
- [Dashboard Guide](docs/DASHBOARD.md)

---

## Author

**Stéphane Truphème** · [Captain Marketing](https://captainmarketing.io)

This plugin is **independent** from DataForSEO, Google, and Anthropic.

---

## License

MIT — see [LICENSE](LICENSE)
