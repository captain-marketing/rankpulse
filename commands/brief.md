---
description: Génère un brief éditorial SEO complet pour un mot-clé via l'agent brief-factory. Analyse la SERP, les mots-clés associés et les gaps concurrentiels pour produire une structure d'article prête à utiliser.
---

# /rankpulse:brief

Lance l'agent `brief-factory` sur le mot-clé fourni.

## Arguments
`$ARGUMENTS` peut contenir :
- `<keyword>` (requis) : mot-clé principal cible, ex. `marketing IA`
- `--domain <domain>` : domaine pour lequel le contenu est produit (améliore le gap analysis)
- `--locale <locale>` : marché cible (défaut `France / fr`)
- `--lang <code>` : langue du brief (défaut `fr`)

## Procédure

1. Extraire `keyword`, `domain`, `locale` et `lang` depuis `$ARGUMENTS`. Le keyword est tout ce qui précède le premier `--`.
2. Si `keyword` absent, demander à l'utilisateur avant de continuer.
3. Vérifier que les credentials DataForSEO sont configurés. Si non, invoquer `/rankpulse:setup` d'abord.
4. Invoquer l'agent `brief-factory` avec le contexte :
   ```
   keyword: <keyword>
   domain: <domain ou vide>
   locale: <locale>
   lang: <lang>
   ```

L'agent orchestre les 4 étapes (SERP → keywords → gap → brief) et livre le brief complet. Ne pas interrompre entre les étapes.
