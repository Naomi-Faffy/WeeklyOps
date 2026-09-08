"""
Jira Cloud REST API Fetcher with local CSV fallback.
Fetches tasks for HPA, Automation, and Website projects.
"""

import os
from pathlib import Path
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("AERP_DATA_DIR", PROJECT_ROOT / "data"))
JIRA_DIR = DATA_DIR / "jira"

JIRA_DOMAIN = os.environ.get("JIRA_DOMAIN", "").strip().rstrip("/")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "").strip()
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "").strip()


def is_available() -> bool:
    """Return True if Jira credentials and domain are configured."""
    return bool(JIRA_DOMAIN and JIRA_EMAIL and JIRA_API_TOKEN)


def _find_fallback_csv(project_name: str) -> Path:
    """Find CSV file regardless of casing (e.g. hpa.csv vs HPA.csv)."""
    target = f"{project_name.lower()}.csv"
    if JIRA_DIR.exists():
        for p in JIRA_DIR.glob("*.csv"):
            if p.name.lower() == target:
                return p
    return JIRA_DIR / f"{project_name}.csv"


def fetch_tasks(project_name: str) -> pd.DataFrame:
    """
    Fetch Jira tasks for a project (e.g. 'HPA', 'Automation', 'Website').
    Falls back to data/jira/<project_name>.csv if API is unavailable.
    """
    if is_available():
        try:
            domain = JIRA_DOMAIN
            if not domain.startswith("http"):
                domain = f"https://{domain}"

            url = f"{domain}/rest/api/3/search"
            jql = f"project = '{project_name}' ORDER BY created DESC"
            params = {
                "jql": jql,
                "maxResults": 100,
                "fields": "issuetype,summary,assignee,status,created,updated,resolutiondate",
            }
            auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
            headers = {"Accept": "application/json"}

            resp = requests.get(url, headers=headers, auth=auth, params=params, timeout=30)
            if resp.status_code == 200:
                issues = resp.json().get("issues", [])
                if issues:
                    rows = []
                    for issue in issues:
                        fields = issue.get("fields", {})
                        assignee = fields.get("assignee")
                        assignee_name = assignee.get("displayName") if assignee else "Unassigned"
                        issue_type = fields.get("issuetype", {}).get("name", "Task")
                        status_name = fields.get("status", {}).get("name", "To Do")

                        rows.append({
                            "Issue Type": issue_type,
                            "Issue key": issue.get("key", ""),
                            "Issue id": issue.get("id", ""),
                            "Summary": fields.get("summary", ""),
                            "Assignee": assignee_name,
                            "Status": status_name,
                            "Created": fields.get("created", ""),
                            "Updated": fields.get("updated", ""),
                            "Resolved": fields.get("resolutiondate", ""),
                        })
                    print(f"  ✓ [Jira] Fetched {len(rows)} issues for {project_name} via live API")
                    return pd.DataFrame(rows)
            print(f"  ⚠ [Jira] API returned HTTP {resp.status_code}, falling back to CSV for {project_name}")
        except Exception as e:
            print(f"  ⚠ [Jira] API error ({e}), falling back to CSV for {project_name}")

    # Fallback to local CSV
    fallback_csv = _find_fallback_csv(project_name)
    if fallback_csv.exists():
        return pd.read_csv(fallback_csv)

    print(f"  ⚠ [Jira] Fallback file not found: {fallback_csv}")
    return pd.DataFrame(columns=["Issue Type", "Issue key", "Issue id", "Summary", "Assignee", "Status", "Created"])

