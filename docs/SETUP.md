# Guide de configuration — DataForSEO

Ce guide explique comment connecter Rankpulse à votre compte DataForSEO.

## Prérequis
- Un compte DataForSEO actif ([dataforseo.com](https://dataforseo.com))
- Python 3 installé
- Claude Code avec le plugin Rankpulse chargé

## Étape 1 — Récupérer vos identifiants

Dans votre espace client DataForSEO :
1. Connectez-vous sur [app.dataforseo.com](https://app.dataforseo.com)
2. Allez dans **API Access** → **API Credentials**
3. Notez votre **Login** (`DATAFORSEO_USERNAME`) et votre **Password** (`DATAFORSEO_PASSWORD`)

> ⚠️ Ce ne sont pas les identifiants de votre compte client — ce sont les clés API spécifiques, générées séparément.

## Étape 2 — Configurer via le skill

La façon la plus simple :
```
/rankpulse:setup
```
Le skill vous guide interactivement et écrit le fichier de credentials.

## Étape 3 — Configuration manuelle (alternative)

Si vous préférez configurer manuellement :

```bash
mkdir -p ~/.config/rankpulse
chmod 700 ~/.config/rankpulse

cat > ~/.config/rankpulse/credentials.env << 'EOF'
DATAFORSEO_USERNAME=votre_login_api
DATAFORSEO_PASSWORD=votre_password_api
EOF

chmod 600 ~/.config/rankpulse/credentials.env
```

## Étape 4 — Définir un budget mensuel (recommandé)

```bash
cat > ~/.config/rankpulse/budget.json << 'EOF'
{ "monthly_usd": 25 }
EOF
chmod 600 ~/.config/rankpulse/budget.json
```

Rankpulse vous avertira quand ce seuil sera atteint (sans bloquer les appels).

## Étape 5 — Tester la connexion

```bash
bash ~/.local/share/claude-plugins/rankpulse/tests/test-connections.sh
```

Résultat attendu :
```
✅ Connexion OK — Ok.
   Solde restant : $XX.XX
```

## Résolution des problèmes

| Erreur | Cause probable | Solution |
|---|---|---|
| HTTP 401 | Identifiants incorrects | Vérifier login/password dans l'espace client DataForSEO |
| `DATAFORSEO_USERNAME manquant` | credentials.env absent ou mal sourcé | Relancer `/rankpulse:setup` |
| Solde $0.00 | Compte vide | Recharger le solde sur [app.dataforseo.com](https://app.dataforseo.com) |

## Fichiers créés

| Fichier | Contenu | Permissions |
|---|---|---|
| `~/.config/rankpulse/credentials.env` | Login + password DataForSEO | `0600` |
| `~/.config/rankpulse/budget.json` | Budget mensuel en USD | `0600` |
| `~/.config/rankpulse/usage.log` | Historique des coûts (JSONL) | `0644` |
