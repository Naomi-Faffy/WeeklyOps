import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# =========================================================
# AERP-16 AUTO-SAVE WRAPPER
# Add this as the FIRST CELL in the notebook
# Keeps your existing HubSpot code unchanged
# =========================================================
from pathlib import Path
import builtins
import os
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
try:
    from IPython.display import display as ipy_display
except Exception:
    def ipy_display(*args, **kwargs):
        return None
from pandas.io.formats.style import Styler
import datetime as dt

# -------------------------
# Output folders on your PC
# -------------------------
PROJECT_ROOT = Path(os.environ.get("AERP_PROJECT_ROOT", Path(__file__).resolve().parent))
DATA_DIR = Path(os.environ.get("AERP_DATA_DIR", PROJECT_ROOT / "data"))

AERP16_BASE_DIR = Path(os.environ.get("AERP_OUTPUT_DIR", PROJECT_ROOT / "AERP_Outputs"))
AERP16_CHART_DIR = AERP16_BASE_DIR / "charts"
AERP16_TABLE_DIR = AERP16_BASE_DIR / "tables"
AERP16_LOG_DIR = AERP16_BASE_DIR / "logs"

AERP16_BASE_DIR.mkdir(parents=True, exist_ok=True)
AERP16_CHART_DIR.mkdir(parents=True, exist_ok=True)
AERP16_TABLE_DIR.mkdir(parents=True, exist_ok=True)
AERP16_LOG_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Run timestamp / manifest
# -------------------------
RUN_STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
PRINT_LOG = AERP16_LOG_DIR / f"printed_outputs_{RUN_STAMP}.txt"
MANIFEST_CSV = AERP16_BASE_DIR / f"output_manifest_{RUN_STAMP}.csv"
SILENT_MODE = os.environ.get("AERP_SILENT", "1").strip().lower() not in {"0", "false", "no"}
VERBOSE_PRINT_LOG = os.environ.get("AERP_VERBOSE_PRINT_LOG", "0").strip().lower() in {"1", "true", "yes"}

_aerp16_manifest = []

def _aerp16_add_manifest(kind, path, note=""):
    _aerp16_manifest.append({
        "kind": kind,
        "path": str(path),
        "note": note
    })

def _aerp16_should_log_print(text):
    if VERBOSE_PRINT_LOG:
        return True
    msg = str(text).strip()
    noisy_prefixes = (
        "AERP-16 auto-save wrapper is active.",
        "Charts folder:",
        "Tables folder:",
        "Logs folder:",
    )
    return not msg.startswith(noisy_prefixes)

# -------------------------
# 1) SAVE ALL print() OUTPUTS
# -------------------------
if not hasattr(builtins, "_aerp16_original_print"):
    builtins._aerp16_original_print = builtins.print

def aerp16_print(*args, **kwargs):
    text = " ".join(str(a) for a in args)

    if not SILENT_MODE:
        builtins._aerp16_original_print(*args, **kwargs)

    if _aerp16_should_log_print(text):
        with open(PRINT_LOG, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        _aerp16_add_manifest("print_log", PRINT_LOG, text[:120])

builtins.print = aerp16_print

# -------------------------
# 2) SAVE ALL PLOTTED FIGURES
# -------------------------
if not hasattr(plt, "_aerp16_original_show"):
    plt._aerp16_original_show = plt.show

_aerp16_fig_counter = {"n": 0}

def aerp16_show(*args, **kwargs):
    figs = [plt.figure(num) for num in plt.get_fignums()]
    if figs:
        for fig in figs:
            _aerp16_fig_counter["n"] += 1
            chart_path = AERP16_CHART_DIR / f"chart_{_aerp16_fig_counter['n']:03d}_{RUN_STAMP}.png"
            fig.savefig(chart_path, dpi=300, bbox_inches="tight")
            _aerp16_add_manifest("chart", chart_path, f"Figure {_aerp16_fig_counter['n']}")
            plt.close(fig)
    return None

plt.show = aerp16_show

# -------------------------
# 3) SAVE ALL display(...) OUTPUTS
#    Works for DataFrame, Series, Styler
# -------------------------
_aerp16_table_counter = {"n": 0}

def aerp16_display(obj):
    _aerp16_table_counter["n"] += 1
    idx = _aerp16_table_counter["n"]

    if isinstance(obj, pd.DataFrame):
        csv_path = AERP16_TABLE_DIR / f"table_{idx:03d}_{RUN_STAMP}.csv"
        xlsx_path = AERP16_TABLE_DIR / f"table_{idx:03d}_{RUN_STAMP}.xlsx"
        obj.to_csv(csv_path, index=False)
        obj.to_excel(xlsx_path, index=False)
        _aerp16_add_manifest("dataframe_csv", csv_path, f"Displayed DataFrame #{idx}")
        _aerp16_add_manifest("dataframe_xlsx", xlsx_path, f"Displayed DataFrame #{idx}")

    elif isinstance(obj, pd.Series):
        csv_path = AERP16_TABLE_DIR / f"series_{idx:03d}_{RUN_STAMP}.csv"
        obj.to_frame(name="value").to_csv(csv_path)
        _aerp16_add_manifest("series_csv", csv_path, f"Displayed Series #{idx}")

    elif isinstance(obj, Styler):
        html_path = AERP16_TABLE_DIR / f"styled_table_{idx:03d}_{RUN_STAMP}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(obj.to_html())
        _aerp16_add_manifest("styled_html", html_path, f"Displayed Styler #{idx}")

    return ipy_display(obj)

display = aerp16_display

print("AERP-16 auto-save wrapper is active.")
print(f"Charts folder: {AERP16_CHART_DIR}")
print(f"Tables folder: {AERP16_TABLE_DIR}")
print(f"Logs folder:   {AERP16_LOG_DIR}")


# In[76]:


# =========================================================
# AERP-14 AUTO-SAVE WRAPPER
# Add this as the FIRST CELL in the notebook
# Keeps your existing code unchanged
# =========================================================
from pathlib import Path
import builtins
import os
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
try:
    from IPython.display import display as ipy_display
except Exception:
    def ipy_display(*args, **kwargs):
        return None
from pandas.io.formats.style import Styler
import datetime as dt

# -------------------------
# Output folders on your PC
# -------------------------
AERP14_BASE_DIR = AERP16_BASE_DIR
AERP14_CHART_DIR = AERP16_CHART_DIR
AERP14_TABLE_DIR = AERP16_TABLE_DIR
AERP14_LOG_DIR = AERP16_LOG_DIR

AERP14_BASE_DIR.mkdir(parents=True, exist_ok=True)
AERP14_CHART_DIR.mkdir(parents=True, exist_ok=True)
AERP14_TABLE_DIR.mkdir(parents=True, exist_ok=True)
AERP14_LOG_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Run timestamp / manifest
# -------------------------
RUN_STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
PRINT_LOG = AERP14_LOG_DIR / f"printed_outputs_{RUN_STAMP}.txt"
MANIFEST_CSV = AERP14_BASE_DIR / f"output_manifest_{RUN_STAMP}.csv"
SILENT_MODE = os.environ.get("AERP_SILENT", "1").strip().lower() not in {"0", "false", "no"}
VERBOSE_PRINT_LOG = os.environ.get("AERP_VERBOSE_PRINT_LOG", "0").strip().lower() in {"1", "true", "yes"}

_aerp14_manifest = []

def _aerp14_add_manifest(kind, path, note=""):
    _aerp14_manifest.append({
        "kind": kind,
        "path": str(path),
        "note": note
    })

def _aerp14_should_log_print(text):
    if VERBOSE_PRINT_LOG:
        return True
    msg = str(text).strip()
    noisy_prefixes = (
        "AERP-14 auto-save wrapper is active.",
        "Charts folder:",
        "Tables folder:",
        "Logs folder:",
    )
    return not msg.startswith(noisy_prefixes)

# -------------------------
# 1) SAVE ALL print() OUTPUTS
# -------------------------
if not hasattr(builtins, "_aerp14_original_print"):
    builtins._aerp14_original_print = builtins.print

def aerp14_print(*args, **kwargs):
    text = " ".join(str(a) for a in args)

    # Keep unattended runs silent by default.
    if not SILENT_MODE:
        builtins._aerp14_original_print(*args, **kwargs)

    # Save meaningful messages; suppress routine wrapper status lines by default.
    if _aerp14_should_log_print(text):
        with open(PRINT_LOG, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        _aerp14_add_manifest("print_log", PRINT_LOG, text[:120])

builtins.print = aerp14_print

# -------------------------
# 2) SAVE ALL PLOTTED FIGURES
# -------------------------
if not hasattr(plt, "_aerp14_original_show"):
    plt._aerp14_original_show = plt.show

_aerp14_fig_counter = {"n": 0}

def aerp14_show(*args, **kwargs):
    figs = [plt.figure(num) for num in plt.get_fignums()]
    if figs:
        for fig in figs:
            _aerp14_fig_counter["n"] += 1
            chart_path = AERP14_CHART_DIR / f"chart_{_aerp14_fig_counter['n']:03d}_{RUN_STAMP}.png"
            fig.savefig(chart_path, dpi=300, bbox_inches="tight")
            _aerp14_add_manifest("chart", chart_path, f"Figure {_aerp14_fig_counter['n']}")
            plt.close(fig)
    return None

plt.show = aerp14_show

# -------------------------
# 3) SAVE ALL display(...) OUTPUTS
#    Works for DataFrame, Series, Styler
# -------------------------
_aerp14_table_counter = {"n": 0}

def aerp14_display(obj):
    _aerp14_table_counter["n"] += 1
    idx = _aerp14_table_counter["n"]

    # DataFrame
    if isinstance(obj, pd.DataFrame):
        csv_path = AERP14_TABLE_DIR / f"table_{idx:03d}_{RUN_STAMP}.csv"
        xlsx_path = AERP14_TABLE_DIR / f"table_{idx:03d}_{RUN_STAMP}.xlsx"
        obj.to_csv(csv_path, index=False)
        obj.to_excel(xlsx_path, index=False)
        _aerp14_add_manifest("dataframe_csv", csv_path, f"Displayed DataFrame #{idx}")
        _aerp14_add_manifest("dataframe_xlsx", xlsx_path, f"Displayed DataFrame #{idx}")

    # Series
    elif isinstance(obj, pd.Series):
        csv_path = AERP14_TABLE_DIR / f"series_{idx:03d}_{RUN_STAMP}.csv"
        obj.to_frame(name="value").to_csv(csv_path)
        _aerp14_add_manifest("series_csv", csv_path, f"Displayed Series #{idx}")

    # Styler
    elif isinstance(obj, Styler):
        html_path = AERP14_TABLE_DIR / f"styled_table_{idx:03d}_{RUN_STAMP}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(obj.to_html())
        _aerp14_add_manifest("styled_html", html_path, f"Displayed Styler #{idx}")

    return ipy_display(obj)

# Make sure your notebook's display(...) uses this wrapper
display = aerp14_display

print("AERP-14 auto-save wrapper is active.")
print(f"Charts folder: {AERP14_CHART_DIR}")
print(f"Tables folder: {AERP14_TABLE_DIR}")
print(f"Logs folder:   {AERP14_LOG_DIR}")

# =========================================================
# API DATA-SOURCE LAYER  (Service Desk = Zoho ManageEngine)
# ---------------------------------------------------------
# Maps each Service Desk export path to a live-API fetcher and intercepts
# pd.read_excel for those paths. Every downstream section below runs
# UNCHANGED - only where the data comes from is swapped (API first, and the
# fetcher falls back to the Excel file if the API is unavailable).
# =========================================================
from pathlib import Path as _Path
from fetchers import service_desk as _sd_api

_SD_SOURCE_MAP = {
    (DATA_DIR / "sevicedesk" / "Ticket.xlsx").resolve(): _sd_api.fetch_tickets,
    (DATA_DIR / "sevicedesk" / "review.xlsx").resolve(): _sd_api.fetch_review,
    (DATA_DIR / "sevicedesk" / "Year.xlsx").resolve(): _sd_api.fetch_year,
    (DATA_DIR / "sevicedesk" / "Worklog.xlsx").resolve(): _sd_api.fetch_worklogs,
    (DATA_DIR / "sevicedesk" / "Survey.xlsx").resolve(): _sd_api.fetch_survey,
}

_orig_read_excel = pd.read_excel
_sd_cache: dict = {}
_sd_in_progress: set = set()


def _sd_mapped_path(path):
    try:
        p = _Path(str(path)).resolve()
    except Exception:
        return None
    for src, _fetch in _SD_SOURCE_MAP.items():
        if p == src or p.name.lower() == src.name.lower():
            return src
    return None


def _api_read_excel(*args, **kwargs):
    if not getattr(_sd_api, "is_available", lambda: False)():
        return _orig_read_excel(*args, **kwargs)
    path = args[0] if args else kwargs.get("io")
    src = _sd_mapped_path(path) if path else None
    if src is not None:
        if src in _sd_in_progress:
            return _orig_read_excel(*args, **kwargs)
        _sd_in_progress.add(src)
        try:
            if src not in _sd_cache:
                _sd_cache[src] = _SD_SOURCE_MAP[src]()
            return _sd_cache[src].copy()
        finally:
            _sd_in_progress.discard(src)
    return _orig_read_excel(*args, **kwargs)


pd.read_excel = _api_read_excel


# In[77]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

file_path = DATA_DIR / "sevicedesk" / "Ticket.xlsx"

# =========================
# 1) READ EXCEL & AUTO HEADER
# =========================
raw = pd.read_excel(file_path, header=None)
header_row = int(raw.notna().sum(axis=1).idxmax())
df = pd.read_excel(file_path, header=header_row)

df.columns = (
    df.columns.astype(str)
    .str.replace('\n', ' ', regex=False)
    .str.replace('\r', ' ', regex=False)
    .str.replace('\u00A0', ' ', regex=False)
    .str.strip()
)

df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)]

# =========================
# 2) AUTO-DETECT CREATED DATE/TIME COLUMN
# =========================
def norm(s):
    return re.sub(r'[\s_\-]+', '', str(s).strip().lower())

date_col = None
best_rate = -1

for c in df.columns:
    parsed = pd.to_datetime(df[c], errors="coerce")
    rate = parsed.notna().mean()
    if rate > best_rate and any(k in norm(c) for k in ["created", "date", "time"]):
        best_rate = rate
        date_col = c

# fallback: most parseable column
if date_col is None or best_rate < 0.30:
    for c in df.columns:
        parsed = pd.to_datetime(df[c], errors="coerce")
        rate = parsed.notna().mean()
        if rate > best_rate:
            best_rate = rate
            date_col = c

if date_col is None or best_rate < 0.30:
    raise ValueError(f"Could not detect a date/time column. Columns: {df.columns.tolist()}")

df["created"] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=["created"]).copy()
df["date_only"] = df["created"].dt.normalize()

# =========================
# 3) AUTO-SELECT LATEST 5 WORKDAYS
# =========================
end_date = df["date_only"].max()
week_days = pd.bdate_range(end=end_date, periods=5)

df_week = df[df["date_only"].isin(week_days)].copy()
if df_week.empty:
    df_week = df[df["date_only"] >= (end_date - pd.Timedelta(days=7))].copy()

if df_week.empty:
    raise ValueError("No data found after parsing dates.")

# =========================
# 4) DAILY COUNTS (FIXED COLUMN NAME)
# =========================
daily_counts = (
    df_week.groupby("date_only")
    .size()
    .reindex(week_days, fill_value=0)
    .rename_axis("date_only")          # [COMPLETE] forces the index name
    .reset_index(name="count")         # [COMPLETE] now column will be 'date_only'
)

daily_counts["day_label"] = daily_counts["date_only"].dt.strftime("%a")

avg_tickets = daily_counts["count"].mean()

# =========================
# 5) PLOT
# =========================
plt.figure(figsize=(10, 4), dpi=120)

plt.bar(
    daily_counts["day_label"],
    daily_counts["count"],
    color="#22489A",
    edgecolor="white"
)

plt.axhline(avg_tickets, linestyle="--", color="green", linewidth=2)

for i, v in enumerate(daily_counts["count"]):
    plt.text(i, v + 0.3, str(int(v)), ha="center", fontweight="bold")

start_str = week_days.min().strftime("%d %b %Y")
end_str   = week_days.max().strftime("%d %b %Y")

plt.title(f"Ticket Volume Across the Week ", fontweight="bold")
plt.xlabel("Day")
plt.ylabel("Ticket Count")
plt.grid(axis="y", linestyle=":", alpha=0.6)

plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_ticket_volume_daily.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_ticket_volume_daily.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[78]:


import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import warnings

warnings.filterwarnings("ignore")

# ============================
# SETTINGS
# ============================
file_path = DATA_DIR / "sevicedesk" / "review.xlsx"  # <-- FIXED (use your real file)

