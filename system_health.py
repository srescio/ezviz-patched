"""System health check for EZVIZ Patched integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ISSUE_URL = "https://github.com/home-assistant/core/issues/151648"
PR_URL = "https://github.com/home-assistant/core/pull/151848"


@callback
def async_register(
    hass: HomeAssistant, register: system_health.SystemHealthRegistration
) -> None:
    """Register system health callbacks."""
    register.async_register_info(ezviz_patched_system_health)


async def ezviz_patched_system_health(hass: HomeAssistant) -> dict[str, Any]:
    """Get EZVIZ Patched system health."""
    info = {
        "component": "EZVIZ Patched",
        "version": "2025.9.0-patched",
    }

    # Check if this is a custom component override
    try:
        # Try to import the custom component
        import custom_components.ezviz

        info["status"] = "Custom component override active"
        info["override"] = True
    except ImportError:
        info["status"] = "Built-in component active"
        info["override"] = False

    # Add issue information
    info["fixed_issue"] = {
        "url": ISSUE_URL,
        "title": "EZVIZ integration - most sensors are unavailable after update to 2025.9.0",
        "pr_url": PR_URL,
        "pr_title": "Fix issue #151648 - Add mode sensor type",
    }

    # Add recommendation
    if info.get("override", False):
        info["recommendation"] = (
            "This custom component fixes issue #151648. "
            "Once the official fix is merged and released in Home Assistant core, "
            "you should remove this custom component to use the official integration."
        )

    return info
