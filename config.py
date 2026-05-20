"""
Configuration — constants and config file loader.
"""

import json
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────
CONFIG_FILE        = "config.json"
PAGE_TIMEOUT       = 30_000   # ms — first navigation attempt
PAGE_TIMEOUT_RETRY = 60_000   # ms — single retry after timeout
PAGE_SETTLE_MS     = 2_000    # ms — wait after domcontentloaded for JS to render
API_CONCURRENCY    = 20       # max concurrent Greenhouse API requests

# ── ATS platform registry — single source of truth for all ATS integrations ──
PLATFORM_REGISTRY: dict[str, dict] = {
    "greenhouse": {
        "hosts":   {"job-boards.greenhouse.io", "job-boards.eu.greenhouse.io"},
        "api_url": "https://boards-api.greenhouse.io/v1/boards/{token}/jobs",
    },
    "ashby": {
        "hosts":   {"jobs.ashbyhq.com"},
        "api_url": "https://api.ashbyhq.com/posting-api/job-board/{token}",
    },
    "lever": {
        "hosts":   {"jobs.lever.co"},
        "api_url": "https://api.lever.co/v0/postings/{token}?mode=json",
    },
    "workable": {
        "hosts":   {"apply.workable.com"},
        "api_url": "https://apply.workable.com/api/v1/widget/accounts/{token}",
    },
    "gem": {
        "hosts":   {"jobs.gem.com"},
        "api_url": "https://api.gem.com/job_board/v0/{token}/job_posts/",
    },
}

CONFIG_DEFAULTS = {
    "concurrency":        5,
    "companies_file":     "data/companies.csv",
    "titles_file":        "data/sqa_titles.csv",
    "output_file":        "data/match.csv",
    "schedule_times":     ["08:08", "13:13", "18:18"],
    "log_dir":              "logs",
    "log_retention_days":   30,
    "logging_enabled":      True,
    "notifications_enabled": True,
    "filters": {"enabled": True, "countries": [], "states": [], "city": "", "remote_only": False, "full_time_only": False},
}


def load_config() -> dict:
    """
    Load config.json and merge with defaults.
    Any key missing from the file falls back to CONFIG_DEFAULTS.
    """
    path = Path(CONFIG_FILE)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return {**CONFIG_DEFAULTS, **json.load(f)}
    return dict(CONFIG_DEFAULTS)
