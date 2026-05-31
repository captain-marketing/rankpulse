# Setup Guide — DataForSEO

This guide explains how to connect Rankpulse to your DataForSEO account.

> 🇫🇷 [Version française](SETUP.fr.md)

## Requirements
- An active DataForSEO account ([dataforseo.com](https://dataforseo.com))
- Python 3 installed
- Claude Code with the Rankpulse plugin loaded

## Step 1 — Get your credentials

In your DataForSEO dashboard:
1. Log in at [app.dataforseo.com](https://app.dataforseo.com)
2. Go to **API Access** → **API Credentials**
3. Note your **Login** (`DATAFORSEO_USERNAME`) and **Password** (`DATAFORSEO_PASSWORD`)

> ⚠️ These are not your account login credentials — they are separate API keys generated specifically for API access.

## Step 2 — Configure via skill

The easiest way:
```
/rankpulse:setup
```
The skill guides you interactively and writes the credentials file.

## Step 3 — Manual configuration (alternative)

If you prefer to configure manually:

```bash
mkdir -p ~/.config/rankpulse
chmod 700 ~/.config/rankpulse

cat > ~/.config/rankpulse/credentials.env << 'EOF'
DATAFORSEO_USERNAME=your_api_login
DATAFORSEO_PASSWORD=your_api_password
EOF

chmod 600 ~/.config/rankpulse/credentials.env
```

## Step 4 — Set a monthly budget (recommended)

```bash
cat > ~/.config/rankpulse/budget.json << 'EOF'
{ "monthly_usd": 25 }
EOF
chmod 600 ~/.config/rankpulse/budget.json
```

Rankpulse will warn you when this threshold is reached (without blocking calls).

## Step 5 — Test the connection

```bash
bash ~/.local/share/claude-plugins/rankpulse/tests/test-connections.sh
```

Expected output:
```
✅ Connection OK — Ok.
   Remaining balance: $XX.XX
```

## Troubleshooting

| Error | Likely cause | Solution |
|---|---|---|
| HTTP 401 | Incorrect credentials | Check login/password in your DataForSEO dashboard |
| `DATAFORSEO_USERNAME missing` | credentials.env absent or not sourced | Re-run `/rankpulse:setup` |
| Balance $0.00 | Empty account | Top up balance at [app.dataforseo.com](https://app.dataforseo.com) |

## Files created

| File | Content | Permissions |
|---|---|---|
| `~/.config/rankpulse/credentials.env` | DataForSEO login + password | `0600` |
| `~/.config/rankpulse/budget.json` | Monthly budget in USD | `0600` |
| `~/.config/rankpulse/usage.log` | Cost history (JSONL) | `0644` |
