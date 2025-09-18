"""Issue monitoring for EZVIZ Patched integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.issue_registry import (
    IssueSeverity,
    async_create_issue,
    async_delete_issue,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ISSUE_URL = "https://api.github.com/repos/home-assistant/core/issues/151648"
ISSUE_ID = "ezviz_patched_temporary_fix"
CHECK_INTERVAL = 24 * 60 * 60  # Check once per day


async def check_issue_status(hass: HomeAssistant) -> None:
    """Check if the GitHub issue is still open."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ISSUE_URL) as response:
                if response.status == 200:
                    issue_data = await response.json()
                    is_closed = issue_data.get("state") == "closed"

                    if is_closed:
                        # Issue is closed, update the repair to recommend removal
                        await update_repair_for_closed_issue(hass)
                    else:
                        # Issue is still open, create/update repair
                        await create_repair_for_open_issue(hass)

    except Exception as e:
        _LOGGER.warning("Failed to check issue status: %s", e)


async def create_repair_for_open_issue(hass: HomeAssistant) -> None:
    """Create repair for open issue."""
    async_create_issue(
        hass,
        DOMAIN,
        ISSUE_ID,
        severity=IssueSeverity.INFO,
        translation_key="temporary_fix_active",
        translation_placeholders={
            "issue_url": "https://github.com/home-assistant/core/issues/151648",
            "issue_title": "EZVIZ sensors unavailable (KeyError: 'mode')",
        },
    )


async def update_repair_for_closed_issue(hass: HomeAssistant) -> None:
    """Update repair for closed issue."""
    async_create_issue(
        hass,
        DOMAIN,
        ISSUE_ID,
        severity=IssueSeverity.WARNING,
        translation_key="issue_closed_remove_component",
        translation_placeholders={
            "issue_url": "https://github.com/home-assistant/core/issues/151648",
            "issue_title": "EZVIZ sensors unavailable (KeyError: 'mode') - RESOLVED",
        },
    )


async def start_issue_monitoring(hass: HomeAssistant) -> None:
    """Start monitoring the GitHub issue status."""

    async def periodic_check():
        while True:
            try:
                await check_issue_status(hass)
                await asyncio.sleep(CHECK_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as e:
                _LOGGER.error("Error in issue monitoring: %s", e)
                await asyncio.sleep(CHECK_INTERVAL)

    # Start the monitoring task
    task = hass.async_create_task(periodic_check())

    # Store the task so it can be cancelled if needed
    if not hasattr(hass.data, "ezviz_patched_tasks"):
        hass.data["ezviz_patched_tasks"] = []
    hass.data["ezviz_patched_tasks"].append(task)
