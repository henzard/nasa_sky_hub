"""Asteroid tracking coordinators (Sentry and CAD)."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..api_client import NASAApiClient, NASAApiError
from ..const import MODULE_ASTEROIDS

_LOGGER = logging.getLogger(__name__)


class SentryCoordinator(DataUpdateCoordinator):
    """Coordinator for Sentry impact risk data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: NASAApiClient,
        update_interval: int = 1800,
    ) -> None:
        """Initialize Sentry coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{MODULE_ASTEROIDS}_sentry",
            update_interval=timedelta(seconds=update_interval),
        )
        self.api_client = api_client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch Sentry impact risk data."""
        _LOGGER.info("Fetching Sentry impact risk data")
        try:
            # Get summary of all Sentry-tracked objects (Mode S)
            # Filter to objects with Palermo Scale >= -3 (moderate risk or higher)
            data = await self.api_client.get_sentry_summary(ps_min=-3)
            
            now_utc = datetime.now(timezone.utc)
            
            # Process Sentry data
            sentry_objects = data.get("data", [])
            
            # Find highest risk objects
            highest_risk = None
            max_ps = -999
            total_threats = len(sentry_objects)
            
            for obj in sentry_objects:
                ps_cum = float(obj.get("ps_cum", "-999"))
                if ps_cum > max_ps:
                    max_ps = ps_cum
                    highest_risk = obj
            
            result = {
                "total_threats": total_threats,
                "highest_risk": highest_risk,
                "max_palermo_scale": max_ps,
                "objects": sentry_objects,
                "last_update": now_utc.isoformat(),
            }
            
            _LOGGER.info(
                "Sentry data fetched: %s threats, max PS=%.2f",
                total_threats,
                max_ps,
            )
            return result

        except NASAApiError as err:
            _LOGGER.error("NASA API error fetching Sentry data: %s", err)
            # Return default data instead of raising to allow retries
            return {
                "count": 0,
                "threats": [],
                "last_update": datetime.now(timezone.utc).isoformat(),
                "error": str(err),
            }
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching Sentry data")
            # Return default data instead of raising to allow retries
            return {
                "count": 0,
                "threats": [],
                "last_update": datetime.now(timezone.utc).isoformat(),
                "error": str(err),
            }


class CADCoordinator(DataUpdateCoordinator):
    """Coordinator for Close Approach Data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: NASAApiClient,
        update_interval: int = 1800,
    ) -> None:
        """Initialize CAD coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{MODULE_ASTEROIDS}_cad",
            update_interval=timedelta(seconds=update_interval),
        )
        self.api_client = api_client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch Close Approach Data."""
        _LOGGER.info("Fetching Close Approach Data")
        try:
            now_utc = datetime.now(timezone.utc)
            date_min = "now"
            # Get approaches in next 60 days
            date_max = "+60"
            # Get approaches within 10 lunar distances (about 0.025 AU)
            dist_max = "10LD"
            
            data = await self.api_client.get_cad_close_approaches(
                date_min=date_min,
                date_max=date_max,
                dist_max=dist_max,
                body="Earth",
                neo=True,
                limit=50,  # Limit to top 50 closest approaches
            )
            
            # Process CAD data
            approaches = []
            fields = data.get("fields", [])
            cad_data = data.get("data", [])
            
            # Parse field indices
            field_map = {field: idx for idx, field in enumerate(fields)}
            
            for entry in cad_data:
                if len(entry) > 0:
                    approach = {
                        "designation": entry[field_map.get("des", 0)] if "des" in field_map else None,
                        "approach_date": entry[field_map.get("cd", 3)] if "cd" in field_map else None,
                        "distance_au": float(entry[field_map.get("dist", 4)]) if "dist" in field_map and entry[field_map.get("dist", 4)] else None,
                        "distance_min_au": float(entry[field_map.get("dist_min", 5)]) if "dist_min" in field_map and entry[field_map.get("dist_min", 5)] else None,
                        "distance_max_au": float(entry[field_map.get("dist_max", 6)]) if "dist_max" in field_map and entry[field_map.get("dist_max", 6)] else None,
                        "velocity_km_s": float(entry[field_map.get("v_rel", 7)]) if "v_rel" in field_map and entry[field_map.get("v_rel", 7)] else None,
                        "absolute_magnitude": float(entry[field_map.get("h", 10)]) if "h" in field_map and entry[field_map.get("h", 10)] else None,
                    }
                    approaches.append(approach)
            
            # Sort by distance (closest first)
            approaches.sort(key=lambda x: x.get("distance_au") or float("inf"))
            
            # Find next approach
            next_approach = approaches[0] if approaches else None
            
            result = {
                "total_approaches": len(approaches),
                "next_approach": next_approach,
                "approaches": approaches[:10],  # Keep top 10 for attributes
                "last_update": now_utc.isoformat(),
            }
            
            _LOGGER.info(
                "CAD data fetched: %s approaches, next: %s",
                len(approaches),
                next_approach.get("designation") if next_approach else "None",
            )
            return result

        except NASAApiError as err:
            _LOGGER.error("NASA API error fetching CAD data: %s", err)
            # Return default data instead of raising to allow retries
            return {
                "count": 0,
                "approaches": [],
                "last_update": datetime.now(timezone.utc).isoformat(),
                "error": str(err),
            }
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching CAD data")
            # Return default data instead of raising to allow retries
            return {
                "count": 0,
                "approaches": [],
                "last_update": datetime.now(timezone.utc).isoformat(),
                "error": str(err),
            }
