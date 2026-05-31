---
description: Lance un audit SEO complet d'un domaine via l'agent seo-auditor. Orchestre SERP, backlinks, audit technique (Tier 0/1/2) et gap analysis en séquence. Produit un rapport scoré 0-100 avec plan d'action priorisé.
---

# /rankpulse:audit-full

Lance l'agent `seo-auditor` sur le domaine fourni.

## Arguments
`$ARGUMENTS` peut contenir :
- `<domain>` (requis) : domaine à auditer, ex. `captainmarketing.io`
- `--vs <competitor>` : concurrent pour la comparaison (optionnel)
- `--tier 0|1|2` : forcer un tier (défaut : tier maximum disponible)
- `--lang <code>` : langue du rapport (défaut `fr`)

## Procédure

1. Extraire `domain`, `competitor`, `tier` et `lang` depuis `$ARGUMENTS`.
2. Si `domain` absent, demander à l'utilisateur avant de continuer.
3. Vérifier que les credentials DataForSEO sont configurés (`~/.config/rankpulse/credentials.env` existe). Si non, invoquer `/rankpulse:setup` d'abord.
4. Déterminer le tier disponible : lire `~/.config/rankpulse/google-api.json`. Si absent → tier 0. Si présent avec `ga4_property_id` → tier 2. Si présent sans → tier 1. Respecter `--tier` si fourni.
5. Invoquer l'agent `seo-auditor` avec le contexte :
   ```
   domain: <domain>
   competitor: <competitor ou vide>
   tier: <tier détecté>
   lang: <lang>
   ```

L'agent orchestre les étapes et produit le rapport complet. Ne pas interrompre le workflow de l'agent entre les étapes.
