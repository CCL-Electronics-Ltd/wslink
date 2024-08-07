"""The mapping of a CCL Entity."""
from __future__ import annotations

from aioccl import CCLDevice, CCLSensor

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

class CCLEntity(Entity):
    """Representation of a CCL Entity."""
    _attr_has_entity_name = True
    _attr_should_poll = False
    
    def __init__(
        self,
        internal: CCLSensor,
        device: CCLDevice,
    ) -> None:
        """Initialize a CCL Entity."""
        self._internal = internal
        self._device = device
        
        self._attr_unique_id = f"{device.device_id}-{internal.key}"
        self__attr_device_info = DeviceInfo(
            identifiers={
                (DOMAIN, device.device_id),
            },
            name = device.model + " - " + device.device_id,
            model = device.model,
            serial_number = device.serial_no,
            manufacturer = "WSLink",
            sw_version = device.version,
        )
        
    def available(self) -> bool:
        return self._internal.value is not None

    async def async_added_to_hass(self) -> None:
        """Run when this Entity has been added to HA."""
        self._device.register_update_cb(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        """Entity being removed from hass."""
        self._device.remove_update_cb(self.async_write_ha_state)
