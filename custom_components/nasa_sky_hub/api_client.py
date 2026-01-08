"""NASA API client with rate limiting."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import NASA_API_BASE
from .rate_limiter import RateLimiter

_LOGGER = logging.getLogger(__name__)


class NASAApiError(Exception):
    """Base exception for NASA API errors."""


class NASAApiClient:
    """Client for NASA API requests."""

    def __init__(
        self,
        api_key: str,
        rate_limiter: RateLimiter,
        hass: Any,
    ) -> None:
        """Initialize NASA API client."""
        self.api_key = api_key
        self.rate_limiter = rate_limiter
        self.hass = hass
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def async_close(self) -> None:
        """Close the aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make an API request with rate limiting."""
        await self.rate_limiter.acquire()

        if params is None:
            params = {}
        params["api_key"] = self.api_key

        session = await self._get_session()
        url = f"{NASA_API_BASE}{endpoint}"

        try:
            async with session.request(method, url, params=params) as response:
                # Record rate limit info
                await self.rate_limiter.record_response(dict(response.headers))

                if response.status == 429:
                    await self.rate_limiter.record_429()
                    raise NASAApiError("Rate limit exceeded")

                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientError as err:
            _LOGGER.error("NASA API request failed: %s", err)
            raise NASAApiError(f"API request failed: {err}") from err

    async def get_apod(self, date: str | None = None) -> dict[str, Any]:
        """Get Astronomy Picture of the Day."""
        params = {}
        if date:
            params["date"] = date
        return await self._request("GET", "/planetary/apod", params)

    async def get_donki_flr(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Get DONKI Solar Flare data."""
        params = {
            "startDate": start_date,
            "endDate": end_date,
        }
        return await self._request("GET", "/DONKI/FLR", params)

    async def get_donki_cme(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Get DONKI CME data."""
        params = {
            "startDate": start_date,
            "endDate": end_date,
        }
        return await self._request("GET", "/DONKI/CME", params)

    async def get_donki_gst(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Get DONKI Geomagnetic Storm data."""
        params = {
            "startDate": start_date,
            "endDate": end_date,
        }
        return await self._request("GET", "/DONKI/GST", params)

    async def get_eonet_events(self, days: int = 30) -> dict[str, Any]:
        """Get EONET Earth events."""
        params = {"days": days}
        return await self._request("GET", "/EONET/events", params)

    async def get_neo_feed(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Get Near Earth Objects feed."""
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return await self._request("GET", "/neo/rest/v1/feed", params)
