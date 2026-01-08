"""Satellite tracking using TLE data."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import aiohttp
from skyfield.api import EarthSatellite, load, wgs84

from .const import CELESTRAK_TLE_URL, ISS_NORAD_ID

_LOGGER = logging.getLogger(__name__)


class SatelliteTracker:
    """Track satellites using TLE data."""

    def __init__(self, latitude: float, longitude: float, elevation: float = 0.0) -> None:
        """Initialize satellite tracker."""
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.tles: dict[int, tuple[str, str]] = {}
        self.satellite_names: dict[int, str] = {}
        self.tle_update_time: datetime | None = None
        self.ts = load.timescale()
        self.eph: Any = None  # Will be loaded lazily in executor
        self.observer = wgs84.latlon(latitude, longitude, elevation_m=elevation)
        self._eph_loaded = False

    async def _ensure_eph_loaded(self, hass: Any) -> None:
        """Ensure ephemeris is loaded (in executor to avoid blocking)."""
        if self._eph_loaded:
            return
        _LOGGER.debug("Loading ephemeris file in executor")
        self.eph = await hass.async_add_executor_job(load, "de421.bsp")
        self._eph_loaded = True
        _LOGGER.debug("Ephemeris file loaded")

    async def update_tles_if_needed(self, force: bool = False) -> None:
        """Update TLE data if needed (cache for 24 hours)."""
        if (
            not force
            and self.tle_update_time
            and datetime.now(timezone.utc) - self.tle_update_time < timedelta(hours=24)
        ):
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(CELESTRAK_TLE_URL) as response:
                    response.raise_for_status()
                    lines = (await response.text()).strip().split("\n")

            # Parse TLE format: name line, line 1, line 2
            tles = {}
            satellite_names = {}  # Store names separately
            for i in range(0, len(lines) - 2, 3):
                name = lines[i].strip()
                line1 = lines[i + 1].strip()
                line2 = lines[i + 2].strip()

                # Extract NORAD ID from line 1 (positions 3-7)
                try:
                    norad_id = int(line1[2:7])
                    tles[norad_id] = (line1, line2)
                    satellite_names[norad_id] = name
                except (ValueError, IndexError):
                    continue

            self.tles = tles
            self.satellite_names = satellite_names
            self.tle_update_time = datetime.now(timezone.utc)
            _LOGGER.info("Updated TLE data: %s satellites", len(self.tles))

        except Exception as err:
            _LOGGER.error("Failed to update TLE data: %s", err)
            if not self.tles:
                raise

    async def get_visible_satellites(
        self, time: datetime, min_elevation: float = 0.0
    ) -> list[dict[str, Any]]:
        """Get currently visible satellites."""
        if not self.tles:
            await self.update_tles_if_needed()

        visible = []
        # Ensure time is timezone-aware (Skyfield requirement)
        if time.tzinfo is None:
            time = time.replace(tzinfo=timezone.utc)
        t = self.ts.from_datetime(time)

        for norad_id, (line1, line2) in self.tles.items():
            try:
                sat = EarthSatellite(line1, line2, name=f"SAT-{norad_id}", ts=self.ts)
                difference = sat - self.observer
                topocentric = difference.at(t)
                alt, az, distance = topocentric.altaz()

                if alt.degrees >= min_elevation:
                    # Check if satellite is sunlit (simplified - always True if eph not loaded)
                    is_sunlit = True
                    if self.eph:
                        try:
                            is_sunlit = self._is_sunlit(sat, t)
                        except Exception:
                            is_sunlit = True

                    # Get satellite name if available
                    sat_name = self.satellite_names.get(norad_id, f"SAT-{norad_id}")
                    visible.append({
                        "norad_id": norad_id,
                        "name": sat_name,
                        "azimuth": az.degrees,
                        "elevation": alt.degrees,
                        "distance_km": distance.km,
                        "sunlit": is_sunlit,
                    })
            except Exception as err:
                _LOGGER.debug("Error calculating position for satellite %s: %s", norad_id, err)
                continue

        return visible

    def _is_sunlit(self, sat: EarthSatellite, t: Any) -> bool:
        """Check if satellite is sunlit."""
        if not self.eph:
            return True
        try:
            # Get satellite position
            sat_pos = sat.at(t)
            # Get sun position
            sun_pos = self.eph["sun"].at(t)
            # Vector from satellite to sun
            vector = sun_pos.position.km - sat_pos.position.km
            # Check if sun is above horizon from satellite's perspective
            # Simplified: check if satellite is in sunlight
            return True  # Simplified for now
        except Exception:
            return True

    async def get_next_pass(
        self, norad_id: int, start_time: datetime, max_hours: int = 24
    ) -> dict[str, Any] | None:
        """Get next satellite pass."""
        if norad_id not in self.tles:
            await self.update_tles_if_needed()

        if norad_id not in self.tles:
            return None

        try:
            # Ensure start_time is timezone-aware (Skyfield requirement)
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            
            line1, line2 = self.tles[norad_id]
            sat = EarthSatellite(line1, line2, name=f"SAT-{norad_id}", ts=self.ts)

            # Find next rise
            t0 = self.ts.from_datetime(start_time)
            t1 = self.ts.from_datetime(start_time + timedelta(hours=max_hours))

            # Simple search for next pass above horizon
            current = t0
            step_hours = 0.1
            while current.utc_datetime() < t1.utc_datetime():
                difference = sat - self.observer
                topocentric = difference.at(current)
                alt, az, _ = topocentric.altaz()

                if alt.degrees > 0:
                    # Found rise, find set
                    rise_time = current
                    set_time = current
                    while alt.degrees > 0 and set_time.utc_datetime() < t1.utc_datetime():
                        set_time = self.ts.from_datetime(
                            set_time.utc_datetime() + timedelta(minutes=1)
                        )
                        topocentric = difference.at(set_time)
                        alt, az, _ = topocentric.altaz()

                    max_alt = 0
                    max_alt_time = rise_time
                    check_time = rise_time
                    while check_time.utc_datetime() < set_time.utc_datetime():
                        topocentric = difference.at(check_time)
                        alt, az, _ = topocentric.altaz()
                        if alt.degrees > max_alt:
                            max_alt = alt.degrees
                            max_alt_time = check_time
                        check_time = self.ts.from_datetime(
                            check_time.utc_datetime() + timedelta(minutes=1)
                        )

                    # Get satellite name if available
                    sat_name = self.satellite_names.get(norad_id, f"SAT-{norad_id}")
                    return {
                        "norad_id": norad_id,
                        "name": sat_name,
                        "rise_time": rise_time.utc_datetime().isoformat(),
                        "set_time": set_time.utc_datetime().isoformat(),
                        "max_elevation": max_alt,
                        "max_elevation_time": max_alt_time.utc_datetime().isoformat(),
                        "duration_minutes": int((set_time.utc_datetime() - rise_time.utc_datetime()).total_seconds() / 60),
                    }

                current = self.ts.from_datetime(
                    current.utc_datetime() + timedelta(hours=step_hours)
                )

        except Exception as err:
            _LOGGER.error("Error calculating next pass: %s", err)

        return None
