# NASA Sky Hub - Home Assistant Integration

<div align="center">
  <img src="logo.png" alt="NASA Sky Hub Logo" width="200"/>
</div>

A comprehensive Home Assistant integration that brings together NASA public APIs, satellite tracking, and sky visibility calculations into actionable, glanceable awareness of what's happening above you.

## Features

- **Space Weather Monitoring** - Real-time solar flares, CMEs, and geomagnetic storms from NASA DONKI
- **Astronomy Picture of the Day** - Daily space imagery with camera entity
- **Satellite Tracking** - Track ISS and other satellites using TLE data from Celestrak
- **Sky Visibility** - Computed astronomical conditions, visible constellations, and stargazing conditions
- **Rate Limit Safe** - Centralized request budgeting with adaptive polling
- **Beautiful Lovelace Dashboards** - Pre-built dashboards for space weather and sky overview

## Installation

See [doc/installation.md](doc/installation.md) for detailed installation instructions.

### Method 1: HACS (Recommended - Easiest)

**Prerequisites**: [HACS](https://hacs.xyz/) must be installed

1. **Add Custom Repository**:
   - Go to HACS → Integrations
   - Click the three dots (⋮) → "Custom repositories"
   - Add repository: `https://github.com/yourusername/nasa_sky_hub`
   - Category: Integration
   - Click "Add"

2. **Install**:
   - Search for "NASA Sky Hub" in HACS
   - Click "Download"
   - Restart Home Assistant

3. **Configure**:
   - Go to Settings → Devices & Services → Add Integration
   - Search for "NASA Sky Hub"

### Method 2: Direct Git Clone

**On Home Assistant OS / Supervised** (SSH access):
```bash
cd /config/custom_components
git clone https://github.com/yourusername/nasa_sky_hub.git nasa_sky_hub
# Restart Home Assistant
```

**On Docker**:
```bash
docker exec -it homeassistant bash
cd /config/custom_components
git clone https://github.com/yourusername/nasa_sky_hub.git nasa_sky_hub
exit
docker restart homeassistant
```

### Method 3: Manual Installation

1. Download ZIP from GitHub
2. Extract `custom_components/nasa_sky_hub` folder
3. Copy to your Home Assistant `custom_components` directory
4. Restart Home Assistant


## Configuration

### Initial Setup

1. **Get a NASA API Key** (free at https://api.nasa.gov/)
   - You can use `DEMO_KEY` for testing, but it has very restrictive rate limits
   - For production use, get your own free API key

2. **Configure via UI**
   - Go to Settings → Devices & Services → Add Integration
   - Search for "NASA Sky Hub"
   - Enter your API key
   - Select which modules to enable:
     - Space Weather (DONKI)
     - Astronomy Picture of the Day
     - Earth Events (EONET)
     - Satellite Tracking
     - Sky Visibility
   - Choose a rate limit profile:
     - **Conservative** - Fewer requests, safer for DEMO_KEY
     - **Balanced** - Recommended for most users
     - **Aggressive** - More frequent updates
   - Set your location (latitude/longitude)

### Modules

#### Space Weather
- Monitors solar flares, CMEs, and geomagnetic storms
- Provides severity levels and alert binary sensors
- Updates every 15-60 minutes depending on profile

#### APOD (Astronomy Picture of the Day)
- Daily space imagery
- Camera entity for viewing images
- Updates once per day

#### Satellite Tracking
- Tracks ISS and other satellites using TLE data
- Shows when satellites are overhead
- Calculates next passes
- Updates every 1-5 minutes depending on profile

#### Sky Visibility
- Computes astronomical night conditions
- Shows visible constellations
- Calculates sky darkness level
- Determines good stargazing conditions
- Updates every 3-10 minutes depending on profile

## Entities

### Sensors

- `sensor.nasa_sky_hub_space_weather_severity` - Current space weather severity
- `sensor.nasa_sky_hub_space_weather_flares_24h` - Number of solar flares in last 24 hours
- `sensor.nasa_sky_hub_apod_title` - APOD title
- `sensor.nasa_sky_hub_apod_date` - APOD date
- `sensor.nasa_sky_hub_satellites_overhead` - Number of satellites currently overhead
- `sensor.nasa_sky_hub_satellites_next_pass` - Time of next satellite pass
- `sensor.nasa_sky_hub_sky_visible_constellations` - List of visible constellations
- `sensor.nasa_sky_hub_sky_brightest_object` - Brightest object currently visible
- `sensor.nasa_sky_hub_sky_darkness_level` - Sky darkness level (0-100%)
- `sensor.nasa_sky_hub_sky_sidereal_time` - Local sidereal time
- `sensor.nasa_api_rate_limit_remaining` - Remaining API requests
- `sensor.nasa_api_rate_status` - API status (normal/warning/degraded)

### Binary Sensors

- `binary_sensor.nasa_sky_hub_space_weather_solar_flare_active` - Solar flare currently active
- `binary_sensor.nasa_sky_hub_space_weather_geomagnetic_storm_active` - Geomagnetic storm active
- `binary_sensor.nasa_sky_hub_space_weather_radiation_storm_active` - Radiation storm active
- `binary_sensor.nasa_sky_hub_satellites_iss_overhead` - ISS currently overhead
- `binary_sensor.nasa_sky_hub_satellites_visible_satellite_pass` - Visible satellite pass within 1 hour
- `binary_sensor.nasa_sky_hub_sky_astronomical_night` - Currently astronomical night
- `binary_sensor.nasa_sky_hub_sky_good_stargazing_conditions` - Good conditions for stargazing

### Camera

- `camera.nasa_sky_hub_apod` - Astronomy Picture of the Day

## Services

### `nasa_sky_hub.refresh_all`
Refresh all data from all enabled modules.

### `nasa_sky_hub.refresh_module`
Refresh data for a specific module.

**Service Data:**
- `module` (required): Module name (space_weather, apod, satellites, sky)

### `nasa_sky_hub.prefetch_apod_range`
Prefetch APOD images for a date range.

**Service Data:**
- `start_date` (required): Start date in ISO format (YYYY-MM-DD)
- `end_date` (required): End date in ISO format (YYYY-MM-DD)

### `nasa_sky_hub.calculate_satellite_passes`
Calculate satellite passes for a time range.

**Service Data:**
- `norad_id` (required): NORAD catalog number
- `hours` (optional): Hours to look ahead (default: 24)

## Lovelace Dashboards

The integration includes pre-built Lovelace dashboards:

### Space Weather Command
- Real-time space weather monitoring
- Solar flare timeline chart
- Active alerts
- Recent flares list

**Import:** Copy `lovelace/dashboards/space_weather.yaml` to your Lovelace configuration

### Night Sky Overview
- Current sky conditions
- Visible constellations
- ISS tracking
- Next satellite passes

**Import:** Copy `lovelace/dashboards/sky_overview.yaml` to your Lovelace configuration

### Earth & Space Events
- APOD showcase
- Space weather badge

**Import:** Copy `lovelace/dashboards/earth_events.yaml` to your Lovelace configuration

### Individual Cards

You can also use individual cards from `lovelace/cards/`:
- `flare_overview.yaml` - Space weather status card
- `flare_timeline.yaml` - Solar flare activity chart
- `whats_above.yaml` - Current sky conditions card

## Rate Limiting

The integration includes intelligent rate limiting:

- Tracks NASA API rate limits from response headers
- Automatically backs off on HTTP 429 responses
- Degrades gracefully when rate limits are low
- Provides sensors to monitor API status

**Rate Limit Sensors:**
- `sensor.nasa_api_rate_limit_remaining` - Shows remaining requests
- `sensor.nasa_api_rate_status` - Shows status (normal/warning/degraded)

## Requirements

- Home Assistant 2023.1 or later
- Python packages (installed automatically):
  - `aiohttp>=3.8.0`
  - `pyephem>=4.1`
  - `skyfield>=1.42`

## Documentation

Detailed documentation is available in the `doc/` folder:

- **[Installation Guide](doc/installation.md)** - Detailed installation instructions
- **[Quick Start Guide](doc/quickstart.md)** - Get started quickly
- **[Testing Guide](doc/testing.md)** - How to test the integration
- **[Dashboard Setup](doc/dashboards.md)** - Setting up Lovelace dashboards
- **[Troubleshooting](doc/troubleshooting.md)** - Common issues and solutions
- **[Logs and Diagnostics](doc/logs-and-diagnostics.md)** - How to get logs for support

## Troubleshooting

See [doc/troubleshooting.md](doc/troubleshooting.md) for detailed troubleshooting guide.

Quick fixes:
- **Rate limit issues**: Check `sensor.nasa_api_rate_limit_remaining`, switch to conservative profile
- **Entities not found**: Verify integration is configured, restart HA, wait 2-3 minutes
- **No data**: Check modules are enabled, verify API key, check logs

## Development

### Project Structure

```
custom_components/nasa_sky_hub/
  __init__.py              # Integration setup
  manifest.json            # Integration manifest
  config_flow.py           # Configuration UI
  api_client.py            # NASA API client
  rate_limiter.py          # Rate limiting
  satellite_tracker.py     # Satellite tracking
  sky_calculator.py        # Sky calculations
  sensor.py                # Sensor entities
  binary_sensor.py         # Binary sensor entities
  camera.py                # Camera entity
  services.py              # Service handlers
  services.yaml            # Service definitions
  diagnostics.py           # Diagnostics
  coordinators/            # Data coordinators
    space_weather.py
    apod.py
    satellites.py
    sky.py
```

## License

MIT License

## Credits

- NASA APIs (https://api.nasa.gov/)
- Celestrak (https://celestrak.org/) for satellite TLE data
- Skyfield library for astronomical calculations

## Support

For issues and feature requests, please open an issue on GitHub.
