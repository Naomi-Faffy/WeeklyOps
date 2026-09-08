"""
Service Desk / ManageEngine API Fetcher with local file fallback.
Supports Zoho OAuth 2.0 (Refresh Token -> Access Token) and ManageEngine SDP API v3.
"""

import json
import os
import time
from pathlib import Path
import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("AERP_DATA_DIR", PROJECT_ROOT / "data"))
SD_DIR = DATA_DIR / "sevicedesk"

# ─── CONFIGURATION & OAUTH CREDENTIALS ────────────────────────────────────────
SDP_INSTANCE_URL = os.environ.get("SDP_INSTANCE_URL", "").strip()
SDP_CLIENT_ID = os.environ.get("SDP_CLIENT_ID", "").strip()
SDP_CLIENT_SECRET = os.environ.get("SDP_CLIENT_SECRET", "").strip()
SDP_REFRESH_TOKEN = os.environ.get("SDP_REFRESH_TOKEN", "").strip()
SDP_ZOHO_REGION = os.environ.get("SDP_ZOHO_REGION", "com").strip().lstrip(".")

# Legacy / direct token fallback
SERVICEDESK_BASE_URL = os.environ.get("SERVICEDESK_BASE_URL", "").strip()
SERVICEDESK_AUTH_TOKEN = os.environ.get("SERVICEDESK_AUTH_TOKEN", "").strip()

# In-memory access token cache
_token_cache = {
    "access_token": None,
    "expires_at": 0
}


def _clean_base_url() -> str:
    """Normalize instance URL, stripping /app/itdesk suffix if present."""
    url = SDP_INSTANCE_URL or SERVICEDESK_BASE_URL
    url = url.rstrip("/")
    if url.endswith("/app/itdesk"):
        url = url[:-len("/app/itdesk")]
    return url


def is_available() -> bool:
    """Return True if SDP OAuth credentials or static auth token are configured."""
    has_oauth = bool(_clean_base_url() and SDP_CLIENT_ID and SDP_CLIENT_SECRET and SDP_REFRESH_TOKEN)
    has_legacy = bool(_clean_base_url() and SERVICEDESK_AUTH_TOKEN)
    return has_oauth or has_legacy


def _get_access_token() -> str:
    """Retrieve or refresh Zoho OAuth access token."""
    now = time.time()
    if _token_cache["access_token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["access_token"]

    if SDP_CLIENT_ID and SDP_CLIENT_SECRET and SDP_REFRESH_TOKEN:
        token_url = f"https://accounts.zoho.{SDP_ZOHO_REGION}/oauth/v2/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": SDP_CLIENT_ID,
            "client_secret": SDP_CLIENT_SECRET,
            "refresh_token": SDP_REFRESH_TOKEN,
        }
        resp = requests.post(token_url, data=data, timeout=20)
        if resp.status_code == 200:
            payload = resp.json()
            access_token = payload.get("access_token")
            expires_in = payload.get("expires_in", 3600)
            if access_token:
                _token_cache["access_token"] = access_token
                _token_cache["expires_at"] = now + expires_in
                return access_token
            raise RuntimeError(f"Zoho token response missing access_token: {payload}")
        else:
            raise RuntimeError(f"Failed to refresh Zoho access token (HTTP {resp.status_code}): {resp.text}")

    if SERVICEDESK_AUTH_TOKEN:
        return SERVICEDESK_AUTH_TOKEN

    raise RuntimeError("No ServiceDesk credentials provided.")


def _get_headers() -> dict:
    token = _get_access_token()
    return {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Accept": "application/vnd.manageengine.sdp.v3+json",
    }


def _read_excel_fallback(file_name: str) -> pd.DataFrame:
    file_path = SD_DIR / file_name
    if not file_path.exists():
        print(f"  [ServiceDesk] Fallback file not found: {file_path}")
        return pd.DataFrame()
    raw = pd.read_excel(file_path, header=None)
    header_row = int(raw.notna().sum(axis=1).idxmax())
    df = pd.read_excel(file_path, header=header_row)
    df.columns = (
        df.columns.astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace("\u00A0", " ", regex=False)
        .str.strip()
    )
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)]
    return df


