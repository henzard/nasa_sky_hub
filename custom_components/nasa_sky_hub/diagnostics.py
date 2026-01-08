"""Diagnostics for NASA Sky Hub."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return comprehensive diagnostics for a config entry."""
    _LOGGER.info("Generating diagnostics for entry %s", entry.entry_id)
    
    data = hass.data[DOMAIN].get(entry.entry_id, {})
    
    # Get all entities for this integration
    entity_registry = er.async_get(hass)
    entities = []
    for entity_entry in entity_registry.entities.values():
        if entity_entry.config_entry_id == entry.entry_id:
            entity_state = hass.states.get(entity_entry.entity_id)
            entities.append({
                "entity_id": entity_entry.entity_id,
                "unique_id": entity_entry.unique_id,
                "name": entity_entry.name,
                "platform": entity_entry.platform,
                "disabled": entity_entry.disabled,
                "state": entity_state.state if entity_state else "unknown",
                "attributes": dict(entity_state.attributes) if entity_state else {},
            })

    # Get coordinator statuses
    coordinators_status = {}
    if "coordinators" in data:
        for name, coordinator in data["coordinators"].items():
            if hasattr(coordinator, "data"):
                coordinators_status[name] = {
                    "last_update": coordinator.data.get("last_update") if isinstance(coordinator.data, dict) else None,
                    "has_data": coordinator.data is not None,
                }

    diagnostics = {
        "integration": {
            "domain": DOMAIN,
            "version": "1.0.0",
            "entry_id": entry.entry_id,
            "title": entry.title,
        },
        "config_entry": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "data": {
                "api_key": "***SET***" if entry.data.get("api_key") else "NOT SET",
                "api_key_is_demo": entry.data.get("api_key") == "DEMO_KEY",
                "location": entry.data.get("location", {}),
                "enabled_modules": entry.data.get("enabled_modules", []),
                "profile": entry.data.get("profile", "balanced"),
            },
            "options": dict(entry.options) if entry.options else {},
        },
        "entities": {
            "count": len(entities),
            "list": entities,
        },
        "rate_limiter": {},
        "api_status": {},
        "coordinators": coordinators_status,
        "platforms": {
            "registered": list(data.get("coordinators", {}).keys()),
        },
    }

    if "rate_limiter" in data:
        diagnostics["rate_limiter"] = data["rate_limiter"].get_status()

    if "api_client" in data:
        diagnostics["api_status"] = {
            "api_key_set": bool(entry.data.get("api_key")),
            "api_key_is_demo": entry.data.get("api_key") == "DEMO_KEY",
            "session_active": data["api_client"]._session is not None,
        }

    _LOGGER.info("Diagnostics generated: %s entities found", len(entities))
    return diagnostics
