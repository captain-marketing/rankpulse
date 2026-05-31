# ARCHITECTURE.md — Rankpulse

> Document de référence à fournir à Claude Code au démarrage de chaque session de build.
> Définit la structure cible, les contraintes et le périmètre du MVP.
> Claude Code ne doit jamais dévier de cette architecture sans validation explicite.
>
> **Version corrigée** (post-audit). Voir « Journal des corrections » en bas pour le diff vs v0.

---

## Identité du projet

- **Nom du plugin** : `rankpulse`
- **Namespace des skills** : `rankpulse:` (appliqué **automatiquement** par Claude Code à partir du nom du plugin — ne jamais le mettre dans les noms de dossiers)
- **Auteur** : Stéphane Truphème (Captain Marketing)
- **Repo GitHub cible** : `github.com/captain-marketing/rankpulse`
- **Licence** : MIT
- **Compatibilité** : Claude Code + Cowork (même format plugin natif, un seul repo) — *à valider, voir contraintes*

---

## Positionnement

Rankpulse n'est pas un outil SEO généraliste. C'est la **couche données de référence** pour l'écosystème Claude Code, alimentée par DataForSEO, Google Search Console et Google Analytics 4. Il expose des données SEO réelles via des skills intelligents qui interprètent, priorisent et transforment les résultats en livrables actionnables. D'autres plugins (claude-seo, content writers, etc.) peuvent s'appuyer sur Rankpulse comme source de données.

---

## Structure du repo (arborescence cible — corrigée)

```
rankpulse/
├── .claude-plugin/
│   └── plugin.json                   # Manifest minimal (le reste est auto-découvert)
├── .mcp.json                         # MCP server DataForSEO (via launcher sécurisé)
├── .gitignore                        # Exclut tout secret / donnée locale
├── commands/                         # Slash commands à interface CLI (flags/arguments)
│   ├── brief.md                      # /rankpulse:brief <keyword>  → agent brief-factory
│   ├── watch.md                      # /rankpulse:watch <domain> --vs <competitor> → competitor-watcher
│   └── audit-full.md                 # /rankpulse:audit-full <domain> → agent seo-auditor
├── skills/                           # Capacités model-invoked (dossiers SANS préfixe ':')
│   ├── setup/SKILL.md                # Credentials DataForSEO + budget + test connexion
│   ├── google-setup/SKILL.md         # Wizard configuration GSC + GA4 (Tier 1 & 2)
│   ├── serp/SKILL.md                 # Analyse SERP Google/Bing/YouTube
│   ├── keywords/SKILL.md             # Keyword research + clustering
│   ├── backlinks/SKILL.md            # Analyse profil de liens
│   ├── audit/SKILL.md                # Audit on-page + technique (3 couches : DataForSEO + GSC + GA4)
│   ├── content-gap/SKILL.md          # Gap analysis concurrentiel
│   ├── aeo/SKILL.md                  # AI visibility / LLM mentions
│   ├── track/SKILL.md                # Déclaration mots-clés à surveiller + snapshots
│   └── dashboard/SKILL.md            # Génération rapport HTML positions
├── agents/
│   ├── seo-auditor.md                # Agent audit complet d'un domaine
│   ├── brief-factory.md              # Agent génération de brief éditorial
│   └── competitor-watcher.md         # Agent veille concurrentielle
├── hooks/
│   └── hooks.json                    # PreToolUse (budget) + PostToolUse (coût réel) + SessionEnd (récap)
├── scripts/
│   ├── mcp-launch.sh                 # Pont credentials disque → env vars, lance le MCP DataForSEO épinglé
│   ├── cost-tracker.py               # Lit le coût RÉEL des réponses DataForSEO, log + budget (stdlib only)
│   ├── dashboard-generator.py        # Génération rapport HTML interactif positions (standalone)
│   ├── gsc_client.py                 # Client Google Search Console (Tier 1, Phase 4)
│   ├── ga4_client.py                 # Client Google Analytics 4 (Tier 2, Phase 4)
│   ├── snapshot.sh                   # Snapshot positions (appelé par cron/launchd, PAS par un hook)
│   └── requirements.txt              # Dépendances Python (Google libs pour Phase 4)
├── docs/
│   ├── SETUP.md                      # Guide configuration credentials DataForSEO
│   ├── GOOGLE-SETUP.md               # Guide configuration GSC + GA4
│   ├── COMMANDS.md                   # Référence complète des commandes
│   ├── COST-GUIDE.md                 # Guide coûts par endpoint DataForSEO
│   └── DASHBOARD.md                  # Guide utilisation dashboard positions
├── tests/
│   ├── test-connections.sh           # Vérification connexion API DataForSEO
│   └── test-google-apis.sh           # Vérification connexion GSC + GA4
├── README.md
├── CHANGELOG.md
└── LICENSE
```

