"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_NAME

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([FastlanePriceSensor(coordinator, entry)], True)

class FastlanePriceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Fastlane Price Sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = DEFAULT_NAME
        self._attr_unique_id = f"{entry.entry_id}_price"
        self._attr_native_unit_of_measurement = "NIS"
        self._attr_icon = "mdi:currency-ils"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data
