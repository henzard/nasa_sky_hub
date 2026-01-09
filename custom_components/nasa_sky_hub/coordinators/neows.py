"""NeoWs (Near Earth Object Web Service) coordinator."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..api_client import NASAApiClient, NASAApiError
from ..const import MODULE_ASTEROIDS

_LOGGER = logging.getLogger(__name__)


class NeoWsCoordinator(DataUpdateCoordinator):
    """Coordinator for NeoWs feed data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: NASAApiClient,
        days_ahead: int = 7,
        update_interval: int = 3600,
    ) -> None:
        """Initialize NeoWs coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{MODULE_ASTEROIDS}_neows",
            update_interval=timedelta(seconds=update_interval),
        )
        self.api_client = api_client
        self.days_ahead = days_ahead

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch NeoWs feed data."""
        now_utc = datetime.now(timezone.utc)
        default_data = {
            "element_count": 0,
            "near_earth_objects": {},
            "potentially_hazardous_count": 0,
            "total_neos": 0,  # Add missing field for sensor
            "closest_approaches": [],
            "last_update": now_utc.isoformat(),
        }
        
        try:
            # Calculate date range
            start_date = now_utc.strftime("%Y-%m-%d")
            end_date = (now_utc + timedelta(days=self.days_ahead)).strftime("%Y-%m-%d")
            
            _LOGGER.info("Fetching NeoWs feed from %s to %s", start_date, end_date)
            data = await self.api_client.get_neo_feed(start_date, end_date)
            
            # Process the feed data
            element_count = data.get("element_count", 0)
            neo_dict = data.get("near_earth_objects", {})
            
            # Flatten all NEOs from all dates into a single list
            all_neos = []
            for date_key, neos_list in neo_dict.items():
                for neo in neos_list:
                    all_neos.append(neo)
            
            # Count potentially hazardous
            pha_count = sum(1 for neo in all_neos if neo.get("is_potentially_hazardous_asteroid", False))
            
            # Find closest approaches
            closest_approaches = []
            for neo in all_neos:
                close_approach_data = neo.get("close_approach_data", [])
                if close_approach_data:
                    # Get the closest approach
                    closest = min(
                        close_approach_data,
                        key=lambda x: float(x.get("miss_distance", {}).get("kilometers", float("inf")))
                    )
                    
                    neo_id = neo.get("id", "")
                    neo_name = neo.get("name", "Unknown")
                    is_hazardous = neo.get("is_potentially_hazardous_asteroid", False)
                    
                    closest_approaches.append({
                        "id": neo_id,
                        "name": neo_name,
                        "is_potentially_hazardous": is_hazardous,
                        "close_approach_date": closest.get("close_approach_date", ""),
                        "close_approach_date_full": closest.get("close_approach_date_full", ""),
                        "miss_distance_km": float(closest.get("miss_distance", {}).get("kilometers", 0)),
                        "miss_distance_lunar": float(closest.get("miss_distance", {}).get("lunar", 0)),
                        "relative_velocity_kmh": float(closest.get("relative_velocity", {}).get("kilometers_per_hour", 0)),
                        "estimated_diameter_min_km": float(neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min", 0)),
                        "estimated_diameter_max_km": float(neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max", 0)),
                        "orbiting_body": closest.get("orbiting_body", "Earth"),
                    })
            
            # Sort by miss distance (closest first)
            closest_approaches.sort(key=lambda x: x["miss_distance_km"])
            
            result = {
                "element_count": element_count,
                "near_earth_objects": neo_dict,
                "potentially_hazardous_count": pha_count,
                "closest_approaches": closest_approaches[:20],  # Top 20 closest
                "total_neos": len(all_neos),
                "last_update": now_utc.isoformat(),
            }
            
            _LOGGER.info(
                "NeoWs data fetched: %s NEOs, %s potentially hazardous, %s closest approaches",
                element_count,
                pha_count,
                len(closest_approaches),
            )
            return result
            
        except NASAApiError as err:
            _LOGGER.error("NASA API error fetching NeoWs feed: %s", err)
            return default_data
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching NeoWs feed")
            return default_data
