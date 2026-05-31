#!/usr/bin/env python3
"""Suivi des coûts API DataForSEO via les hooks Claude Code.

Invoqué par hooks/hooks.json avec un payload JSON sur stdin :
  --pre      PreToolUse  : avertit si le budget mensuel est dépassé (n'interrompt pas).
  --post     PostToolUse : lit le coût RÉEL renvoyé par DataForSEO et l'enregistre.
  --summary  SessionEnd  : affiche le récap des coûts de la session/mois.

Conçu pour ne JAMAIS bloquer : sort toujours en code 0, échoue en silence.
Stockage : ~/.config/rankpulse/usage.log (JSONL), budget dans budget.json.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "rankpulse"
USAGE_LOG = CONFIG_DIR / "usage.log"
BUDGET_FILE = CONFIG_DIR / "budget.json"


def read_payload() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def extract_cost(tool_response) -> float:
    """Récupère le coût réel d'une réponse DataForSEO (champ `cost`)."""
    obj = tool_response
    if isinstance(obj, str):
        try:
            obj = json.loads(obj)
        except Exception:
            m = re.search(r'"cost"\s*:\s*([0-9.]+)', obj)
            return float(m.group(1)) if m else 0.0
    if isinstance(obj, dict):
        if isinstance(obj.get("cost"), (int, float)):
            return float(obj["cost"])
        tasks = obj.get("tasks")
        if isinstance(tasks, list):
            return sum(float(t.get("cost", 0) or 0) for t in tasks if isinstance(t, dict))
    return 0.0


def month_total() -> float:
    if not USAGE_LOG.exists():
        return 0.0
    prefix = datetime.now(timezone.utc).strftime("%Y-%m")
    total = 0.0
    for line in USAGE_LOG.read_text().splitlines():
        try:
            e = json.loads(line)
            if str(e.get("ts", "")).startswith(prefix):
                total += float(e.get("cost", 0) or 0)
        except Exception:
            continue
    return total


def monthly_budget() -> float:
    try:
        return float(json.loads(BUDGET_FILE.read_text()).get("monthly_usd", 0) or 0)
    except Exception:
        return 0.0


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--post"
    payload = read_payload()

    if mode == "--pre":
        budget = monthly_budget()
        if budget > 0 and month_total() >= budget:
            sys.stderr.write(
                f"[rankpulse] ⚠️ Budget mensuel atteint (${budget:.2f}). "
                f"Dépensé ce mois : ${month_total():.2f}.\n"
            )
        return 0

    if mode == "--post":
        cost = extract_cost(payload.get("tool_response"))
        if cost > 0:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "tool": payload.get("tool_name", "unknown"),
                "cost": round(cost, 6),
            }
            with USAGE_LOG.open("a") as f:
                f.write(json.dumps(entry) + "\n")
        return 0

    if mode == "--summary":
        total = month_total()
        if total > 0:
            budget = monthly_budget()
            line = f"[rankpulse] Coûts DataForSEO ce mois : ${total:.2f}"
            if budget > 0:
                line += f" / ${budget:.2f} budget ({total / budget * 100:.0f}%)"
            sys.stderr.write(line + "\n")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
