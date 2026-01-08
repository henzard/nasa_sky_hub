"""Sky visibility coordinator."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
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
        try:
            # Ensure ephemeris is loaded (in executor to avoid blocking)
            await self.calculator._ensure_eph_loaded(self.hass)
            now = datetime.now()

            # Calculate various sky conditions
            is_astronomical_night = self.calculator.is_astronomical_night(now)
            darkness_level = self.calculator.get_darkness_level(now)
            visible_constellations = self.calculator.get_visible_constellations(now)
            brightest_object = self.calculator.get_brightest_object(now)
            sidereal_time = self.calculator.get_sidereal_time(now)

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
            raise UpdateFailed(f"Error calculating sky data: {err}") from err
