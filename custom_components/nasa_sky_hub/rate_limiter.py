"""Rate limiter for NASA API requests."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from .const import (
    PROFILE_AGGRESSIVE,
    PROFILE_BALANCED,
    PROFILE_CONSERVATIVE,
    RATE_LIMIT_DEGRADED_THRESHOLD,
    RATE_LIMIT_WARNING_THRESHOLD,
)

_LOGGER = logging.getLogger(__name__)


class RateLimiter:
    """Central rate limiter for NASA API requests."""

    def __init__(self, profile: str = "balanced") -> None:
        """Initialize rate limiter."""
        self.profile = profile
        self.remaining = 1000  # Default limit
        self.limit = 1000
        self.reset_time: datetime | None = None
        self._lock = asyncio.Lock()
        self._backoff_until: datetime | None = None
        self._consecutive_429s = 0

    async def acquire(self) -> bool:
        """Acquire permission to make a request."""
        async with self._lock:
            # Check if we're in backoff
            if self._backoff_until and datetime.now() < self._backoff_until:
                wait_time = (self._backoff_until - datetime.now()).total_seconds()
                _LOGGER.debug("Rate limiter in backoff, waiting %s seconds", wait_time)
                await asyncio.sleep(wait_time)
                self._backoff_until = None

            # Check remaining requests
            if self.remaining <= 0:
                if self.reset_time and datetime.now() < self.reset_time:
                    wait_time = (self.reset_time - datetime.now()).total_seconds()
                    _LOGGER.warning(
                        "Rate limit exhausted, waiting %s seconds until reset",
                        wait_time,
                    )
                    await asyncio.sleep(wait_time)
                else:
                    # Reset expired, assume we have requests again
                    self.remaining = self.limit

            # Check degraded mode threshold
            if self.remaining < RATE_LIMIT_DEGRADED_THRESHOLD:
                _LOGGER.warning(
                    "Rate limit degraded: %s remaining (threshold: %s)",
                    self.remaining,
                    RATE_LIMIT_DEGRADED_THRESHOLD,
                )
            elif self.remaining < RATE_LIMIT_WARNING_THRESHOLD:
                _LOGGER.info(
                    "Rate limit warning: %s remaining (threshold: %s)",
                    self.remaining,
                    RATE_LIMIT_WARNING_THRESHOLD,
                )

            return True

    async def record_response(self, headers: dict[str, Any]) -> None:
        """Record rate limit information from response headers."""
        async with self._lock:
            if "X-RateLimit-Remaining" in headers:
                try:
                    self.remaining = int(headers["X-RateLimit-Remaining"])
                except (ValueError, TypeError):
                    pass

            if "X-RateLimit-Limit" in headers:
                try:
                    self.limit = int(headers["X-RateLimit-Limit"])
                except (ValueError, TypeError):
                    pass

            if "X-RateLimit-Reset" in headers:
                try:
                    reset_timestamp = int(headers["X-RateLimit-Reset"])
                    self.reset_time = datetime.fromtimestamp(reset_timestamp)
                except (ValueError, TypeError):
                    pass

            # Reset consecutive 429s on successful request
            self._consecutive_429s = 0

    async def record_429(self) -> None:
        """Record a 429 Too Many Requests response."""
        async with self._lock:
            self._consecutive_429s += 1
            # Exponential backoff: 2^consecutive_429s minutes, max 60 minutes
            backoff_minutes = min(2 ** self._consecutive_429s, 60)
            self._backoff_until = datetime.now() + timedelta(minutes=backoff_minutes)
            _LOGGER.warning(
                "Rate limit 429 received, backing off for %s minutes",
                backoff_minutes,
            )

    def get_status(self) -> dict[str, Any]:
        """Get current rate limiter status."""
        return {
            "remaining": self.remaining,
            "limit": self.limit,
            "reset_time": self.reset_time.isoformat() if self.reset_time else None,
            "profile": self.profile,
            "in_backoff": (
                self._backoff_until is not None
                and datetime.now() < self._backoff_until
            ),
            "backoff_until": (
                self._backoff_until.isoformat() if self._backoff_until else None
            ),
        }