**Règles de structure Claude Code :**
- Seul `plugin.json` vit dans `.claude-plugin/`. Tous les dossiers de composants (`commands/`, `agents/`, `skills/`, `hooks/`) sont à la **racine** du plugin.
- Les dossiers de skills n'ont **pas** de préfixe `rankpulse:` — le namespace est ajouté automatiquement. Un `:` dans un nom de dossier casse le chargement et est problématique sur macOS/Git.
- Le manifest est **minimal** : Claude Code auto-découvre commands/agents/skills/hooks/MCP. Ne pas lister de chemins manuellement.

---

## Manifest plugin.json (structure cible — corrigée)

```json
{
  "name": "rankpulse",
  "version": "1.0.0",
  "description": "Live SEO data layer for Claude Code. Powered by DataForSEO, Google Search Console, and GA4. SERP, keyword research, backlinks, technical audit, content gap, AI visibility, and position tracking dashboard — with real-time API cost tracking.",
  "author": {
    "name": "Stéphane Truphème",
    "email": "stephane.trupheme@captainmarketing.io",
    "url": "https://captainmarketing.io"
  },
  "license": "MIT",
  "homepage": "https://github.com/captain-marketing/rankpulse"
}
```

> Pas de tableau `skills`/`agents`/`hooks`/`mcpServers` : tout est auto-découvert depuis les dossiers conventionnels. Ajouter ces tableaux dupliquerait l'enregistrement et propagerait des erreurs de chemin.

---

## Configuration MCP (.mcp.json — corrigée)

Le plugin utilise le MCP server DataForSEO officiel `dataforseo-mcp-server`, **épinglé en version 2.9.4** (jamais `@latest` : reproductibilité). Les credentials sont stockés dans `~/.config/rankpulse/credentials.env` (`0600`), jamais dans le repo. Le launcher `scripts/mcp-launch.sh` fait le pont : il charge le fichier puis exporte les variables attendues **avant** de lancer le serveur.

```json
{
  "mcpServers": {
    "dataforseo": {
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/mcp-launch.sh",
      "env": {
        "DATAFORSEO_SIMPLE_FILTER": "true",
        "DATAFORSEO_FULL_RESPONSE": "false"
      }
    }
  }
}
```

**Points critiques :**
- Variables d'environnement officielles : `DATAFORSEO_USERNAME` et `DATAFORSEO_PASSWORD` (⚠️ **pas** `DATAFORSEO_LOGIN` — le serveur ne s'authentifierait pas).
- **Field filtering** géré nativement par le serveur via `DATAFORSEO_SIMPLE_FILTER=true` (+ `DATAFORSEO_FULL_RESPONSE=false`). C'est le seul mécanisme valide : un plugin ne peut pas post-traiter les réponses d'un MCP. → il n'existe **pas** de `scripts/field-filter.json`.

---

## Système de tiers Google APIs

Rankpulse fonctionne sans aucun credential Google (Tier 0). Les tiers suivants enrichissent progressivement l'audit et le dashboard. Chaque tier est indépendant et additif.

| Tier | Credentials requis | APIs débloquées | Ce que ça ajoute |
|---|---|---|---|
| **0** | Aucun | DataForSEO uniquement | SERP, keywords, backlinks, audit technique, gap analysis |
| **1** | Service Account (recommandé) ou OAuth Google | Google Search Console | Indexation réelle, impressions, CTR, URL Inspection, couverture |
| **2** | + GA4 Property ID | Google Analytics 4 | Trafic organique réel, landing pages, conversions, device/pays |