primary_blue = '#22489A'
primary_green = '#32B24B'

distinct_colors = [
    '#FFC107',  # amber
    '#FF6F61',  # coral/red
    '#8E44AD',  # purple
    '#FF9800',  # orange
    '#6D4C41',  # brown
    '#2C2C2C',  # dark grey
]

# ============================
# HELPERS
# ============================
def norm(s: str) -> str:
    return re.sub(r'[\s_\-]+', '', str(s).strip().lower())

def clean_cols(cols):
    return (
        pd.Index(cols)
        .astype(str)
        .str.strip()
        .str.replace('\n', ' ', regex=False)
        .str.replace('\r', ' ', regex=False)
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace(' ', '_')
        .str.lower()
    )

def load_with_auto_header(path: str) -> pd.DataFrame:
    """
    Handles Excel/CSV where the header row isn't the first row.
    Excel: finds the row with the most filled cells.
    CSV: tries normal read; if columns are 'Unnamed', re-reads with detected header row.
    """
    ext = os.path.splitext(path)[1].lower()

    if ext in [".xlsx", ".xls"]:
        raw = pd.read_excel(path, header=None)
        if raw.dropna(how="all").empty:
            raise ValueError("The Excel sheet looks empty.")
        header_row = int(raw.notna().sum(axis=1).idxmax())
        df_ = pd.read_excel(path, header=header_row)
        df_.columns = clean_cols(df_.columns)
        return df_.dropna(how="all").copy()

    if ext == ".csv":
        df_ = pd.read_csv(path, encoding="utf-8", errors="replace")
        df_.columns = clean_cols(df_.columns)

        # If CSV still came in as unnamed columns, try detecting header row
        if all(str(c).startswith("unnamed") for c in df_.columns):
            raw = pd.read_csv(path, header=None, encoding="utf-8", errors="replace")
            header_row = int(raw.notna().sum(axis=1).idxmax())
            df_ = pd.read_csv(path, header=header_row, encoding="utf-8", errors="replace")
            df_.columns = clean_cols(df_.columns)

        return df_.dropna(how="all").copy()

    raise ValueError("Unsupported file type. Use .xlsx/.xls or .csv")

def pick_column(df_, candidates, contains_any=None):
    cand_norm = {norm(c) for c in candidates}
    for c in df_.columns:
        if norm(c) in cand_norm:
            return c
    if contains_any:
        for c in df_.columns:
            nc = norm(c)
            if all(k in nc for k in contains_any):
                return c
    return None

# ============================
# LOAD DATA
# ============================
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

df = load_with_auto_header(file_path)

# ============================
# FIND REQUIRED COLUMNS
# ============================
date_col = pick_column(
    df,
    candidates=["created_date", "created date", "created_time", "created time", "created", "created_dt"],
    contains_any=["created"]
)

status_col = pick_column(
    df,
    candidates=["status", "ticket_status", "ticket status", "state"],
    contains_any=["status"]
)

if date_col is None or status_col is None:
    raise KeyError(
        "Could not detect required columns.\n"
        f"Detected columns: {df.columns.tolist()}\n"
        f"Date column found: {date_col}\n"
        f"Status column found: {status_col}"
    )

# ============================
# PARSE CREATED DATE (ROBUST)
# ============================
df[date_col] = df[date_col].astype(str).str.strip()

df["created_dt"] = pd.to_datetime(df[date_col], errors="coerce")

# Fallback to your explicit format if too many NaT
if df["created_dt"].isna().mean() > 0.30:
    df["created_dt"] = pd.to_datetime(
        df[date_col],
        format="%b %d, %Y %I:%M %p",
        errors="coerce"
    )

df = df.dropna(subset=["created_dt"]).copy()
df["date_only"] = df["created_dt"].dt.normalize()

# ============================
# LAST 5 WORKING DAYS (MON-FRI)
# ============================
end_date = df["date_only"].max()
last_5_workdays = pd.bdate_range(end=end_date, periods=5)

df_filtered = df[df["date_only"].isin(last_5_workdays)].copy()

# ============================
# COUNT PER STATUS (ALL STATUSES)
# ============================
df_filtered["status_clean"] = df_filtered[status_col].astype(str).str.strip()
status_counts = df_filtered["status_clean"].value_counts(dropna=False)

total_count = int(status_counts.sum())

# ============================
# COLOUR MAP (Closed=Blue, Open=Green, others distinct)
# ============================
color_map = {}

for s in status_counts.index:
    sl = str(s).strip().lower()
    if sl == "closed":
        color_map[s] = primary_blue
    elif sl == "open":
        color_map[s] = primary_green

# assign remaining
cycle_i = 0
for s in status_counts.index:
    if s not in color_map:
        color_map[s] = distinct_colors[cycle_i % len(distinct_colors)]
        cycle_i += 1

total_color = "#2C2C2C"

# ============================
# KPI TILES
# ============================
labels = list(status_counts.index) + ["Total Tickets"]
values = [int(v) for v in status_counts.values] + [total_count]
colors = [color_map[s] for s in status_counts.index] + [total_color]

n_tiles = len(labels)
cols = 2 if n_tiles == 4 else min(3, n_tiles)
rows = (n_tiles + cols - 1) // cols

fig, ax = plt.subplots(figsize=(14, 5.0 + (rows - 1) * 2.8), dpi=120)
ax.axis("off")

x_margin = 0.10 if n_tiles == 4 else 0.06
y_margin = 0.18

tile_w = (1 - 2 * x_margin) / cols
tile_h = (1 - 2 * y_margin) / rows

title_fs = 16
value_fs = 42

for i, (lab, val, col) in enumerate(zip(labels, values, colors)):
    r = i // cols
    c = i % cols

    x = x_margin + c * tile_w
    y_top = 1 - y_margin - r * tile_h
    y = y_top - tile_h

    rect = plt.Rectangle(
        (x, y),
        tile_w * 0.95,
        tile_h * 0.86,
        transform=ax.transAxes,
        facecolor="white",
        edgecolor="#E5E7EB",
        linewidth=1.4
    )
    ax.add_patch(rect)

    ax.text(
        x + (tile_w * 0.95) / 2,
        y + tile_h * 0.62,
        str(lab),
        ha="center",
        va="center",
        fontsize=title_fs,
        fontweight="bold",
        color=col,
        transform=ax.transAxes,
        wrap=True
    )

    ax.text(
        x + (tile_w * 0.95) / 2,
        y + tile_h * 0.28,
        f"{val}",
        ha="center",
        va="center",
        fontsize=value_fs,
        fontweight="bold",
        color=col,
        transform=ax.transAxes
    )

start_date = last_5_workdays.min()
ax.text(
    0.5, 0.06,
    f"Last 5 Working Days: {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}",
    ha="center",
    va="center",
    fontsize=12,
    color=primary_blue,
    transform=ax.transAxes
)

plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_ticket_kpi_tiles.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_ticket_kpi_tiles.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[79]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings

warnings.filterwarnings("ignore")

file_path = DATA_DIR / "sevicedesk" / "review.xlsx"

# =========================
# LOAD + CLEAN HEADERS
# =========================
df = pd.read_excel(file_path)

df.columns = (
    df.columns.astype(str)
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
)

def norm(s):
    return re.sub(r"[\s_\-]+", "", str(s).strip().lower())

# =========================
# AUTO-DETECT CREATED / ID / STATUS
# =========================
created_col = None
id_col = None
status_col = None

# detect created datetime column (best parseable + name hints)
date_hints = ["createdtime", "createddate", "created", "date", "time"]
best_rate = -1
for c in df.columns:
    parsed = pd.to_datetime(df[c], errors="coerce")
    rate = parsed.notna().mean()
    name_ok = any(h in norm(c) for h in date_hints)
    if name_ok and rate > best_rate:
        best_rate = rate
        created_col = c

# fallback: best parseable column
if created_col is None or best_rate < 0.30:
    best_c, best_rate = None, -1
    for c in df.columns:
        parsed = pd.to_datetime(df[c], errors="coerce")
        rate = parsed.notna().mean()
        if rate > best_rate:
            best_rate = rate
            best_c = c
    created_col = best_c

# detect id column
for c in df.columns:
    if any(k in norm(c) for k in ["requestid", "ticketid", "reqid"]):
        id_col = c
        break

# fallback id: most unique column
if id_col is None:
    best_c, best_score = None, -1
    for c in df.columns:
        s = df[c].dropna()
        if s.empty:
            continue
        score = s.nunique() / len(s)
        if score > best_score:
            best_score = score
            best_c = c
    id_col = best_c

# detect status column
for c in df.columns:
    if any(k in norm(c) for k in ["status", "state"]):
        status_col = c
        break

# fallback status: column that contains "closed" often
if status_col is None:
    best_c, best_score = None, -1
    for c in df.columns:
        s = df[c].astype(str).str.lower()
        score = s.str.contains(r"\bclosed\b", regex=True, na=False).mean()
        if score > best_score:
            best_score = score
            best_c = c
    status_col = best_c

if created_col is None or id_col is None or status_col is None:
    raise ValueError(
        "Could not detect required columns.\n"
        f"created_col={created_col}, id_col={id_col}, status_col={status_col}\n"
        f"Available columns: {df.columns.tolist()}"
    )

print("USING COLUMNS:")
print("Created:", created_col)
print("ID:", id_col)
print("Status:", status_col)

# =========================
# BUILD CREATED_TIME, DATE_ONLY, IS_CLOSED
# =========================
df["CREATED_TIME"] = pd.to_datetime(df[created_col], errors="coerce")
df = df.dropna(subset=["CREATED_TIME"]).copy()

df["DATE_ONLY"] = df["CREATED_TIME"].dt.normalize()

df["STATUS_CLEAN"] = (
    df[status_col].astype(str)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
    .str.lower()
)

df["IS_CLOSED"] = df["STATUS_CLEAN"].str.contains(r"\bclosed\b", regex=True, na=False)

# =========================
# LAST 5 WORKING DAYS
# =========================
end_date = df["DATE_ONLY"].max()
last_5_days = pd.bdate_range(end=end_date, periods=5)

df_5days = df[df["DATE_ONLY"].isin(last_5_days)].copy()

# =========================
# DAILY AGGREGATION (FIXED)
# =========================
daily = (
    df_5days.groupby(df_5days["DATE_ONLY"])
    .agg(
        TOTAL_OPENED=(id_col, "count"),
        TOTAL_CLOSED=("IS_CLOSED", "sum")
    )
    .reindex(last_5_days, fill_value=0)
)

daily.index.name = "DATE"
daily = daily.reset_index()
daily["DAY_LABEL"] = daily["DATE"].dt.strftime("%a %d")

display(daily)

# =========================
# PLOT
# =========================
BLUE  = "#22489A"
GREEN = "#32B24B"

plt.figure(figsize=(10, 4), dpi=130)

plt.plot(
    daily["DAY_LABEL"], daily["TOTAL_OPENED"],
    marker="o", linewidth=2.6, color=GREEN,
    label="Total Tickets Opened"
)

plt.plot(
    daily["DAY_LABEL"], daily["TOTAL_CLOSED"],
    marker="o", linestyle="--", linewidth=2.6, color=BLUE,
    label="Tickets Closed"
)

# value labels
ymax = max(daily["TOTAL_OPENED"].max(), 1)
offset = ymax * 0.06

for _, r in daily.iterrows():
    plt.text(r["DAY_LABEL"], r["TOTAL_OPENED"] + offset, str(int(r["TOTAL_OPENED"])),
             ha="center", fontweight="bold", fontsize=9, color=GREEN)
    plt.text(r["DAY_LABEL"], r["TOTAL_CLOSED"] + offset, str(int(r["TOTAL_CLOSED"])),
             ha="center", fontweight="bold", fontsize=9, color=BLUE)

start = last_5_days.min().strftime("%d %b %Y")
end   = last_5_days.max().strftime("%d %b %Y")

plt.title(f"Tickets Opened vs Tickets Closed",
          fontweight="bold")
plt.xlabel("Day")
plt.ylabel("Number of Tickets")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_tickets_opened_closed.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_tickets_opened_closed.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[80]:


import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os
import re
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# SETTINGS
# ============================================================
file_path = DATA_DIR / "sevicedesk" / "review.xlsx"

base_colors = ['#22489A', '#32B24B']  # Blue, Green
extra_colors = [
    '#FFC107',  # amber
    '#FF6F61',  # coral/red
    '#8E44AD',  # purple
    '#FF9800',  # orange
    '#6D4C41',  # brown
    '#2C2C2C',  # dark grey
]

# ============================================================
# HELPERS
# ============================================================
def norm(s: str) -> str:
    return re.sub(r'[\s_\-]+', '', str(s).strip().lower())

def clean_cols(cols):
    return (
        pd.Index(cols)
        .astype(str)
        .str.strip()
        .str.replace('\n', ' ', regex=False)
        .str.replace('\r', ' ', regex=False)
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace(' ', '_')
        .str.lower()
    )

def load_excel_with_auto_header(path: str) -> pd.DataFrame:
    """
    Reads an Excel file even when headers are not on the first row.
    Detects the row with the most non-empty cells and uses it as header.
    """
    raw = pd.read_excel(path, header=None)

    # If the sheet is completely empty
    if raw.dropna(how="all").empty:
        raise ValueError("The Excel sheet looks empty.")

    header_row = int(raw.notna().sum(axis=1).idxmax())
    df_ = pd.read_excel(path, header=header_row)

    df_.columns = clean_cols(df_.columns)

    # Drop fully empty rows
    df_ = df_.dropna(how="all").copy()
    return df_

def pick_column(df_: pd.DataFrame, candidates, contains_any=None):
    """
    Pick a column by exact normalized match first,
    then by 'contains' fallback.
    """
    cand_norm = {norm(c) for c in candidates}
    for c in df_.columns:
        if norm(c) in cand_norm:
            return c

    if contains_any:
        for c in df_.columns:
            nc = norm(c)
            if all(k in nc for k in contains_any):
                return c

    return None

# ============================================================
# LOAD DATA (AUTO HANDLE XLSX HEADERS)
# ============================================================
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

ext = os.path.splitext(file_path)[1].lower()
if ext in [".xlsx", ".xls"]:
    df = load_excel_with_auto_header(file_path)
elif ext == ".csv":
    df = pd.read_csv(file_path, encoding="utf-8", errors="replace")
    df.columns = clean_cols(df.columns)
else:
    raise ValueError("Unsupported file type. Use .xlsx/.xls or .csv")

# ============================================================
# AUTO-DETECT REQUIRED COLUMNS
# ============================================================
date_col = pick_column(
    df,
    candidates=["created_date", "created date", "created_time", "created time", "created", "created_dt"],
    contains_any=["created"]  # fallback: any column that contains "created"
)

status_col = pick_column(
    df,
    candidates=["status", "ticket_status", "ticket status", "state"],
    contains_any=["status"]  # fallback: any column that contains "status"
)

if date_col is None or status_col is None:
    raise KeyError(
        "Could not detect required columns.\n"
        f"Detected columns: {df.columns.tolist()}\n"
        f"Date column found: {date_col}\n"
        f"Status column found: {status_col}"
    )

# ============================================================
# PARSE CREATED DATE (ROBUST)
# Example expected: Jan 16, 2026 03:46 PM
# ============================================================
df[date_col] = df[date_col].astype(str).str.strip()

# First attempt: flexible parser
df["created_dt"] = pd.to_datetime(df[date_col], errors="coerce")

# If too many NaT, try your explicit format
if df["created_dt"].isna().mean() > 0.30:
    df["created_dt"] = pd.to_datetime(
        df[date_col],
        format="%b %d, %Y %I:%M %p",
        errors="coerce"
    )

df = df.dropna(subset=["created_dt"]).copy()
df["date_only"] = df["created_dt"].dt.normalize()

# ============================================================
# LAST 5 WORKING DAYS (MON-FRI)
# ============================================================
end_date = df["date_only"].max()
last_5_workdays = pd.bdate_range(end=end_date, periods=5)

df_week = df[df["date_only"].isin(last_5_workdays)].copy()

# ============================================================
# GROUP DATA
# ============================================================
ticket_summary = (
    df_week
    .groupby(["date_only", status_col])
    .size()
    .reset_index(name="count")
)

ticket_summary["count"] = pd.to_numeric(ticket_summary["count"], errors="coerce").fillna(0)

# ============================================================
# COLORS
# ============================================================
statuses = ticket_summary[status_col].dropna().unique()
color_cycle = itertools.cycle(base_colors + extra_colors)
status_colors = {status: next(color_cycle) for status in statuses}

# ============================================================
# PIVOT FOR GROUPED BAR CHART
# ============================================================
pivot_df = (
    ticket_summary
    .pivot(index="date_only", columns=status_col, values="count")
    .fillna(0)
    .astype(float)
    .sort_index()
)

