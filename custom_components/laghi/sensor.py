"""Platform for sensor integration."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import LAKE_SENSORS
from .coordinator import LaghiDataUpdateCoordinator


async def async_setup_entry(
    _hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Laghi sensors from a config entry."""
    coordinator: LaghiDataUpdateCoordinator = entry.runtime_data

    entities = []
    if coordinator.data:
        for lake_data in coordinator.data:
            lake_name = lake_data["name"]
            if lake_name in coordinator.configured_lakes:
                for sensor_type, sensor_config in LAKE_SENSORS.items():
                    if sensor_type in lake_data and "value" in lake_data[sensor_type]:
                        entities.append(
                            LaghiSensor(
                                coordinator,
                                lake_name,
                                sensor_type,
                                sensor_config,
                            )
                        )

    async_add_entities(entities)


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
        return self.coordinator.last_update_success
