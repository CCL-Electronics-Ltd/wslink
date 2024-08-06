"""The Integration for WSLink weather stations."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry

from aioccl import CCLServer, CCLDevice

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry for a single CCL device."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = CCLDevice(
        entry.data["passkey"]
    )

    CCLServer.add_copy(hass.data[DOMAIN][entry.entry_id])
    await CCLServer.run()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
