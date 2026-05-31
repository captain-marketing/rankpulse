# Position Dashboard Guide

The Rankpulse dashboard is a standalone HTML report generated locally — no server, no external dependencies, no data transmission.

> 🇫🇷 [Version française](DASHBOARD.fr.md)

## Quick start

```
# 1. Add a domain and keywords to track
/rankpulse:track add captainmarketing.io --keywords "ai marketing,ai marketing consultant,digital marketing agency"

# 2. Generate and open the dashboard
/rankpulse:dashboard
```

## Full workflow

### Step 1 — Declare keywords

```
/rankpulse:track add <domain> --keywords "kw1,kw2,kw3"
```

- The first `add` immediately takes a snapshot of all positions (cost: ~$0.003 per keyword).
- The skill offers to activate weekly automatic snapshots via `launchd` (macOS).

**Tip:** limit to 10–15 keywords per domain to control costs. Prioritise keywords where you already have a position in the top 50 results.

### Step 2 — List tracked keywords

```
/rankpulse:track list
/rankpulse:track list --domain captainmarketing.io
```

### Step 3 — Generate the dashboard

```
/rankpulse:dashboard
/rankpulse:dashboard --domain captainmarketing.io
/rankpulse:dashboard --period 8w
/rankpulse:dashboard --domain captainmarketing.io --period 90d --output ~/Desktop/seo-report.html
```

The HTML file is automatically opened in your default browser.

## Dashboard content

### Overview
- Header: tracked domain(s), period, generation date
- Summary of DataForSEO costs for the current month

### Per-domain table

| Column | Description |
|---|---|
| Keyword | The tracked query |
| Current position | Latest known position in Google top 20 |
| Best | Best historical position over the period |
| Trend | Coloured badge ▲ (gain) / ▼ (loss) / = (stable) if delta > 3 |
| Evolution | Inline SVG curve of positions week by week |

### Visual alerts
- 🟢 **Gain ≥ 3 positions** — green badge
- 🔴 **Loss ≥ 3 positions** — red badge
- **Outside top 20** — shown in grey italic (the page does not appear in the top 20 results)

## Weekly automation

After the first `/rankpulse:track add`, the skill offers to create a launchd agent on macOS:

```xml
<!-- ~/Library/LaunchAgents/io.rankpulse.snapshot.plist -->
<!-- Runs snapshot.sh every Monday at 08:00 -->
```

To activate manually on macOS:
```bash
# Generate the plist (ask /rankpulse:track to create it)
launchctl load ~/Library/LaunchAgents/io.rankpulse.snapshot.plist
```

On Linux (cron):
```bash
# Add via crontab -e
0 8 * * 1 /path/to/rankpulse/scripts/snapshot.sh >> ~/.config/rankpulse/snapshot.log 2>&1
```

## Data storage

| File | Content | Typical size |
|---|---|---|
| `~/.config/rankpulse/tracking.db` | SQLite snapshots | ~2 MB (12 months × 20 keywords) |
| `~/.config/rankpulse/snapshot.log` | Automatic snapshot log | < 100 KB |
| `~/.config/rankpulse/dashboard.html` | Last generated report | ~30–100 KB |

All data remains 100% local. No external transmission.

## Reset tracking

```
/rankpulse:track remove captainmarketing.io
```
Removes the domain, its keywords, and all its snapshots from the database.
