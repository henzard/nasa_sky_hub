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

from .const import DOMAIN, MODULE_APOD, MODULE_ASTEROIDS, MODULE_SATELLITES, MODULE_SKY, MODULE_SPACE_WEATHER
from .coordinators.apod import APODCoordinator
from .coordinators.asteroids import CADCoordinator, SentryCoordinator
from .coordinators.neows import NeoWsCoordinator
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

ASTEROID_SENTRY_SENSORS = [
    SensorEntityDescription(
        key="total_threats",
        name="Asteroid Impact Threats",
        icon="mdi:asteroid",
        native_unit_of_measurement="threats",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="max_palermo_scale",
        name="Highest Palermo Scale",
        icon="mdi:alert-circle",
        state_class=SensorStateClass.MEASUREMENT,
    ),
]

ASTEROID_CAD_SENSORS = [
    SensorEntityDescription(
        key="total_approaches",
        name="Close Approaches (60 days)",
        icon="mdi:orbit",
        native_unit_of_measurement="approaches",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="next_approach",
        name="Next Close Approach",
        icon="mdi:rocket-launch",
    ),
]

NEO_WS_SENSORS = [
    SensorEntityDescription(
        key="total_neos",
        name="Near Earth Objects",
        icon="mdi:asteroid",
        native_unit_of_measurement="objects",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="potentially_hazardous",
        name="Potentially Hazardous Objects",
        icon="mdi:alert-circle",
        native_unit_of_measurement="objects",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="closest_approach",
        name="Closest Approach",
        icon="mdi:rocket-launch",
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
    _LOGGER.info("Setting up sensors for entry %s", entry.entry_id)
    data = hass.data[DOMAIN][entry.entry_id]
    api_client = data["api_client"]
    rate_limiter = data["rate_limiter"]
    location = data["location"]
    enabled_modules = data.get("enabled_modules", [])

    _LOGGER.debug("Enabled modules: %s", enabled_modules)
    _LOGGER.debug("Location: %s", location)

    entities: list[SensorEntity] = []

    # Rate limit sensors (always enabled)
    _LOGGER.debug("Creating rate limit sensors")
    entities.extend(
        RateLimitSensor(rate_limiter, desc)
        for desc in RATE_LIMIT_SENSORS
    )

    # Space Weather sensors
    if MODULE_SPACE_WEATHER in enabled_modules:
        _LOGGER.info("Setting up Space Weather sensors")
        coordinator = SpaceWeatherCoordinator(
            hass,
            api_client,
            update_interval=1800,
        )
        try:
            await coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("Space Weather coordinator refreshed, data: %s", coordinator.data is not None)
        except Exception as err:
            # If setup timed out, just request a refresh instead
            if "ConfigEntryState" in str(err):
                _LOGGER.debug("Setup timed out, requesting refresh instead")
                await coordinator.async_request_refresh()
            else:
                _LOGGER.warning("Failed to refresh space weather coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            SpaceWeatherSensor(coordinator, desc)
            for desc in SPACE_WEATHER_SENSORS
        )
        # Store coordinator for diagnostics
        data["coordinators"][MODULE_SPACE_WEATHER] = coordinator

    # APOD sensors
    if MODULE_APOD in enabled_modules:
        _LOGGER.info("Setting up APOD sensors")
        coordinator = APODCoordinator(
            hass,
            api_client,
            update_interval=86400,
        )
        try:
            await coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("APOD coordinator refreshed, data: %s", coordinator.data is not None)
        except Exception as err:
            # If setup timed out, just request a refresh instead
            if "ConfigEntryState" in str(err):
                _LOGGER.debug("Setup timed out, requesting refresh instead")
                await coordinator.async_request_refresh()
            else:
                _LOGGER.warning("Failed to refresh APOD coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            APODSensor(coordinator, desc)
            for desc in APOD_SENSORS
        )
        data["coordinators"][MODULE_APOD] = coordinator

    # Satellite sensors
    if MODULE_SATELLITES in enabled_modules:
        _LOGGER.info("Setting up Satellite sensors")
        coordinator = SatelliteCoordinator(
            hass,
            api_client,
            location,
            update_interval=180,
        )
        try:
            await coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("Satellite coordinator refreshed, data: %s", coordinator.data is not None)
        except Exception as err:
            # If setup timed out, just request a refresh instead
            if "ConfigEntryState" in str(err):
                _LOGGER.debug("Setup timed out, requesting refresh instead")
                await coordinator.async_request_refresh()
            else:
                _LOGGER.warning("Failed to refresh satellite coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            SatelliteSensor(coordinator, desc)
            for desc in SATELLITE_SENSORS
        )
        data["coordinators"][MODULE_SATELLITES] = coordinator

    # Sky sensors
    if MODULE_SKY in enabled_modules:
        _LOGGER.info("Setting up Sky sensors")
        coordinator = SkyCoordinator(
            hass,
            location,
            update_interval=300,
        )
        try:
            await coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("Sky coordinator refreshed, data: %s", coordinator.data is not None)
        except Exception as err:
            # If setup timed out, just request a refresh instead
            if "ConfigEntryState" in str(err):
                _LOGGER.debug("Setup timed out, requesting refresh instead")
                await coordinator.async_request_refresh()
            else:
                _LOGGER.warning("Failed to refresh sky coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            SkySensor(coordinator, desc)
            for desc in SKY_SENSORS
        )
        data["coordinators"][MODULE_SKY] = coordinator

    # Asteroid sensors (Sentry and CAD)
    if MODULE_ASTEROIDS in enabled_modules:
        _LOGGER.info("Setting up Asteroid sensors")
        
        # Sentry coordinator (impact risk)
        sentry_coordinator = SentryCoordinator(
            hass,
            api_client,
            update_interval=1800,
        )
        try:
            await sentry_coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("Sentry coordinator refreshed, data: %s", sentry_coordinator.data is not None)
        except Exception as err:
            # If setup timed out, just request a refresh instead
            if "ConfigEntryState" in str(err):
                _LOGGER.debug("Setup timed out, requesting refresh instead")
                await sentry_coordinator.async_request_refresh()
            else:
                _LOGGER.warning("Failed to refresh Sentry coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            SentrySensor(sentry_coordinator, desc)
            for desc in ASTEROID_SENTRY_SENSORS
        )
        data["coordinators"][f"{MODULE_ASTEROIDS}_sentry"] = sentry_coordinator
        
        # CAD coordinator (close approaches)
        cad_coordinator = CADCoordinator(
            hass,
            api_client,
            update_interval=1800,
        )
        try:
            await cad_coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("CAD coordinator refreshed, data: %s", cad_coordinator.data is not None)
        except Exception as err:
            # If setup timed out, just request a refresh instead
            if "ConfigEntryState" in str(err):
                _LOGGER.debug("Setup timed out, requesting refresh instead")
                await cad_coordinator.async_request_refresh()
            else:
                _LOGGER.warning("Failed to refresh CAD coordinator on setup: %s", err)
            # Don't fail setup, coordinator will retry later
        entities.extend(
            CADSensor(cad_coordinator, desc)
            for desc in ASTEROID_CAD_SENSORS
        )
        data["coordinators"][f"{MODULE_ASTEROIDS}_cad"] = cad_coordinator
        
        # NeoWs feed coordinator (uses NASA NeoWs API)
        neows_coordinator = NeoWsCoordinator(
            hass,
            api_client,
            days_ahead=7,  # Default to 7 days ahead
            update_interval=DEFAULT_UPDATE_INTERVALS[profile][MODULE_ASTEROIDS],
        )
        try:
            await neows_coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("NeoWs coordinator refreshed, data: %s", neows_coordinator.data is not None)
        except Exception as err:
            _LOGGER.warning("Failed to refresh NeoWs coordinator on setup: %s", err)
            if "ConfigEntryState" in str(err):
                _LOGGER.debug("Setup timed out, requesting refresh instead")
                await neows_coordinator.async_request_refresh()
            # Don't fail setup, coordinator will retry later
        entities.extend(
            NeoWsSensor(neows_coordinator, desc)
            for desc in NEO_WS_SENSORS
        )
        data["coordinators"][f"{MODULE_ASTEROIDS}_neows"] = neows_coordinator

    _LOGGER.info("Created %s sensor entities", len(entities))
    # Log entity details for diagnostics
    for entity in entities:
        unique_id = getattr(entity, '_attr_unique_id', 'unknown')
        desc_key = getattr(entity.entity_description, 'key', 'unknown') if hasattr(entity, 'entity_description') else 'unknown'
        coordinator_name = getattr(entity.coordinator, 'name', 'unknown') if hasattr(entity, 'coordinator') else 'unknown'
        _LOGGER.debug("Entity: unique_id=%s, key=%s, coordinator=%s", unique_id, desc_key, coordinator_name)
    async_add_entities(entities, update_before_add=False)


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
        if data is None:
            return None
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
        if data is None:
            return {}
        if self.entity_description.key == "severity":
            # Limit attributes to prevent exceeding 16KB limit
            flares = data.get("flares", [])[:10]  # Only most recent 10 flares
            cmes = data.get("cmes", [])[:5]  # Only most recent 5 CMEs
            storms = data.get("storms", [])[:5]  # Only most recent 5 storms
            return {
                "flares": flares,
                "cmes": cmes,
                "storms": storms,
                "total_flares": len(data.get("flares", [])),
                "total_cmes": len(data.get("cmes", [])),
                "total_storms": len(data.get("storms", [])),
            }
        return {}


class APODSensor(BaseSensor):
    """APOD sensor."""

    @property
    def native_value(self) -> str | None:
        """Return sensor value."""
        data = self.coordinator.data
        if data is None:
            return None
        return data.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        if data is None:
            return {}
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
        if data is None:
            return None
        key = self.entity_description.key

        if key == "satellites_overhead":
            return data.get("satellites_overhead", 0)
        elif key == "next_pass":
            next_pass = data.get("next_pass")
            if next_pass:
                # Return formatted time string with satellite name
                sat_name = next_pass.get("name", "Satellite")
                rise_time_str = next_pass.get("rise_time", "")
                if rise_time_str:
                    try:
                        from datetime import datetime, timezone
                        rise_time = datetime.fromisoformat(rise_time_str.replace("Z", "+00:00"))
                        # Format as "HH:MM" in local time (or UTC if timezone conversion fails)
                        return f"{sat_name} at {rise_time.strftime('%H:%M')}"
                    except Exception:
                        return rise_time_str
                return rise_time_str
            return None
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        if data is None:
            return {}
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
        if data is None:
            return None
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
        if data is None:
            return {}
        attrs = {}
        if self.entity_description.key == "brightest_object":
            attrs["brightest_object"] = data.get("brightest_object", {})
        elif self.entity_description.key == "visible_constellations":
            attrs["constellations"] = data.get("visible_constellations", [])
        return attrs


class SentrySensor(BaseSensor):
    """Sentry impact risk sensor."""

    @property
    def native_value(self) -> str | int | float | None:
        """Return sensor value."""
        data = self.coordinator.data
        if data is None:
            return None
        key = self.entity_description.key

        if key == "total_threats":
            return data.get("total_threats", 0)
        elif key == "max_palermo_scale":
            return data.get("max_palermo_scale", None)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        if data is None:
            return {}
        
        attrs = {
            "last_update": data.get("last_update"),
        }
        
        highest_risk = data.get("highest_risk")
        if highest_risk:
            attrs["highest_risk_object"] = {
                "designation": highest_risk.get("des"),
                "fullname": highest_risk.get("fullname"),
                "palermo_scale": highest_risk.get("ps_cum"),
                "impact_probability": highest_risk.get("ip"),
                "diameter_km": highest_risk.get("diameter"),
                "last_observation": highest_risk.get("last_obs"),
            }
        
        # Include top 5 threats
        objects = data.get("objects", [])
        if objects:
            attrs["top_threats"] = [
                {
                    "designation": obj.get("des"),
                    "fullname": obj.get("fullname"),
                    "palermo_scale": obj.get("ps_cum"),
                    "impact_probability": obj.get("ip"),
                }
                for obj in objects[:5]
            ]
        
        return attrs


class CADSensor(BaseSensor):
    """Close Approach Data sensor."""

    @property
    def native_value(self) -> str | int | None:
        """Return sensor value."""
        data = self.coordinator.data
        if data is None:
            return None
        key = self.entity_description.key

        if key == "total_approaches":
            return data.get("total_approaches", 0)
        elif key == "next_approach":
            approaches = data.get("approaches", [])
            if not approaches:
                return None
            # CAD data is sorted by date, so the first one is the next
            next_approach = approaches[0]
            return next_approach.get("close_approach_date_full")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        if data is None:
            return {}
        
        attrs = {
            "last_update": data.get("last_update"),
        }
        
        next_approach = data.get("next_approach")
        if next_approach:
            attrs["next_approach"] = {
                "designation": next_approach.get("designation"),
                "approach_date": next_approach.get("approach_date"),
                "distance_au": next_approach.get("distance_au"),
                "distance_min_au": next_approach.get("distance_min_au"),
                "distance_max_au": next_approach.get("distance_max_au"),
                "velocity_km_s": next_approach.get("velocity_km_s"),
                "absolute_magnitude": next_approach.get("absolute_magnitude"),
            }
        
        # Include upcoming approaches
        approaches = data.get("approaches", [])
        if approaches:
            attrs["upcoming_approaches"] = [
                {
                    "designation": app.get("designation"),
                    "approach_date": app.get("approach_date"),
                    "distance_au": app.get("distance_au"),
                    "velocity_km_s": app.get("velocity_km_s"),
                }
                for app in approaches[:10]
            ]
        
        return attrs


class NeoWsSensor(BaseSensor):
    """NeoWs feed sensor."""

    @property
    def native_value(self) -> str | int | None:
        """Return sensor value."""
        data = self.coordinator.data
        if data is None:
            return None
        key = self.entity_description.key

        if key == "total_neos":
            return data.get("total_neos", 0)
        elif key == "potentially_hazardous":
            return data.get("potentially_hazardous_count", 0)
        elif key == "closest_approach":
            approaches = data.get("closest_approaches", [])
            if not approaches:
                return None
            closest = approaches[0]
            return closest.get("close_approach_date_full")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        if data is None:
            return {}
        attrs = {}
        key = self.entity_description.key
        
        if key == "total_neos":
            attrs["element_count"] = data.get("element_count", 0)
            attrs["potentially_hazardous_count"] = data.get("potentially_hazardous_count", 0)
        elif key == "potentially_hazardous":
            # Include list of potentially hazardous objects
            approaches = data.get("closest_approaches", [])
            pha_objects = [a for a in approaches if a.get("is_potentially_hazardous", False)]
            attrs["hazardous_objects"] = pha_objects[:10]  # Top 10
        elif key == "closest_approach":
            approaches = data.get("closest_approaches", [])
            if approaches:
                attrs["closest_approaches"] = approaches[:10]  # Top 10 closest
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
