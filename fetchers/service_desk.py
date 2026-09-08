"""
Service Desk / ManageEngine API Fetcher with local file fallback.
Fetches ticket, review, year-to-date, worklog, and survey data.
"""

import os
from pathlib import Path
import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("AERP_DATA_DIR", PROJECT_ROOT / "data"))
SD_DIR = DATA_DIR / "sevicedesk"

BASE_URL = os.environ.get("SERVICEDESK_BASE_URL", "").rstrip("/")
AUTH_TOKEN = os.environ.get("SERVICEDESK_AUTH_TOKEN", "")


def is_available() -> bool:
    """Return True if Service Desk API credentials and endpoint are configured."""
    return bool(BASE_URL and AUTH_TOKEN)


def _get_headers() -> dict:
    return {
        "authtoken": AUTH_TOKEN,
        "Authorization": f"Zoho-oauthtoken {AUTH_TOKEN}",
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
    """Fetch recent tickets from Service Desk API, or fall back to Ticket.xlsx."""
    if is_available():
        try:
            url = f"{BASE_URL}/api/v3/requests"
            resp = requests.get(url, headers=_get_headers(), timeout=30)
            if resp.status_code == 200:
                data = resp.json().get("requests", [])
                if data:
                    print(f"  ✓ [ServiceDesk] Fetched {len(data)} tickets via live API")
                    return pd.json_normalize(data)
            print(f"  ⚠ [ServiceDesk] API returned HTTP {resp.status_code}, falling back to Ticket.xlsx")
        except Exception as e:
            print(f"  ⚠ [ServiceDesk] API error ({e}), falling back to Ticket.xlsx")

    return _read_excel_fallback("Ticket.xlsx")


def fetch_review() -> pd.DataFrame:
    """Fetch review data from Service Desk API, or fall back to review.xlsx."""
    if is_available():
        try:
            url = f"{BASE_URL}/api/v3/requests/review"
            resp = requests.get(url, headers=_get_headers(), timeout=30)
            if resp.status_code == 200:
                data = resp.json().get("requests", [])
                if data:
                    print(f"  ✓ [ServiceDesk] Fetched {len(data)} review records via live API")
                    return pd.json_normalize(data)
        except Exception as e:
            print(f"  ⚠ [ServiceDesk] Review API error ({e}), falling back to review.xlsx")

    return _read_excel_fallback("review.xlsx")


def fetch_year() -> pd.DataFrame:
    """Fetch yearly tickets from Service Desk API, or fall back to Year.xlsx."""
    if is_available():
        try:
            url = f"{BASE_URL}/api/v3/reports/yearly_tickets"
            resp = requests.get(url, headers=_get_headers(), timeout=30)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                if data:
                    print(f"  ✓ [ServiceDesk] Fetched {len(data)} yearly records via live API")
                    return pd.json_normalize(data)
        except Exception as e:
            print(f"  ⚠ [ServiceDesk] Yearly API error ({e}), falling back to Year.xlsx")

    return _read_excel_fallback("Year.xlsx")


def fetch_worklogs() -> pd.DataFrame:
    """Fetch worklogs from Service Desk API, or fall back to Worklog.xlsx."""
    if is_available():
        try:
            url = f"{BASE_URL}/api/v3/worklogs"
            resp = requests.get(url, headers=_get_headers(), timeout=30)
            if resp.status_code == 200:
                data = resp.json().get("worklogs", [])
                if data:
                    print(f"  ✓ [ServiceDesk] Fetched {len(data)} worklogs via live API")
                    return pd.json_normalize(data)
        except Exception as e:
            print(f"  ⚠ [ServiceDesk] Worklogs API error ({e}), falling back to Worklog.xlsx")

    return _read_excel_fallback("Worklog.xlsx")


def fetch_survey() -> pd.DataFrame:
    """Fetch survey data from Service Desk API, or fall back to Survey.xlsx."""
    if is_available():
        try:
            url = f"{BASE_URL}/api/v3/surveys"
            resp = requests.get(url, headers=_get_headers(), timeout=30)
            if resp.status_code == 200:
                data = resp.json().get("surveys", [])
                if data:
                    print(f"  ✓ [ServiceDesk] Fetched {len(data)} surveys via live API")
                    return pd.json_normalize(data)
        except Exception as e:
            print(f"  ⚠ [ServiceDesk] Survey API error ({e}), falling back to Survey.xlsx")

    return _read_excel_fallback("Survey.xlsx")

