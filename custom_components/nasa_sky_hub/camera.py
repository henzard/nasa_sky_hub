"""Camera entity for APOD."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODULE_APOD

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up camera from config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    api_client = data["api_client"]
    enabled_modules = data.get("enabled_modules", [])

    if MODULE_APOD not in enabled_modules:
        return

    from .coordinators.apod import APODCoordinator

    coordinator = APODCoordinator(
        hass,
        api_client,
        update_interval=86400,
    )
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        # If setup timed out, just request a refresh instead
        if "ConfigEntryState" in str(err):
            _LOGGER.debug("Setup timed out, requesting refresh instead")
            await coordinator.async_request_refresh()
        else:
            _LOGGER.warning("Failed to refresh APOD coordinator on setup: %s", err)
        # Don't fail setup, coordinator will retry later

    _LOGGER.info("Created APOD camera entity")
    async_add_entities([APODCamera(coordinator)], update_before_add=False)


class APODCamera(CoordinatorEntity, Camera):
    """Camera entity for Astronomy Picture of the Day."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize APOD camera."""
        CoordinatorEntity.__init__(self, coordinator)
        Camera.__init__(self)
        self._attr_name = "NASA Sky Hub APOD"
        self._attr_unique_id = "nasa_sky_hub_apod"
        self._webrtc_provider = None  # Required by Camera base class

    @property
    def entity_picture(self) -> str | None:
        """Return URL of the entity picture."""
        data = self.coordinator.data
        if data is None:
            return None
        # Prefer HD URL if available
        return data.get("hdurl") or data.get("url")

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        import aiohttp

        data = self.coordinator.data
        if data is None:
            return None
        url = data.get("hdurl") or data.get("url")

        if not url:
            return None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.read()
        except Exception as err:
            _LOGGER.error("Failed to fetch APOD image: %s", err)
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        if data is None:
            return {}
        return {
            "title": data.get("title", ""),
            "date": data.get("date", ""),
            "explanation": data.get("explanation", ""),
            "media_type": data.get("media_type", "image"),
        }