# Ensure all 5 workdays appear even if zero tickets
pivot_df = pivot_df.reindex(last_5_workdays, fill_value=0)

# ============================================================
# PLOT GROUPED BAR CHART
# ============================================================
fig, ax = plt.subplots(figsize=(13, 6.8), dpi=120)

pivot_df.plot(
    kind="bar",
    stacked=False,
    ax=ax,
    color=[status_colors[col] for col in pivot_df.columns],
    width=0.85,
    edgecolor="white",
    linewidth=0.7
)

start_date = last_5_workdays.min()

ax.set_title(
    f"Tickets by Date",
    fontsize=18,
    fontweight="bold",
    color="#22489A",
    pad=12
)

ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Number of Tickets", fontsize=12)

ax.set_xticklabels(
    [d.strftime("%a %b %d") for d in pivot_df.index],
    rotation=0,
    fontsize=11
)

ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(
    title="Status",
    title_fontsize=11,
    fontsize=10,
    frameon=True
)

# Value labels (safe for small datasets)
for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", fontsize=9, padding=2)

plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_tickets_by_date.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_tickets_by_date.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[81]:


import pandas as pd
import re
import warnings

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

file_path = DATA_DIR / "sevicedesk" / "Ticket.xlsx"

# =========================================================
# 1) LOAD EXCEL (auto-detect header row)
# =========================================================
raw = pd.read_excel(file_path, header=None)
header_row = int(raw.notna().sum(axis=1).idxmax())
df = pd.read_excel(file_path, header=header_row)

# Clean headers
df.columns = (
    df.columns.astype(str)
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
)

# Drop unnamed columns
df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)].copy()

def norm(s: str) -> str:
    return re.sub(r"[\s_\-]+", "", str(s).strip().lower())

col_map = {norm(c): c for c in df.columns}

def find_col(*candidates):
    for cand in candidates:
        k = norm(cand)
        if k in col_map:
            return col_map[k]
    return None

# =========================================================
# 2) MAP YOUR REAL COLUMNS (from your screenshot list)
# =========================================================
reqid_col   = find_col("RequestID", "Request Id", "Request ID")
requester   = find_col("Requester", "Requestor")
category    = find_col("Category")
subject     = find_col("Subject")
site        = find_col("Site")
urgency     = find_col("Urgency", "Priority")
created     = find_col("Created Time", "Created")
technician  = find_col("Technician", "Assigned To", "Assignee")
completed   = find_col("Completed Time", "Completed", "Completion Time")

missing = [name for col, name in [
    (reqid_col, "RequestID"),
    (requester, "Requester"),
    (category, "Category"),
    (subject, "Subject"),
    (site, "Site"),
    (urgency, "Urgency"),
    (created, "Created Time"),
    (technician, "Technician"),
    (completed, "Completed Time"),
] if col is None]

if missing:
    raise KeyError(
        "Missing required columns: " + ", ".join(missing) +
        "\nColumns found: " + ", ".join(df.columns.astype(str).tolist())
    )

# =========================================================
# 3) BUILD THE TABLE + DERIVE STATUS
# =========================================================
df2 = df[[reqid_col, requester, category, subject, site, urgency, created, technician, completed]].copy()
df2 = df2.rename(columns={
    reqid_col:  "RequestID",
    requester:  "Requester",
    category:   "Category",
    subject:    "Subject",
    site:       "Site",
    urgency:    "Urgency",
    created:    "Created Time",
    technician: "Technician",
    completed:  "Completed Time",
})

# Parse times safely
df2["Created Time"] = pd.to_datetime(df2["Created Time"], errors="coerce")
df2["Completed Time"] = pd.to_datetime(df2["Completed Time"], errors="coerce")

# Anything with NO completed time = not closed
df2["Request Status"] = df2["Completed Time"].apply(lambda x: "Open" if pd.isna(x) else "Closed")

# =========================================================
# 4) FILTER: EVERYTHING EXCEPT CLOSED
# =========================================================
df2 = df2[df2["Request Status"] != "Closed"].copy()

# Drop Completed Time from final view (optional)
df2 = df2.drop(columns=["Completed Time"])

# Sort latest first
df2 = df2.sort_values("Created Time", ascending=False)

# =========================================================
# 5) BEAUTIFUL TABLE STYLING
# =========================================================
GREEN  = "#32B24B"
BLUE   = "#22489A"
BORDER = "#E5E7EB"
TEXT   = "#111827"
MUTED  = "#6B7280"

def zebra_rows(i: int) -> str:
    return "background-color: #F7F7F7;" if i % 2 else "background-color: white;"

def style_status(val):
    v = str(val).strip().lower()
    if v == "open":
        return "color: #32B24B; font-weight: 900;"
    return f"color: {TEXT}; font-weight: 800;"

def style_urgency(val):
    v = str(val).strip().lower()
    if "high" in v or "critical" in v or "urgent" in v:
        return "color: #EF4444; font-weight: 900;"
    if "medium" in v:
        return "color: #F59E0B; font-weight: 900;"
    if "low" in v:
        return f"color: {BLUE}; font-weight: 800;"
    return f"color: {MUTED}; font-weight: 700;"

styler = (
    df2.style
    .set_table_styles([
        {"selector": "th",
         "props": [
             ("background-color", "white"),
             ("color", TEXT),
             ("font-weight", "900"),
             ("border-bottom", f"2px solid {BORDER}"),
             ("padding", "12px 10px"),
             ("text-align", "left"),
         ]},
        {"selector": "td",
         "props": [
             ("border-bottom", f"1px solid {BORDER}"),
             ("padding", "10px 10px"),
             ("color", TEXT),
             ("vertical-align", "middle"),
         ]},
        {"selector": "table",
         "props": [
             ("border-collapse", "separate"),
             ("border-spacing", "0"),
             ("width", "100%"),
         ]},
    ])
    .apply(lambda s: [zebra_rows(i) for i in range(len(s))], axis=0)
    .hide(axis="index")
)

styler = styler.map(style_status, subset=["Request Status"])
styler = styler.map(style_urgency, subset=["Urgency"])
styler = styler.set_properties(subset=["Subject"], **{"white-space": "normal", "min-width": "360px"})

styler = styler.format({
    "Created Time": lambda x: x.strftime("%Y-%m-%d\n%H:%M:%S") if hasattr(x, "strftime") else x
})

styler


# In[82]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings
import itertools

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

file_path = DATA_DIR / "sevicedesk" / "Ticket.xlsx"

# =========================
# 1) READ EXCEL & AUTO HEADER ROW
# =========================
raw = pd.read_excel(file_path, header=None)
header_row = int(raw.notna().sum(axis=1).idxmax())
df = pd.read_excel(file_path, header=header_row)

# Clean headers
df.columns = (
    df.columns.astype(str)
    .str.replace('\n', ' ', regex=False)
    .str.replace('\r', ' ', regex=False)
    .str.replace('\u00A0', ' ', regex=False)
    .str.strip()
)

# Drop unnamed columns
df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)]

def norm(s):
    return re.sub(r'[\s_\-]+', '', str(s).strip().lower())

# =========================
# 2) AUTO-DETECT CREATED DATE/TIME COLUMN
# =========================
date_col = None
best_rate = -1

for c in df.columns:
    parsed = pd.to_datetime(df[c], errors="coerce")
    rate = parsed.notna().mean()
    name_hint = any(k in norm(c) for k in ["created", "date", "time"])
    if name_hint and rate > best_rate:
        best_rate = rate
        date_col = c

# fallback: best parseable column
if date_col is None or best_rate < 0.30:
    for c in df.columns:
        parsed = pd.to_datetime(df[c], errors="coerce")
        rate = parsed.notna().mean()
        if rate > best_rate:
            best_rate = rate
            date_col = c

if date_col is None or best_rate < 0.30:
    raise ValueError(f"Could not detect date/time column. Columns: {df.columns.tolist()}")

df["created"] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=["created"]).copy()
df["date_only"] = df["created"].dt.normalize()

# =========================
# 3) AUTO-DETECT SITE COLUMN
# =========================
site_col = None

for c in df.columns:
    if "site" in str(c).lower():
        site_col = c
        break

if site_col is None:
    best_col, best_score = None, -1
    n = len(df)
    for c in df.columns:
        s = df[c].astype(str).str.strip()
        s = s[s.ne("") & s.ne("nan")]
        if len(s) < max(10, n * 0.2):
            continue

        if "id" in str(c).lower():
            continue

        uniq = s.nunique()
        # site-like: categorical (not too unique)
        if 2 <= uniq <= min(200, int(len(s) * 0.8)):
            unique_ratio = uniq / len(s)
            avg_len = s.map(len).mean()
            score = (1 - unique_ratio) * 0.7 + (1 / (1 + avg_len)) * 0.3
            if score > best_score:
                best_score = score
                best_col = c

    site_col = best_col

if site_col is None:
    raise ValueError("Could not detect the Site column from the file.")

# =========================
# 4) AUTO-SELECT LATEST 5 WORKING DAYS IN THIS FILE
# =========================
end_date = df["date_only"].max()
week_days = pd.bdate_range(end=end_date, periods=5)

df_week = df[df["date_only"].isin(week_days)].copy()

# fallback: if missing some business days in the data, still keep last 7 calendar days
if df_week.empty:
    df_week = df[df["date_only"] >= (end_date - pd.Timedelta(days=7))].copy()

if df_week.empty:
    raise ValueError("No tickets found after parsing dates.")

# =========================
# 5) COUNT TICKETS BY SITE
# =========================
site_counts = (
    df_week[site_col]
    .astype(str)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
    .replace({"": "Unknown", "nan": "Unknown"})
    .value_counts()
)

TOP_N = 15
if len(site_counts) > TOP_N:
    site_counts = site_counts.head(TOP_N)

# =========================
# 6) PLOT (WIDER, NOT SQUASHED)
# =========================
plt.figure(figsize=(16, 4), dpi=120)

palette = [
    "#22489A", "#32B24B", "#22C55E", "#EC4899", "#F59E0B",
    "#06B6D4", "#A855F7", "#10B981", "#F97316", "#64748B",
    "#84CC16", "#EF4444", "#14B8A6", "#8B5CF6", "#D946EF"
]
colors = list(itertools.islice(itertools.cycle(palette), len(site_counts)))

plt.bar(site_counts.index.astype(str), site_counts.values, color=colors, width=0.55)

start_str = week_days.min().strftime("%d %b %Y")
end_str   = week_days.max().strftime("%d %b %Y")

plt.title(f"Tickets by Site ({start_str} - {end_str})", fontweight="bold", color="#22489A")
plt.xlabel("Site")
plt.ylabel("Tickets")
plt.ylim(0, max(site_counts.values) + 2)

plt.xticks(rotation=25, ha="right")
plt.grid(axis="y", linestyle=":", alpha=0.6)

for i, v in enumerate(site_counts.values):
    plt.text(i, v + 0.1, str(int(v)), ha="center", fontweight="bold")

plt.gcf().set_constrained_layout(True)

try:
    _chart_path = AERP14_CHART_DIR / "chart_tickets_by_site.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_tickets_by_site.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

PRIMARY_BLUE = "#22489A"
PRIMARY_GREEN = "#32B24B"

file_path = DATA_DIR / "sevicedesk" / "Year.xlsx"

# =========================
# HELPERS
# =========================
def norm(s):
    return re.sub(r'[\s_\-]+', '', str(s).strip().lower())

def safe_to_datetime(s):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        # (pandas >= 3.0 removed infer_datetime_format; to_datetime auto-infers)
        return pd.to_datetime(s, errors="coerce")

def clean_headers(cols):
    return (
        cols.astype(str)
        .str.replace('\n', ' ', regex=False)
        .str.replace('\r', ' ', regex=False)
        .str.replace('\u00A0', ' ', regex=False)
        .str.strip()
    )

def auto_read_sheet_with_header(excel_path, sheet_name):
    raw = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, engine="openpyxl")
    if raw.empty:
        return pd.DataFrame(), None

    header_row = int(raw.notna().sum(axis=1).idxmax())
    df_local = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row, engine="openpyxl")

    df_local.columns = clean_headers(df_local.columns)
    df_local = df_local.loc[:, ~df_local.columns.astype(str).str.match(r"^Unnamed", case=False)]
    df_local = df_local.dropna(how="all")

    if df_local.shape[1] == 0:
        return pd.DataFrame(), header_row

    return df_local, header_row

# =========================
# 1) FIND BEST SHEET + HEADER ROW
# =========================
xl = pd.ExcelFile(file_path, engine="openpyxl")

best_sheet = None
best_df = None
best_header_row = None
best_score = -1

for sh in xl.sheet_names:
    temp_df, hr = auto_read_sheet_with_header(file_path, sh)
    if temp_df is None or temp_df.empty:
        continue

    score = (temp_df.shape[0] * 2) + (temp_df.shape[1] * 5)
    if score > best_score:
        best_score = score
        best_sheet = sh
        best_df = temp_df.copy()
        best_header_row = hr

if best_df is None or best_df.empty or best_df.shape[1] == 0:
    raise ValueError(
        "Could not find a sheet with usable data in Year.xlsx. "
        "Open the file and confirm the data is present and not all merged/blank."
    )

df = best_df.copy()



# =========================
# 2) AUTO-DETECT DATE COLUMN
# =========================
date_col = None
best_rate = -1
date_hints = ["created", "createddate", "createdtime", "date", "datetime", "time", "logged", "opened", "resolved"]

for c in df.columns:
    parsed = safe_to_datetime(df[c])
    rate = parsed.notna().mean()
    name_ok = any(h in norm(c) for h in date_hints)
    if name_ok and rate > best_rate:
        best_rate = rate
        date_col = c

if date_col is None or best_rate < 0.20:
    for c in df.columns:
        parsed = safe_to_datetime(df[c])
        rate = parsed.notna().mean()
        if rate > best_rate:
            best_rate = rate
            date_col = c

if date_col is None or best_rate < 0.20:
    raise ValueError(
        "Could not detect a date column reliably.\n"
        f"Columns: {df.columns.tolist()}\n"
        "Tip: Your date column may be stored as text in a non-standard way."
    )

df["CREATED_DT"] = safe_to_datetime(df[date_col])
df = df.dropna(subset=["CREATED_DT"]).copy()



# =========================
# 3) AUTO-DETECT REQUESTER + SITE COLUMNS
# =========================
requester_col = None
site_col = None

for c in df.columns:
    cn = norm(c)
    if "requester" in cn and requester_col is None:
        requester_col = c
    if ("site" in cn or "organization" in cn or "company" in cn) and site_col is None:
        site_col = c

if requester_col is None:
    raise ValueError(f"Requester column not found. Columns: {df.columns.tolist()}")




# =========================
# 4) CLASSIFY TICKETS INTO TWO GROUPS
# =========================
HPA_REQUESTER_NORM = norm("tatenda chiota")
HPA_SITE_KEYWORDS = ["health professionals authority", "hpa"]
HPA_SITE_KEYWORDS_NORM = [norm(k) for k in HPA_SITE_KEYWORDS]

def classify(row):
    requester = norm(row[requester_col]) if pd.notna(row[requester_col]) else ""
    site = norm(row[site_col]) if site_col and pd.notna(row[site_col]) else ""

    is_hpa = (
        HPA_REQUESTER_NORM in requester
        or any(k in site for k in HPA_SITE_KEYWORDS_NORM)
    )
    return "HPA" if is_hpa else "Support"

df["Ticket_Group"] = df.apply(classify, axis=1)

# --- DEBUG: confirm the split actually happened ---

direct_match_count = df[requester_col].apply(
    lambda x: HPA_REQUESTER_NORM in norm(x) if pd.notna(x) else False
).sum()


# =========================
# 5) FILTER YEAR 2026 + ISO WEEK
# =========================
df_2026 = df[df["CREATED_DT"].dt.year == 2026].copy()

if df_2026.empty:
    years_found = sorted(df["CREATED_DT"].dt.year.dropna().unique().tolist())
    raise ValueError(f"No rows found for year 2026. Years present: {years_found}")

iso = df_2026["CREATED_DT"].dt.isocalendar()
df_2026["ISO_WEEK"] = iso["week"].astype(int)

# =========================
# 6) WEEKLY COUNTS PER GROUP
# =========================
all_weeks = pd.DataFrame({"ISO_WEEK": range(1, df_2026["ISO_WEEK"].max() + 1)})

hpa_weekly = (
    df_2026[df_2026["Ticket_Group"] == "HPA"]
    .groupby("ISO_WEEK").size()
    .reset_index(name="HPA")
)

support_weekly = (
    df_2026[df_2026["Ticket_Group"] == "Support"]
    .groupby("ISO_WEEK").size()
    .reset_index(name="Support")
)

