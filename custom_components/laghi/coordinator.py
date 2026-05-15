"""Data coordinator for the Laghi.net integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from requests.exceptions import RequestException

from .const import DOMAIN
from .laghi import Laghi

_LOGGER = logging.getLogger(__name__)


class LaghiDataUpdateCoordinator(DataUpdateCoordinator[list[dict[str, Any]]]):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, scan_interval: timedelta, configured_lakes: list[str]) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )
        self.laghi = Laghi()
        self.configured_lakes = configured_lakes

    async def _async_update_data(self) -> list[dict[str, Any]]:
        """Update data via library."""
        try:
            all_data = await self.hass.async_add_executor_job(self.laghi.get_data)
        except (RequestException, OSError, TimeoutError, ValueError, TypeError, KeyError) as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        if not all_data:
            raise UpdateFailed("Failed to get data from laghi.net")

        filtered_data = [
            lake_data for lake_data in all_data if lake_data.get("name") in self.configured_lakes
        ]

        if not filtered_data:
            raise UpdateFailed("No data available for configured lakes")

        return filtered_data
