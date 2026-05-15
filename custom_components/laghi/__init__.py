"""The Laghi.net integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import AVAILABLE_LAKES, CONF_LAKES, DEFAULT_SCAN_INTERVAL
from .coordinator import LaghiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Laghi.net from a config entry."""
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

    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        raise
    except (TimeoutError, OSError, UpdateFailed) as err:
        raise ConfigEntryNotReady(
            f"Failed to fetch initial data from laghi.net: {err}"
        ) from err
    except ConfigEntryError:
        raise
    except (ValueError, TypeError) as err:
        raise ConfigEntryError(
            f"Invalid response while setting up laghi integration: {err}"
        ) from err
    except Exception as err:
        raise ConfigEntryError(f"Unexpected setup failure: {err}") from err

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Laghi.net component."""
    return True
