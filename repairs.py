"""Repairs platform for EZVIZ Patched integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.repairs import RepairsFlow, confirm_reissue_step
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.issue_registry import (
    IssueSeverity,
    async_create_issue,
    async_delete_issue,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ISSUE_ID = "ezviz_patched_temporary_fix"
ISSUE_URL = "https://github.com/home-assistant/core/issues/151648"


async def async_create_fixes(hass: HomeAssistant) -> None:
    """Create repairs for EZVIZ Patched."""
    # Check if we're using the custom component
    try:
        import custom_components.ezviz

        is_custom_component = True
    except ImportError:
        is_custom_component = False

    if is_custom_component:
        async_create_issue(
            hass,
            DOMAIN,
            ISSUE_ID,
            severity=IssueSeverity.INFO,
            translation_key="temporary_fix_active",
            translation_placeholders={
                "issue_url": ISSUE_URL,
                "issue_title": "EZVIZ sensors unavailable (KeyError: 'mode')",
            },
        )


async def async_delete_fixes(hass: HomeAssistant) -> None:
    """Delete repairs for EZVIZ Patched."""
    async_delete_issue(hass, DOMAIN, ISSUE_ID)


class EzvizPatchedRepairsFlow(RepairsFlow):
    """Handler for EZVIZ Patched repairs."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        return await self.async_step_confirm_remove()

    async def async_step_confirm_remove(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the confirmation step."""
        if user_input is not None:
            if user_input.get("remove_component"):
                # User wants to remove the custom component
                return self.async_create_entry(
                    title="Remove EZVIZ Patched",
                    data={"action": "remove_component"},
                )
            else:
                # User wants to keep the component
                return self.async_create_entry(
                    title="Keep EZVIZ Patched",
                    data={"action": "keep_component"},
                )

        return self.async_show_form(
            step_id="confirm_remove",
            data_schema=self.add_suggested_values_to_schema(
                {},
                {
                    "remove_component": False,
                },
            ),
            description_placeholders={
                "issue_url": ISSUE_URL,
                "issue_title": "EZVIZ sensors unavailable (KeyError: 'mode')",
            },
        )