weekly = (
    all_weeks
    .merge(hpa_weekly, on="ISO_WEEK", how="left")
    .merge(support_weekly, on="ISO_WEEK", how="left")
    .fillna(0)
)
weekly["HPA"] = weekly["HPA"].astype(int)
weekly["Support"] = weekly["Support"].astype(int)
weekly["TOTAL"] = weekly["HPA"] + weekly["Support"]


# =========================
# 7) LINE GRAPH - TWO LINES
# =========================
fig, ax = plt.subplots(figsize=(16, 6), dpi=120)

# HPA line - green
ax.plot(
    weekly["ISO_WEEK"], weekly["HPA"],
    linewidth=2.8, marker="o", markersize=5,
    color=PRIMARY_GREEN, label="HPA"
)

# Support line - blue
ax.plot(
    weekly["ISO_WEEK"], weekly["Support"],
    linewidth=2.8, marker="s", markersize=5,
    color=PRIMARY_BLUE, label="Support"
)

# Target line
ax.axhline(y=14, color='red', linestyle='--', linewidth=1.8, label='Target (14 tickets/week)')

ax.set_title("Weekly Ticket Trend by Group - Year 2026", fontsize=15, fontweight="bold")
ax.set_xlabel("Week Number")
ax.set_ylabel("Number of Tickets")

# Tick every 4 weeks
tick_weeks = weekly["ISO_WEEK"][::4]
ax.set_xticks(tick_weeks)
ax.set_xticklabels(tick_weeks)

ax.legend(loc="upper left", framealpha=0.9)
ax.grid(True, linestyle=":", alpha=0.5)
plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_ytd_ticket_trend.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_ytd_ticket_trend.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()

# In[84]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

PRIMARY_BLUE = "#22489A"   # Billable
PRIMARY_GREEN = "#32B24B"  # Non billable

file_path = DATA_DIR / "sevicedesk" / "Year.xlsx"

# =========================
# HELPERS
# =========================
def norm(s):
    return re.sub(r'[\s_\-]+', '', str(s).strip().lower())

def safe_to_datetime(s):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return pd.to_datetime(s, errors="coerce")

def clean_headers(cols):
    return (
        cols.astype(str)
        .str.replace('\n', ' ', regex=False)
        .str.replace('\r', ' ', regex=False)
        .str.replace('\u00A0', ' ', regex=False)
        .str.strip()
    )

def auto_read_sheet_with_header(excel_path, sheet_name):
    raw = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, engine="openpyxl")
    if raw.empty:
        return pd.DataFrame(), None

    header_row = int(raw.notna().sum(axis=1).idxmax())
    df_local = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row, engine="openpyxl")

    df_local.columns = clean_headers(df_local.columns)
    df_local = df_local.loc[:, ~df_local.columns.astype(str).str.match(r"^Unnamed", case=False)]
    df_local = df_local.dropna(how="all")

    if df_local.shape[1] == 0:
        return pd.DataFrame(), header_row

    return df_local, header_row

# =========================
# 1) FIND BEST SHEET + HEADER ROW
# =========================
xl = pd.ExcelFile(file_path, engine="openpyxl")

best_sheet = None
best_df = None
best_header_row = None
best_score = -1

for sh in xl.sheet_names:
    temp_df, hr = auto_read_sheet_with_header(file_path, sh)
    if temp_df is None or temp_df.empty:
        continue
    score = (temp_df.shape[0] * 2) + (temp_df.shape[1] * 5)
    if score > best_score:
        best_score = score
        best_sheet = sh
        best_df = temp_df.copy()
        best_header_row = hr

if best_df is None or best_df.empty or best_df.shape[1] == 0:
    raise ValueError(
        "Could not find a sheet with usable data in Year.xlsx. "
        "Open the file and confirm the data is present and not all merged/blank."
    )

df = best_df.copy()


# =========================
# 2) AUTO-DETECT DATE COLUMN
# =========================
date_col = None
best_rate = -1
date_hints = ["created", "createddate", "createdtime", "date", "datetime", "time", "logged", "opened", "resolved"]

for c in df.columns:
    parsed = safe_to_datetime(df[c])
    rate = parsed.notna().mean()
    name_ok = any(h in norm(c) for h in date_hints)
    if name_ok and rate > best_rate:
        best_rate = rate
        date_col = c

if date_col is None or best_rate < 0.20:
    for c in df.columns:
        parsed = safe_to_datetime(df[c])
        rate = parsed.notna().mean()
        if rate > best_rate:
            best_rate = rate
            date_col = c

if date_col is None or best_rate < 0.20:
    raise ValueError(
        "Could not detect a date column reliably.\n"
        f"Columns: {df.columns.tolist()}"
    )

df["CREATED_DT"] = safe_to_datetime(df[date_col])
df = df.dropna(subset=["CREATED_DT"]).copy()


# =========================
# 3) FILTER YEAR 2026 + ISO WEEK
# =========================
df_2026 = df[df["CREATED_DT"].dt.year == 2026].copy()

if df_2026.empty:
    years_found = sorted(df["CREATED_DT"].dt.year.dropna().unique().tolist())
    raise ValueError(f"No rows found for year 2026. Years present: {years_found}")

iso = df_2026["CREATED_DT"].dt.isocalendar()
df_2026["ISO_WEEK"] = iso["week"].astype(int)

# =========================
# 4) AUTO-DETECT BILLING STATUS COLUMN
# =========================
billing_col = None

billing_hints = ["billing", "billable", "billingstatus", "billing status", "charge", "chargeable", "contractual"]
for c in df_2026.columns:
    if any(h in norm(c) for h in [norm(x) for x in billing_hints]):
        billing_col = c
        break

# fallback: find a text column with billable-ish values
if billing_col is None:
    bill_words = ["billable", "no billable", "non billable", "nonbillable", "non", "not", "contract", "contractual"]
    best_hits = -1
    best_col = None
    for c in df_2026.columns:
        if df_2026[c].dtype == "object" or str(df_2026[c].dtype).startswith("string"):
            s = df_2026[c].astype(str).str.lower()
            hits = int(s.apply(lambda x: any(w in x for w in bill_words)).sum())
            if hits > best_hits:
                best_hits = hits
                best_col = c
    billing_col = best_col

if billing_col is None:
    raise ValueError(
        "Could not detect a Billing Status column.\n"
        f"Columns: {df_2026.columns.tolist()}\n"
        "Tip: Make sure a billing column exists (e.g., Billing Status / Billable / Chargeable)."
    )

# Clean billing
df_2026["BILLING_CLEAN"] = (
    df_2026[billing_col]
    .astype(str)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
    .str.lower()
)


# =========================
# 5) CLASSIFY BILLABLE vs NON BILLABLE
# IMPORTANT: "no billable" => NON BILLABLE
# Contractual => BILLABLE
# =========================
non_billable_pattern = re.compile(
    r"(?:\bno\b\s*[- ]*\s*\bbillable\b)|"
    r"(?:\bnon\b\s*[- ]*\s*\bbillable\b)|"
    r"(?:\bnonbillable\b)|"
    r"(?:\bnot\b\s*\bbillable\b)|"
    r"(?:\bunbillable\b)",
    re.IGNORECASE
)

billable_pattern = re.compile(
    r"(?:\bbillable\b)|(?:\bcontract\b)|(?:\bcontractual\b)",
    re.IGNORECASE
)

def classify_billing(v: str) -> str:
    if not isinstance(v, str):
        return "NON BILLABLE"
    x = v.strip().lower()

    # 1) NON BILLABLE FIRST (so "no billable"/"non billable" doesn't become billable)
    if non_billable_pattern.search(x):
        return "NON BILLABLE"

    # 2) BILLABLE (Contractual counts here)
    if billable_pattern.search(x):
        return "BILLABLE"

    # 3) Default
    if x == "" or x == "nan":
        return "NON BILLABLE"

    return "NON BILLABLE"

df_2026["BILLING_GROUP"] = df_2026["BILLING_CLEAN"].apply(classify_billing)


# =========================
# 6) WEEKLY SPLIT TABLE
# =========================
weekly_split = (
    df_2026.groupby(["ISO_WEEK", "BILLING_GROUP"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
    .sort_values("ISO_WEEK")
)

# guarantee both columns exist
if "BILLABLE" not in weekly_split.columns:
    weekly_split["BILLABLE"] = 0
if "NON BILLABLE" not in weekly_split.columns:
    weekly_split["NON BILLABLE"] = 0


# =========================
# 7) TWO-LINE GRAPH (BRAND COLOURS)
# =========================
plt.figure(figsize=(16,6), dpi=120)

plt.plot(
    weekly_split["ISO_WEEK"],
    weekly_split["BILLABLE"],
    linewidth=2.8,
    marker="o",
    markersize=4.5,
    color=PRIMARY_GREEN,
    label="Billable (incl. Contractual)"
)

plt.plot(
    weekly_split["ISO_WEEK"],
    weekly_split["NON BILLABLE"],
    linewidth=2.8,
    marker="o",
    markersize=4.5,
    color=PRIMARY_BLUE,
    label="Non billable"
)

plt.title("Weekly Ticket Trend (2026) - Billable vs Non billable", fontsize=15, fontweight="bold")
plt.xlabel("Week Number")
plt.ylabel("Number of Tickets")

weeks = weekly_split["ISO_WEEK"].tolist()
plt.xticks(ticks=weeks[::4], labels=weeks[::4])

plt.grid(True, linestyle=":", alpha=0.5)
plt.legend()
plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_ytd_billing_split.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_ytd_billing_split.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[85]:


import warnings
import pandas as pd
import matplotlib.pyplot as plt
import re

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

file_path = DATA_DIR / "sevicedesk" / "Ticket.xlsx"

# =========================
# 1) LOAD EXCEL (auto header)
# =========================
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

df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)].copy()

def norm(s):
    return re.sub(r"[\s_\-]+", "", str(s).strip().lower())

# =========================
# 2) AUTO-DETECT CREATED TIME (for last 5 working days)
# =========================
date_col = None
best_rate = -1
for c in df.columns:
    parsed = pd.to_datetime(df[c], errors="coerce")
    rate = parsed.notna().mean()
    if any(k in norm(c) for k in ["created", "date", "time"]) and rate > best_rate:
        best_rate = rate
        date_col = c

# fallback: best parseable column
if date_col is None or best_rate < 0.30:
    for c in df.columns:
        parsed = pd.to_datetime(df[c], errors="coerce")
        rate = parsed.notna().mean()
        if rate > best_rate:
            best_rate = rate
            date_col = c
            best_rate = rate

if date_col is None or best_rate < 0.30:
    raise ValueError(f"Could not detect a date/time column. Columns: {df.columns.tolist()}")

df["created"] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=["created"]).copy()
df["date_only"] = df["created"].dt.normalize()

# =========================
# 3) FIND BILLING STATUS COLUMN
# =========================
billing_col = None
for c in df.columns:
    if "billingstatus" in norm(c):
        billing_col = c
        break

if billing_col is None:
    raise KeyError(
        "Billing Status column not found.\n"
        f"Columns found: {df.columns.tolist()}"
    )

# =========================
# 4) LAST 5 WORKING DAYS
# =========================
end_date = df["date_only"].max()
last_5_workdays = pd.bdate_range(end=end_date, periods=5)

df_5 = df[df["date_only"].isin(last_5_workdays)].copy()

# fallback if export skips days
if df_5.empty:
    df_5 = df[df["date_only"] >= (end_date - pd.Timedelta(days=7))].copy()

if df_5.empty:
    raise ValueError("No tickets found in the last 5 working days after parsing dates.")

billing = (
    df_5[billing_col]
    .astype(str)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
    .str.lower()
)

# =========================
# 5) CORRECT CLASSIFICATION (no overlap!)
# =========================
is_nonbillable = billing.str.contains(r"\bnon\s*-\s*billable\b|\bnon\s*billable\b|nonbillable", regex=True, na=False)

# Only check billable/contractual on rows that are NOT non-billable
is_billable = (~is_nonbillable) & billing.str.contains(r"\bcontractual\b|\bbillable\b", regex=True, na=False)

# Optional: anything else (blank/unknown)
is_unknown = ~(is_billable | is_nonbillable)

billable_count = int(is_billable.sum())
non_billable_count = int(is_nonbillable.sum())
unknown_count = int(is_unknown.sum())

total_count = int(len(df_5))

start_str = last_5_workdays.min().strftime("%b %d, %Y")
end_str   = last_5_workdays.max().strftime("%b %d, %Y")

# =========================
# 6) KPI TILES (pretty interface)
# =========================
BLUE  = "#22489A"
GREEN = "#32B24B"
DARK  = "#111827"
BORDER = "#E5E7EB"
AMBER = "#F59E0B"

fig, ax = plt.subplots(figsize=(12, 6), dpi=160)
ax.axis("off")

tiles = [
    ("Billable", billable_count, GREEN),          # Billable + Contractual
    ("Non-Billable", non_billable_count, BLUE),
    ("Total Tickets", total_count, DARK),
]

x_margin = 0.08
gap = 0.04
tile_w = (1 - 2*x_margin - 2*gap) / 3
tile_h = 0.52
y = 0.26

for i, (title, value, color) in enumerate(tiles):
    x = x_margin + i * (tile_w + gap)

    rect = plt.Rectangle(
        (x, y),
        tile_w,
        tile_h,
        transform=ax.transAxes,
        facecolor="white",
        edgecolor=BORDER,
        linewidth=1.6
    )
    ax.add_patch(rect)

    ax.text(
        x + tile_w/2,
        y + tile_h*0.72,
        title,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=color,
        transform=ax.transAxes
    )

    ax.text(
        x + tile_w/2,
        y + tile_h*0.35,
        f"{value}",
        ha="center",
        va="center",
        fontsize=52,
        fontweight="bold",
        color=color,
        transform=ax.transAxes
    )

ax.text(
    0.5, 0.12,
    f"Last 5 Working Days: {start_str} - {end_str}",
    ha="center",
    va="center",
    fontsize=12,
    fontweight="bold",
    color=BLUE,
    transform=ax.transAxes
)

plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_billing_kpi_tiles.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_billing_kpi_tiles.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[86]:


import warnings
import pandas as pd
import matplotlib.pyplot as plt
import re
import os

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

file_path = DATA_DIR / "sevicedesk" / "Ticket.xlsx"

# =========================
# LOAD EXCEL (auto-find header row)
# =========================
raw = pd.read_excel(file_path, header=None)

header_row_candidates = raw.index[
    raw.apply(lambda row: row.astype(str).str.lower().str.contains("request id", na=False).any(), axis=1)
].tolist()

header_row = int(header_row_candidates[0]) if header_row_candidates else int(raw.notna().sum(axis=1).idxmax())
df = pd.read_excel(file_path, header=header_row)

# Clean headers
df.columns = (
    df.columns.astype(str)
    .str.replace('\n', ' ', regex=False)
    .str.replace('\r', ' ', regex=False)
    .str.strip()
)

# Drop Unnamed columns
df = df.loc[:, ~df.columns.str.match(r"^Unnamed", case=False)]

# =========================
# FIND COLUMNS (robust)
# =========================
def norm(s: str) -> str:
    return re.sub(r'[\s_\-]+', '', str(s).strip().lower())

col_norm = {c: norm(c) for c in df.columns}

def find_col(*targets):
    targets = {norm(t) for t in targets}
    for c, n in col_norm.items():
        if n in targets:
            return c
    return None

created_col = find_col("Created Time", "Created_Time", "Created Date", "Created_Date", "Created")
worklog_col = find_col("Worklog Type", "Worklog_Type", "Billing Status", "Billing_Status")

if created_col is None:
    raise KeyError(f"Could not find Created Time column. Columns: {df.columns.tolist()}")
if worklog_col is None:
    raise KeyError(f"Could not find Worklog Type/Billing Status column. Columns: {df.columns.tolist()}")

df = df.rename(columns={created_col: "created_time", worklog_col: "worklog_type"})

# =========================
# PARSE CREATED TIME (robust)
# =========================
dt = pd.to_datetime(df["created_time"], errors="coerce")

# If many NaT, try dayfirst=True
if dt.isna().mean() > 0.30:
    dt2 = pd.to_datetime(df["created_time"], errors="coerce", dayfirst=True)
    dt = dt2 if dt2.isna().mean() < dt.isna().mean() else dt

df["created_time"] = dt
df = df.dropna(subset=["created_time"]).copy()

# Normalize worklog type
df["worklog_type"] = df["worklog_type"].astype(str).str.strip()
df["worklog_type_norm"] = df["worklog_type"].str.lower().str.strip()

# =========================
# AUTO-PICK THE LATEST MON-FRI WEEK IN THE DATA
# (Your file is 19-23 Jan 2026, so it will pick that)
# =========================
df["date_only"] = df["created_time"].dt.normalize()
end_date = df["date_only"].max()

