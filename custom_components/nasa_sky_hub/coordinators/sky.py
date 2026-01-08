"""Sky visibility coordinator."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import MODULE_SKY
from ..sky_calculator import SkyCalculator

_LOGGER = logging.getLogger(__name__)


class SkyCoordinator(DataUpdateCoordinator):
    """Coordinator for sky visibility calculations."""

    def __init__(
        self,
        hass: HomeAssistant,
        location: dict[str, float],
        update_interval: int = 300,
    ) -> None:
        """Initialize sky coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=MODULE_SKY,
            update_interval=timedelta(seconds=update_interval),
        )
        self.location = location
        self.calculator = SkyCalculator(
            latitude=location.get("latitude", 0),
            longitude=location.get("longitude", 0),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Calculate sky visibility data."""
        now = datetime.now(timezone.utc)
        
        # Return default values if calculator fails
        default_data = {
            "astronomical_night": False,
            "darkness_level": 0.0,
            "visible_constellations": [],
            "brightest_object": {"name": "Unknown", "type": "none", "magnitude": 0},
            "sidereal_time": "00:00:00",
            "good_stargazing": False,
            "last_update": now.isoformat(),
        }
        
        try:
            # Ensure ephemeris is loaded (in executor to avoid blocking)
            await self.calculator._ensure_eph_loaded(self.hass)
            
            if not self.calculator.eph:
                _LOGGER.warning("Ephemeris not loaded, returning default sky data")
                return default_data

            # Calculate various sky conditions with error handling
            try:
                is_astronomical_night = self.calculator.is_astronomical_night(now)
            except Exception as err:
                _LOGGER.warning("Error calculating astronomical night: %s", err)
                is_astronomical_night = False
                
            try:
                darkness_level = self.calculator.get_darkness_level(now)
            except Exception as err:
                _LOGGER.warning("Error calculating darkness level: %s", err)
                darkness_level = 0.0
                
            try:
                visible_constellations = self.calculator.get_visible_constellations(now)
            except Exception as err:
                _LOGGER.warning("Error calculating visible constellations: %s", err)
                visible_constellations = []
                
            try:
                brightest_object = self.calculator.get_brightest_object(now)
            except Exception as err:
                _LOGGER.warning("Error calculating brightest object: %s", err)
                brightest_object = {"name": "Unknown", "type": "none", "magnitude": 0}
                
            try:
                sidereal_time = self.calculator.get_sidereal_time(now)
            except Exception as err:
                _LOGGER.warning("Error calculating sidereal time: %s", err)
                sidereal_time = "00:00:00"

            # Determine if conditions are good for stargazing
            good_conditions = (
                is_astronomical_night
                and darkness_level > 0.7
                and len(visible_constellations) > 5
            )

            return {
                "astronomical_night": is_astronomical_night,
                "darkness_level": darkness_level,
                "visible_constellations": visible_constellations,
                "brightest_object": brightest_object,
                "sidereal_time": sidereal_time,
                "good_stargazing": good_conditions,
                "last_update": now.isoformat(),
            }

        except Exception as err:
            _LOGGER.error("Error in sky coordinator update: %s", err, exc_info=True)
            # Return default data instead of raising UpdateFailed
            # This allows entities to register and show as unavailable rather than not existing
            return default_data
