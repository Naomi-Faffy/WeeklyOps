# ZHD Weekly Operations Report Automation

Automated pipeline for generating and distributing the ZHD Weekly Operations Review presentation. Powered by Python and GitHub Actions.

---

## Overview

This pipeline automates the end-to-end collection, analysis, chart generation, and PowerPoint presentation assembly for ZHD weekly operations reviews. It aggregates metrics across multiple operational systems:
- **Service Desk (Zoho ManageEngine)**: Ticket volumes, resolution times, worklogs, billing status, and customer survey ratings.
- **HubSpot CRM**: RFQs (tickets), deal pipelines, and hardware/software sales conversions.
- **Jira Cloud**: HPA, Automation, and Website engineering task tracking and status distribution.

The generated PowerPoint report is automatically populated, archived, uploaded as a GitHub Actions workflow artifact, and optionally emailed directly to stakeholders via SMTP.

---

## Repository Structure

```text
├── .github/
│   └── workflows/
│       └── pipeline.yml                 # GitHub Actions automated workflow
├── fetchers/                            # Live API fetcher layer with local file fallbacks
│   ├── __init__.py
│   ├── service_desk.py                  # Service Desk / Zoho ManageEngine API
│   ├── hubspot.py                       # HubSpot CRM Tickets & Deals API
│   └── jira.py                          # Jira Cloud REST API
├── data/                                # Baseline & fallback data files
│   ├── sevicedesk/                      # Ticket.xlsx, review.xlsx, Year.xlsx, Worklog.xlsx, Survey.xlsx
│   ├── hubspot/                         # HW Sales.xlsx, RFQs.xlsx
│   └── jira/                            # Automation.csv, hpa.csv, Website.csv
├── AERP_Outputs/                        # Output directory (generated on execution)
│   ├── charts/                          # Exported visual charts & KPI tiles
│   ├── tables/                          # Exported data tables & styled HTML
│   ├── logs/                            # Execution logs & manifests
│   └── archive/                         # Timestamped presentation archives
├── ZHD_Weekly_Ops_Review_Template.pptx   # Master slide deck template
├── run_pipeline.py                      # Main pipeline execution script
├── store_report.py                      # Presentation archiving utility
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Git ignore rules
└── README.md                            # Documentation
```

---

## Dual-Mode Data Architecture

The pipeline supports dual-mode execution for maximum resilience:

1. **Live API Mode**: When corresponding API credentials are provided as environment variables / GitHub Secrets, the pipeline fetches real-time data directly from HubSpot, Jira, and Service Desk.
2. **Local Fallback Mode**: If API credentials are not configured or if an external service is unreachable, the fetchers seamlessly fall back to the datasets stored in `data/`, guaranteeing that the pipeline never fails due to transient network issues.

---

## GitHub Actions Automation

The pipeline runs automatically via [.github/workflows/pipeline.yml](.github/workflows/pipeline.yml):

### Triggers
- **Scheduled**: Every Monday at **06:00 UTC** (`08:00 AM Central/South Africa Time`).
- **Manual (`workflow_dispatch`)**: Can be triggered on demand at any time from the GitHub Actions tab by clicking **Run workflow**.

### Workflow Artifacts
After each run, the generated PowerPoint presentation (`ZHD_Weekly_Ops_YYYYMMDD_HHMMSS.pptx`), manifest CSV, and generated charts are saved under the **Artifacts** section of the GitHub Actions run for 30 days.

---

## Configuration & GitHub Secrets

To enable live API integration and automated email dispatch, add the following secrets in your GitHub repository under **Settings > Secrets and variables > Actions**:

### 1. Live API Credentials (Optional)
| Secret Name | Description | Example |
|---|---|---|
| `HUBSPOT_ACCESS_TOKEN` | HubSpot Private App access token | `pat-na1-...` |
| `JIRA_DOMAIN` | Atlassian domain hostname | `yourcompany.atlassian.net` |
| `JIRA_EMAIL` | Atlassian user email address | `user@company.com` |
| `JIRA_API_TOKEN` | Atlassian API token | `ATATT3...` |
| `SERVICEDESK_BASE_URL` | Service Desk instance URL | `https://servicedesk.yourcompany.com` |
| `SERVICEDESK_AUTH_TOKEN` | ManageEngine API token / OAuth token | `...` |

### 2. Email Delivery (Optional)
| Secret Name | Description | Example |
|---|---|---|
| `SMTP_SERVER` | Outgoing SMTP host | `smtp.office365.com` |
| `SMTP_PORT` | SMTP port (typically 587 for TLS) | `587` |
| `SMTP_USER` | Email username / sender address | `tafara@zhdconsulting.com` |
| `SMTP_PASSWORD` | Mail password or Office 365 App Password | `...` |
| `EMAIL_TO` | Recipient email address(es) | `tafara@zhdconsulting.com` |

*Note: If SMTP credentials are not provided, email delivery is cleanly skipped and the report remains available via GitHub Artifacts and local output.*

---

## Local Development & Execution

To run the pipeline locally on your machine:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Naomi-Faffy/WeeklyOps.git
   cd WeeklyOps
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline**:
   ```bash
   python run_pipeline.py
   ```

The generated PowerPoint deck and charts will be created in `AERP_Outputs/`.
