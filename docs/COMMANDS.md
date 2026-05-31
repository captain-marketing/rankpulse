# Rankpulse Commands Reference

All commands follow the format `/rankpulse:<skill-or-command> [arguments]`.
Parameters in `[]` are optional. Arguments are expressed in natural language.

> 🇫🇷 [Version française](COMMANDS.fr.md)

---

## Data skills (directly invocable)

### `/rankpulse:setup`
Configure DataForSEO credentials and set the monthly budget.

```
/rankpulse:setup
```
No arguments — the skill is interactive.

---

### `/rankpulse:google-setup`
Configure access to Google Search Console (Tier 1) and Google Analytics 4 (Tier 2).

```
/rankpulse:google-setup
```
No arguments — interactive wizard. See [GOOGLE-SETUP.md](GOOGLE-SETUP.md).

---

### `/rankpulse:serp`
Analyze the Google results page for a keyword.

```
/rankpulse:serp <keyword> [--locale <country/language>] [--device desktop|mobile] [--engine google|bing|youtube]
```

| Parameter | Default | Example |
|---|---|---|
| keyword | required | `marketing automation` |
| locale | United States / en | `United Kingdom / en` |
| device | desktop | `mobile` |
| engine | google | `youtube` |

---

### `/rankpulse:keywords`
Keyword research and thematic clustering.

```
/rankpulse:keywords <keyword> [--depth quick|standard|deep] [--locale <...>]
```

| Depth | What it does | Estimated cost |
|---|---|---|
| quick | Ideas + volumes | ~$0.01 |
| standard | + Related + Suggestions | ~$0.03 |
| deep | + Difficulty + Intent | ~$0.08 |

---

### `/rankpulse:backlinks`
Analyze a domain's link profile.

```
/rankpulse:backlinks <domain> [--compare <competitor>] [--depth quick|standard]
```

> ⚠️ Requires the DataForSEO Backlinks API ($100/month minimum). See [COST-GUIDE.md](COST-GUIDE.md).

---

### `/rankpulse:audit`
Technical and on-page audit of a URL (1 to 3 layers depending on available tier).

```
/rankpulse:audit <url> [--tier 0|1|2] [--lang fr|en]
```

Available tiers:
- **Tier 0**: DataForSEO (technical + on-page + Core Web Vitals)
- **Tier 1**: + Google Search Console (indexation, impressions, CTR)
- **Tier 2**: + Google Analytics 4 (organic sessions, conversions)

---

### `/rankpulse:content-gap`
Identify competitor keywords absent from your domain.

```
/rankpulse:content-gap <domain> --vs <competitor> [--focus gaps|overlap] [--locale <...>]
```

---

### `/rankpulse:aeo`
Analyze a brand's visibility in LLM responses.

```
/rankpulse:aeo <brand> [--engines chatgpt|gemini|perplexity|all] [--keywords "kw1,kw2"] [--compare <competitor>]
```

---

### `/rankpulse:track`
Manage position tracking (local SQLite database).

```
/rankpulse:track add <domain> --keywords "kw1,kw2" [--locale <...>]
/rankpulse:track list [--domain <domain>]
/rankpulse:track remove <domain> [--keyword <kw>]
/rankpulse:track snapshot [--domain <domain>]
```

---

### `/rankpulse:dashboard`
Generate the position tracking HTML report.

```
/rankpulse:dashboard [--domain <domain>] [--period 4w|8w|12w|90d] [--output <path>]
```

---

## Orchestrated commands (launch an agent)

### `/rankpulse:audit-full`
Full SEO audit of a domain (agent `seo-auditor`).

```
/rankpulse:audit-full <domain> [--vs <competitor>] [--tier 0|1|2] [--lang fr|en]
```
Estimated duration: 3–8 minutes depending on tier and number of pages audited.

---

### `/rankpulse:brief`
Generate an SEO editorial brief (agent `brief-factory`).

```
/rankpulse:brief <keyword> [--domain <domain>] [--locale <...>] [--lang fr|en]
```

---

### `/rankpulse:watch`
Comparative competitive intelligence (agent `competitor-watcher`).

```
/rankpulse:watch <domain> --vs <competitor> [--keywords "kw1,kw2"] [--locale <...>]
```

---

## Global options

| Option | Description | Default |
|---|---|---|
| `--lang` | Output language | `en` |
| `--locale` | Target market (country + language) | `United States / en` |
| `--tier` | Google APIs tier to use | auto-detected |
