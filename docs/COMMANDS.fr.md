# Référence des commandes Rankpulse

Toutes les commandes suivent le format `/rankpulse:<skill-ou-commande> [arguments]`.
Les paramètres entre `[]` sont optionnels. Les arguments s'expriment en langage naturel.

---

## Skills de données (invocables directement)

### `/rankpulse:setup`
Configure les credentials DataForSEO et définit le budget mensuel.

```
/rankpulse:setup
```
Aucun argument — le skill est interactif.

---

### `/rankpulse:google-setup`
Configure l'accès à Google Search Console (Tier 1) et Google Analytics 4 (Tier 2).

```
/rankpulse:google-setup
```
Aucun argument — wizard interactif. Voir [GOOGLE-SETUP.md](GOOGLE-SETUP.md).

---

### `/rankpulse:serp`
Analyse la page de résultats Google pour un mot-clé.

```
/rankpulse:serp <keyword> [--locale <pays/langue>] [--device desktop|mobile] [--engine google|bing|youtube]
```

| Paramètre | Défaut | Exemple |
|---|---|---|
| keyword | requis | `marketing automation` |
| locale | France / fr | `Belgique / fr` |
| device | desktop | `mobile` |
| engine | google | `youtube` |

---

### `/rankpulse:keywords`
Recherche de mots-clés et clustering thématique.

```
/rankpulse:keywords <keyword> [--depth quick|standard|deep] [--locale <...>]
```

| Depth | Ce que ça fait | Coût estimé |
|---|---|---|
| quick | Idées + volumes | ~$0.01 |
| standard | + Related + Suggestions | ~$0.03 |
| deep | + Difficulté + Intention | ~$0.08 |

---

### `/rankpulse:backlinks`
Analyse le profil de liens d'un domaine.

```
/rankpulse:backlinks <domain> [--compare <competitor>] [--depth quick|standard]
```

---

### `/rankpulse:audit`
Audit technique et on-page d'une URL (1 à 3 couches selon le tier disponible).

```
/rankpulse:audit <url> [--tier 0|1|2] [--lang fr|en]
```

Tiers disponibles :
- **Tier 0** : DataForSEO (technique + on-page + Core Web Vitals)
- **Tier 1** : + Google Search Console (indexation, impressions, CTR)
- **Tier 2** : + Google Analytics 4 (sessions organiques, conversions)

---

### `/rankpulse:content-gap`
Identifie les mots-clés du concurrent absents de votre domaine.

```
/rankpulse:content-gap <domain> --vs <competitor> [--focus gaps|overlap] [--locale <...>]
```

---

### `/rankpulse:aeo`
Analyse la visibilité d'une marque dans les réponses des LLMs.

```
/rankpulse:aeo <brand> [--engines chatgpt|gemini|perplexity|all] [--keywords "kw1,kw2"] [--compare <competitor>]
```

---

### `/rankpulse:track`
Gère le suivi de positions (base SQLite locale).

```
/rankpulse:track add <domain> --keywords "kw1,kw2" [--locale <...>]
/rankpulse:track list [--domain <domain>]
/rankpulse:track remove <domain> [--keyword <kw>]
/rankpulse:track snapshot [--domain <domain>]
```

---

### `/rankpulse:dashboard`
Génère le rapport HTML de suivi des positions.

```
/rankpulse:dashboard [--domain <domain>] [--period 4w|8w|12w|90d] [--output <path>]
```

---

## Commandes orchestrées (lancent un agent)

### `/rankpulse:audit-full`
Audit SEO complet d'un domaine (agent `seo-auditor`).

```
/rankpulse:audit-full <domain> [--vs <competitor>] [--tier 0|1|2] [--lang fr|en]
```
Durée estimée : 3–8 minutes selon le tier et le nombre de pages auditées.

---

### `/rankpulse:brief`
Génère un brief éditorial SEO (agent `brief-factory`).

```
/rankpulse:brief <keyword> [--domain <domain>] [--locale <...>] [--lang fr|en]
```

---

### `/rankpulse:watch`
Veille concurrentielle comparée (agent `competitor-watcher`).

```
/rankpulse:watch <domain> --vs <competitor> [--keywords "kw1,kw2"] [--locale <...>]
```

---

## Options globales

| Option | Description | Défaut |
|---|---|---|
| `--lang` | Langue du livrable | `fr` |
| `--locale` | Marché cible (pays + langue) | `France / fr` |
| `--tier` | Tier Google APIs à utiliser | auto-détecté |
