"""Sky visibility calculations."""
from __future__ import annotations

import logging
from datetime import datetime
from math import acos, cos, degrees, radians, sin
from typing import Any

from skyfield.api import load, wgs84

_LOGGER = logging.getLogger(__name__)


class SkyCalculator:
    """Calculate sky visibility conditions."""

    def __init__(self, latitude: float, longitude: float, elevation: float = 0.0) -> None:
        """Initialize sky calculator."""
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.ts = load.timescale()
        self.eph = load("de421.bsp")
        self.observer = wgs84.latlon(latitude, longitude, elevation_m=elevation)

        # Bright stars (simplified catalog)
        self.bright_stars = [
            {"name": "Sirius", "ra": 6.7525, "dec": -16.7161, "mag": -1.46},
            {"name": "Canopus", "ra": 6.3992, "dec": -52.6956, "mag": -0.74},
            {"name": "Arcturus", "ra": 14.2610, "dec": 19.1824, "mag": -0.05},
            {"name": "Vega", "ra": 18.6156, "dec": 38.7837, "mag": 0.03},
            {"name": "Capella", "ra": 5.2782, "dec": 45.9980, "mag": 0.08},
            {"name": "Rigel", "ra": 5.2423, "dec": -8.2016, "mag": 0.18},
            {"name": "Procyon", "ra": 7.6550, "dec": 5.2249, "mag": 0.40},
            {"name": "Betelgeuse", "ra": 5.9195, "dec": 7.4071, "mag": 0.45},
        ]

        # Major constellations (simplified)
        self.constellations = [
            {"name": "Orion", "ra": 5.5, "dec": 5.0},
            {"name": "Ursa Major", "ra": 11.0, "dec": 50.0},
            {"name": "Cassiopeia", "ra": 1.0, "dec": 60.0},
            {"name": "Cygnus", "ra": 20.5, "dec": 45.0},
            {"name": "Lyra", "ra": 18.8, "dec": 36.8},
            {"name": "Scorpius", "ra": 16.9, "dec": -30.0},
            {"name": "Leo", "ra": 10.7, "dec": 13.0},
            {"name": "Taurus", "ra": 4.5, "dec": 16.5},
        ]

    def get_sidereal_time(self, time: datetime) -> str:
        """Calculate local sidereal time."""
        t = self.ts.from_datetime(time)
        lst = self.observer.lst_hours_at(t)
        hours = int(lst)
        minutes = int((lst - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

    def is_astronomical_night(self, time: datetime) -> bool:
        """Check if it's astronomical night (sun 18° below horizon)."""
        t = self.ts.from_datetime(time)
        astro = self.eph["sun"] + self.observer
        sun_alt, _, _ = astro.at(t).observe(self.eph["earth"]).apparent().altaz()
        return sun_alt.degrees < -18.0

    def get_darkness_level(self, time: datetime) -> float:
        """Get darkness level (0.0 = daylight, 1.0 = darkest)."""
        t = self.ts.from_datetime(time)
        astro = self.eph["sun"] + self.observer
        sun_alt, _, _ = astro.at(t).observe(self.eph["earth"]).apparent().altaz()

        # Map sun altitude to darkness level
        if sun_alt.degrees > 0:
            return 0.0
        elif sun_alt.degrees > -6:
            # Civil twilight
            return 0.3
        elif sun_alt.degrees > -12:
            # Nautical twilight
            return 0.6
        elif sun_alt.degrees > -18:
            # Astronomical twilight
            return 0.8
        else:
            # Astronomical night
            return 1.0

    def get_visible_constellations(self, time: datetime) -> list[str]:
        """Get list of currently visible constellations."""
        visible = []
        t = self.ts.from_datetime(time)

        for const in self.constellations:
            # Convert RA/Dec to altitude
            # Simplified calculation
            lst_hours = self.observer.lst_hours_at(t)
            ha = lst_hours - const["ra"]
            dec_rad = radians(const["dec"])
            lat_rad = radians(self.latitude)
            ha_rad = radians(ha * 15)

            sin_alt = sin(dec_rad) * sin(lat_rad) + cos(dec_rad) * cos(lat_rad) * cos(ha_rad)
            alt = degrees(acos(max(-1, min(1, sin_alt))))

            if alt > 10:  # Above horizon
                visible.append(const["name"])

        return visible

    def get_brightest_object(self, time: datetime) -> dict[str, Any]:
        """Get brightest object currently visible."""
        t = self.ts.from_datetime(time)
        brightest = None
        max_mag = float("inf")

        # Check moon
        moon = self.eph["moon"]
        moon_alt, _, _ = self.observer.at(t).observe(moon).apparent().altaz()
        if moon_alt.degrees > 0:
            # Moon is very bright
            moon_mag = -12.6  # Full moon magnitude
            if moon_mag < max_mag:
                max_mag = moon_mag
                brightest = {"name": "Moon", "type": "moon", "magnitude": moon_mag}

        # Check bright stars
        for star in self.bright_stars:
            lst_hours = self.observer.lst_hours_at(t)
            ha = lst_hours - star["ra"]
            dec_rad = radians(star["dec"])
            lat_rad = radians(self.latitude)
            ha_rad = radians(ha * 15)

            sin_alt = sin(dec_rad) * sin(lat_rad) + cos(dec_rad) * cos(lat_rad) * cos(ha_rad)
            alt = degrees(acos(max(-1, min(1, sin_alt))))

            if alt > 10 and star["mag"] < max_mag:
                max_mag = star["mag"]
                brightest = {
                    "name": star["name"],
                    "type": "star",
                    "magnitude": star["mag"],
                    "altitude": alt,
                }

        return brightest or {"name": "None", "type": "none", "magnitude": 0}
