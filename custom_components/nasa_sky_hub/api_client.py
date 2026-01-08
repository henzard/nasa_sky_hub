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
        _LOGGER.debug("Making API request: %s %s", method, endpoint)
        await self.rate_limiter.acquire()

        if params is None:
            params = {}
        params["api_key"] = "***" if self.api_key != "DEMO_KEY" else "DEMO_KEY"
        _LOGGER.debug("Request params: %s", {k: v for k, v in params.items() if k != "api_key"})

        session = await self._get_session()
        url = f"{NASA_API_BASE}{endpoint}"

        try:
            _LOGGER.debug("Request URL: %s", url)
            async with session.request(method, url, params=params) as response:
                _LOGGER.debug("Response status: %s", response.status)
                # Record rate limit info
                await self.rate_limiter.record_response(dict(response.headers))
                _LOGGER.debug("Rate limit remaining: %s", self.rate_limiter.remaining)

                if response.status == 429:
                    _LOGGER.warning("Rate limit 429 received for %s", endpoint)
                    await self.rate_limiter.record_429()
                    raise NASAApiError("Rate limit exceeded")

                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Response received, data type: %s", type(data).__name__)
                return data

        except aiohttp.ClientError as err:
            _LOGGER.error("NASA API request failed for %s: %s", endpoint, err)
            raise NASAApiError(f"API request failed: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error in API request to %s", endpoint)
            raise NASAApiError(f"Unexpected error: {err}") from err

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
