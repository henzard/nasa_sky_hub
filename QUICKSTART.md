# NASA Sky Hub - Quick Start Guide

## Installation

1. **Copy the integration** to your Home Assistant `custom_components` directory:
   ```
   custom_components/nasa_sky_hub/
   ```

2. **Restart Home Assistant**

3. **Add Integration**:
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "NASA Sky Hub"
   - Click to configure

## Configuration Steps

### Step 1: API Key
- Enter your NASA API key (get one free at https://api.nasa.gov/)
- Or use `DEMO_KEY` for testing (very limited)

### Step 2: Select Modules
Choose which features to enable:
- ✅ Space Weather (DONKI) - Solar flares, CMEs, storms
- ✅ Astronomy Picture of the Day - Daily space images
- ✅ Earth Events (EONET) - Natural events tracking
- ✅ Satellite Tracking - ISS and other satellites
- ✅ Sky Visibility - Constellations, darkness, stargazing conditions

### Step 3: Rate Limit Profile
- **Conservative** - Fewer requests, safer for DEMO_KEY
- **Balanced** - Recommended for most users (default)
- **Aggressive** - More frequent updates

### Step 4: Location
- Set your latitude and longitude
- Used for satellite tracking and sky calculations
- Defaults to your Home Assistant location

## Using the Integration

### Entities Created

After setup, you'll have sensors, binary sensors, and a camera:

**Key Sensors:**
- `sensor.nasa_sky_hub_space_weather_severity` - Current space weather status
- `sensor.nasa_sky_hub_solar_flares_24h` - Flares in last 24 hours
- `sensor.nasa_sky_hub_satellites_overhead` - Number of satellites overhead
- `binary_sensor.nasa_sky_hub_iss_overhead` - Is ISS overhead?
- `camera.nasa_sky_hub_apod` - Today's astronomy picture

### Adding Lovelace Dashboards

1. Go to Settings → Dashboards
2. Click the three dots menu → "Edit Dashboard"
3. Click the three dots again → "Raw configuration editor"
4. Copy the contents of `lovelace/dashboards/space_weather.yaml`
5. Paste and save

Or add individual cards from `lovelace/cards/` to your existing dashboard.

### Services

Call services from Developer Tools → Services:

**Refresh all data:**
```yaml
service: nasa_sky_hub.refresh_all
```

**Refresh specific module:**
```yaml
service: nasa_sky_hub.refresh_module
data:
  module: space_weather
```

**Prefetch APOD images:**
```yaml
service: nasa_sky_hub.prefetch_apod_range
data:
  start_date: "2024-01-01"
  end_date: "2024-01-07"
```

## Troubleshooting

### Rate Limit Warnings
- Check `sensor.nasa_api_rate_limit_remaining`
- Switch to a more conservative profile
- Get your own API key instead of DEMO_KEY

### No Data Appearing
- Check logs for errors
- Verify API key is correct
- Ensure modules are enabled
- Check internet connectivity

### Satellite Tracking Not Working
- Verify location is set correctly
- Check that satellites module is enabled
- Look for TLE update errors in logs

## Next Steps

- Add Lovelace dashboards for space weather monitoring
- Create automations based on space weather alerts
- Set up notifications for ISS passes
- Use sky visibility sensors for stargazing automations

## Support

For issues, feature requests, or questions:
- Check the README.md for detailed documentation
- Review entity attributes for additional data
- Check Home Assistant logs for errors
