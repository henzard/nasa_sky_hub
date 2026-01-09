"""NASA Sky Hub integration for Home Assistant."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .api_client import NASAApiClient
from .const import DOMAIN
from .rate_limiter import RateLimiter

_LOGGER = logging.getLogger(__name__)

# Enable detailed logging
logging.getLogger(__name__).setLevel(logging.DEBUG)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CAMERA,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the NASA Sky Hub integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NASA Sky Hub from a config entry."""
    _LOGGER.info("=" * 60)
    _LOGGER.info("NASA Sky Hub: Starting setup for entry %s", entry.entry_id)
    _LOGGER.info("=" * 60)
    
    api_key = entry.data.get("api_key", "DEMO_KEY")
    location = entry.data.get("location", {})
    enabled_modules = entry.data.get("enabled_modules", [])
    # If no modules enabled, default to all modules (backward compatibility)
    if not enabled_modules:
        from .const import ALL_MODULES
        enabled_modules = ALL_MODULES
        _LOGGER.warning("No modules enabled in config, defaulting to all modules: %s", enabled_modules)
    profile = entry.data.get("profile", "balanced")

    _LOGGER.info("Configuration:")
    _LOGGER.info("  API Key: %s", "***" if api_key != "DEMO_KEY" else "DEMO_KEY")
    _LOGGER.info("  Location: %s", location)
    _LOGGER.info("  Enabled Modules: %s", enabled_modules)
    _LOGGER.info("  Profile: %s", profile)

    # Initialize rate limiter
    rate_limiter = RateLimiter(profile=profile)
    _LOGGER.debug("Rate limiter initialized with profile: %s", profile)

    # Initialize API client
    api_client = NASAApiClient(
        api_key=api_key,
        rate_limiter=rate_limiter,
        hass=hass,
    )
    _LOGGER.debug("API client initialized")

    # Store in hass.data
    hass.data[DOMAIN][entry.entry_id] = {
        "api_client": api_client,
        "rate_limiter": rate_limiter,
        "location": location,
        "enabled_modules": enabled_modules,
        "coordinators": {},  # Will be populated by platforms
    }
    _LOGGER.debug("Data stored in hass.data[%s][%s]", DOMAIN, entry.entry_id)

    # Forward setup to platforms
    _LOGGER.info("Setting up platforms: %s", PLATFORMS)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.info("Platforms setup complete")

    # Register services (only once per domain)
    if DOMAIN not in hass.data.get("_service_registered", {}):
        _LOGGER.debug("Registering services")
        await _register_services(hass, entry)
        hass.data.setdefault("_service_registered", {})[DOMAIN] = True
        _LOGGER.info("Services registered")

    _LOGGER.info("NASA Sky Hub setup complete for entry %s", entry.entry_id)
    _LOGGER.info("=" * 60)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id, {})
        # Close API client session
        if "api_client" in data:
            await data["api_client"].async_close()
    return unload_ok


async def _register_services(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register custom services."""
    from .services import (
        async_refresh_all,
        async_refresh_module,
        async_prefetch_apod_range,
        async_calculate_satellite_passes,
    )

    async def refresh_all_service(call: Any) -> None:
        """Handle refresh_all service call."""
        await async_refresh_all(hass, call)

    async def refresh_module_service(call: Any) -> None:
        """Handle refresh_module service call."""
        await async_refresh_module(hass, call)

    async def prefetch_apod_range_service(call: Any) -> None:
        """Handle prefetch_apod_range service call."""
        await async_prefetch_apod_range(hass, call)

    async def calculate_satellite_passes_service(call: Any) -> None:
        """Handle calculate_satellite_passes service call."""
        await async_calculate_satellite_passes(hass, call)

    hass.services.async_register(DOMAIN, "refresh_all", refresh_all_service)
    hass.services.async_register(DOMAIN, "refresh_module", refresh_module_service)
    hass.services.async_register(DOMAIN, "prefetch_apod_range", prefetch_apod_range_service)
    hass.services.async_register(DOMAIN, "calculate_satellite_passes", calculate_satellite_passes_service)
