#!/usr/bin/env python3
"""Générateur de dashboard HTML standalone pour Rankpulse.

Lit tracking.db + usage.log et produit un fichier HTML auto-contenu
(zéro dépendance externe — SVG + CSS + JS inline).

Usage :
  python3 dashboard-generator.py [--domain example.com] [--period 12w] [--output ~/dashboard.html]
"""
import argparse
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "rankpulse"
DB_PATH = CONFIG_DIR / "tracking.db"
USAGE_LOG = CONFIG_DIR / "usage.log"


# ── Data loading ──────────────────────────────────────────────────────────────

def parse_period(period: str) -> int:
    """Retourne le nombre de jours correspondant à la période."""
    if period.endswith("w"):
        return int(period[:-1]) * 7
    if period.endswith("d"):
        return int(period[:-1])
    return 84  # défaut 12w


def load_data(domain_filter: str | None, days: int) -> dict:
    if not DB_PATH.exists():
        return {}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    domain_clause = f"AND d.domain = '{domain_filter}'" if domain_filter else ""
    keywords = conn.execute(f"""
        SELECT k.id, k.keyword, d.domain
        FROM keywords k
        JOIN domains d ON k.domain_id = d.id
        WHERE 1=1 {domain_clause}
        ORDER BY d.domain, k.keyword
    """).fetchall()

    data = {}
    for kw in keywords:
        snapshots = conn.execute("""
            SELECT taken_at, position FROM snapshots
            WHERE keyword_id = ? AND taken_at >= ?
            ORDER BY taken_at ASC
        """, (kw["id"], cutoff)).fetchall()

        data[f"{kw['domain']}||{kw['keyword']}"] = {
            "domain": kw["domain"],
            "keyword": kw["keyword"],
            "snapshots": [{"date": s["taken_at"][:10], "pos": s["position"]} for s in snapshots],
        }

    conn.close()
    return data


def month_cost() -> float:
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


# ── SVG chart generation ──────────────────────────────────────────────────────

def sparkline_svg(snapshots: list, width=200, height=60) -> str:
    """Génère une courbe SVG inline à partir d'une liste de snapshots."""
    positions = [s["pos"] for s in snapshots if s["pos"] is not None]
    if len(positions) < 2:
        return "<span class='no-data'>données insuffisantes</span>"

    # Inverser : position 1 = haut du graphe
    max_pos = max(positions) + 1
    min_pos = max(1, min(positions) - 1)
    pad = 6

    def x(i):
        return pad + (i / (len(positions) - 1)) * (width - 2 * pad)

    def y(p):
        return pad + ((p - min_pos) / (max_pos - min_pos)) * (height - 2 * pad)

    points = " ".join(f"{x(i):.1f},{y(p):.1f}" for i, p in enumerate(positions))
    last = positions[-1]
    prev = positions[-2]
    color = "#22c55e" if last < prev else ("#ef4444" if last > prev else "#6b7280")

    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>'
        f'<circle cx="{x(len(positions)-1):.1f}" cy="{y(last):.1f}" r="3" fill="{color}"/>'
        f"</svg>"
    )


# ── HTML generation ───────────────────────────────────────────────────────────

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #f8fafc; color: #1e293b; padding: 24px; }
h1 { font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }
.meta { color: #64748b; font-size: 0.875rem; margin-bottom: 24px; }
.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 20px; margin-bottom: 16px; }
.domain-title { font-weight: 600; font-size: 1rem; color: #475569;
                margin-bottom: 12px; padding-bottom: 8px;
                border-bottom: 1px solid #f1f5f9; }
table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
th { text-align: left; padding: 8px 12px; background: #f8fafc;
     color: #64748b; font-weight: 600; border-bottom: 2px solid #e2e8f0; }
td { padding: 10px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 9999px;
         font-size: 0.75rem; font-weight: 600; }
.gain { background: #dcfce7; color: #16a34a; }
.loss { background: #fee2e2; color: #dc2626; }
.stable { background: #f1f5f9; color: #64748b; }
.no-rank { color: #94a3b8; font-style: italic; }
.cost-bar { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
            padding: 16px 20px; margin-bottom: 24px; display: flex;
            align-items: center; gap: 16px; }
.cost-val { font-size: 1.25rem; font-weight: 700; color: #0f172a; }
.cost-label { font-size: 0.8rem; color: #64748b; }
.no-data { color: #94a3b8; font-size: 0.75rem; }
"""


def trend_badge(snapshots: list) -> str:
    positions = [s["pos"] for s in snapshots if s["pos"] is not None]
    if len(positions) < 2:
        return '<span class="badge stable">—</span>'
    delta = positions[-2] - positions[-1]  # positif = gain (position diminue)
    if delta >= 3:
        return f'<span class="badge gain">▲ {delta}</span>'
    if delta <= -3:
        return f'<span class="badge loss">▼ {abs(delta)}</span>'
    return '<span class="badge stable">= stable</span>'


def render_html(data: dict, period: str, domain_filter: str | None) -> str:
    now = datetime.now().strftime("%d/%m/%Y à %H:%M")
    cost = month_cost()
    domain_label = domain_filter or "tous les domaines"

    # Grouper par domaine
    by_domain: dict[str, list] = {}
    for v in data.values():
        by_domain.setdefault(v["domain"], []).append(v)

    rows_html = ""
    for domain, keywords in sorted(by_domain.items()):
        rows = ""
        for kw in sorted(keywords, key=lambda k: k["keyword"]):
            snaps = kw["snapshots"]
            current_pos = next((s["pos"] for s in reversed(snaps) if s["pos"] is not None), None)
            best_pos = min((s["pos"] for s in snaps if s["pos"] is not None), default=None)
            pos_cell = f"<strong>{current_pos}</strong>" if current_pos else '<span class="no-rank">hors top 20</span>'
            best_cell = str(best_pos) if best_pos else "—"
            rows += (
                f"<tr>"
                f"<td>{kw['keyword']}</td>"
                f"<td>{pos_cell}</td>"
                f"<td>{best_cell}</td>"
                f"<td>{trend_badge(snaps)}</td>"
                f"<td>{sparkline_svg(snaps)}</td>"
                f"</tr>"
            )
        rows_html += f"""
        <div class="card">
          <div class="domain-title">{domain}</div>
          <table>
            <thead><tr>
              <th>Mot-clé</th><th>Position actuelle</th>
              <th>Meilleure</th><th>Tendance</th><th>Évolution</th>
            </tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>"""

    if not rows_html:
        rows_html = '<div class="card"><p style="color:#94a3b8">Aucune donnée disponible. Lance <code>/rankpulse:track add</code>.</p></div>'

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rankpulse — Dashboard ({domain_label})</title>
  <style>{CSS}</style>
</head>
<body>
  <h1>Rankpulse — Suivi des positions</h1>
  <p class="meta">Généré le {now} · Période : {period} · Domaine : {domain_label}</p>

  <div class="cost-bar">
    <div>
      <div class="cost-val">${cost:.2f}</div>
      <div class="cost-label">Coûts DataForSEO ce mois</div>
    </div>
  </div>

  {rows_html}

  <p style="margin-top:24px; font-size:0.75rem; color:#94a3b8">
    Généré par Rankpulse · Données 100 % locales
  </p>
</body>
</html>"""


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default=None)
    parser.add_argument("--period", default="12w")
    parser.add_argument("--output", default=str(CONFIG_DIR / "dashboard.html"))
    args = parser.parse_args()

    days = parse_period(args.period)
    data = load_data(args.domain, days)
    html = render_html(data, args.period, args.domain)

    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