Configuration via `/rankpulse:google-setup`. Credentials stockés dans `~/.config/rankpulse/google-api.json` (`0600`), jamais dans le repo.

**Mécanisme d'accès (important) :** il n'existe pas de MCP Google. Les données GSC/GA4 sont récupérées par des scripts Python dédiés (`scripts/gsc_client.py`, `scripts/ga4_client.py`) que les skills `audit`/`track`/`dashboard` appellent en sous-processus. Dépendances déclarées dans `scripts/requirements.txt`. **Service Account** est la méthode primaire (pas de callback navigateur, compatible CI/Cowork) ; OAuth est optionnel et nécessite que l'utilisateur fournisse son propre client OAuth GCP.

### Ce que GSC + GA4 apportent à l'audit (Tier 1 + 2)

Sans Google APIs, `audit` analyse la page techniquement. Avec :
- **GSC (Tier 1)** : statut d'indexation réel, impressions 3 derniers mois, CTR moyen, position moyenne réelle, problèmes de couverture, résultats URL Inspection.
- **GA4 (Tier 2)** : sessions organiques, taux d'engagement, pages par session, conversions du canal organique, comparaison mobile/desktop.

Résultat : audit en 3 couches — technique (DataForSEO) + visibilité (GSC) + performance business (GA4) — avec score global pondéré et recommandations priorisées par impact réel.

---

## Périmètre MVP (v1.0.0)

### Skills (10 — model-invoked, `/rankpulse:<skill>`)

| Skill | Invocation | Sources de données | Priorité |
|---|---|---|---|
| setup | `/rankpulse:setup` | DataForSEO `/v3/appendix/user_data` | P0 |
| google-setup | `/rankpulse:google-setup` | Service Account / OAuth Google | P0 |
| serp | `/rankpulse:serp` | DataForSEO SERP → Google Organic Live Advanced | P0 |
| keywords | `/rankpulse:keywords` | DataForSEO Labs → Keyword Ideas, Related, Search Volume | P0 |
| backlinks | `/rankpulse:backlinks` | DataForSEO Backlinks → Summary, Referring Domains, Anchors | P1 |
| audit | `/rankpulse:audit` | DataForSEO On-Page + GSC (Tier 1) + GA4 (Tier 2) | P1 |
| content-gap | `/rankpulse:content-gap` | DataForSEO Labs → Domain Intersection, Ranked Keywords | P1 |
| aeo | `/rankpulse:aeo` | DataForSEO AI Optimization → LLM Mentions, ChatGPT Scraper | P2 |
| track | `/rankpulse:track` | DataForSEO SERP + GSC (Tier 1) | P2 |
| dashboard | `/rankpulse:dashboard` | `tracking.db` local + GSC (Tier 1) | P2 |

> Les paramètres (locale, device, depth, period, --vs, --tier, --lang…) sont passés en langage naturel à l'invocation du skill. Si une interface CLI stricte à flags est requise, créer une **command** miroir dans `commands/` (voir ci-dessous).

### Commands (3 — entrées orchestrées, interface à flags)

Les agents ne sont pas des slash commands : on les déclenche via une command qui invoque l'agent.

| Command | Invocation | Agent ciblé |
|---|---|---|
| brief | `/rankpulse:brief <keyword>` | brief-factory |
| watch | `/rankpulse:watch <domain> --vs <competitor>` | competitor-watcher |
| audit-full | `/rankpulse:audit-full <domain>` | seo-auditor |

### Agents (3 — sous-agents invoqués via Task)

| Agent | Déclenché par | Ce qu'il fait |
|---|---|---|
| seo-auditor | command `audit-full` | Orchestre SERP + backlinks + audit 3 couches + gap, produit rapport scoré 0-100 |
| brief-factory | command `brief` | SERP → keyword research → gap → brief éditorial complet |
| competitor-watcher | command `watch` | Snapshot comparatif, détecte changements de position et nouveaux backlinks |

