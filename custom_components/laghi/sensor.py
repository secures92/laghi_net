"""Platform for sensor integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import Throttle

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, LAKE_SENSORS, CONF_LAKES, AVAILABLE_LAKES
from .laghi import Laghi

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=DEFAULT_SCAN_INTERVAL)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    
    scan_interval = config.get(CONF_SCAN_INTERVAL, timedelta(minutes=DEFAULT_SCAN_INTERVAL))
    
    # Get configured lakes from YAML, default to all lakes
    configured_lakes = config.get(CONF_LAKES, AVAILABLE_LAKES)
    
    # Validate configured lakes
    valid_lakes = []
    for lake in configured_lakes:
        if lake in AVAILABLE_LAKES:
            valid_lakes.append(lake)
        else:
            _LOGGER.warning("Unknown lake '%s' in configuration. Available lakes: %s", lake, AVAILABLE_LAKES)
    
    if not valid_lakes:
        _LOGGER.error("No valid lakes configured. Available lakes: %s", AVAILABLE_LAKES)
        return
    
    coordinator = LaghiDataUpdateCoordinator(hass, scan_interval, valid_lakes)
    
    # Fetch initial data so we have data when entities are added
    await coordinator.async_config_entry_first_refresh()
    
    entities = []
    
    # Create sensors for each configured lake and each measurement type
    if coordinator.data:
        for lake_data in coordinator.data:
            lake_name = lake_data["name"]
            
            # Only create sensors for configured lakes
            if lake_name in valid_lakes:
                for sensor_type, sensor_config in LAKE_SENSORS.items():
                    if sensor_type in lake_data and "value" in lake_data[sensor_type]:
                        entities.append(
                            LaghiSensor(
                                coordinator,
                                lake_name,
                                sensor_type,
                                sensor_config
                            )
                        )
    
    async_add_entities(entities, update_before_add=True)


class LaghiDataUpdateCoordinator(DataUpdateCoordinator):
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
            if not all_data:
                raise UpdateFailed("Failed to get data from laghi.net")
            
            # Filter data to only include configured lakes
            filtered_data = []
            for lake_data in all_data:
                if lake_data["name"] in self.configured_lakes:
                    filtered_data.append(lake_data)
            
            return filtered_data
        except Exception as exception:
            raise UpdateFailed(f"Error communicating with API: {exception}") from exception


class LaghiSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Laghi sensor."""

    def __init__(
        self, 
        coordinator: LaghiDataUpdateCoordinator, 
        lake_name: str, 
        sensor_type: str,
        sensor_config: dict[str, Any]
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._lake_name = lake_name
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        
        # Create unique identifier and friendly name
        self._attr_unique_id = f"laghi_{lake_name.lower().replace(' ', '_')}_{sensor_type}"
        self._attr_name = f"{lake_name} {sensor_config['name']}"
        self._attr_icon = sensor_config["icon"]
        
        if sensor_config.get("device_class"):
            self._attr_device_class = sensor_config["device_class"]
        
        if sensor_config.get("state_class"):
            self._attr_state_class = sensor_config["state_class"]

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        if not self.coordinator.data:
            return None
        
        # Find the data for our specific lake
        for lake_data in self.coordinator.data:
            if lake_data["name"] == self._lake_name:
                if self._sensor_type in lake_data and "value" in lake_data[self._sensor_type]:
                    return lake_data[self._sensor_type]["value"]
        
        return None

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        if not self.coordinator.data:
            return None
        
        # Find the data for our specific lake
        for lake_data in self.coordinator.data:
            if lake_data["name"] == self._lake_name:
                if self._sensor_type in lake_data and "unit" in lake_data[self._sensor_type]:
                    return lake_data[self._sensor_type]["unit"]
        
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the state attributes."""
        if not self.coordinator.data:
            return None
        
        # Find the data for our specific lake
        for lake_data in self.coordinator.data:
            if lake_data["name"] == self._lake_name:
                attributes = {
                    "lake_name": self._lake_name,
                    "sensor_type": self._sensor_type,
                }
                
                # Add timestamp if available
                if "timestamp" in lake_data and lake_data["timestamp"]:
                    from datetime import datetime
                    attributes["last_updated"] = datetime.fromtimestamp(lake_data["timestamp"]).isoformat()
                
                return attributes
        
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.native_value is not None
