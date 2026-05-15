"""The Laghi.net integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError

from .const import AVAILABLE_LAKES, CONF_LAKES, DEFAULT_SCAN_INTERVAL, DOMAIN
from .sensor import LaghiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Laghi.net from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    configured_lakes = entry.options.get(CONF_LAKES, AVAILABLE_LAKES)
    valid_lakes = [lake for lake in configured_lakes if lake in AVAILABLE_LAKES]
    invalid_lakes = [lake for lake in configured_lakes if lake not in AVAILABLE_LAKES]

    if invalid_lakes:
        _LOGGER.warning(
            "Ignoring unknown lakes in config entry: %s. Available lakes: %s",
            invalid_lakes,
            AVAILABLE_LAKES,
        )

    if not valid_lakes:
        raise ConfigEntryError(
            f"No valid lakes configured. Available lakes: {', '.join(AVAILABLE_LAKES)}"
        )

    scan_interval_seconds = entry.options.get(CONF_SCAN_INTERVAL)
    if scan_interval_seconds is None:
        scan_interval = timedelta(minutes=DEFAULT_SCAN_INTERVAL)
    else:
        scan_interval = timedelta(seconds=scan_interval_seconds)

    coordinator = LaghiDataUpdateCoordinator(hass, scan_interval, valid_lakes)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    
    return unload_ok


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Laghi.net component from configuration.yaml."""
    # This integration supports configuration via configuration.yaml
    return True
