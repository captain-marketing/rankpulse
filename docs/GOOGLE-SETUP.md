# Setup Guide — Google APIs (Tier 1 & 2)

This guide covers configuring access to Google Search Console and Google Analytics 4. These tiers are **100% optional** — Rankpulse works without them.

> 🇫🇷 [Version française](GOOGLE-SETUP.fr.md)

## What you unlock

| Tier | What it adds |
|---|---|
| **Tier 1 — GSC** | Real indexation, impressions, CTR, average position, URL Inspection |
| **Tier 2 — GA4** | Organic sessions, engagement, conversions, mobile/desktop breakdown |

## Method A: Service Account (individual GCP accounts)

The Service Account does not require a browser callback and works in CI/Cowork.

> **⚠️ Google Workspace** — If your email address is managed by a Google Workspace organisation, the Service Account will likely be **blocked**: GSC and GA4 return "email address not found" because the SA is not in your domain's identity directory. Use **Method B (OAuth)** in that case.

### 1. Create a GCP project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (e.g. `rankpulse`) or select an existing one
3. **APIs & Services** → **Library** → Enable:
   - `Google Search Console API`
   - `Google Analytics Data API`

### 2. Create the Service Account

1. **IAM & Admin** → **Service Accounts** → **Create Service Account**
2. Name: `rankpulse-sa` · Description: `Rankpulse SEO plugin`
3. Skip the "Roles" steps (permissions are managed in GSC/GA4)
4. **Keys** → **Add Key** → **JSON** → Download

### 3. Add Rankpulse fields to the JSON file

Open the downloaded file and add these fields at the root:

```json
{
  "auth_type": "service_account",
  "site_url": "https://your-domain.com/",
  "ga4_property_id": "123456789",
  ...existing service account fields...
}
```

> `site_url` must match **exactly** the property in GSC (with or without trailing `/`, http vs https — these are different properties).

### 4. Grant GSC access (Tier 1)

1. [Google Search Console](https://search.google.com/search-console) → select your property
2. **Settings** → **Users and permissions** → **Add user**
3. Email: the `client_email` from the Service Account (e.g. `rankpulse-sa@project.iam.gserviceaccount.com`)
4. Permission: **Owner** or **Full**

### 5. Grant GA4 access (Tier 2)

1. [Google Analytics](https://analytics.google.com) → Admin → select your GA4 property
2. **Access Management** → **+** → Add the `client_email` from the Service Account
3. Role: **Viewer**
4. Get the **GA4 Property ID**: displayed under the property name (numeric format, e.g. `123456789`)

### 6. Install the file

```bash
cp ~/Downloads/rankpulse-sa-key.json ~/.config/rankpulse/google-api.json
chmod 600 ~/.config/rankpulse/google-api.json
```

### 7. Test

```
/rankpulse:google-setup
```
The skill runs `tests/test-google-apis.sh` automatically at the end.

Or directly:
```bash
bash ~/.local/share/claude-plugins/rankpulse/tests/test-google-apis.sh
```

---

## Method B: OAuth (recommended for Google Workspace)

Use this if your domain is managed by Google Workspace, or if you don't have GCP access to create a Service Account.

1. In GCP → **Credentials** → **Create Credentials** → **OAuth client ID**
2. Type: **Desktop app**
3. Download the client file (`client_id` + `client_secret`)
4. Get a `refresh_token` via the OAuth flow (see [Google guide](https://developers.google.com/identity/protocols/oauth2/native-app))
5. Write `~/.config/rankpulse/google-api.json`:

```json
{
  "auth_type": "oauth",
  "site_url": "https://your-domain.com/",
  "ga4_property_id": "123456789",
  "client_id": "...",
  "client_secret": "...",
  "refresh_token": "..."
}
```

---

## Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| `403 Forbidden` GSC | SA email not added to the property | Step 4 |
| "Email address not found" GSC/GA4 | Google Workspace — SA blocked by identity directory | Use **Method B (OAuth)** |
| `site_url` mismatch | Exact format difference (http/https, trailing slash) | Check in GSC → Settings |
| `ga4_property_id missing` | Field absent from JSON | Add the field to `google-api.json` |
| `Missing dependency` in ga4_client | Python called from env without site-packages | Run `python3 scripts/ga4_client.py --days 7` directly |
| `google-analytics-data` missing | Python dependencies not installed | `pip install -r scripts/requirements.txt` |