### Hooks (événements Claude Code valides uniquement)

| Événement | Matcher | Action |
|---|---|---|
| `PreToolUse` | `mcp__dataforseo__.*` | `cost-tracker.py --pre` : avertit si budget mensuel atteint (n'interrompt pas) |
| `PostToolUse` | `mcp__dataforseo__.*` | `cost-tracker.py --post` : lit le coût **réel** renvoyé par DataForSEO, log dans `usage.log` |
| `SessionEnd` | — | `cost-tracker.py --summary` : récap des coûts du mois |

> ⚠️ Il n'existe **aucun** hook planifié/cron dans Claude Code. Le snapshot hebdomadaire des positions n'est **pas** un hook (voir section Dashboard).

---

## Dashboard de suivi des positions

Généré à la demande via `/rankpulse:dashboard`. Produit un fichier HTML interactif standalone (zéro serveur, zéro dépendance externe) ouvert dans le navigateur.

### Invocation
```
/rankpulse:track add captainmarketing.io --keywords "marketing IA,consultant marketing IA"
/rankpulse:track list
/rankpulse:dashboard
/rankpulse:dashboard --domain captainmarketing.io --period 90d
```

### Contenu
- Évolution des positions sur 4, 8, 12 semaines (courbes par mot-clé)
- Alertes visuelles : gains/pertes significatifs (> 3 positions)
- Top pages organiques (depuis GSC si Tier 1 actif)
- Comparaison optionnelle avec 1 ou 2 concurrents
- Résumé coûts API du mois en cours

### Snapshots automatiques (remplace le hook « Schedule » inexistant)
Le suivi hebdomadaire est assuré par `scripts/snapshot.sh`, déclenché par un planificateur **externe** :
- macOS : `launchd` (un `.plist` proposé par `/rankpulse:track` lors du premier `add`)
- Linux/CI : `cron`
- Repli : exécution manuelle / au lancement de `/rankpulse:dashboard` (snapshot à la volée si le dernier date de > 7 jours)

### Stockage
Snapshots dans `~/.config/rankpulse/tracking.db` (SQLite, ~2 Mo pour 12 mois × 20 mots-clés). Données 100 % locales, zéro transmission externe.

---

## Contraintes non négociables

1. **Credentials** : jamais hardcodés, jamais dans le repo. Uniquement env vars ou fichiers dans `~/.config/rankpulse/` en `0600`. DataForSEO → `credentials.env` ; Google → `google-api.json`. `.gitignore` couvre `*.env`, `credentials.*`, `google-api.json`, `budget.json`, `usage.log`, `tracking.db`.
2. **Coûts API** : le hook `PreToolUse` avertit avant un appel quand le budget mensuel est atteint ; le coût **réel** (champ `cost` de DataForSEO) est lu en `PostToolUse`, pas estimé. Budget configurable via `/rankpulse:setup`.
3. **Field filtering** : géré par le serveur MCP (`DATAFORSEO_SIMPLE_FILTER=true`), pas par un fichier de plugin.
4. **Namespace** : tous les skills/commands utilisent `rankpulse:` (appliqué automatiquement). Éviter les conflits avec d'autres plugins (notamment claude-seo).
5. **Compatibilité Cowork** : objectif « sans modification ». **À tester explicitement** : écritures `~/.config/`, SQLite, sous-processus Python, hooks, Service Account Google. Ne rien supposer.
6. **Langue des livrables** : français par défaut, configurable via `--lang`.
7. **Tier 0 complet** : 100 % fonctionnel sans aucun credential Google. Tiers 1 et 2 = enrichissements optionnels, jamais prérequis.
8. **Runtimes** : Python 3 requis (scripts) ; `bash`, `curl`, `jq` (optionnel) pour les tests. `/rankpulse:setup` vérifie leur présence.

---

## Ce que ce plugin n'est PAS

- Il ne génère pas de contenu rédigé (articles) — rôle d'autres plugins
- Il ne fait pas de crawl full-site (Firecrawl / Screaming Frog pour ça)
- Il n'est pas un SaaS ni une application à serveur persistant
- Il n'a pas de dashboard temps réel (snapshots hebdomadaires)

---

## Ordre de build recommandé pour Claude Code

```
Phase 1 — Fondations  [FAIT lors du scaffold]
  1. Structure de dossiers complète
  2. plugin.json + .mcp.json + .gitignore
  3. scripts/mcp-launch.sh (pont credentials → env)
  4. skills/setup (credentials + budget + test)
  5. scripts/cost-tracker.py + hooks/hooks.json
  6. tests/test-connections.sh

Phase 2 — Skills core DataForSEO (P0)
  7. skills/serp
  8. skills/keywords

Phase 3 — Skills enrichissement DataForSEO (P1)
  9. skills/backlinks
  10. skills/audit (Tier 0 uniquement)
  11. skills/content-gap

Phase 4 — Intégration Google APIs
  12. scripts/requirements.txt + gsc_client.py + ga4_client.py
  13. skills/google-setup (Service Account prioritaire, OAuth optionnel)
  14. tests/test-google-apis.sh
  15. skills/audit — couche GSC (Tier 1)
  16. skills/audit — couche GA4 (Tier 2)

Phase 5 — Agents + Commands
  17. agents/brief-factory + commands/brief.md
  18. agents/seo-auditor + commands/audit-full.md
  19. agents/competitor-watcher + commands/watch.md

Phase 6 — Dashboard + AEO
  20. skills/track + scripts/dashboard-generator.py + skills/dashboard
  21. scripts/snapshot.sh + plist/cron (snapshot hebdo externe)
  22. skills/aeo

Phase 7 — Finalisation marketplace
  23. docs/ complets
  24. README.md marketplace-ready + marketplace.json (entrée d'install)
  25. CHANGELOG.md + LICENSE
```

---

## Journal des corrections (vs v0)

| # | Problème v0 | Correction appliquée |
|---|---|---|
| 1 | `DATAFORSEO_LOGIN` (auth impossible) | → `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` |
| 2 | Dossiers `skills/rankpulse:xxx/` (`:` invalide) | → `skills/xxx/`, namespace auto |
| 3 | Hook `Schedule` inexistant | → `snapshot.sh` via launchd/cron externe |
| 4 | `field-filter.json` (mécanisme impossible) | → `DATAFORSEO_SIMPLE_FILTER` côté serveur MCP |
| 5 | Commands dashboard/brief/watch sans foyer | → `commands/` + skill `dashboard` |
| 6 | Agents traités comme slash commands | → commands qui invoquent les agents |
| 7 | `plugin.json` avec tableaux de chemins | → manifest minimal auto-découvert, `author` en objet |
| 8 | Tier 1/2 Google sans mécanisme | → `gsc_client.py` / `ga4_client.py` + `requirements.txt` |
| 9 | Creds fichier non reliés aux env vars MCP | → launcher `mcp-launch.sh` (pont) |
| 10 | `npx @latest` non reproductible | → épinglé `dataforseo-mcp-server@2.9.4` |
| 11 | Coût « avant exécution » en PostToolUse | → `PreToolUse` (budget) + coût réel en PostToolUse |
| 12 | OAuth Google sous-estimé | → Service Account primaire, OAuth optionnel |
| 13 | Runtimes Python/jq non déclarés | → `requirements.txt` + check au `setup` |

---

## Références utiles pour Claude Code

- Doc skills : https://code.claude.com/docs/en/skills
- Doc plugins : https://code.claude.com/docs/en/plugins-reference
- Exemples plugins officiels : https://github.com/anthropics/claude-code/tree/main/plugins
- claude-seo (référence architecture) : https://github.com/AgriciDaniel/claude-seo
- DataForSEO MCP (officiel, TypeScript) : https://github.com/dataforseo/mcp-server-typescript
- DataForSEO MCP npm : https://www.npmjs.com/package/dataforseo-mcp-server
- DataForSEO API docs : https://docs.dataforseo.com
- Google Search Console API : https://developers.google.com/webmaster-tools
- Google Analytics Data API (GA4) : https://developers.google.com/analytics/devguides/reporting/data/v1
