# Guide de configuration — Google APIs (Tier 1 & 2)

Ce guide détaille la configuration des accès Google Search Console et Google Analytics 4. Ces tiers sont **100 % optionnels** — Rankpulse fonctionne sans eux.

## Ce que vous débloquez

| Tier | Ce que ça ajoute |
|---|---|
| **Tier 1 — GSC** | Indexation réelle, impressions, CTR, position moyenne, URL Inspection |
| **Tier 2 — GA4** | Sessions organiques, engagement, conversions, mobile/desktop |

## Méthode A : Service Account (comptes GCP individuels)

Le Service Account ne nécessite pas de callback navigateur et fonctionne en CI/Cowork.

> **⚠️ Google Workspace** — Si votre adresse email est gérée par une organisation Google Workspace, le Service Account sera probablement **bloqué** : GSC et GA4 renvoient "adresse e-mail introuvable" car le SA n'est pas dans l'annuaire identitaire de votre domaine. Utilisez la **Méthode B (OAuth)** dans ce cas.

### 1. Créer un projet GCP

1. Aller sur [console.cloud.google.com](https://console.cloud.google.com)
2. Créer un nouveau projet (ex. `rankpulse`) ou en sélectionner un existant
3. **APIs et services** → **Bibliothèque** → Activer :
   - `Google Search Console API`
   - `Google Analytics Data API`

### 2. Créer le Service Account

1. **IAM et administration** → **Comptes de service** → **Créer un compte de service**
2. Nom : `rankpulse-sa` · Description : `Rankpulse SEO plugin`
3. Ignorer les étapes "Rôles" (les permissions se gèrent côté GSC/GA4)
4. **Clés** → **Ajouter une clé** → **JSON** → Télécharger

### 3. Ajouter les champs Rankpulse au fichier JSON

Ouvrir le fichier téléchargé et ajouter ces champs à la racine :

```json
{
  "auth_type": "service_account",
  "site_url": "https://votre-domaine.com/",
  "ga4_property_id": "123456789",
  ...champs Service Account existants...
}
```

> `site_url` doit correspondre **exactement** à la propriété dans GSC (avec ou sans `/`, http vs https — ce sont des propriétés différentes).

### 4. Donner accès à GSC (Tier 1)

1. [Google Search Console](https://search.google.com/search-console) → sélectionner la propriété
2. **Paramètres** → **Utilisateurs et autorisations** → **Ajouter un utilisateur**
3. Email : l'adresse `client_email` du Service Account (ex. `rankpulse-sa@projet.iam.gserviceaccount.com`)
4. Permission : **Propriétaire** ou **Éditeur complet**

### 5. Donner accès à GA4 (Tier 2)

1. [Google Analytics](https://analytics.google.com) → Administration → sélectionner la propriété GA4
2. **Gestion des accès** → **+** → Ajouter le `client_email` du Service Account
3. Rôle : **Lecteur**
4. Récupérer le **GA4 Property ID** : affiché sous le nom de la propriété (format numérique, ex. `123456789`)

### 6. Installer le fichier

```bash
cp ~/Téléchargements/rankpulse-sa-key.json ~/.config/rankpulse/google-api.json
chmod 600 ~/.config/rankpulse/google-api.json
```

### 7. Tester

```
/rankpulse:google-setup
```
Le skill lance automatiquement `tests/test-google-apis.sh` à la fin.

Ou directement :
```bash
bash ~/.local/share/claude-plugins/rankpulse/tests/test-google-apis.sh
```

---

## Méthode B : OAuth (recommandée pour Google Workspace)

À utiliser si votre domaine est géré par Google Workspace, ou si vous n'avez pas accès à GCP pour créer un Service Account.

1. Dans GCP → **Identifiants** → **Créer des identifiants** → **ID client OAuth**
2. Type : **Application de bureau**
3. Télécharger le fichier client (`client_id` + `client_secret`)
4. Obtenir un `refresh_token` via le flux OAuth (voir [guide Google](https://developers.google.com/identity/protocols/oauth2/native-app))
5. Écrire `~/.config/rankpulse/google-api.json` :

```json
{
  "auth_type": "oauth",
  "site_url": "https://votre-domaine.com/",
  "ga4_property_id": "123456789",
  "client_id": "...",
  "client_secret": "...",
  "refresh_token": "..."
}
```

---

## Résolution des problèmes

| Erreur | Cause | Solution |
|---|---|---|
| `403 Forbidden` GSC | Email SA pas ajouté à la propriété | Étape 4 |
| "adresse e-mail introuvable" GSC/GA4 | Compte Google Workspace — SA bloqué par l'annuaire | Utiliser **Méthode B (OAuth)** |
| `site_url` ne correspond pas | Format exact différent (http/https, /final) | Vérifier dans GSC → Paramètres |
| `ga4_property_id manquant` | Champ absent du JSON | Ajouter le champ dans `google-api.json` |
| `Dépendance manquante` dans ga4_client | Python appelé depuis un env sans site-packages | `python3 scripts/ga4_client.py --days 7` directement |
| `google-analytics-data` manquant | Dépendances Python non installées | `pip install -r scripts/requirements.txt` |
