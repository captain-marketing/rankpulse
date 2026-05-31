---
description: Lance une analyse de veille concurrentielle via l'agent competitor-watcher. Compare les positions organiques, les backlinks et les gaps de contenu entre un domaine cible et un concurrent.
---

# /rankpulse:watch

Lance l'agent `competitor-watcher` pour une comparaison domaine vs concurrent.

## Arguments
`$ARGUMENTS` peut contenir :
- `<domain>` (requis) : domaine à surveiller, ex. `captainmarketing.io`
- `--vs <competitor>` (requis) : domaine concurrent, ex. `digitaleo.fr`
- `--keywords "kw1,kw2"` : mots-clés à surveiller spécifiquement (optionnel)
- `--locale <locale>` : marché (défaut `France / fr`)
- `--lang <code>` : langue du rapport (défaut `fr`)

## Procédure

1. Extraire `domain`, `competitor`, `keywords`, `locale` et `lang` depuis `$ARGUMENTS`.
2. Si `domain` ou `competitor` absents, demander les deux avant de continuer.
3. Vérifier que les credentials DataForSEO sont configurés. Si non, invoquer `/rankpulse:setup` d'abord.
4. Invoquer l'agent `competitor-watcher` avec le contexte :
   ```
   domain: <domain>
   competitor: <competitor>
   keywords: <liste ou vide>
   locale: <locale>
   lang: <lang>
   ```

L'agent produit le rapport différentiel complet avec alertes positions et opportunités de liens. Ne pas interrompre entre les étapes.
