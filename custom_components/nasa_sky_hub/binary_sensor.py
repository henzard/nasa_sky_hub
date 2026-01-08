"""Binary sensor entities for NASA Sky Hub."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    MODULE_SATELLITES,
    MODULE_SKY,
    MODULE_SPACE_WEATHER,
    SEVERITY_ELEVATED,
    SEVERITY_SEVERE,
    SEVERITY_STORM,
)

_LOGGER = logging.getLogger(__name__)

SPACE_WEATHER_BINARY_SENSORS = [
    BinarySensorEntityDescription(
        key="solar_flare_active",
        name="Solar Flare Active",
        device_class=BinarySensorDeviceClass.SAFETY,
    ),
    BinarySensorEntityDescription(
        key="geomagnetic_storm_active",
        name="Geomagnetic Storm Active",
        device_class=BinarySensorDeviceClass.SAFETY,
    ),
    BinarySensorEntityDescription(
        key="radiation_storm_active",
        name="Radiation Storm Active",
        device_class=BinarySensorDeviceClass.SAFETY,
    ),
]

SATELLITE_BINARY_SENSORS = [
    BinarySensorEntityDescription(
        key="iss_overhead",
        name="ISS Overhead",
        device_class=None,
    ),
    BinarySensorEntityDescription(
        key="visible_satellite_pass",
        name="Visible Satellite Pass",
        device_class=None,
    ),
]

SKY_BINARY_SENSORS = [
    BinarySensorEntityDescription(
        key="astronomical_night",
        name="Astronomical Night",
        device_class=None,
    ),
    BinarySensorEntityDescription(
        key="good_stargazing_conditions",
        name="Good Stargazing Conditions",
        device_class=None,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors from config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    api_client = data["api_client"]
    location = data["location"]
    enabled_modules = data.get("enabled_modules", [])

    entities: list[BinarySensorEntity] = []

    # Space Weather binary sensors
    if MODULE_SPACE_WEATHER in enabled_modules:
        from .coordinators.space_weather import SpaceWeatherCoordinator
        coordinator = SpaceWeatherCoordinator(
            hass,
            api_client,
            update_interval=1800,
        )
        try:
            await coordinator.async_config_entry_first_refresh()
        except Exception as err:
            _LOGGER.warning("Failed to refresh space weather coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            SpaceWeatherBinarySensor(coordinator, desc)
            for desc in SPACE_WEATHER_BINARY_SENSORS
        )
        data["coordinators"][MODULE_SPACE_WEATHER] = coordinator

    # Satellite binary sensors
    if MODULE_SATELLITES in enabled_modules:
        from .coordinators.satellites import SatelliteCoordinator
        coordinator = SatelliteCoordinator(
            hass,
            api_client,
            location,
            update_interval=180,
        )
        try:
            await coordinator.async_config_entry_first_refresh()
        except Exception as err:
            _LOGGER.warning("Failed to refresh satellite coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            SatelliteBinarySensor(coordinator, desc)
            for desc in SATELLITE_BINARY_SENSORS
        )
        data["coordinators"][MODULE_SATELLITES] = coordinator

    # Sky binary sensors
    if MODULE_SKY in enabled_modules:
        from .coordinators.sky import SkyCoordinator
        coordinator = SkyCoordinator(
            hass,
            location,
            update_interval=300,
        )
        try:
            await coordinator.async_config_entry_first_refresh()
        except Exception as err:
            _LOGGER.warning("Failed to refresh sky coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            SkyBinarySensor(coordinator, desc)
            for desc in SKY_BINARY_SENSORS
        )
        data["coordinators"][MODULE_SKY] = coordinator

    async_add_entities(entities)


class BaseBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Base binary sensor class."""

    def __init__(
        self,
        coordinator: Any,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.name}_{description.key}"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return f"NASA Sky Hub {self.entity_description.name}"


class SpaceWeatherBinarySensor(BaseBinarySensor):
    """Space weather binary sensor."""

    @property
    def is_on(self) -> bool:
        """Return sensor state."""
        data = self.coordinator.data
        key = self.entity_description.key

        if key == "solar_flare_active":
            flares = data.get("flares", [])
            # Check for flares in last 6 hours
            return len(flares) > 0
        elif key == "geomagnetic_storm_active":
            storms = data.get("storms", [])
            return len(storms) > 0
        elif key == "radiation_storm_active":
            # Check severity for radiation storm indicators
            severity = data.get("severity", "")
            return severity in [SEVERITY_STORM, SEVERITY_SEVERE]
        return False

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        attrs = {}
        if self.entity_description.key == "solar_flare_active":
            flares = data.get("flares", [])
            if flares:
                latest = flares[0]
                attrs.update({
                    "latest_flare_class": latest.get("classType", ""),
                    "latest_flare_begin": latest.get("beginTime", ""),
                    "source_region": latest.get("sourceLocation", ""),
                })
        return attrs


class SatelliteBinarySensor(BaseBinarySensor):
    """Satellite binary sensor."""

    @property
    def is_on(self) -> bool:
        """Return sensor state."""
        data = self.coordinator.data
        key = self.entity_description.key

        if key == "iss_overhead":
            return data.get("iss_overhead", False)
        elif key == "visible_satellite_pass":
            next_pass = data.get("next_pass")
            if next_pass:
                # Check if pass is soon (within 1 hour)
                from datetime import datetime
                rise_time_str = next_pass.get("rise_time")
                if rise_time_str:
                    try:
                        rise_time = datetime.fromisoformat(rise_time_str.replace("Z", "+00:00"))
                        time_until = (rise_time - datetime.now()).total_seconds()
                        return 0 < time_until < 3600  # Within next hour
                    except Exception:
                        pass
            return False
        return False

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        attrs = {}
        if self.entity_description.key == "iss_overhead" and data.get("iss_data"):
            attrs.update({
                "azimuth": data["iss_data"].get("azimuth"),
                "elevation": data["iss_data"].get("elevation"),
                "distance_km": data["iss_data"].get("distance_km"),
            })
        elif self.entity_description.key == "visible_satellite_pass" and data.get("next_pass"):
            attrs.update(data["next_pass"])
        return attrs


class SkyBinarySensor(BaseBinarySensor):
    """Sky visibility binary sensor."""

    @property
    def is_on(self) -> bool:
        """Return sensor state."""
        data = self.coordinator.data
        key = self.entity_description.key

        if key == "astronomical_night":
            return data.get("astronomical_night", False)
        elif key == "good_stargazing_conditions":
            return data.get("good_stargazing", False)
        return False

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        return {
            "darkness_level": data.get("darkness_level", 0.0),
            "visible_constellations": data.get("visible_constellations", []),
        }
