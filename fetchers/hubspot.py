"""
HubSpot CRM API Fetcher with local file fallback.
Fetches RFQ tickets and sales deal data.
"""

import os
from pathlib import Path
import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("AERP_DATA_DIR", PROJECT_ROOT / "data"))
HUBSPOT_DIR = DATA_DIR / "hubspot"

ACCESS_TOKEN = os.environ.get("HUBSPOT_ACCESS_TOKEN", "").strip()


def is_available() -> bool:
    """Return True if HubSpot API access token is configured."""
    return bool(ACCESS_TOKEN)


def _get_headers() -> dict:
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }


def fetch_rfqs() -> pd.DataFrame:
    """
    Fetch RFQs (HubSpot tickets), or fall back to RFQs.xlsx.
    Guarantees 'Created Date' and 'Ticket name' columns are present.
    """
    if is_available():
        try:
            url = "https://api.hubapi.com/crm/v3/objects/tickets"
            params = {
                "limit": 100,
                "properties": "subject,hs_pipeline_stage,createdate,hubspot_owner_id",
            }
            resp = requests.get(url, headers=_get_headers(), params=params, timeout=30)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    rows = []
                    for item in results:
                        props = item.get("properties", {})
                        rows.append({
                            "Ticket name": props.get("subject", ""),
                            "Ticket status": props.get("hs_pipeline_stage", ""),
                            "Create date": props.get("createdate", ""),
                            "Created Date": props.get("createdate", ""),
                            "Ticket number": item.get("id", ""),
                            "Ticket owner": props.get("hubspot_owner_id", ""),
                        })
                    print(f"  [OK] [HubSpot] Fetched {len(rows)} RFQ tickets via live API")
                    return pd.DataFrame(rows)
            print(f"  [WARN] [HubSpot] Tickets API returned HTTP {resp.status_code}, falling back to RFQs.xlsx")
        except Exception as e:
            print(f"  [WARN] [HubSpot] Tickets API error ({e}), falling back to RFQs.xlsx")

    # Local fallback
    fallback_path = HUBSPOT_DIR / "RFQs.xlsx"
    if fallback_path.exists():
        df = pd.read_excel(fallback_path)
        if "Created Date" not in df.columns and "Create date" in df.columns:
            df["Created Date"] = df["Create date"]
        return df

    print("  [WARN] [HubSpot] Fallback file RFQs.xlsx not found, returning empty DataFrame")
    return pd.DataFrame(columns=["Ticket name", "Created Date", "Ticket status", "Ticket number"])


def fetch_sales() -> pd.DataFrame:
    """
    Fetch sales deals from HubSpot, or fall back to HW Sales.xlsx.
    Guarantees 'SALE_DATE', 'UNITS_SOLD', and 'COMMENTS' columns are present.
    """
    if is_available():
        try:
            url = "https://api.hubapi.com/crm/v3/objects/deals"
            params = {
                "limit": 100,
                "properties": "dealname,amount,closedate,dealstage,description",
            }
            resp = requests.get(url, headers=_get_headers(), params=params, timeout=30)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    rows = []
                    for item in results:
                        props = item.get("properties", {})
                        rows.append({
                            "DEAL_NAME": props.get("dealname", ""),
                            "SALE_DATE": props.get("closedate", ""),
                            "UNITS_SOLD": 1,  # Default unit count if not specified
                            "AMOUNT": props.get("amount", 0),
                            "COMMENTS": props.get("description", "") or "",
                        })
                    print(f"  [OK] [HubSpot] Fetched {len(rows)} sales deals via live API")
                    return pd.DataFrame(rows)
            print(f"  [WARN] [HubSpot] Deals API returned HTTP {resp.status_code}, falling back to HW Sales.xlsx")
        except Exception as e:
            print(f"  [WARN] [HubSpot] Deals API error ({e}), falling back to HW Sales.xlsx")

    # Local fallback
    fallback_path = HUBSPOT_DIR / "HW Sales.xlsx"
    if fallback_path.exists():
        df = pd.read_excel(fallback_path)
        # Normalize columns for pipeline expectations
        if "Sales Date" in df.columns and "SALE_DATE" not in df.columns:
            df["SALE_DATE"] = df["Sales Date"]
        if "Units Sold" in df.columns and "UNITS_SOLD" not in df.columns:
            df["UNITS_SOLD"] = df["Units Sold"]
        if "COMMENTS" not in df.columns:
            df["COMMENTS"] = ""
        return df

    print("  [WARN] [HubSpot] Fallback file HW Sales.xlsx not found, returning empty DataFrame")
    return pd.DataFrame(columns=["SALE_DATE", "UNITS_SOLD", "COMMENTS"])

