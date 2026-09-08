"""
Fetchers package for ZHD Automation Pipeline.
Provides data-fetching layers with live API connectivity and local fallback support.
"""

from . import service_desk
from . import hubspot
from . import jira

__all__ = ["service_desk", "hubspot", "jira"]

