# DataForSEO API Cost Guide

Rankpulse tracks costs in real time and alerts you when your monthly budget is reached. This guide details the cost per endpoint and best practices for keeping expenses under control.

> 🇫🇷 [Version française](COST-GUIDE.fr.md)

## Cost per command

| Command | Endpoints used | Estimated cost per call |
|---|---|---|
| `/rankpulse:serp` | SERP Organic Live Advanced | $0.002 – $0.006 |
| `/rankpulse:keywords` (quick) | Labs Keyword Ideas | ~$0.010 |
| `/rankpulse:keywords` (standard) | + Related + Suggestions | ~$0.025 |
| `/rankpulse:keywords` (deep) | + Bulk Difficulty + Intent | ~$0.060 |
| `/rankpulse:backlinks` (quick) | Backlinks Summary | ~$0.010 |
| `/rankpulse:backlinks` (standard) | + Referring Domains + Anchors | ~$0.030 |
| `/rankpulse:audit` (Tier 0) | On-Page Instant + Lighthouse | ~$0.015 |
| `/rankpulse:content-gap` | Domain Intersection + Ranked Keywords | ~$0.040 |
| `/rankpulse:aeo` (per engine) | LLM Mentions + ChatGPT Scraper | $0.050 – $0.200 |
| `/rankpulse:track snapshot` (per keyword) | SERP Organic Live Advanced | $0.002 – $0.006 |
| `/rankpulse:audit-full` (full agent) | Combination of 4–5 calls | $0.10 – $0.25 |
| `/rankpulse:brief` (agent) | SERP + Keywords + Gap | ~$0.08 |
| `/rankpulse:watch` (agent) | SERP × N + Backlinks + Gap | $0.05 – $0.15 |

> DataForSEO costs are billed in USD, deducted from your account balance. They vary based on the volume of results requested.

## ⚠️ Backlinks API — minimum commitment required

The DataForSEO Backlinks API requires a **minimum commitment of $100/month**, subscribed separately. Without this subscription, any backlinks request returns error `40204`.

- The `/rankpulse:backlinks` and `/rankpulse:watch` skills operate in degraded mode without backlinks (SERP positions and gap analysis remain available, link profile is unavailable).
- To activate: contact DataForSEO support and request Backlinks API access.
- Free alternative to estimate authority: Ahrefs Free (Ahrefs.com → Free Backlink Checker).

## Most expensive endpoints

**Watch these particularly:**

1. **AEO / LLM Mentions** — $0.05 to $0.20 per query/engine. Use `--engines chatgpt` in targeted mode rather than `--engines all`.
2. **Keywords deep** — The `deep` mode chains 4 endpoints. On a list of 50 keywords, expect $2–4.
3. **Backlinks on large domains** — Referring domains and anchors on domains with millions of backlinks can return large volumes.

## Real-time cost tracking

Rankpulse records each actual cost (the `cost` field in DataForSEO responses) to `~/.config/rankpulse/usage.log`:

```json
{"ts": "2026-05-30T10:00:00+00:00", "tool": "mcp__dataforseo__serp_organic_live_advanced", "cost": 0.003}
```

At the end of each session, the month's total cost is displayed automatically.

## Set a monthly budget

```bash
echo '{ "monthly_usd": 50 }' > ~/.config/rankpulse/budget.json
chmod 600 ~/.config/rankpulse/budget.json
```

Rankpulse displays a warning when the budget is reached (without blocking calls).

## Best practices

**Reduce costs:**
- Use `depth=quick` for initial exploration, `standard` or `deep` only for validated topics.
- For tracking, limit to 10–15 priority keywords per domain.
- For AEO, test one engine at a time before running `--engines all`.
- Avoid repeated manual snapshots — let the weekly automation do the work.

**Estimate before a large call:**
Skills display the estimated cost before any request > $0.01. Confirmation is requested above $0.50.

## Recommended monthly budget

| Profile | Typical usage | Suggested budget |
|---|---|---|
| Discovery / testing | A few analyses per week | $10–20/month |
| Solo consultant | 5–10 domains tracked, regular audits | $30–60/month |
| Agency (10+ clients) | Full audits + intensive tracking + AEO | $100–200/month |
