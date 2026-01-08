"""APOD coordinator."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..api_client import NASAApiClient, NASAApiError
from ..const import MODULE_APOD

_LOGGER = logging.getLogger(__name__)


class APODCoordinator(DataUpdateCoordinator):
    """Coordinator for Astronomy Picture of the Day."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: NASAApiClient,
        update_interval: int = 86400,
    ) -> None:
        """Initialize APOD coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=MODULE_APOD,
            update_interval=timedelta(seconds=update_interval),
        )
        self.api_client = api_client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch APOD data."""
        try:
            data = await self.api_client.get_apod()
            return {
                "title": data.get("title", ""),
                "date": data.get("date", ""),
                "explanation": data.get("explanation", ""),
                "url": data.get("url", ""),
                "hdurl": data.get("hdurl", ""),
                "media_type": data.get("media_type", "image"),
                "last_update": datetime.now(timezone.utc).isoformat(),
            }
        except NASAApiError as err:
            raise UpdateFailed(f"Error fetching APOD data: {err}") from err