# last 5 business days ending at end_date
week_days = pd.bdate_range(end=end_date, periods=5)

df_week = df[df["date_only"].isin(week_days)].copy()

# If still empty (rare), just use last 5 business days from end_date anyway
if df_week.empty:
    df_week = df[df["date_only"] >= week_days.min()].copy()

# =========================
# DAILY COUNTS
# =========================
billable_mask = df_week["worklog_type_norm"].isin(["billable", "contractual"])
nonbillable_mask = df_week["worklog_type_norm"].isin(["non-billable", "non billable", "nonbillable"])

billable_daily = (
    df_week[billable_mask]
    .groupby(df_week["date_only"])
    .size()
    .reindex(week_days, fill_value=0)
)

nonbillable_daily = (
    df_week[nonbillable_mask]
    .groupby(df_week["date_only"])
    .size()
    .reindex(week_days, fill_value=0)
)

# =========================
# PLOT: TWO GRAPHS
# =========================
fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=120)

# --- Billable per day ---
axes[0].plot(
    week_days, billable_daily.values,
    marker="o", linewidth=2,
    color="#32B24B",
    label="Billable (incl. Contractual)"
)
axes[0].set_title(
    f"Billable Volume per Day ",
    fontweight="bold", color="#22489A"
)
axes[0].set_xlabel("Day")
axes[0].set_ylabel("Tickets Count")
axes[0].grid(True, linestyle=":", alpha=0.6)
axes[0].legend(title="Worklog Type")

for x, y in zip(week_days, billable_daily.values):
    axes[0].text(x, y + 0.1, str(int(y)), ha="center", fontsize=9, fontweight="bold")

# --- Non-Billable per day ---
axes[1].plot(
    week_days, nonbillable_daily.values,
    marker="o", linewidth=2,
    color="#FF9800",
    label="Non-Billable"
)
axes[1].set_title(
    f"Non-Billable Volume per Day ",
    fontweight="bold", color="#22489A"
)
axes[1].set_xlabel("Day")
axes[1].set_ylabel("Tickets Count")
axes[1].grid(True, linestyle=":", alpha=0.6)
axes[1].legend(title="Worklog Type")

for x, y in zip(week_days, nonbillable_daily.values):
    axes[1].text(x, y + 0.1, str(int(y)), ha="center", fontsize=9, fontweight="bold")

# Nice x labels
for ax in axes:
    ax.set_xticks(week_days)
    ax.set_xticklabels([d.strftime("%a %d") for d in week_days], rotation=0)

plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_billable_daily_lines.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_billable_daily_lines.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[87]:


import pandas as pd
import matplotlib.pyplot as plt
import itertools

# =========================
# LOAD FROM SERVICE DESK API (worklogs)
# =========================
df = _sd_api.fetch_worklogs()

# =========================
# CLEAN HEADERS
# =========================
df.columns = (
    df.columns.astype(str)
    .str.replace('\n', ' ', regex=False)
    .str.replace('\r', ' ', regex=False)
    .str.strip()
)

# Normalize key column names (robust)
rename_map = {
    'Created Time': 'created_time',
    'Created date': 'created_time',
    'Created Date': 'created_time',
    'Time Spent': 'time_spent',
    'Worklog Type': 'worklog_type',
    'Work Log Type': 'worklog_type',
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

required = ['created_time', 'time_spent', 'worklog_type']
missing = [c for c in required if c not in df.columns]
if missing:
    raise KeyError(f"Missing columns: {missing}. Found columns: {df.columns.tolist()}")

# =========================
# PARSE DATES + HOURS
# =========================
df['created_time'] = pd.to_datetime(df['created_time'], errors='coerce')
df = df.dropna(subset=['created_time'])

df['time_spent_td'] = pd.to_timedelta(df['time_spent'].astype(str), errors='coerce')
df = df.dropna(subset=['time_spent_td'])

df['hours'] = df['time_spent_td'].dt.total_seconds() / 3600

# =========================
# FILTER: LAST 5 WORKING DAYS (DYNAMIC)
# =========================
df['date_only'] = df['created_time'].dt.normalize()
end_date = df['date_only'].max()
last_5_workdays = pd.bdate_range(end=end_date, periods=5)

df_range = df[df['date_only'].isin(last_5_workdays)].copy()

# =========================
# GROUP BY WORKLOG TYPE
# =========================
df_range['worklog_type'] = df_range['worklog_type'].astype(str).str.strip()

summary = df_range.groupby('worklog_type')['hours'].sum().sort_values(ascending=False)

if summary.empty:
    print("No data found in the last 5 working days.")
else:
    # =========================
    # COLOURS (YOUR MAIN BLUE/GREEN + DISTINCT OTHERS)
    # - Billable: Blue (#22489A)
    # - Contractual: Green (#32B24B)
    # - Non-Billable: distinct (not close to blue/green)
    # - Any other types: distinct cycle
    # =========================
    primary_blue = '#22489A'
    primary_green = '#32B24B'

    distinct_colors = [
        '#FFC107',  # amber
        '#FF6F61',  # coral/red
        '#8E44AD',  # purple
        '#FF9800',  # orange
        '#6D4C41',  # brown
        '#2C2C2C',  # dark grey
    ]

    # Flexible mapping based on type names (works with changing datasets)
    color_map = {}
    for k in summary.index:
        kl = k.lower()
        if 'billable' in kl and 'non' not in kl:
            color_map[k] = primary_blue
        elif 'contract' in kl:
            color_map[k] = '#FF9800'
        elif 'non' in kl and 'billable' in kl:
            color_map[k] = primary_green
        else:
            # assign later from distinct cycle
            pass

    cycle = itertools.cycle(distinct_colors)
    for k in summary.index:
        if k not in color_map:
            # ensure we don't accidentally reuse the same colors too much for the first few
            c = next(cycle)
            # avoid conflict with primary colors (even though these are distinct already)
            while c in {primary_blue, primary_green}:
                c = next(cycle)
            color_map[k] = c

    colors = [color_map[k] for k in summary.index]

    # =========================
    # PLOT (NICER + READABLE)
    # =========================
    start_date = last_5_workdays.min()

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=300)

    # ---- BAR CHART ----
    ax = axes[0]
    bars = ax.bar(summary.index, summary.values, color=colors, edgecolor='white', linewidth=0.8)

    ax.set_title(
        f"Total Time Spent by Worklog Type)",
        fontweight='bold', color=primary_blue
    )
    ax.set_xlabel("Worklog Type")
    ax.set_ylabel("Total Time Spent (hours)")

    ax.grid(axis='y', linestyle='--', alpha=0.25)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Rotate labels only if needed
    max_label_len = max(len(str(x)) for x in summary.index)
    ax.tick_params(axis='x', rotation=25 if max_label_len > 10 else 0)

    # Value labels (clean)
    y_max = max(summary.values.max(), 1)
    ax.set_ylim(0, y_max * 1.18)

    for b in bars:
        v = b.get_height()
        ax.text(
            b.get_x() + b.get_width() / 2,
            v + y_max * 0.02,
            f"{v:.2f}".rstrip('0').rstrip('.'),
            ha='center', va='bottom',
            fontweight='bold', fontsize=9, color='#111827'
        )

    # ---- PIE CHART ----
    ax2 = axes[1]
    wedges, texts, autotexts = ax2.pie(
        summary.values,
        labels=summary.index,
        autopct='%1.1f%%',
        startangle=70,
        colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    ax2.set_title("Distribution of Total Time Spent", fontweight='bold', color=primary_blue)

    # Improve autopct readability
    for t in autotexts:
        t.set_fontweight('bold')
        t.set_fontsize(9)
        t.set_color('white')

    # Optional: slightly smaller label text on pie if many categories
    for t in texts:
        t.set_fontsize(9)

    plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_worklog_bar_pie.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_worklog_bar_pie.png"
plt.savefig(_chart_path, dpi=300, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[ ]:





# In[ ]:


import pandas as pd
import re
import warnings
try:
    from IPython.display import display
except Exception:
    def display(*args, **kwargs):
        return None

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

file_path = DATA_DIR / "sevicedesk" / "Ticket.xlsx"

# =========================
# 1) READ EXCEL & AUTO HEADER
# =========================
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

def norm(s: str) -> str:
    return re.sub(r"[\s_\-]+", "", str(s).strip().lower())

norm_map = {norm(c): c for c in df.columns}

def pick(*names):
    for n in names:
        if norm(n) in norm_map:
            return norm_map[norm(n)]
    return None

# =========================
# 2) DETECT REQUIRED COLUMNS
# =========================
col_requestid = pick("RequestID", "Request Id", "REQUEST ID")
col_subject   = pick("Subject", "Request Title", "Title", "TICKET SUBJECT")
col_site      = pick("Site")
col_requester = pick("Requester", "Requested By", "Created By")
col_category  = pick("Category")
col_created   = pick("Created Time", "Created Date", "Created_Time", "Created")
col_billing   = pick("Billing Status", "Billing_Status", "BILLING STATUS")

missing = [k for k, v in {
    "RequestID": col_requestid,
    "Subject": col_subject,
    "Site": col_site,
    "Requester": col_requester,
    "Category": col_category,
    "Created_Time": col_created,
    "Billing_Status": col_billing
}.items() if v is None]

if missing:
    raise KeyError(f"Missing required columns: {missing}\nColumns found: {df.columns.tolist()}")

# =========================
# 3) CLEAN BILLING STATUS
# =========================
df["_billing_clean"] = (
    df[col_billing]
    .astype(str)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
    .str.lower()
)


tatenda_name = "Tatenda Chihota"

def style_table(final_table: pd.DataFrame):
    def highlight_summary(row):
        if str(row.get("RequestID", "")).startswith("Tatenda Chihota (TOTAL)"):
            return ["background-color: #ECFDF5; font-weight: 600;"] * len(row)
        return [""] * len(row)

    return (
        final_table.style
        .apply(highlight_summary, axis=1)
        .set_table_styles([
            {"selector": "th", "props": "background-color: #F9FAFB; font-weight: 600;"},
            {"selector": "td", "props": "border: 1px solid #E5E7EB; padding: 6px;"},
            {"selector": "table", "props": "border-collapse: collapse; width: 100%;"},
        ])
    )

# =========================
# BILLABLE TABLE (WITH Tatenda TOTAL)
# =========================
df_billable = df[df["_billing_clean"].eq("billable")].copy()

print("BILLABLE TICKETS")
print("---------------")

if df_billable.empty:
    print("No tickets found for Billing Status = BILLABLE")
else:
    requester_clean = (
        df_billable[col_requester]
        .astype(str)
        .str.replace("\u00A0", " ", regex=False)
        .str.strip()
    )

    is_tatenda = requester_clean.str.lower().eq(tatenda_name.lower())
    tatenda_total = int(is_tatenda.sum())

    others_billable = df_billable.loc[~is_tatenda, [
        col_requestid, col_subject, col_site, col_requester, col_category, col_created, col_billing
    ]].copy()

    others_billable[col_created] = pd.to_datetime(others_billable[col_created], errors="coerce")
    others_billable = others_billable.sort_values(by=col_created, ascending=False)

    tatenda_row = pd.DataFrame([{
        col_requestid: "Tatenda Chihota (TOTAL)",
        col_subject: f"{tatenda_total} ticket(s)",
        col_site: "",
        col_requester: tatenda_name,
        col_category: "",
        col_created: "",
        col_billing: "Billable"
    }])

    final_billable = pd.concat([tatenda_row, others_billable], ignore_index=True)

    final_billable = final_billable.rename(columns={
        col_requestid: "RequestID",
        col_subject: "Subject",
        col_site: "Site",
        col_requester: "Requester",
        col_category: "Category",
        col_created: "Created_Time",
        col_billing: "Billing_Status"
    })

    display(style_table(final_billable))

# =========================
# CONTRACTUAL TABLE (NO Tatenda TOTAL SECTION)
# =========================
df_contractual = df[df["_billing_clean"].eq("contractual")].copy()

print("\nCONTRACTUAL TICKETS")
print("-------------------")

if df_contractual.empty:
    print("No tickets found for Billing Status = CONTRACTUAL")
else:
    contractual_table = df_contractual[[
        col_requestid, col_subject, col_site, col_requester, col_category, col_created, col_billing
    ]].copy()

    contractual_table[col_created] = pd.to_datetime(contractual_table[col_created], errors="coerce")
    contractual_table = contractual_table.sort_values(by=col_created, ascending=False)

    contractual_table = contractual_table.rename(columns={
        col_requestid: "RequestID",
        col_subject: "Subject",
        col_site: "Site",
        col_requester: "Requester",
        col_category: "Category",
        col_created: "Created_Time",
        col_billing: "Billing_Status"
    })

    display(style_table(contractual_table))

# ── Save billing tables as images for PPT ──────────────────────────────────
import subprocess as _sp

def _styler_to_png(styler_obj, png_name):
    """Save a pandas Styler as PNG using wkhtmltoimage, with matplotlib fallback."""
    _html_p = AERP14_TABLE_DIR / f"{png_name}.html"
    _png_p  = AERP14_CHART_DIR / f"{png_name}.png"
    # Write HTML
    with open(_html_p, "w", encoding="utf-8") as _f:
        _f.write(styler_obj.to_html())
    # Try wkhtmltoimage
    try:
        _r = _sp.run(
            ["wkhtmltoimage", "--width", "1400", "--quality", "92", "--zoom", "1.3",
             str(_html_p), str(_png_p)],
            capture_output=True, timeout=30
        )
        if _png_p.exists() and _png_p.stat().st_size > 5000:
            print(f"  [OK] {png_name}.png saved via wkhtmltoimage")
            return
    except Exception: pass
    # Fallback: render table as matplotlib figure
    import matplotlib.pyplot as _plt
    import pandas as _pd
    _df = styler_obj.data if hasattr(styler_obj, 'data') else styler_obj
    _fig, _ax = _plt.subplots(figsize=(18, max(3, len(_df) * 0.45 + 1.2)))
    _ax.axis("off")
    _tbl = _ax.table(
        cellText=_df.values,
        colLabels=_df.columns,
        cellLoc="center", loc="center"
    )
    _tbl.auto_set_font_size(False)
    _tbl.set_fontsize(9)
    _tbl.auto_set_column_width(col=list(range(len(_df.columns))))
    for (_r, _c), _cell in _tbl.get_celld().items():
        if _r == 0:
            _cell.set_facecolor("#22489A")
            _cell.set_text_props(color="white", fontweight="bold")
        elif _r % 2 == 0:
            _cell.set_facecolor("#F7F7F7")
    _plt.tight_layout()
    _plt.savefig(_png_p, dpi=150, bbox_inches="tight")
    _plt.close(_fig)
    print(f"  [OK] {png_name}.png saved via matplotlib fallback")

if not df_billable.empty:
    _styler_to_png(style_table(final_billable), "table_billable")
if not df_contractual.empty:
    _styler_to_png(style_table(contractual_table), "table_contractual")


# In[89]:


import warnings
import pandas as pd
import matplotlib.pyplot as plt
import re
import itertools

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

file_path = DATA_DIR / "sevicedesk" / "Survey.xlsx"

# =========================================================
# 1) LOAD EXCEL (auto-detect header row)
# =========================================================
raw = pd.read_excel(file_path, header=None)
header_row = int(raw.notna().sum(axis=1).idxmax())
df = pd.read_excel(file_path, header=header_row)

# Clean headers
df.columns = (
    df.columns.astype(str)
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
)

# Drop "Unnamed" columns
df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)].copy()

def norm(s: str) -> str:
    return re.sub(r"[\s_\-]+", "", str(s).strip().lower())

# =========================================================
# 2) AUTO-DETECT DATE COLUMN (for week/year)
# =========================================================
date_col = None
best_rate = -1

name_hints = ["date", "time", "created", "submitted", "timestamp", "response"]

for c in df.columns:
    parsed = pd.to_datetime(df[c], errors="coerce")
    rate = parsed.notna().mean()
    if rate > best_rate and any(h in norm(c) for h in name_hints):
        best_rate = rate
        date_col = c

# fallback: choose the most parseable column overall
if date_col is None or best_rate < 0.30:
    for c in df.columns:
        parsed = pd.to_datetime(df[c], errors="coerce")
        rate = parsed.notna().mean()
        if rate > best_rate:
            best_rate = rate
            date_col = c

if date_col is None or best_rate < 0.30:
    raise ValueError(
        "Could not detect a usable date/time column in Survey.xlsx.\n"
        f"Columns found: {df.columns.tolist()}"
    )

df["dt"] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=["dt"]).copy()

# ISO week/year
iso = df["dt"].dt.isocalendar()
df["year"] = iso.year.astype(int)
df["week"] = iso.week.astype(int)

