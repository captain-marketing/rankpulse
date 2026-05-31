#!/usr/bin/env python3
"""Client Google Analytics 4 pour Rankpulse (Tier 2).

Appelé en sous-processus par le skill audit et dashboard.
Lit les credentials dans ~/.config/rankpulse/google-api.json.
Renvoie du JSON sur stdout ; les erreurs vont sur stderr.

Usage :
  python3 ga4_client.py --url https://example.com/page --days 90
  python3 ga4_client.py --days 30                     # toutes les landing pages organiques
"""
import argparse
import json
import site
import sys
from datetime import date, timedelta
from pathlib import Path

# Ensure site-packages are in sys.path when called as a subprocess from a skill
for _sp in site.getsitepackages():
    if _sp not in sys.path:
        sys.path.insert(0, _sp)

CONFIG_FILE = Path.home() / ".config" / "rankpulse" / "google-api.json"


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        print(json.dumps({
            "error": "google-api.json introuvable",
            "hint": "Lance /rankpulse:google-setup pour configurer l'accès GA4.",
        }))
        sys.exit(0)
    return json.loads(CONFIG_FILE.read_text())


def _missing_dep(package: str):
    print(json.dumps({
        "error": f"Dépendance manquante : {package}",
        "hint": "pip install -r scripts/requirements.txt",
    }))
    sys.exit(0)


def build_ga4_client(cfg: dict):
    auth_type = cfg.get("auth_type", "service_account")
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
    except ImportError:
        _missing_dep("google-analytics-data")

    if auth_type == "service_account":
        try:
            from google.oauth2 import service_account as sa_module
        except ImportError:
            _missing_dep("google-auth")
        sa_info = {k: v for k, v in cfg.items() if k not in ("auth_type", "site_url", "ga4_property_id")}
        scopes = ["https://www.googleapis.com/auth/analytics.readonly"]
        creds = sa_module.Credentials.from_service_account_info(sa_info, scopes=scopes)
        return BetaAnalyticsDataClient(credentials=creds)
    elif auth_type == "oauth":
        try:
            from google.oauth2.credentials import Credentials
        except ImportError:
            _missing_dep("google-auth")
        creds = Credentials(
            token=None,
            refresh_token=cfg["refresh_token"],
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"],
            token_uri="https://oauth2.googleapis.com/token",
        )
        return BetaAnalyticsDataClient(credentials=creds)
    else:
        print(json.dumps({"error": f"auth_type inconnu : {auth_type}"}))
        sys.exit(0)


def run_report(client, property_id: str, url: str | None, days: int) -> dict:
    try:
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Metric, Dimension,
            FilterExpression, Filter, StringFilter,
        )
    except ImportError:
        _missing_dep("google-analytics-data")

    end = date.today()
    start = end - timedelta(days=days)

    dimensions = [Dimension(name="landingPagePlusQueryString"), Dimension(name="deviceCategory")]
    metrics = [
        Metric(name="sessions"),
        Metric(name="engagedSessions"),
        Metric(name="engagementRate"),
        Metric(name="conversions"),
    ]

    # Filtre : canal organique
    channel_filter = FilterExpression(filter=Filter(
        field_name="sessionDefaultChannelGroup",
        string_filter=StringFilter(value="Organic Search", match_type="EXACT"),
    ))

    # Filtre optionnel sur l'URL
    if url:
        from google.analytics.data_v1beta.types import FilterExpressionList
        path = "/" + url.split("/", 3)[-1] if "://" in url else url
        url_filter = FilterExpression(filter=Filter(
            field_name="landingPagePlusQueryString",
            string_filter=StringFilter(value=path, match_type="BEGINS_WITH"),
        ))
        row_filter = FilterExpression(and_group=FilterExpressionList(expressions=[channel_filter, url_filter]))
    else:
        row_filter = channel_filter

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dimensions,
        metrics=metrics,
        date_ranges=[DateRange(start_date=start.isoformat(), end_date=end.isoformat())],
        dimension_filter=row_filter,
        limit=25,
    )

    try:
        response = client.run_report(request)
    except Exception as e:
        return {"error": str(e)}

    rows = []
    total_sessions = total_engaged = total_conversions = 0.0

    for row in response.rows:
        dims = [d.value for d in row.dimension_values]
        vals = [float(m.value) for m in row.metric_values]
        total_sessions += vals[0]
        total_engaged += vals[1]
        total_conversions += vals[3]
        rows.append({
            "landing_page": dims[0],
            "device": dims[1],
            "sessions": int(vals[0]),
            "engaged_sessions": int(vals[1]),
            "engagement_rate": round(vals[2], 4),
            "conversions": int(vals[3]),
        })

    return {
        "period_days": days,
        "total_organic_sessions": int(total_sessions),
        "total_engaged_sessions": int(total_engaged),
        "avg_engagement_rate": round(total_engaged / total_sessions, 4) if total_sessions else 0,
        "total_conversions": int(total_conversions),
        "top_landing_pages": rows[:10],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=None, help="URL filtre (optionnel)")
    parser.add_argument("--days", type=int, default=90, help="Fenêtre temporelle (défaut 90)")
    args = parser.parse_args()

    cfg = load_config()
    property_id = cfg.get("ga4_property_id")
    if not property_id:
        print(json.dumps({
            "error": "ga4_property_id manquant dans google-api.json",
            "hint": "Relance /rankpulse:google-setup pour configurer GA4.",
        }))
        sys.exit(0)

    client = build_ga4_client(cfg)
    data = run_report(client, str(property_id), args.url, args.days)

    output = {"property_id": property_id, "url_filter": args.url, **data}
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
