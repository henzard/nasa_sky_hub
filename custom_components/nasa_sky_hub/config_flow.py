"""Config flow for NASA Sky Hub."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    ALL_MODULES,
    DOMAIN,
    MODULE_APOD,
    MODULE_EARTH_EVENTS,
    MODULE_SATELLITES,
    MODULE_SKY,
    MODULE_SPACE_WEATHER,
    PROFILE_BALANCED,
    PROFILE_CONSERVATIVE,
    PROFILE_AGGRESSIVE,
)

_LOGGER = logging.getLogger(__name__)


class NASASkyHubConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NASA Sky Hub."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow."""
        self.data: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            api_key = user_input.get(CONF_API_KEY, "").strip()
            if not api_key:
                errors[CONF_API_KEY] = "api_key_required"
            elif api_key == "DEMO_KEY":
                # Show warning but allow
                _LOGGER.warning(
                    "Using DEMO_KEY - rate limits are very restrictive. "
                    "Get a free API key at https://api.nasa.gov/"
                )

            if not errors:
                self.data.update(user_input)
                return await self.async_step_modules()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_KEY,
                        default=user_input.get(CONF_API_KEY, "") if user_input else "",
                        description={"suggested_value": "DEMO_KEY"},
                    ): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "api_key_url": "https://api.nasa.gov/",
            },
        )

    async def async_step_modules(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle module selection step."""
        if user_input is not None:
            self.data["enabled_modules"] = user_input.get("modules", [])
            self.data["profile"] = user_input.get("profile", PROFILE_BALANCED)
            return await self.async_step_location()

        # Default: enable all modules
        default_modules = ALL_MODULES

        return self.async_show_form(
            step_id="modules",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "modules",
                        default=default_modules,
                    ): cv.multi_select(
                        {
                            MODULE_SPACE_WEATHER: "Space Weather (DONKI)",
                            MODULE_APOD: "Astronomy Picture of the Day",
                            MODULE_EARTH_EVENTS: "Earth Events (EONET)",
                            MODULE_SATELLITES: "Satellite Tracking",
                            MODULE_SKY: "Sky Visibility",
                        }
                    ),
                    vol.Required(
                        "profile",
                        default=PROFILE_BALANCED,
                    ): vol.In(
                        {
                            PROFILE_CONSERVATIVE: "Conservative (fewer requests)",
                            PROFILE_BALANCED: "Balanced (recommended)",
                            PROFILE_AGGRESSIVE: "Aggressive (more frequent updates)",
                        }
                    ),
                }
            ),
            description_placeholders={
                "note": "Select which modules to enable. You can change this later in options.",
            },
        )

    async def async_step_location(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle location configuration step."""
        if user_input is not None:
            self.data["location"] = {
                CONF_LATITUDE: user_input.get(CONF_LATITUDE),
                CONF_LONGITUDE: user_input.get(CONF_LONGITUDE),
            }
            return self.async_create_entry(title="NASA Sky Hub", data=self.data)

        # Try to get location from HA config
        ha_lat = self.hass.config.latitude
        ha_lon = self.hass.config.longitude

        return self.async_show_form(
            step_id="location",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_LATITUDE,
                        default=ha_lat,
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_LONGITUDE,
                        default=ha_lon,
                    ): vol.Coerce(float),
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> NASASkyHubOptionsFlowHandler:
        """Get the options flow handler."""
        return NASASkyHubOptionsFlowHandler(config_entry)


class NASASkyHubOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for NASA Sky Hub."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        enabled_modules = self.config_entry.data.get("enabled_modules", [])
        intervals = {}

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "space_weather_interval",
                        default=1800,
                    ): vol.All(vol.Coerce(int), vol.Range(min=300, max=86400)),
                    vol.Optional(
                        "apod_interval",
                        default=86400,
                    ): vol.All(vol.Coerce(int), vol.Range(min=3600, max=86400)),
                    vol.Optional(
                        "satellites_interval",
                        default=180,
                    ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
                    vol.Optional(
                        "sky_interval",
                        default=300,
                    ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
                }
            ),
        )
