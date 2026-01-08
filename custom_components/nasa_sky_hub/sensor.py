"""Sensor entities for NASA Sky Hub."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODULE_APOD, MODULE_SATELLITES, MODULE_SKY, MODULE_SPACE_WEATHER
from .coordinators.apod import APODCoordinator
from .coordinators.satellites import SatelliteCoordinator
from .coordinators.sky import SkyCoordinator
from .coordinators.space_weather import SpaceWeatherCoordinator

_LOGGER = logging.getLogger(__name__)

SPACE_WEATHER_SENSORS = [
    SensorEntityDescription(
        key="severity",
        name="Space Weather Severity",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="flares_24h",
        name="Solar Flares (24h)",
        icon="mdi:solar-power",
        native_unit_of_measurement="flares",
        state_class=SensorStateClass.MEASUREMENT,
    ),
]

APOD_SENSORS = [
    SensorEntityDescription(
        key="title",
        name="APOD Title",
        icon="mdi:image",
    ),
    SensorEntityDescription(
        key="date",
        name="APOD Date",
        icon="mdi:calendar",
        device_class=SensorDeviceClass.DATE,
    ),
]

SATELLITE_SENSORS = [
    SensorEntityDescription(
        key="satellites_overhead",
        name="Satellites Overhead",
        icon="mdi:satellite-variant",
        native_unit_of_measurement="satellites",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="next_pass",
        name="Next Satellite Pass",
        icon="mdi:satellite",
    ),
]

SKY_SENSORS = [
    SensorEntityDescription(
        key="visible_constellations",
        name="Visible Constellations",
        icon="mdi:star",
    ),
    SensorEntityDescription(
        key="brightest_object",
        name="Brightest Object Overhead",
        icon="mdi:star-circle",
    ),
    SensorEntityDescription(
        key="darkness_level",
        name="Sky Darkness Level",
        icon="mdi:weather-night",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="sidereal_time",
        name="Sidereal Time",
        icon="mdi:clock-outline",
    ),
]

RATE_LIMIT_SENSORS = [
    SensorEntityDescription(
        key="rate_remaining",
        name="NASA API Rate Limit Remaining",
        icon="mdi:api",
        native_unit_of_measurement="requests",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="rate_status",
        name="NASA API Status",
        icon="mdi:api",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors from config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    api_client = data["api_client"]
    rate_limiter = data["rate_limiter"]
    location = data["location"]
    enabled_modules = data.get("enabled_modules", [])

    entities: list[SensorEntity] = []

    # Rate limit sensors (always enabled)
    entities.extend(
        RateLimitSensor(rate_limiter, desc)
        for desc in RATE_LIMIT_SENSORS
    )

    # Space Weather sensors
    if MODULE_SPACE_WEATHER in enabled_modules:
        coordinator = SpaceWeatherCoordinator(
            hass,
            api_client,
            update_interval=1800,
        )
        await coordinator.async_config_entry_first_refresh()
        entities.extend(
            SpaceWeatherSensor(coordinator, desc)
            for desc in SPACE_WEATHER_SENSORS
        )

    # APOD sensors
    if MODULE_APOD in enabled_modules:
        coordinator = APODCoordinator(
            hass,
            api_client,
            update_interval=86400,
        )
        await coordinator.async_config_entry_first_refresh()
        entities.extend(
            APODSensor(coordinator, desc)
            for desc in APOD_SENSORS
        )

    # Satellite sensors
    if MODULE_SATELLITES in enabled_modules:
        coordinator = SatelliteCoordinator(
            hass,
            api_client,
            location,
            update_interval=180,
        )
        await coordinator.async_config_entry_first_refresh()
        entities.extend(
            SatelliteSensor(coordinator, desc)
            for desc in SATELLITE_SENSORS
        )

    # Sky sensors
    if MODULE_SKY in enabled_modules:
        coordinator = SkyCoordinator(
            hass,
            location,
            update_interval=300,
        )
        await coordinator.async_config_entry_first_refresh()
        entities.extend(
            SkySensor(coordinator, desc)
            for desc in SKY_SENSORS
        )

    async_add_entities(entities)


class BaseSensor(CoordinatorEntity, SensorEntity):
    """Base sensor class."""

    def __init__(
        self,
        coordinator: Any,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.name}_{description.key}"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return f"NASA Sky Hub {self.entity_description.name}"


class SpaceWeatherSensor(BaseSensor):
    """Space weather sensor."""

    @property
    def native_value(self) -> str | int | None:
        """Return sensor value."""
        data = self.coordinator.data
        key = self.entity_description.key

        if key == "severity":
            return data.get("severity", "unknown")
        elif key == "flares_24h":
            return data.get("flares_24h", 0)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        if self.entity_description.key == "severity":
            return {
                "flares": data.get("flares", []),
                "cmes": data.get("cmes", []),
                "storms": data.get("storms", []),
            }
        return {}


class APODSensor(BaseSensor):
    """APOD sensor."""

    @property
    def native_value(self) -> str | None:
        """Return sensor value."""
        data = self.coordinator.data
        return data.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        return {
            "explanation": data.get("explanation", ""),
            "url": data.get("url", ""),
            "hdurl": data.get("hdurl", ""),
            "media_type": data.get("media_type", "image"),
        }


class SatelliteSensor(BaseSensor):
    """Satellite sensor."""

    @property
    def native_value(self) -> str | int | None:
        """Return sensor value."""
        data = self.coordinator.data
        key = self.entity_description.key

        if key == "satellites_overhead":
            return data.get("satellites_overhead", 0)
        elif key == "next_pass":
            next_pass = data.get("next_pass")
            if next_pass:
                return next_pass.get("rise_time")
            return None
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        attrs = {
            "satellites": data.get("satellites", []),
            "iss_overhead": data.get("iss_overhead", False),
        }
        if data.get("iss_data"):
            attrs["iss_data"] = data["iss_data"]
        if data.get("next_pass"):
            attrs["next_pass"] = data["next_pass"]
        return attrs


class SkySensor(BaseSensor):
    """Sky visibility sensor."""

    @property
    def native_value(self) -> str | float | None:
        """Return sensor value."""
        data = self.coordinator.data
        key = self.entity_description.key

        if key == "visible_constellations":
            consts = data.get("visible_constellations", [])
            return ", ".join(consts) if consts else "None"
        elif key == "brightest_object":
            obj = data.get("brightest_object", {})
            return obj.get("name", "None")
        elif key == "darkness_level":
            level = data.get("darkness_level", 0.0)
            return int(level * 100)
        elif key == "sidereal_time":
            return data.get("sidereal_time", "")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        attrs = {}
        if self.entity_description.key == "brightest_object":
            attrs["brightest_object"] = data.get("brightest_object", {})
        elif self.entity_description.key == "visible_constellations":
            attrs["constellations"] = data.get("visible_constellations", [])
        return attrs


class RateLimitSensor(SensorEntity):
    """Rate limit sensor."""

    def __init__(
        self,
        rate_limiter: Any,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize rate limit sensor."""
        self.rate_limiter = rate_limiter
        self.entity_description = description
        self._attr_unique_id = f"nasa_api_{description.key}"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return f"NASA API {self.entity_description.name}"

    @property
    def native_value(self) -> str | int | None:
        """Return sensor value."""
        status = self.rate_limiter.get_status()
        key = self.entity_description.key

        if key == "rate_remaining":
            return status.get("remaining", 0)
        elif key == "rate_status":
            remaining = status.get("remaining", 0)
            if remaining < 50:
                return "degraded"
            elif remaining < 100:
                return "warning"
            return "normal"
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return self.rate_limiter.get_status()
