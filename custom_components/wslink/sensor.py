
"""Platform for sensor integration."""
from __future__ import annotations

import dataclasses
import time

from aioccl import CCLDevice, CCLSensor, CCLSensorTypes

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    EntityCategory,
    UnitOfPressure,
    UnitOfTemperature,
    PERCENTAGE,
    DEGREE,
    UnitOfSpeed,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

CCL_SENSOR_DESCRIPTIONS: dict[str, SensorEntityDescription] = {
    CCLSensorTypes.PRESSURE: SensorEntityDescription(\
        key="PRESSURE",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.HPA,
    ),
    CCLSensorTypes.TEMPERATURE: SensorEntityDescription(
        key="TEMPERATURE",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    CCLSensorTypes.HUMIDITY: SensorEntityDescription(
        key="HUMIDITY",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    CCLSensorTypes.WIND_DIRECITON: SensorEntityDescription(
        key="WIND_DIRECTION",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=DEGREE,
    ),
    CCLSensorTypes.WIND_SPEED: SensorEntityDescription(
        key="WIND_SPEED",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    device: CCLDevice = hass.data[DOMAIN][entry.entry_id]

    def _new_sensor(sensor: CCLSensor) -> None:
        """Add a sensor to the data entry."""
        entity_description = dataclasses.replace(
                CCL_SENSOR_DESCRIPTIONS[sensor.sensor_type],
                key=sensor.key,
                name=sensor.name,
            )
        async_add_entities([CCLSensorEntity(sensor, device, entity_description)])

    device.register_new_sensor_cb(_new_sensor)
    entry.async_on_unload(lambda: device.remove_new_sensor_cb(_new_sensor))

    for key, sensor in device.sensors.items():
        _new_sensor(sensor)


class CCLSensorEntity(SensorEntity):
    """Representation of a Sensor."""
    _attr_has_entity_name = True
    _attr_should_poll = False
    
    def __init__(
        self,
        sensor: CCLSensor,
        device: CCLDevice,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize a CCL Sensor Entity."""
        self._sensor = sensor
        self._device = device

        self._attr_device_info = DeviceInfo(
            identifiers={
                (DOMAIN, self._device.device_id),
            },
            name = self._device.model + " - " + self._device.device_id,
            model = self._device.model,
            serial_number = self._device.serial_no,
            manufacturer = "WSLink",
            sw_version = self._device.version,
        )

        self._attr_available = self._sensor.value is not None

        self._attr_unique_id = f"{self._device.device_id}-{self._sensor.key}"
        
        self.entity_description = entity_description

    @property
    def native_value(self) -> None | str | int | float:
        """Return the state of the sensor."""
        return self._sensor.value

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._device.register_update_cb(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._device.remove_update_cb(self.async_write_ha_state)
