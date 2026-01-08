"""NASA API client with rate limiting."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import EONET_API_BASE, NASA_API_BASE, SSD_API_BASE
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
        # Use actual API key for request, mask in logs
        params["api_key"] = self.api_key
        _LOGGER.debug("Request params: %s", {k: ("***" if k == "api_key" and v != "DEMO_KEY" else v) for k, v in params.items()})

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
        """Get EONET Earth events.
        
        EONET is accessed directly through eonet.gsfc.nasa.gov, not api.nasa.gov.
        It does not require an API key.
        """
        params = {"days": days}
        # EONET uses a different base URL and doesn't require API key
        session = await self._get_session()
        url = f"{EONET_API_BASE}/events"
        
        try:
            _LOGGER.debug("Making EONET API request: GET %s", url)
            async with session.request("GET", url, params=params) as response:
                _LOGGER.debug("EONET response status: %s", response.status)
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("EONET response received, data type: %s", type(data).__name__)
                return data
        except aiohttp.ClientError as err:
            _LOGGER.error("EONET API request failed: %s", err)
            raise NASAApiError(f"EONET API request failed: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error in EONET API request")
            raise NASAApiError(f"Unexpected error: {err}") from err

    async def get_neo_feed(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Get Near Earth Objects feed."""
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return await self._request("GET", "/neo/rest/v1/feed", params)

    async def _ssd_request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a request to SSD/CNEOS API (no API key required)."""
        _LOGGER.debug("Making SSD API request: GET %s", endpoint)
        # SSD APIs don't use rate limiting (they're separate from api.nasa.gov)
        # But we'll still use the session for connection pooling
        
        if params is None:
            params = {}
        
        session = await self._get_session()
        url = f"{SSD_API_BASE}{endpoint}"
        
        try:
            _LOGGER.debug("SSD request URL: %s", url)
            _LOGGER.debug("SSD request params: %s", params)
            async with session.request("GET", url, params=params) as response:
                _LOGGER.debug("SSD response status: %s", response.status)
                
                if response.status == 429:
                    _LOGGER.warning("Rate limit 429 received for %s", endpoint)
                    raise NASAApiError("Rate limit exceeded")
                
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("SSD response received, data type: %s", type(data).__name__)
                return data
                
        except aiohttp.ClientError as err:
            _LOGGER.error("SSD API request failed for %s: %s", endpoint, err)
            raise NASAApiError(f"SSD API request failed: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error in SSD API request to %s", endpoint)
            raise NASAApiError(f"Unexpected error: {err}") from err

    async def get_sentry_summary(
        self,
        ip_min: float | None = None,
        ps_min: int | None = None,
        h_max: float | None = None,
    ) -> dict[str, Any]:
        """Get Sentry impact risk summary (Mode S).
        
        Returns summary data for all Sentry-tracked asteroids with impact risk.
        """
        params = {}
        if ip_min is not None:
            params["ip-min"] = ip_min
        if ps_min is not None:
            params["ps-min"] = ps_min
        if h_max is not None:
            params["h-max"] = h_max
        return await self._ssd_request("/sentry.api", params)

    async def get_sentry_object(self, designation: str) -> dict[str, Any]:
        """Get Sentry impact risk details for a specific asteroid (Mode O).
        
        Args:
            designation: Asteroid designation (e.g., "99942" or "2000 SG344")
        """
        params = {"des": designation}
        return await self._ssd_request("/sentry.api", params)

    async def get_cad_close_approaches(
        self,
        date_min: str | None = None,
        date_max: str | None = None,
        dist_max: str | None = None,
        body: str = "Earth",
        neo: bool = True,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Get Close Approach Data (CAD) for asteroids/comets.
        
        Args:
            date_min: Minimum date (YYYY-MM-DD or "now")
            date_max: Maximum date (YYYY-MM-DD or "+60" for 60 days)
            dist_max: Maximum approach distance (e.g., "0.05" AU or "10LD")
            body: Target body (Earth, Moon, Mars, etc.)
            neo: Filter to NEOs only
            limit: Limit number of results
        """
        params = {}
        if date_min:
            params["date-min"] = date_min
        if date_max:
            params["date-max"] = date_max
        if dist_max:
            params["dist-max"] = dist_max
        params["body"] = body
        if neo:
            params["neo"] = "true"
        if limit:
            params["limit"] = limit
        return await self._ssd_request("/cad.api", params)
