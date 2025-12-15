"""The Fastlane IL integration."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .scraper import get_price

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Fastlane IL from a config entry."""
    
    hass.data.setdefault(DOMAIN, {})
    
    scan_interval = entry.options.get("scan_interval", entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL))
    
    coordinator = FastlaneDataUpdateCoordinator(
        hass,
        scan_interval_minutes=scan_interval,
    )
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)

class FastlaneDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Fastlane data."""

    def __init__(self, hass: HomeAssistant, scan_interval_minutes: int) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval_minutes),
        )
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        """Fetch data from API."""
        price = await get_price(self.session)
        if price == "Error" or price == "Unknown":
             # We might want to raise UpdateFailed to mark the sensor unavailable
             # Or just return "Unknown" but usually UpdateFailed is better for HA
             if price == "Error":
                 raise UpdateFailed("Error fetching data from Fastlane")
        return price