# =========================================================
# 3) COUNT RESPONSES PER WEEK (each row = 1 response)
# =========================================================
weekly = (
    df.groupby(["year", "week"])
      .size()
      .reset_index(name="count")
)

# pivot for plotting (weeks 1..51 like your image)
weeks = list(range(1, 52))
pivot = (
    weekly.pivot(index="week", columns="year", values="count")
          .reindex(weeks)
          .fillna(0)
)

# =========================================================
# 4) PICK "CURRENT WEEK" LINE (red dashed)
# - If today's week is close to the latest week in the latest year, use today.
# - Otherwise, use (max week in latest year + 1) to mimic your screenshot.
# =========================================================
latest_year = int(df["year"].max())
max_week_in_latest_year = int(df.loc[df["year"] == latest_year, "week"].max())

today = pd.Timestamp.today()
today_iso = today.isocalendar()
today_year = int(today_iso.year)
today_week = int(today_iso.week)

if today_year == latest_year and abs(today_week - max_week_in_latest_year) <= 3:
    current_week_line = today_week
else:
    current_week_line = min(max_week_in_latest_year + 1, 51)

# =========================================================
# 5) PLOT (matches style in your screenshot)
# =========================================================
fig, ax = plt.subplots(figsize=(16, 4), dpi=150)

# Colors: make 2026 (or first year) blue like your image
years = list(pivot.columns)
palette = itertools.cycle(["#22489A", "#9467bd", "#2ca02c", "#e377c2", "#ff7f0e", "#8c564b"])
year_colors = {y: next(palette) for y in years}
if 2026 in year_colors:
    year_colors[2026] = "#22489A"

# Bar width handling for multiple years
n_years = max(len(years), 1)
bar_total_width = 0.80
bar_w = bar_total_width / n_years
x = pd.Series(pivot.index, index=pivot.index).values  # weeks

for i, y in enumerate(years):
    offset = (i - (n_years - 1) / 2) * bar_w
    ax.bar(
        x + offset,
        pivot[y].values,
        width=bar_w * 0.95,
        label=str(y),
        color=year_colors[y],
        edgecolor="white",
        linewidth=0.6
    )

# Green target line at 1
ax.axhline(1, color="green", linestyle="--", linewidth=2)

# Red "current week" vertical line
ax.axvline(current_week_line, color="red", linestyle="--", linewidth=2.5)

# Titles/labels
ax.set_title("Survey Response per Week", fontweight="bold", fontsize=16)
ax.set_xlabel("Week")
ax.set_ylabel("count")

ax.set_xlim(1, 51)
ax.set_xticks(range(1, 52, 2))

ax.grid(axis="y", linestyle=":", alpha=0.35)
ax.set_axisbelow(True)

ax.legend(title="Year", loc="lower right", frameon=True)

plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_survey_weekly.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_survey_weekly.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode


# In[89]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import timedelta
from pathlib import Path
import os

PRIMARY_BLUE  = "#22489A"
PRIMARY_GREEN = "#32B24B"
WHITE         = "#FFFFFF"
LIGHT_GREY    = "#F4F6FB"
MID_GREY      = "#D0D7E8"
TEXT_DARK     = "#1A1A2E"
EPIC_BG       = "#EEF2FB"

STATUS_COLORS = {
    "Done":        "#32B24B",
    "In Progress": "#F59E0B",
    "To Do":       "#22489A",
}

ISSUE_TYPE_COLORS = {
    "Epic":    "#7B5EA7",
    "Task":    "#22489A",
    "Subtask": "#0EA5E9",
}

def _read_jira_data(file_path):
    """Load DataFrame from Excel (.xlsx/.xls) or CSV file with path/extension fallback."""
    p = Path(file_path)
    if not p.exists():
        alt_xlsx = p.with_suffix(".xlsx")
        alt_csv  = p.with_suffix(".csv")
        if alt_xlsx.exists():
            p = alt_xlsx
        elif alt_csv.exists():
            p = alt_csv
        elif p.parent.exists():
            for f in p.parent.iterdir():
                if f.stem.lower() == p.stem.lower() and f.suffix.lower() in [".xlsx", ".xls", ".csv"]:
                    p = f
                    break

    if not p.exists():
        raise FileNotFoundError(f"Jira data file not found: {file_path}")

    if p.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(p)

    try:
        df = pd.read_csv(p, encoding="utf-8-sig")
    except pd.errors.ParserError:
        df = pd.read_csv(p, encoding="utf-8-sig", engine="python", on_bad_lines="skip")
    if df.shape[1] == 1 and "\t" in str(df.columns[0]):
        df = pd.read_csv(p, sep="\t", encoding="utf-8-sig", engine="python", on_bad_lines="skip")
    return df

def plot_jira_file(file_path, output_folder, title, filename):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)

    df = _read_jira_data(file_path)

    lower_cols   = {str(c).strip().lower(): c for c in df.columns}
    updated_col  = lower_cols.get("updated") or lower_cols.get("updated date") or lower_cols.get("last updated")
    issue_col    = lower_cols.get("issue key") or lower_cols.get("issuekey")
    summary_col  = lower_cols.get("summary")
    assignee_col = lower_cols.get("assignee")
    status_col   = lower_cols.get("status")
    type_col     = lower_cols.get("issue type") or lower_cols.get("issuetype") or lower_cols.get("type")

    required = {
        "Updated":   updated_col,
        "Issue key": issue_col,
        "Summary":   summary_col,
        "Assignee":  assignee_col,
        "Status":    status_col,
    }
    missing = [k for k, v in required.items() if v is None]
    if missing:
        raise KeyError(f"Missing required Jira columns: {missing}. Found columns: {df.columns.tolist()}")

    df[updated_col] = pd.to_datetime(df[updated_col], dayfirst=True, errors="coerce")
    cutoff = pd.Timestamp.now().floor("D") - timedelta(days=5)

    has_type  = type_col is not None
    keep_cols = ([type_col] if has_type else []) + [issue_col, summary_col, assignee_col, status_col]
    new_names = (["Issue Type"] if has_type else []) + ["Issue key", "Summary", "Assignee", "Status"]

    df_f = (
        df[df[updated_col] >= cutoff][keep_cols]
        .reset_index(drop=True)
    )
    df_f.columns = new_names

    if df_f.empty:
        fig, ax = plt.subplots(figsize=(10, 3), facecolor=WHITE)
        ax.text(0.5, 0.5, "No updates in the last 5 days",
                ha="center", va="center",
                fontsize=14, fontweight="bold", color=TEXT_DARK,
                fontfamily="DejaVu Sans")
        ax.axis("off")
        plt.savefig(output_path, bbox_inches="tight", dpi=150)
        plt.close()
        print(f"Placeholder saved: {output_path}")
        return

    n_rows   = len(df_f)
    ROW_H    = 0.52
    HEADER_H = 0.70
    TITLE_H  = 0.80
    FOOTER_H = 0.30
    fig_h    = TITLE_H + HEADER_H + n_rows * ROW_H + FOOTER_H
    fig_w    = 16 if has_type else 15

    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=WHITE)

    title_ax = fig.add_axes([0, 1 - TITLE_H / fig_h, 1, TITLE_H / fig_h])
    title_ax.set_facecolor(PRIMARY_BLUE)
    title_ax.axis("off")
    title_ax.text(0.5, 0.5, title, ha="center", va="center",
                  fontsize=17, fontweight="bold", color=WHITE,
                  fontfamily="DejaVu Sans")

    table_top = 1 - TITLE_H / fig_h
    table_ax  = fig.add_axes([0.01, FOOTER_H / fig_h, 0.98, table_top - FOOTER_H / fig_h])
    table_ax.axis("off")

    if has_type:
        cols   = ["Type", "Issue Key", "Summary", "Assignee", "Status"]
        col_ws = [0.08,    0.10,        0.44,       0.22,       0.12  ]
    else:
        cols   = ["Issue Key", "Summary", "Assignee", "Status"]
        col_ws = [0.11,         0.48,       0.22,       0.13  ]

    total_rows = n_rows + 1
    row_h_norm = 1 / total_rows

    def draw_cell(ax, row, col, text, bg, fg=TEXT_DARK,
                  bold=False, fontsize=10, align="left", pad=0.012):
        x = sum(col_ws[:col])
        y = 1 - (row + 1) * row_h_norm
        w = col_ws[col]
        h = row_h_norm
        rect = patches.FancyBboxPatch(
            (x + 0.002, y + 0.003), w - 0.004, h - 0.006,
            boxstyle="round,pad=0.005", linewidth=0,
            facecolor=bg, edgecolor="none",
            transform=ax.transAxes, clip_on=False
        )
        ax.add_patch(rect)
        ha = "center" if align == "center" else "left"
        tx = x + pad if align == "left" else x + w / 2
        ax.text(tx, y + h / 2, str(text), ha=ha, va="center",
                fontsize=fontsize, fontweight="bold" if bold else "normal",
                color=fg, fontfamily="DejaVu Sans",
                transform=ax.transAxes, clip_on=False)

    for ci, col_name in enumerate(cols):
        draw_cell(table_ax, 0, ci, col_name.upper(), PRIMARY_BLUE, WHITE, True, 10, "center")

    for ri, row_data in enumerate(df_f.values.tolist()):
        if has_type:
            issue_type = str(row_data[0]) if pd.notna(row_data[0]) else "Task"
            is_epic    = issue_type.lower() == "epic"
            row_bg     = EPIC_BG if is_epic else (WHITE if ri % 2 == 0 else LIGHT_GREY)
            data_cells = row_data[1:]
            col_offset = 1
        else:
            issue_type = None
            is_epic    = False
            row_bg     = WHITE if ri % 2 == 0 else LIGHT_GREY
            data_cells = row_data
            col_offset = 0

        if has_type:
            badge_color = ISSUE_TYPE_COLORS.get(issue_type, MID_GREY)
            draw_cell(table_ax, ri + 1, 0, issue_type,
                      badge_color, WHITE, True, 8, "center")

        for ci, cell_val in enumerate(data_cells):
            col_idx   = ci + col_offset
            cell_text = str(cell_val) if pd.notna(cell_val) else "-"

            if ci == 1:
                max_len = 65 if has_type else 72
                if len(cell_text) > max_len:
                    cell_text = cell_text[:max_len - 3] + "…"
                indent = 0.012 if is_epic else 0.025
                draw_cell(table_ax, ri + 1, col_idx, cell_text,
                          row_bg, TEXT_DARK, is_epic, 9.5, "left", pad=indent)

            elif ci == 3:
                draw_cell(table_ax, ri + 1, col_idx, cell_text,
                          STATUS_COLORS.get(cell_text, MID_GREY), WHITE, True, 9, "center")

            else:
                draw_cell(table_ax, ri + 1, col_idx, cell_text,
                          row_bg, TEXT_DARK, False, 9.5, "left")

    footer_ax = fig.add_axes([0, 0, 1, FOOTER_H / fig_h])
    footer_ax.set_facecolor(PRIMARY_GREEN)
    footer_ax.axis("off")

    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved: {output_path}")


output_folder = str(AERP14_CHART_DIR)
hpa_csv       = str(DATA_DIR / "jira" / "hpa.csv" if (DATA_DIR / "jira" / "hpa.csv").exists() else DATA_DIR / "jira" / "HPA.csv")

plot_jira_file(hpa_csv, output_folder, "HPA Tasks (Last 5 Days)", "hpa_tasks.png")


# In[90]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import timedelta
from pathlib import Path
import os

PRIMARY_BLUE  = "#22489A"
PRIMARY_GREEN = "#32B24B"
WHITE         = "#FFFFFF"
LIGHT_GREY    = "#F4F6FB"
MID_GREY      = "#D0D7E8"
TEXT_DARK     = "#1A1A2E"
EPIC_BG       = "#EEF2FB"

STATUS_COLORS = {
    "Done":        "#32B24B",
    "In Progress": "#F59E0B",
    "To Do":       "#22489A",
}

ISSUE_TYPE_COLORS = {
    "Epic":    "#7B5EA7",
    "Task":    "#22489A",
    "Subtask": "#0EA5E9",
}

output_folder = str(AERP14_CHART_DIR)
Automation_csv = str(DATA_DIR / "jira" / "Automation.csv")

plot_jira_file(Automation_csv, output_folder, "Automation Tasks (Last 5 Days)", "automation_tasks.png")


# In[91]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import timedelta
from pathlib import Path
import os

PRIMARY_BLUE  = "#22489A"
PRIMARY_GREEN = "#32B24B"
WHITE         = "#FFFFFF"
LIGHT_GREY    = "#F4F6FB"
MID_GREY      = "#D0D7E8"
TEXT_DARK     = "#1A1A2E"
EPIC_BG       = "#EEF2FB"

STATUS_COLORS = {
    "Done":        "#32B24B",
    "In Progress": "#F59E0B",
    "To Do":       "#22489A",
}

ISSUE_TYPE_COLORS = {
    "Epic":    "#7B5EA7",
    "Task":    "#22489A",
    "Subtask": "#0EA5E9",
}

output_folder = str(AERP14_CHART_DIR)
Website_csv   = str(DATA_DIR / "jira" / "Website.csv")

plot_jira_file(Website_csv, output_folder, "Website Tasks (Last 5 Days)", "Website_tasks.png")


# In[92]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

# Data now comes from the HubSpot API (RFQs = HubSpot tickets)
from fetchers import hubspot as _hubspot_fetcher

try:
    _chart_path = AERP14_CHART_DIR / "chart_rfq_weekly_volume.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_rfq_weekly_volume.png"

def _empty_graph():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_facecolor("#FFFFFF")
    ax.bar(["Mon", "Tue", "Wed", "Thu", "Fri"], [0, 0, 0, 0, 0],
           color="#32B24B", width=0.55)
    ax.set_title("Weekly RFQ Volume", fontweight="bold")
    ax.set_xlabel("Day")
    ax.set_ylabel("RFQ Count")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.text(0.5, 0.55, "No RFQs received this week",
            ha="center", va="center", transform=ax.transAxes,
            fontsize=13, color="#999999", style="italic")
    plt.tight_layout()
    plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
    plt.show()
    plt.close("all")
    print(f"Empty placeholder saved: {_chart_path}")

def norm(s):
    return re.sub(r'[\s_\-]+', '', str(s).lower())

