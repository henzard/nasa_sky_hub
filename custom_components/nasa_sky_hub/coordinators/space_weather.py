"""Space Weather coordinator."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..api_client import NASAApiClient, NASAApiError
from ..const import MODULE_SPACE_WEATHER, SEVERITY_ELEVATED, SEVERITY_QUIET, SEVERITY_SEVERE, SEVERITY_STORM

_LOGGER = logging.getLogger(__name__)


class SpaceWeatherCoordinator(DataUpdateCoordinator):
    """Coordinator for space weather data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: NASAApiClient,
        update_interval: int = 1800,
    ) -> None:
        """Initialize space weather coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=MODULE_SPACE_WEATHER,
            update_interval=timedelta(seconds=update_interval),
        )
        self.api_client = api_client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch space weather data."""
        _LOGGER.info("Fetching space weather data")
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=3)
            _LOGGER.debug("Fetching data from %s to %s", start_date.date(), end_date.date())

            # Fetch flares, CMEs, and geomagnetic storms
            flares = await self.api_client.get_donki_flr(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
            cmes = await self.api_client.get_donki_cme(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
            storms = await self.api_client.get_donki_gst(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )

            # Process flares
            now_utc = datetime.now(timezone.utc)
            recent_flares = [
                f for f in flares
                if datetime.fromisoformat(f.get("beginTime", "").replace("Z", "+00:00")) >
                (now_utc - timedelta(hours=24))
            ]

            # Determine severity
            severity = SEVERITY_QUIET
            x_flares = [f for f in recent_flares if f.get("classType", "").startswith("X")]
            m_flares = [f for f in recent_flares if f.get("classType", "").startswith("M")]

            active_storms = [
                s for s in storms
                if datetime.fromisoformat(s.get("startTime", "").replace("Z", "+00:00")) <= now_utc
                and datetime.fromisoformat(s.get("endTime", "").replace("Z", "+00:00")) >= now_utc
            ]

            if x_flares or (active_storms and any(s.get("allKpIndex", [{}])[0].get("kpIndex", 0) >= 8 for s in active_storms)):
                severity = SEVERITY_SEVERE
            elif m_flares or (active_storms and any(s.get("allKpIndex", [{}])[0].get("kpIndex", 0) >= 6 for s in active_storms)):
                severity = SEVERITY_STORM
            elif recent_flares or active_storms:
                severity = SEVERITY_ELEVATED

            result = {
                "severity": severity,
                "flares_24h": len(recent_flares),
                "flares": recent_flares,
                "cmes": cmes,
                "storms": active_storms,
                "last_update": now_utc.isoformat(),
            }
            _LOGGER.info("Space weather data fetched: severity=%s, flares_24h=%s", severity, len(recent_flares))
            return result

        except NASAApiError as err:
            _LOGGER.error("NASA API error fetching space weather: %s", err)
            raise UpdateFailed(f"Error fetching space weather data: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching space weather data")
            raise UpdateFailed(f"Unexpected error: {err}") from err