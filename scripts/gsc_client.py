#!/usr/bin/env python3
"""Client Google Search Console pour Rankpulse (Tier 1).

Appelé en sous-processus par le skill audit et track.
Lit les credentials dans ~/.config/rankpulse/google-api.json.
Renvoie du JSON sur stdout ; les erreurs vont sur stderr.

Usage :
  python3 gsc_client.py --url https://example.com/page --days 90
  python3 gsc_client.py --site https://example.com/ --days 30 --inspect
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

CONFIG_FILE = Path.home() / ".config" / "rankpulse" / "google-api.json"

SCOPES_SC = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/webmasters",
]
SCOPES_INSPECT = ["https://www.googleapis.com/auth/webmasters"]


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        print(
            json.dumps({
                "error": "google-api.json introuvable",
                "hint": "Lance /rankpulse:google-setup pour configurer l'accès GSC.",
            })
        )
        sys.exit(0)
    return json.loads(CONFIG_FILE.read_text())


def build_credentials(cfg: dict):
    auth_type = cfg.get("auth_type", "service_account")
    if auth_type == "service_account":
        try:
            from google.oauth2 import service_account as sa_module
        except ImportError:
            _missing_dep("google-auth")
        sa_info = {k: v for k, v in cfg.items() if k not in ("auth_type", "site_url", "ga4_property_id")}
        return sa_module.Credentials.from_service_account_info(sa_info, scopes=SCOPES_SC)
    elif auth_type == "oauth":
        try:
            from google.oauth2.credentials import Credentials
        except ImportError:
            _missing_dep("google-auth")
        return Credentials(
            token=None,
            refresh_token=cfg["refresh_token"],
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"],
            token_uri="https://oauth2.googleapis.com/token",
        )
    else:
        print(json.dumps({"error": f"auth_type inconnu : {auth_type}"}))
        sys.exit(0)


def _missing_dep(package: str):
    print(json.dumps({
        "error": f"Dépendance manquante : {package}",
        "hint": "pip install -r scripts/requirements.txt",
    }))
    sys.exit(0)


def query_search_analytics(service, site_url: str, url: str, days: int) -> dict:
    end = date.today()
    start = end - timedelta(days=days)
    body = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": ["query", "page"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "equals",
                "expression": url,
            }]
        }],
        "rowLimit": 25,
    }
    try:
        resp = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    except Exception as e:
        return {"error": str(e)}

    rows = resp.get("rows", [])
    return {
        "total_clicks": sum(r.get("clicks", 0) for r in rows),
        "total_impressions": sum(r.get("impressions", 0) for r in rows),
        "avg_ctr": round(sum(r.get("ctr", 0) for r in rows) / len(rows), 4) if rows else 0,
        "avg_position": round(sum(r.get("position", 0) for r in rows) / len(rows), 1) if rows else 0,
        "top_queries": [
            {
                "query": r["keys"][0],
                "clicks": r.get("clicks", 0),
                "impressions": r.get("impressions", 0),
                "ctr": round(r.get("ctr", 0), 4),
                "position": round(r.get("position", 0), 1),
            }
            for r in rows[:10]
        ],
        "period_days": days,
    }


def query_index_status(service, site_url: str, url: str) -> dict:
    try:
        resp = (
            service.urlInspection()
            .index()
            .inspect(body={"inspectionUrl": url, "siteUrl": site_url})
            .execute()
        )
        result = resp.get("inspectionResult", {})
        index_result = result.get("indexStatusResult", {})
        return {
            "verdict": index_result.get("verdict", "unknown"),
            "coverage_state": index_result.get("coverageState", "unknown"),
            "robots_txt_state": index_result.get("robotsTxtState", "unknown"),
            "indexing_state": index_result.get("indexingState", "unknown"),
            "last_crawl_time": index_result.get("lastCrawlTime"),
            "canonical": index_result.get("googleCanonical"),
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="URL de la page à analyser")
    parser.add_argument("--days", type=int, default=90, help="Fenêtre temporelle (défaut 90)")
    parser.add_argument("--inspect", action="store_true", help="Inclure URL Inspection")
    args = parser.parse_args()

    cfg = load_config()
    site_url = cfg.get("site_url")
    if not site_url:
        print(json.dumps({"error": "site_url manquant dans google-api.json"}))
        sys.exit(0)

    try:
        from googleapiclient.discovery import build
    except ImportError:
        _missing_dep("google-api-python-client")

    creds = build_credentials(cfg)
    service = build("searchconsole", "v1", credentials=creds)

    output = {
        "url": args.url,
        "site_url": site_url,
        "search_analytics": query_search_analytics(service, site_url, args.url, args.days),
    }
    if args.inspect:
        output["index_status"] = query_index_status(service, site_url, args.url)

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