try:
    # =========================
    # 1) DATA FROM HUBSPOT API (RFQs = HubSpot tickets)
    # =========================
    df = _hubspot_fetcher.fetch_rfqs()

    # =========================
    # 2) AUTO-DETECT CREATED DATE COLUMN
    # =========================
    date_col = None
    best_rate = -1

    for c in df.columns:
        parsed = pd.to_datetime(df[c], errors="coerce")
        rate = parsed.notna().mean()
        if rate > best_rate and any(k in norm(c) for k in ["created", "date", "time"]):
            best_rate = rate
            date_col = c

    if date_col is None:
        for c in df.columns:
            parsed = pd.to_datetime(df[c], errors="coerce")
            rate = parsed.notna().mean()
            if rate > best_rate:
                best_rate = rate
                date_col = c

    if best_rate < 0.5 or date_col is None:
        raise ValueError("No date column")

    df["created"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["created"])

    if df.empty:
        raise ValueError("No data")

    # =========================
    # 3) AUTO-DETECT STATUS COLUMN
    # =========================
    status_col = next((c for c in df.columns if "status" in c.lower()), None)

    if status_col is None:
        pattern = r"(open|closed|pending|on\s*hold|approved|rejected)"
        best_col, best_score = None, -1
        for c in df.columns:
            s = df[c].astype(str).str.lower()
            score = s.str.contains(pattern, regex=True, na=False).mean()
            if score > best_score:
                best_col, best_score = c, score
        if best_score <= 0:
            raise ValueError("No status column")
        status_col = best_col

    df["status_clean"] = (
        df[status_col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # =========================
    # 4) FILTER LATEST WEEK (ISO)
    # =========================
    iso = df["created"].dt.isocalendar()
    df["iso_week"] = iso.week.astype(int)
    df["iso_year"] = iso.year.astype(int)

    year = df["iso_year"].max()
    week = df[df["iso_year"] == year]["iso_week"].max()

    df_week = df[(df["iso_week"] == week) & (df["iso_year"] == year)].copy()

    if df_week.empty:
        raise ValueError("No data this week")

    # =========================
    # 5) RFQ VOLUME (JUST THIS WEEK)
    # =========================
    daily_counts = (
        df_week
        .groupby(df_week["created"].dt.strftime("%a"))
        .size()
        .reindex(["Mon", "Tue", "Wed", "Thu", "Fri"], fill_value=0)
    )

    plt.figure(figsize=(10, 4))
    plt.bar(
        daily_counts.index,
        daily_counts.values,
        color="#32B24B",
        width=0.55
    )

    for i, v in enumerate(daily_counts.values):
        plt.text(i, v + 0.1, str(v), ha="center", fontweight="bold")

    plt.title("Weekly RFQ Volume", fontweight="bold")
    plt.xlabel("Day")
    plt.ylabel("RFQ Count")
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
    plt.show()
    plt.close("all")
    plt.close()
    print(f"Saved: {_chart_path}")

except Exception:
    _empty_graph()
# In[93]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings
import os
import shutil
import tempfile

warnings.filterwarnings("ignore")

# =========================
# SETTINGS
# =========================
TARGET_YEAR = 2026

PRIMARY_BLUE = "#22489A"
PRIMARY_GREEN = "#32B24B"

# =========================
# DATA FROM HUBSPOT API (RFQs = HubSpot tickets)
# =========================
rfq = _hubspot_fetcher.fetch_rfqs()
rfq["RFQ_DATE"] = pd.to_datetime(rfq["Created Date"], errors="coerce")
rfq = rfq.dropna(subset=["RFQ_DATE"]).copy()

# =========================
# 3) WEEKLY COUNTS (ISO)
# =========================
iso = rfq["RFQ_DATE"].dt.isocalendar()
rfq["ISO_WEEK"] = iso.week.astype(int)
rfq["ISO_YEAR"] = iso.year.astype(int)

rfq = rfq[rfq["ISO_YEAR"] == TARGET_YEAR]

weekly_counts = (
    rfq.groupby("ISO_WEEK")
    .size()
    .reindex(range(1, 54), fill_value=0)
)

# =========================
# 4) LINE GRAPH (CLEAN)
# =========================
plt.figure(figsize=(16, 4.8), dpi=130)

plt.plot(
    weekly_counts.index,
    weekly_counts.values,
    linewidth=3,
    color=PRIMARY_GREEN
)

plt.title(f"{TARGET_YEAR} RFQs - Count per Week", fontsize=18, fontweight="bold", color=PRIMARY_BLUE)
plt.xlabel(f"Week ({TARGET_YEAR})", fontsize=12)
plt.ylabel("Number of RFQs", fontsize=12)

plt.xticks(range(1, 54, 2))  # reduce clutter
plt.grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_ytd_rfq_line.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_ytd_rfq_line.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import warnings
import os
import shutil
import tempfile

warnings.filterwarnings("ignore")

# =========================
# SETTINGS
# =========================
# [COMPLETE] RFQ years to include up to 2026
MIN_YEAR = 2022
MAX_YEAR = 2026

# Brand colours (+ extras)
PRIMARY_BLUE = "#22489A"
PRIMARY_GREEN = "#32B24B"
ACCENTS = ["#5DADE2", "#AF7AC5", "#F39C12", "#32B24B", "#22489A", "#E74C3C", "#48C9B0", "#7F8C8D"]

# =========================
# DATA FROM HUBSPOT API (RFQs = HubSpot tickets)
# =========================
rfq_dates = pd.to_datetime(_hubspot_fetcher.fetch_rfqs()["Created Date"], errors="coerce").dropna()
rfq_dates = rfq_dates[
    (rfq_dates.dt.year >= MIN_YEAR) & (rfq_dates.dt.year <= MAX_YEAR)
]

rfqs = pd.DataFrame({
    "YEAR": rfq_dates.dt.year.astype(int),
    "QUARTER": rfq_dates.dt.quarter.astype(int),
})

# =========================
# 2) RFQ COUNT BY YEAR & QUARTER
# =========================
pivot = (
    rfqs.groupby(["YEAR", "QUARTER"])
    .size()
    .reset_index(name="RFQ COUNT")
    .pivot(index="QUARTER", columns="YEAR", values="RFQ COUNT")
    .fillna(0)
)

# Ensure only 2022..2026 in that exact order
pivot = pivot.reindex(columns=list(range(MIN_YEAR, MAX_YEAR + 1)), fill_value=0)

# Ensure quarters 1..4 exist
for q in [1, 2, 3, 4]:
    if q not in pivot.index:
        pivot.loc[q] = 0
pivot = pivot.sort_index()

display(pivot)

# =========================
# 3) GROUPED BAR CHART
# =========================
years = pivot.columns.tolist()
quarters = pivot.index.tolist()

x = np.arange(len(quarters))
bar_width = 0.18 if len(years) <= 5 else 0.14  # 2022..2026 = 5 bars per quarter

plt.figure(figsize=(14, 7), dpi=120)

for i, year in enumerate(years):
    offset = (i - (len(years) - 1) / 2) * bar_width
    bars = plt.bar(
        x + offset,
        pivot[year].values,
        width=bar_width,
        color=ACCENTS[i % len(ACCENTS)],
        label=str(year),
        edgecolor="white",
        linewidth=0.6
    )

    # Value labels
    for b in bars:
        h = b.get_height()
        if h > 0:
            plt.text(
                b.get_x() + b.get_width() / 2,
                h,
                f"{int(h)}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold"
            )

plt.title("RFQs Count by Quarter and Year ", fontsize=16, fontweight="bold")
plt.xlabel("Quarter")
plt.ylabel("RFQ Count")
plt.xticks(x, [str(q) for q in quarters])
plt.grid(axis="y", linestyle=":", alpha=0.5)

# Optional benchmark line (average count)
plt.axhline(pivot.values.mean(), linestyle="--", linewidth=1.6, color=PRIMARY_GREEN, alpha=0.85)

plt.legend(title="Year", loc="upper left")
plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_rfq_by_quarter_multiyear.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path(".") / "chart_rfq_by_quarter_multiyear.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import warnings
import os
import shutil
import tempfile

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

# =========================
# BRAND COLOURS
# =========================
PRIMARY_BLUE = "#22489A"
PRIMARY_GREEN = "#32B24B"
ACCENTS = ["#5DADE2", "#AF7AC5", "#F39C12","#32B24B","#22489A", "#E74C3C", "#48C9B0"]

# =========================
# DATA FROM HUBSPOT API (Sales = HubSpot deals)
# =========================
sales = _hubspot_fetcher.fetch_sales()
sales["SALE_DATE"] = pd.to_datetime(sales["SALE_DATE"], errors="coerce", utc=True)
sales["UNITS_SOLD"] = pd.to_numeric(sales["UNITS_SOLD"], errors="coerce")
sales = sales.dropna(subset=["SALE_DATE", "UNITS_SOLD"]).copy()
sales = sales[sales["UNITS_SOLD"] > 0]      # safety
sales = sales[sales["UNITS_SOLD"] < 10000]  # sanity cap

sales["YEAR"] = sales["SALE_DATE"].dt.year
sales["QUARTER"] = sales["SALE_DATE"].dt.quarter

# =========================
# 2) AGGREGATE: UNITS BY YEAR & QUARTER
# =========================
pivot = (
    sales.groupby(["YEAR", "QUARTER"])["UNITS_SOLD"]
    .sum()
    .reset_index()
    .pivot(index="QUARTER", columns="YEAR", values="UNITS_SOLD")
    .fillna(0)
    .sort_index()
)

display(pivot)

# =========================
# 3) GROUPED BAR CHART (LIKE YOUR IMAGE)
# =========================
years = pivot.columns.tolist()
quarters = pivot.index.tolist()

x = np.arange(len(quarters))
bar_width = 0.18

plt.figure(figsize=(14,7), dpi=120)

# Map year colors dynamically: latest year gets PRIMARY_BLUE, previous year gets PRIMARY_GREEN
sorted_years = sorted(years)
max_yr = max(sorted_years) if sorted_years else 2026
older_colors = ["#94A3B8", "#5DADE2", "#AF7AC5", "#F39C12", "#E74C3C"]

year_color_map = {}
for yr in sorted_years:
    if yr == max_yr:
        year_color_map[yr] = PRIMARY_BLUE       # Latest year (2026) -> Primary Blue
    elif yr == max_yr - 1:
        year_color_map[yr] = PRIMARY_GREEN      # Previous year (2025) -> Primary Green
    else:
        # Earlier historical years (2022, 2023, 2024)
        offset = max_yr - 2 - yr
        idx = max(0, offset) % len(older_colors)
        year_color_map[yr] = older_colors[idx]

for i, year in enumerate(years):
    offset = (i - (len(years) - 1) / 2) * bar_width
    bars = plt.bar(
        x + offset,
        pivot[year],
        width=bar_width,
        color=year_color_map.get(year, PRIMARY_BLUE),
        label=str(year),
        edgecolor="white"
    )

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                h,
                f"{int(h)}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold"
            )

plt.title(
    "Units Sold by Quarter and Year",
    fontsize=16,
    fontweight="bold"
)
plt.xlabel("Quarter")
plt.ylabel("Units Sold")
plt.xticks(x, quarters)
plt.grid(axis="y", linestyle=":", alpha=0.5)

# Optional benchmark line
plt.axhline(pivot.values.mean(), linestyle="--", color=PRIMARY_GREEN, alpha=0.8)

plt.legend(title="Year")
plt.tight_layout()

try:
    _chart_path = AERP14_CHART_DIR / "chart_units_sold_by_quarter.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path(".") / "chart_units_sold_by_quarter.png"
plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
plt.close("all")  # headless mode
plt.close()


# In[96]:


import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings
import os
import shutil
import tempfile

warnings.filterwarnings("ignore")

# =========================
# SETTINGS
# =========================
SOURCE_FILE = DATA_DIR / "hubspot" / "HW Sales.xlsx"
TARGET_YEAR = 2026

# Brand colours
BLUE = "#22489A"
GREEN = "#32B24B"

# =========================
# SAFETY COPY (OneDrive locks)
# =========================
tmp_file = os.path.join(tempfile.gettempdir(), "HW_Sales_TEMP.xlsx")
shutil.copy2(SOURCE_FILE, tmp_file)
file_path = tmp_file

# =========================
# HELPERS
# =========================
def norm(s):
    return re.sub(r"[\s_\-]+", "", str(s).strip().lower())

def clean_headers(cols):
    return (
        cols.astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace("\u00A0", " ", regex=False)
        .str.strip()
    )

def safe_datetime(col):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return pd.to_datetime(col, errors="coerce")

def auto_header_read(path, sheet_name):
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None, engine="openpyxl")
    if raw.empty:
        return pd.DataFrame()
    header_row = int(raw.notna().sum(axis=1).idxmax())
    df = pd.read_excel(path, sheet_name=sheet_name, header=header_row, engine="openpyxl")
    df.columns = clean_headers(df.columns)
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)]
    df = df.dropna(how="all")
    return df

def detect_date_col(df):
    hints = ["salesdate","sale date","date","orderdate","created","created date","datetime","time"]
    best_col, best_rate = None, -1

    for c in df.columns:
        parsed = safe_datetime(df[c])
        rate = parsed.notna().mean()
        name_ok = any(norm(h) in norm(c) for h in hints)
        if name_ok and rate > best_rate:
            best_col, best_rate = c, rate

    if best_col is None or best_rate < 0.20:
        for c in df.columns:
            parsed = safe_datetime(df[c])
            rate = parsed.notna().mean()
            if rate > best_rate:
                best_col, best_rate = c, rate

    return best_col, best_rate

def find_comments_col(df):
    # You said: comments column holds "Quotation"
    candidates = ["comment", "comments", "remark", "remarks", "note", "notes", "description", "details"]
    for c in df.columns:
        if any(norm(x) in norm(c) for x in candidates):
            return c
    return None

def valid_year_dates(dt):
    return dt[(dt.notna()) & (dt.dt.year >= 2022) & (dt.dt.year <= TARGET_YEAR)]

# =========================
# 1) DATA FROM HUBSPOT API (Sales = HubSpot deals)
# =========================
sales_yr = _hubspot_fetcher.fetch_sales()
sales_yr["SALE_DATE"] = pd.to_datetime(sales_yr["SALE_DATE"], errors="coerce")
sales_yr = sales_yr.dropna(subset=["SALE_DATE"]).copy()

TARGET_YEAR_ACTUAL = TARGET_YEAR
sales_yr_sub = sales_yr[sales_yr["SALE_DATE"].dt.year == TARGET_YEAR].copy()
if sales_yr_sub.empty and not sales_yr.empty:
    latest_avail = int(sales_yr["SALE_DATE"].dt.year.max())
    print(f"  Note: No sales found for {TARGET_YEAR}, using latest available year ({latest_avail})")
    TARGET_YEAR_ACTUAL = latest_avail
    sales_yr_sub = sales_yr[sales_yr["SALE_DATE"].dt.year == latest_avail].copy()

sales_yr = sales_yr_sub

# Quotation-conversion signal comes from the fetcher (deal went through the
# "Quotation/ Proposal Sent" stage) and is surfaced via the COMMENTS column.
sales_yr["HAS_QUOTATION_COMMENT"] = (
    sales_yr["COMMENTS"].astype(str)
    .str.replace("\u00A0", " ", regex=False)
    .str.strip()
    .str.lower()
    .str.contains(r"\bquotation\b", na=False)
)

try:
    _chart_path = AERP14_CHART_DIR / "chart_sales_conversion_pie.png"
except NameError:
    import pathlib; _chart_path = pathlib.Path("charts") / "chart_sales_conversion_pie.png"

if sales_yr.empty:
    print(f"  Note: No sales rows found for year {TARGET_YEAR}.")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    ax.text(0.5, 0.5, f"No sales data available for {TARGET_YEAR}",
            ha="center", va="center", fontsize=14, color="#333333")
    ax.axis("off")
    plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
    plt.close("all")
