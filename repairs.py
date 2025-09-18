"""Repairs platform for EZVIZ Patched integration."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.issue_registry import (
    IssueSeverity,
    async_create_issue,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ISSUE_ID = "ezviz_patched_temporary_fix"
ISSUE_URL = "https://github.com/home-assistant/core/issues/151648"


async def async_create_fixes(hass: HomeAssistant) -> None:
    """Create repairs for EZVIZ Patched."""
    _LOGGER.info("Creating EZVIZ Patched repair issue")
    
    # Create the issue
    async_create_issue(
        hass,
        DOMAIN,
        ISSUE_ID,
        is_fixable=False,
        is_persistent=False,
        severity=IssueSeverity.WARNING,
        issue_domain=DOMAIN,
        breaks_in_ha_version="2025.9.0",
        translation_key="temporary_fix_active",
        translation_placeholders={
            "issue_url": ISSUE_URL,
        },
    )
    
    _LOGGER.info("EZVIZ Patched repair issue created successfully")