def fetch_tickets() -> pd.DataFrame:
    """Fetch recent tickets from Service Desk API v3, or fall back to Ticket.xlsx."""
    base_url = _clean_base_url()
    if is_available():
        try:
            url = f"{base_url}/api/v3/requests"
            headers = _get_headers()
            params = {
                "input_data": json.dumps({
                    "list_info": {
                        "row_count": 100,
                        "search_fields": {},
                        "sort_fields": [{"field": "created_time", "order": "desc"}]
                    }
                })
            }
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            if resp.status_code == 200:
                requests_list = resp.json().get("requests", [])
                if requests_list:
                    rows = []
                    for req in requests_list:
                        created = req.get("created_time")
                        created_str = created.get("display_value") if isinstance(created, dict) else str(created or "")
                        completed = req.get("completed_time")
                        completed_str = completed.get("display_value") if isinstance(completed, dict) else (str(completed) if completed else "")
                        
                        site_obj = req.get("site") or (req.get("requester") or {}).get("site") or {}
                        site_name = site_obj.get("name", "") if isinstance(site_obj, dict) else str(site_obj or "")

                        rows.append({
                            "RequestID": req.get("display_id") or req.get("id", ""),
                            "Subject": req.get("subject", ""),
                            "Created Time": created_str,
                            "Request Mode": req.get("mode", {}).get("name", "") if isinstance(req.get("mode"), dict) else "",
                            "Requester": req.get("requester", {}).get("name", "") if isinstance(req.get("requester"), dict) else "",
                            "Site": site_name,
                            "Category": req.get("category", {}).get("name", "") if isinstance(req.get("category"), dict) else "",
                            "Sub Category": req.get("subcategory", {}).get("name", "") if isinstance(req.get("subcategory"), dict) else "",
                            "Billing Status": req.get("status", {}).get("name", "") if isinstance(req.get("status"), dict) else "",
                            "Technician": req.get("technician", {}).get("name", "") if isinstance(req.get("technician"), dict) else "",
                            "Urgency": req.get("urgency", {}).get("name", "") if isinstance(req.get("urgency"), dict) else "",
                            "VIP User": (req.get("requester") or {}).get("is_vip_user", False),
                            "Billing Code": "",
                            "Completed Time": completed_str,
                            "Closing Comments": "",
                            "Template": req.get("template", {}).get("name", "") if isinstance(req.get("template"), dict) else "",
                            "AI Usage": "",
                            "Solution Aid": ""
                        })
                    print(f"  [OK] [ServiceDesk] Fetched {len(rows)} tickets via live API")
                    return pd.DataFrame(rows)
            print(f"  [WARN] [ServiceDesk] API returned HTTP {resp.status_code}, falling back to Ticket.xlsx")
        except Exception as e:
            print(f"  [WARN] [ServiceDesk] API error ({e}), falling back to Ticket.xlsx")

    return _read_excel_fallback("Ticket.xlsx")


def fetch_review() -> pd.DataFrame:
    """Fetch review data from Service Desk API, or fall back to review.xlsx."""
    return _read_excel_fallback("review.xlsx")


def fetch_year() -> pd.DataFrame:
    """Fetch yearly tickets from Service Desk API, or fall back to Year.xlsx."""
    return _read_excel_fallback("Year.xlsx")


def fetch_worklogs() -> pd.DataFrame:
    """Fetch worklogs from Service Desk API, or fall back to Worklog.xlsx."""
    return _read_excel_fallback("Worklog.xlsx")


def fetch_survey() -> pd.DataFrame:
    """Fetch survey data from Service Desk API, or fall back to Survey.xlsx."""
    return _read_excel_fallback("Survey.xlsx")
