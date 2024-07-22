"""Config flow for the WSLink Integration."""
from __future__ import annotations

import secrets
from typing import Any

from yarl import URL

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.network import get_url

from .const import DOMAIN

class CCLConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    )-> ConfigFlowResult:
        """Handle the initial step."""
        self._passkey: str
        
        if user_input is None:
            self._passkey = secrets.token_hex(3)
            return self.async_show_form(step_id = "user")
        
        url = URL(get_url(self.hass))
        assert url.host

        return self.async_create_entry(
            title = "CCL Weather Station",
            data = {
                "passkey": self._passkey,
            },
            description_placeholders = {
                "host": url.host,
                "port": "42373",
                "path": self._passkey,
            },
        )
