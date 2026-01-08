"""Satellite tracking coordinator."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..api_client import NASAApiClient
from ..const import CELESTRAK_TLE_URL, ISS_NORAD_ID, MODULE_SATELLITES
from ..satellite_tracker import SatelliteTracker

_LOGGER = logging.getLogger(__name__)


class SatelliteCoordinator(DataUpdateCoordinator):
    """Coordinator for satellite tracking."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: NASAApiClient,
        location: dict[str, float],
        update_interval: int = 180,
    ) -> None:
        """Initialize satellite coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=MODULE_SATELLITES,
            update_interval=timedelta(seconds=update_interval),
        )
        self.api_client = api_client
        self.location = location
        self.tracker = SatelliteTracker(
            latitude=location.get("latitude", 0),
            longitude=location.get("longitude", 0),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch satellite tracking data."""
        try:
            # Update TLEs if needed (cache for 24 hours)
            await self.tracker.update_tles_if_needed()

            # Get current satellite positions
            now = datetime.now()
            satellites = await self.tracker.get_visible_satellites(now)

            # Find ISS specifically
            iss_data = None
            for sat in satellites:
                if sat.get("norad_id") == ISS_NORAD_ID:
                    iss_data = sat
                    break

            # Find next pass
            next_pass = await self.tracker.get_next_pass(ISS_NORAD_ID, now)

            return {
                "satellites_overhead": len(satellites),
                "satellites": satellites,
                "iss_overhead": iss_data is not None,
                "iss_data": iss_data,
                "next_pass": next_pass,
                "last_update": now.isoformat(),
            }

        except Exception as err:
            raise UpdateFailed(f"Error fetching satellite data: {err}") from err
