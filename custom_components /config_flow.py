from __future__ import annotations

from homeassistant import config_entries
from .const import DOMAIN

from typing import Any

import voluptuous as vol

from homeassistant import data_entry_flow

class CclConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, str] | None = None):

        def __init__(self) -> None:
            """Initialize the config flow."""
            self.data_schema = vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("unique_id"): str,
                }
            )

        if user_input is not None:
            return self.async_create_entry(
                title = "Title of the entry",
                data = user_input
                )

        errors={}
        
        return self.async_show_form(
            step_id="user", data_schema=self.data_schema, errors=errors
        )
