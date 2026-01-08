"""Diagnostics for NASA Sky Hub."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = hass.data[DOMAIN].get(entry.entry_id, {})

    diagnostics = {
        "config_entry": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "data": {
                "api_key": "***" if entry.data.get("api_key") else None,
                "location": entry.data.get("location", {}),
                "enabled_modules": entry.data.get("enabled_modules", []),
                "profile": entry.data.get("profile", "balanced"),
            },
        },
        "rate_limiter": {},
        "api_status": {},
    }

    if "rate_limiter" in data:
        diagnostics["rate_limiter"] = data["rate_limiter"].get_status()

    if "api_client" in data:
        diagnostics["api_status"] = {
            "api_key_set": bool(entry.data.get("api_key")),
            "api_key_is_demo": entry.data.get("api_key") == "DEMO_KEY",
        }

    return diagnostics
