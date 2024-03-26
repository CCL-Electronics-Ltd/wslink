from __future__ import annotations

import asyncio

from homeassistant.core import HomeAssistant

class CclHub:
    def __init__(self, hass: HomeAssistant, name: str, unique_id: str)-> None:
        self._hass = hass
        self._name = name
        self._id = unique_id.lower()

    @property
    def hub_id(self)-> str:
        return self._id
