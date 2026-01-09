"""Service handlers for NASA Sky Hub."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_refresh_all(hass: HomeAssistant, call: ServiceCall) -> None:
    """Refresh all coordinators."""
    entry_id = call.data.get("entry_id")
    if not entry_id:
        # Use first entry if not specified
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            _LOGGER.error("No NASA Sky Hub config entries found")
            return
        entry_id = entries[0].entry_id

    data = hass.data[DOMAIN].get(entry_id)
    if not data:
        _LOGGER.error("Config entry not found: %s", entry_id)
        return

    # Refresh all coordinators
    coordinators = data.get("coordinators", {})
    if not coordinators:
        _LOGGER.warning("No coordinators found for entry %s", entry_id)
        return

    _LOGGER.info("Refreshing all coordinators for entry %s", entry_id)
    for name, coordinator in coordinators.items():
        if hasattr(coordinator, "async_request_refresh"):
            await coordinator.async_request_refresh()
            _LOGGER.debug("Refreshed coordinator: %s", name)


async def async_refresh_module(hass: HomeAssistant, call: ServiceCall) -> None:
    """Refresh a specific module."""
    entry_id = call.data.get("entry_id")
    if not entry_id:
        # Use first entry if not specified
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            _LOGGER.error("No NASA Sky Hub config entries found")
            return
        entry_id = entries[0].entry_id

    module = call.data.get("module")
    if not module:
        _LOGGER.error("Module name required")
        return

    data = hass.data[DOMAIN].get(entry_id)
    if not data:
        _LOGGER.error("Config entry not found: %s", entry_id)
        return

    coordinators = data.get("coordinators", {})
    
    # Try to find coordinator by module name
    coordinator = coordinators.get(module)
    if coordinator is None:
        # Some modules have multiple coordinators (e.g., asteroids has sentry, cad, neows)
        # Try to find any coordinator that starts with the module name
        for name, coord in coordinators.items():
            if name.startswith(module):
                coordinator = coord
                break
    
    if coordinator is None:
        _LOGGER.error("Coordinator not found for module: %s", module)
        return

    _LOGGER.info("Refreshing module %s for entry %s", module, entry_id)
    if hasattr(coordinator, "async_request_refresh"):
        await coordinator.async_request_refresh()
        _LOGGER.debug("Refreshed coordinator: %s", module)


async def async_prefetch_apod_range(hass: HomeAssistant, call: ServiceCall) -> None:
    """Prefetch APOD images for a date range."""
    entry_id = call.data.get("entry_id")
    start_date = call.data.get("start_date")
    end_date = call.data.get("end_date")

    if not start_date or not end_date:
        _LOGGER.error("start_date and end_date required")
        return

    data = hass.data[DOMAIN].get(entry_id)
    if not data:
        _LOGGER.error("Config entry not found: %s", entry_id)
        return

    api_client = data["api_client"]

    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            try:
                await api_client.get_apod(date=date_str)
                _LOGGER.info("Prefetched APOD for %s", date_str)
            except Exception as err:
                _LOGGER.error("Failed to prefetch APOD for %s: %s", date_str, err)
            current += timedelta(days=1)
    except Exception as err:
        _LOGGER.error("Error prefetching APOD range: %s", err)


async def async_calculate_satellite_passes(hass: HomeAssistant, call: ServiceCall) -> None:
    """Calculate satellite passes for a time range."""
    entry_id = call.data.get("entry_id")
    norad_id = call.data.get("norad_id")
    hours = call.data.get("hours", 24)

    if not norad_id:
        _LOGGER.error("norad_id required")
        return

    data = hass.data[DOMAIN].get(entry_id)
    if not data:
        _LOGGER.error("Config entry not found: %s", entry_id)
        return

    # This would use the satellite tracker to calculate passes
    _LOGGER.info("Calculating passes for satellite %s over next %s hours", norad_id, hours)
