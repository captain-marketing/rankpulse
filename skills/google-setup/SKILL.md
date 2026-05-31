---
name: google-setup
description: Configure l'accès à Google Search Console (Tier 1) et Google Analytics 4 (Tier 2) pour enrichir les audits et le dashboard Rankpulse. Wizard interactif qui guide étape par étape la création d'un Service Account GCP, l'ajout des permissions GSC/GA4, et le test de connexion. Invocable via /rankpulse:google-setup.
---

# Rankpulse — Configuration Google APIs

Configure les accès GSC et GA4. Rankpulse fonctionne sans eux (Tier 0) — ces tiers sont des enrichissements optionnels.

## Règles de sécurité
- Les credentials ne vont JAMAIS dans le repo.
- Fichier cible : `~/.config/rankpulse/google-api.json` permissions `0600`.
- Le Service Account est la méthode recommandée : pas de callback navigateur, compatible CI/Cowork.

## Structure du fichier google-api.json

```json
{
  "auth_type": "service_account",
  "site_url": "https://example.com/",
  "ga4_property_id": "123456789",
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...",
  "client_email": "rankpulse@project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

Pour OAuth (si Service Account impossible) : `"auth_type": "oauth"` avec `client_id`, `client_secret`, `refresh_token`.

## Procédure — Service Account (recommandée)

### Étape 1 — Projet GCP et Service Account

Guider l'utilisateur pour :

1. Aller sur https://console.cloud.google.com → créer ou sélectionner un projet.
2. Activer les APIs : **Google Search Console API** et **Google Analytics Data API**.
3. IAM et administration → Comptes de service → Créer un compte de service (`rankpulse-sa`).
4. Générer une clé JSON → télécharger le fichier.
5. Ajouter dans le JSON téléchargé les deux champs Rankpulse :
   - `"auth_type": "service_account"`
   - `"site_url": "<URL exacte de la propriété GSC, ex. https://example.com/>"`
   - `"ga4_property_id": "<ID numérique de la propriété GA4>"` (si Tier 2)

### Étape 2 — Permissions GSC (Tier 1)

1. Google Search Console → Paramètres → Utilisateurs et autorisations → Ajouter l'email `client_email` du Service Account avec le rôle **Propriétaire** ou **Éditeur restreint**.
2. Vérifier que la `site_url` correspond exactement à la propriété GSC (avec ou sans `/` final, http vs https — elles sont différentes dans GSC).

### Étape 3 — Permissions GA4 (Tier 2, optionnel)

1. Google Analytics → Administration → Propriété → Gestion des accès → Ajouter l'email du Service Account avec le rôle **Lecteur**.
2. Récupérer le **GA4 Property ID** (numérique, affiché sous le nom de la propriété).

### Étape 4 — Écrire le fichier

```bash
# Fusionner le JSON Service Account + les champs Rankpulse, puis :
cp <fichier-sa.json> ~/.config/rankpulse/google-api.json
chmod 600 ~/.config/rankpulse/google-api.json
```

### Étape 5 — Tester

Lancer `bash "${CLAUDE_PLUGIN_ROOT}/tests/test-google-apis.sh"`.

Ce script :
- Vérifie que `google-api.json` existe et est lisible.
- Appelle `scripts/gsc_client.py` sur la `site_url` (0 jour de données, juste l'auth).
- Appelle `scripts/ga4_client.py` si `ga4_property_id` présent.
- Affiche le résultat : Tier 1 ✅/❌, Tier 2 ✅/❌.

## Procédure alternative — OAuth

Si le Service Account n'est pas possible (accès admin GCP refusé) :
1. Créer un client OAuth dans GCP (type « Application de bureau »).
2. Récupérer `client_id` et `client_secret`.
3. Obtenir un `refresh_token` via le flow OAuth (documenter dans `docs/GOOGLE-SETUP.md`).
4. Écrire `google-api.json` avec `"auth_type": "oauth"`.

## Sortie attendue
Confirmation du Tier activé (1 et/ou 2), propriété GSC testée, property_id GA4 vérifié. Français par défaut.