else:
    converted = int(sales_yr["HAS_QUOTATION_COMMENT"].sum())
    total_sales = int(len(sales_yr))
    no_sale_after_quote = max(0, total_sales - converted)

    sizes = [converted, no_sale_after_quote]
    labels = ["Converted to Sales (Quotation)", "No Sale After Quotation"]
    colors = [BLUE, GREEN]

    plt.figure(figsize=(10, 6), dpi=120)
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
        startangle=140,
        colors=colors,
        textprops={"fontsize": 11}
    )

    plt.title(f"Sales Conversion Rate from Quotation/{TARGET_YEAR_ACTUAL}", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(_chart_path, dpi=200, bbox_inches="tight")
    plt.close("all")


# In[97]:


# =========================================================
# AERP-16 FINALIZE / SAVE MANIFEST
# Add this as the LAST CELL in the notebook
# =========================================================
manifest_df = pd.DataFrame(_aerp16_manifest).drop_duplicates()
manifest_df.to_csv(MANIFEST_CSV, index=False)

print("\nAERP-16 run complete.")
print(f"Manifest saved to: {MANIFEST_CSV}")
print(f"Total saved items: {len(manifest_df)}")

manifest_df


# In[98]:


# =========================================================
# AERP-14 FINALIZE / SAVE MANIFEST
# Add this as the LAST CELL in the notebook
# =========================================================
manifest_df = pd.DataFrame(_aerp14_manifest).drop_duplicates()
manifest_df.to_csv(MANIFEST_CSV, index=False)

print("\nAERP-14 run complete.")
print(f"Manifest saved to: {MANIFEST_CSV}")
print(f"Total saved items: {len(manifest_df)}")

manifest_df


# In[99]:


# ── DIAGNOSTIC: list all saved chart/table files ──────────
from pathlib import Path
import pandas as pd

print("=== CHARTS ===")
for p in sorted(AERP14_CHART_DIR.glob("*.png")):
    print(f"  {p.name}")

print("=== TABLES (HTML) ===")
for p in sorted(AERP14_TABLE_DIR.glob("*.html")):
    print(f"  {p.name}")

print("=== TABLES (PNG) ===")
for p in sorted((AERP14_TABLE_DIR / "png").glob("*.png")):
    print(f"  {p.name}")


# In[ ]:


# =========================================================
# AERP-10  PPT GENERATOR  - ZHD TEMPLATE (title-based, v5)
# Finds each slide by its TITLE so slide order/count
# in the template does not matter.
# =========================================================

import re, subprocess, sys
import datetime as dt
from pathlib import Path

def _ensure(pkg, import_as=None):
    import importlib
    try: return importlib.import_module(import_as or pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
        return importlib.import_module(import_as or pkg)

_ensure("python-pptx", "pptx")
_ensure("Pillow", "PIL")

from pptx import Presentation
from pptx.util import Emu
from pptx.oxml.ns import qn
from PIL import Image as PILImage

# ─── PATHS ────────────────────────────────────────────────
_SEARCH_ROOT = PROJECT_ROOT

def _find_template(root):
    for folder in [root, root.parent, Path(".")]:
        if not folder.exists(): continue
        for p in sorted(folder.glob("*.pptx")):
            if any(k in p.name.lower() for k in ["zhd", "template"]):
                return p
    return None

TEMPLATE_PATH = _find_template(_SEARCH_ROOT)
if TEMPLATE_PATH is None:
    raise FileNotFoundError(
        "Cannot find ZHD template .pptx\n"
        f"Searched: {_SEARCH_ROOT}\n"
        "Place ZHD_Weekly_Ops_Review_Template.pptx in that folder."
    )
print(f"Template: {TEMPLATE_PATH.name}")

RUN_DATE = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
PPT_PATH = AERP14_BASE_DIR / f"ZHD_Weekly_Ops_{RUN_DATE}.pptx"
C = AERP14_CHART_DIR

# ─── HELPERS ──────────────────────────────────────────────
def _exact(name):
    p = C / name
    return p if p.exists() else None

def _latest(pattern):
    """Newest file matching glob pattern in chart dir."""
    hits = sorted(C.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return hits[0] if hits else None

def _html_to_png(stem):
    """Convert named HTML table → PNG via wkhtmltoimage with matplotlib chart fallback."""
    TMP = AERP14_BASE_DIR / "tmp_imgs"
    TMP.mkdir(exist_ok=True)
    out = TMP / f"{stem}.png"
    if out.exists() and out.stat().st_size > 0:
        return out
    chart_fb = AERP14_CHART_DIR / f"{stem}.png"
    if chart_fb.exists() and chart_fb.stat().st_size > 0:
        return chart_fb
    # look for html in table dir
    html_hits = sorted(AERP14_TABLE_DIR.glob(f"{stem}*.html"),
                       key=lambda p: p.stat().st_mtime, reverse=True)
    if not html_hits:
        # fallback: time-ordered styled_table files
        all_html = sorted(AERP14_TABLE_DIR.glob("styled_table_*.html"),
                          key=lambda p: p.stat().st_mtime)
        idx = {"table_billable": 0, "table_contractual": 1}.get(stem, 0)
        html_hits = [all_html[idx]] if idx < len(all_html) else []
    if not html_hits:
        print(f"  [WARN]  No HTML found for {stem}")
        return None
    try:
        subprocess.run(
            ["wkhtmltoimage", "--width", "1400", "--quality", "92", "--zoom", "1.3",
             str(html_hits[0]), str(out)],
            capture_output=True, timeout=30
        )
        if out.exists() and out.stat().st_size > 0:
            print(f"  [OK]  {stem} → PNG")
            return out
    except Exception as e:
        print(f"  [WARN]  wkhtmltoimage: {e}")
    return None

def _replace_pic(slide, pic_index, img_path):
    """Replace pic by index using direct spTree children, preserving image aspect ratio and centering within placeholder bounds."""
    sp_tree = slide.shapes._spTree
    pics = [c for c in sp_tree if c.tag.endswith("}pic") or c.tag == qn("p:pic")]
    if pic_index >= len(pics):
        raise IndexError(f"Slide has {len(pics)} pic(s); asked for [{pic_index}]")
    old = pics[pic_index]
    xfrm = old.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm")
    off  = xfrm.find("{http://schemas.openxmlformats.org/drawingml/2006/main}off")
    ext  = xfrm.find("{http://schemas.openxmlformats.org/drawingml/2006/main}ext")
    x  = int(off.get("x")); y  = int(off.get("y"))
    cx = int(ext.get("cx")); cy = int(ext.get("cy"))

    # Preserve aspect ratio to prevent image distortion & blurriness
    try:
        with PILImage.open(str(img_path)) as img:
            img_w, img_h = img.size
        if img_w > 0 and img_h > 0 and cx > 0 and cy > 0:
            img_aspect = img_w / img_h
            box_aspect = cx / cy
            if img_aspect > box_aspect:
                # Image is wider than box -> fit width
                new_w = cx
                new_h = int(cx / img_aspect)
                new_x = x
                new_y = y + int((cy - new_h) / 2)
            else:
                # Image is taller than box -> fit height
                new_h = cy
                new_w = int(cy * img_aspect)
                new_y = y
                new_x = x + int((cx - new_w) / 2)
        else:
            new_x, new_y, new_w, new_h = x, y, cx, cy
    except Exception:
        new_x, new_y, new_w, new_h = x, y, cx, cy

    new_shape = slide.shapes.add_picture(str(img_path), Emu(new_x), Emu(new_y), Emu(new_w), Emu(new_h))
    new_elem  = new_shape._element
    sp_tree.remove(new_elem)
    pos = list(sp_tree).index(old)
    sp_tree.remove(old)
    sp_tree.insert(pos, new_elem)

def _find_slide(prs, title_fragment, exclude=None):
    """Return slide whose TITLE contains title_fragment (case-insensitive).
    Only checks text shapes in the top 25% of the slide to avoid matching
    agenda bullet text on the Agenda slide.
    If exclude is given, skip slides whose title contains that string."""
    frag = title_fragment.lower().strip()
    excl = exclude.lower().strip() if exclude else None
    slide_h = prs.slide_height
    for slide in prs.slides:
        for sh in slide.shapes:
            if not sh.has_text_frame: continue
            top = sh.top if sh.top is not None else 9999999
            if top > slide_h * 0.25: continue
            t = sh.text_frame.text.strip().lower()
            if frag in t:
                if excl and excl in t:
                    continue
                return slide
    return None

# ─── ASSET MAP ────────────────────────────────────────────
# Each value: explicit name first, then numbered-chart fallback, then None
# Numbered chart fallback order (from AERP wrapper execution order):
#   chart_001 = ticket_volume_daily   chart_002 = ticket_kpi_tiles
#   chart_003 = tickets_opened_closed  chart_004 = tickets_by_date
#   chart_005 = tickets_by_site        chart_006 = ytd_ticket_trend
#   chart_007 = ytd_billing_split      chart_008 = billing_kpi_tiles
#   chart_009 = billable_daily_lines   chart_010 = worklog_bar_pie
#   chart_011 = survey_weekly          chart_012 = automation_tasks (dup)
#   chart_013 = Website_tasks (dup)    chart_014 = rfq_weekly_volume
#   chart_015 = ytd_rfq_line           chart_016 = rfq_by_quarter_multiyear
#   chart_017 = units_sold_by_quarter  chart_018 = sales_conversion_pie (dup)

def _asset(name, fallback_glob=None):
    p = _exact(name)
    if p: return p
    if fallback_glob:
        return _latest(fallback_glob)
    return None


def _stack_v(*paths, gap=20):
    """Stack multiple images vertically, return path to combined PNG."""
    from PIL import Image as _PIL
    valid = [p for p in paths if p and Path(p).exists()]
    if not valid: return None
    if len(valid) == 1: return valid[0]
    imgs = [_PIL.open(p).convert("RGB") for p in valid]
    w = max(i.width for i in imgs)
    h = sum(i.height for i in imgs) + gap * (len(imgs)-1)
    canvas = _PIL.new("RGB", (w, h), (255,255,255))
    y = 0
    for im in imgs:
        canvas.paste(im, ((w - im.width)//2, y))
        y += im.height + gap
    out = AERP14_BASE_DIR / "tmp_imgs" / ("stacked_" + "_".join(Path(p).stem for p in valid[:2]) + ".png")
    out.parent.mkdir(exist_ok=True)
    canvas.save(out, dpi=(150,150))
    return out

ASSETS = {
    # Slide: Ticket Review - Volume & Closure Rate
    "s3_topleft_bar":      _asset("chart_ticket_volume_daily.png",   "chart_001_*.png"),
    "s3_topright_small":   _asset("chart_ticket_kpi_tiles.png",      "chart_002_*.png"),
    "s3_bottom_line":      _asset("chart_tickets_opened_closed.png", "chart_003_*.png"),
    # Slide: Ticket Review - In Queue (single chart only)
    "s4_inqueue":          _asset("chart_tickets_by_date.png",       "chart_004_*.png"),
    # Slide: Ticket Review - In Queue (legacy slot, kept for fallback matching)
    "s5_inqueue":          _asset("chart_tickets_by_date.png",       "chart_004_*.png"),
    # Slide: Ticket Review - Last 7 Days
    "s6_last7days":        _asset("chart_tickets_by_site.png",       "chart_005_*.png"),
    # Slide: Tickets - Weekly Tracking
    "s7_top_trend":        _asset("chart_ytd_ticket_trend.png",      "chart_006_*.png"),
    "s7_bot_opened":       _asset("chart_ytd_billing_split.png",     "chart_007_*.png"),
    # Slide: Billing Status - Weekly & Worklogs
    "s8_kpi_small":        _asset("chart_billing_kpi_tiles.png",     "chart_008_*.png"),
    "s8_billable_lines":   _asset("chart_billable_daily_lines.png",  "chart_009_*.png"),
    "s8_worklog_bar":      _stack_v(
                                _asset("chart_worklog_bar_pie.png",       "chart_010_*.png"),
                                _asset("chart_ytd_billing_split.png",    "chart_007_*.png"),
                                _asset("chart_billable_daily_lines.png", "chart_009_*.png"),
                            ),
    # Slide: Billing Status - Last Week & Worklogs
    "s9_worklog":          _asset("chart_worklog_bar_pie.png",       "chart_010_*.png"),
    # Slide: Billing Status - Last Week  (pic[2] and pic[3] - skipping tiny icons at 0,1)
    "s10_billable_tbl":    _exact("table_billable.png") or _html_to_png("table_billable"),
    "s10_contractual_tbl": _exact("table_contractual.png") or _html_to_png("table_contractual"),
    # Slide: Survey
    "s11_survey":          _asset("chart_survey_weekly.png",         "chart_011_*.png"),
    # Slide: Projects & Tasks-SE
    "s12_se_tasks":        _asset("automation_tasks.png",            "chart_012_*.png"),
    # Slide: Projects & Tasks-DS
    "s13_ds_tasks":        _asset("hpa_tasks.png",                   "chart_013_*.png"),
    # Slide: RFQ Review
    "s14_rfq_weekly":      _asset("chart_rfq_weekly_volume.png",     "chart_014_*.png"),
    # Slide: Sales Review
    "s15_top_rfq_line":    _asset("chart_ytd_rfq_line.png",          "chart_015_*.png"),
    "s15_bot_rfq_bar":     _asset("chart_rfq_by_quarter_multiyear.png", "chart_016_*.png"),
    # Slide: Product Sales
    "s16_units_bar":       _asset("chart_units_sold_by_quarter.png", "chart_01[78]_*.png"),
    "s16_conv_pie":        _asset("chart_sales_conversion_pie.png",  "chart_018_*.png"),
}

missing = [k for k, v in ASSETS.items() if v is None]
if missing:
    print(f"\n[WARN]  Missing assets: {missing}")
else:
    print(f"\n[COMPLETE]  All {len(ASSETS)} assets resolved")

# ─── TITLE-BASED SLIDE MAP ────────────────────────────────
# Format: (title_fragment, pic_index, asset_key)
# title_fragment matched case-insensitively against slide title text
TITLE_SLIDE_MAP = [
    # Ticket Review - Volume & Closure Rate  (3 slots, XML order: topright, topleft, bottom)
    ("Volume &Closure Rate",     0, "s3_topright_small"),
    ("Volume &Closure Rate",     1, "s3_topleft_bar"),
    ("Volume &Closure Rate",     2, "s3_bottom_line"),
    # Ticket Review - In Queue (single chart only)
    ("In Queue",                 0, "s4_inqueue"),
    # Ticket Review - Last 7 Days
    ("Last 7 Days",              0, "s6_last7days"),
    # Tickets - Weekly Tracking
    ("Weekly Tracking",          0, "s7_top_trend"),
    ("Weekly Tracking",          1, "s7_bot_opened"),
    # Billing Status - Weekly & Worklogs
    ("Weekly &Worklogs",         0, "s8_kpi_small"),
    ("Weekly &Worklogs",         1, "s8_billable_lines"),
    # slots [2] and [3] merged into slot [1] via _stack_v above
    # Billing Status - Last Week & Worklogs
    ("Last Week &Worklogs",      0, "s9_worklog"),
    # Billing Status - Last Week (tiny icons at 0,1 are skipped; real slots at 2,3)
    ("Status-Last Week",         2, "s10_billable_tbl"),
    ("Status-Last Week",         3, "s10_contractual_tbl"),
    # Survey
    ("Survey",                   0, "s11_survey"),
    # Projects & Tasks SE
    ("Tasks-SE",                 0, "s12_se_tasks"),
    # Projects & Tasks DS
    ("Tasks-DS",                 0, "s13_ds_tasks"),
    # RFQ Review
    ("RFQ Review",               0, "s14_rfq_weekly"),
    # Sales Review
    ("Sales Review",             0, "s15_top_rfq_line"),
    ("Sales Review",             1, "s15_bot_rfq_bar"),
    # Product Sales
    ("Product Sales",            0, "s16_units_bar"),
    ("Product Sales",            1, "s16_conv_pie"),
]

# ─── BUILD ────────────────────────────────────────────────
prs = Presentation(str(TEMPLATE_PATH))

# Update date on cover slide (date of next Tuesday)
_today = dt.datetime.now()
_days_until_tuesday = (1 - _today.weekday()) % 7
if _days_until_tuesday == 0:
    _days_until_tuesday = 7
_next_tuesday = _today + dt.timedelta(days=_days_until_tuesday)
next_tuesday_str = _next_tuesday.strftime("%d %B %Y").lstrip("0")

for shape in prs.slides[0].shapes:
    if shape.has_text_frame:
        for para in shape.text_frame.paragraphs:
            full = "".join(r.text for r in para.runs)
            if re.search(r'\d{1,2}\s+\w+\s+\d{4}', full) and para.runs:
                para.runs[0].text = next_tuesday_str
                for r in para.runs[1:]: r.text = ""
                break

filled = skipped = 0
_slide_cache = {}   # cache title→slide to avoid repeated scans

for title_frag, pic_idx, asset_key in TITLE_SLIDE_MAP:
    # Find slide (cached)
    if title_frag not in _slide_cache:
        # For "Status-Last Week", exclude slides that also contain "Worklogs"
        _excl = "worklogs" if title_frag == "Status-Last Week" else None
        _slide_cache[title_frag] = _find_slide(prs, title_frag, exclude=_excl)
    slide = _slide_cache[title_frag]

    if slide is None:
        print(f"  -  No slide matching '{title_frag}' (skipped)")
        skipped += 1
        continue

    img = ASSETS.get(asset_key)
    if img is None:
        slide_num = list(prs.slides).index(slide) + 1
        print(f"  -  Slide {slide_num} '{title_frag}'[{pic_idx}] ({asset_key}): asset missing")
        skipped += 1
        continue

    slide_num = list(prs.slides).index(slide) + 1
    try:
        _replace_pic(slide, pic_idx, img)
        print(f"  [OK]  Slide {slide_num} '{title_frag[:30]}'[{pic_idx}] ← {Path(img).name}")
        filled += 1
    except Exception as e:
        print(f"  [FAIL]  Slide {slide_num} '{title_frag}'[{pic_idx}] ({asset_key}): {e}")
        skipped += 1

prs.save(str(PPT_PATH))
print(f"\n{'='*60}")
print(f"Saved → {PPT_PATH}")
print(f"Filled: {filled}  |  Skipped: {skipped}")
print("ZHD WEEKLY OPS REPORT COMPLETE [COMPLETE]")

try:
    from store_report import archive_pipeline_run
    archive_pipeline_run(pptx_path=PPT_PATH)
except Exception as _arch_err:
    print(f"Note: Dashboard auto-archive ({_arch_err})")



# In[102]:


import smtplib
from email.message import EmailMessage

def send_email():
    try:
        smtp_server = os.environ.get("SMTP_SERVER", "").strip()
        raw_port = os.environ.get("SMTP_PORT", "").strip()
        smtp_port = int(raw_port) if raw_port.isdigit() else 587
        smtp_user = os.environ.get("SMTP_USER", "").strip()
        smtp_password = os.environ.get("SMTP_PASSWORD", "").strip()
        email_to = os.environ.get("EMAIL_TO", "tafara@zhdconsulting.com").strip()

        if not (smtp_server and smtp_user and smtp_password):
            print("\nNote: SMTP credentials not configured (SMTP_SERVER, SMTP_USER, SMTP_PASSWORD). Skipping email send.")
            print(f"Generated presentation saved locally: {PPT_PATH}")
            return

        msg = EmailMessage()
        msg["Subject"] = "Weekly Operations Report"
        msg["From"] = smtp_user
        msg["To"] = email_to
        msg.set_content("Please find attached the latest Weekly Operations Report.")

        if PPT_PATH.exists():
            with open(PPT_PATH, "rb") as f:
                data = f.read()
            msg.add_attachment(data, maintype="application", subtype="vnd.openxmlformats-officedocument.presentationml.presentation", filename=PPT_PATH.name)

        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.ehlo()
            if smtp_port != 25:
                server.starttls()
                server.ehlo()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"  [OK] Report successfully sent to {email_to} via SMTP")
    except Exception as e:
        print(f"  [WARN] Failed to send email via SMTP: {e}")

send_email()


# In[ ]:




