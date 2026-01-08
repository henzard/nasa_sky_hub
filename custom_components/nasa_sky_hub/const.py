"""Constants for NASA Sky Hub integration."""
from __future__ import annotations

DOMAIN = "nasa_sky_hub"

# NASA API endpoints
NASA_API_BASE = "https://api.nasa.gov"
APOD_ENDPOINT = f"{NASA_API_BASE}/planetary/apod"
DONKI_ENDPOINT = f"{NASA_API_BASE}/DONKI"
# EONET is accessed directly, not through api.nasa.gov
EONET_API_BASE = "https://eonet.gsfc.nasa.gov/api/v3"
EONET_ENDPOINT = f"{EONET_API_BASE}/events"
EPIC_ENDPOINT = f"{NASA_API_BASE}/EPIC"
NEO_ENDPOINT = f"{NASA_API_BASE}/neo/rest/v1"

# Celestrak endpoints
CELESTRAK_BASE = "https://celestrak.org/NORAD/elements"
CELESTRAK_TLE_URL = f"{CELESTRAK_BASE}/stations.txt"

# SSD/CNEOS endpoints (JPL, no API key required)
SSD_API_BASE = "https://ssd-api.jpl.nasa.gov"
SSD_SENTRY_ENDPOINT = f"{SSD_API_BASE}/sentry.api"
SSD_CAD_ENDPOINT = f"{SSD_API_BASE}/cad.api"

# Module names
MODULE_SPACE_WEATHER = "space_weather"
MODULE_APOD = "apod"
MODULE_EARTH_EVENTS = "earth_events"
MODULE_SATELLITES = "satellites"
MODULE_SKY = "sky"
MODULE_ASTEROIDS = "asteroids"

ALL_MODULES = [
    MODULE_SPACE_WEATHER,
    MODULE_APOD,
    MODULE_EARTH_EVENTS,
    MODULE_SATELLITES,
    MODULE_SKY,
    MODULE_ASTEROIDS,
]

# Rate limit profiles
PROFILE_CONSERVATIVE = "conservative"
PROFILE_BALANCED = "balanced"
PROFILE_AGGRESSIVE = "aggressive"

# Default polling intervals (seconds)
DEFAULT_INTERVALS = {
    PROFILE_CONSERVATIVE: {
        MODULE_SPACE_WEATHER: 3600,  # 1 hour
        MODULE_APOD: 86400,  # 24 hours
        MODULE_EARTH_EVENTS: 7200,  # 2 hours
        MODULE_SATELLITES: 300,  # 5 minutes
        MODULE_SKY: 600,  # 10 minutes
        MODULE_ASTEROIDS: 3600,  # 1 hour
    },
    PROFILE_BALANCED: {
        MODULE_SPACE_WEATHER: 1800,  # 30 minutes
        MODULE_APOD: 86400,  # 24 hours
        MODULE_EARTH_EVENTS: 3600,  # 1 hour
        MODULE_SATELLITES: 180,  # 3 minutes
        MODULE_SKY: 300,  # 5 minutes
        MODULE_ASTEROIDS: 1800,  # 30 minutes
    },
    PROFILE_AGGRESSIVE: {
        MODULE_SPACE_WEATHER: 900,  # 15 minutes
        MODULE_APOD: 86400,  # 24 hours
        MODULE_EARTH_EVENTS: 1800,  # 30 minutes
        MODULE_SATELLITES: 60,  # 1 minute
        MODULE_SKY: 180,  # 3 minutes
        MODULE_ASTEROIDS: 900,  # 15 minutes
    },
}

# Rate limit thresholds
RATE_LIMIT_WARNING_THRESHOLD = 100
RATE_LIMIT_DEGRADED_THRESHOLD = 50

# Space weather severity levels
SEVERITY_QUIET = "quiet"
SEVERITY_ELEVATED = "elevated"
SEVERITY_STORM = "storm"
SEVERITY_SEVERE = "severe"

# Solar flare classes
FLARE_CLASS_C = "C"
FLARE_CLASS_M = "M"
FLARE_CLASS_X = "X"

# Satellite NORAD IDs
ISS_NORAD_ID = 25544
