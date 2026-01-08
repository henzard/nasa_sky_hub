# Widget Setup Guide

## Verify Entities Are Registered

After restarting Home Assistant, verify entities are created:

1. **Go to Settings → Devices & Services**
2. **Click on "NASA Sky Hub" integration**
3. **Click "Entities" tab**
4. **You should see entities like:**
   - `sensor.nasa_sky_hub_space_weather_severity`
   - `sensor.nasa_sky_hub_space_weather_flares_24h`
   - `sensor.nasa_sky_hub_apod_title`
   - `sensor.nasa_sky_hub_apod_date`
   - `sensor.nasa_sky_hub_satellites_overhead`
   - `sensor.nasa_sky_hub_satellites_next_pass`
   - `sensor.nasa_sky_hub_sky_visible_constellations`
   - `sensor.nasa_sky_hub_sky_brightest_object`
   - `sensor.nasa_sky_hub_sky_darkness_level`
   - `sensor.nasa_sky_hub_sky_sidereal_time`
   - `binary_sensor.nasa_sky_hub_space_weather_solar_flare_active`
   - `binary_sensor.nasa_sky_hub_space_weather_geomagnetic_storm_active`
   - `binary_sensor.nasa_sky_hub_space_weather_radiation_storm_active`
   - `binary_sensor.nasa_sky_hub_satellites_iss_overhead`
   - `binary_sensor.nasa_sky_hub_satellites_visible_satellite_pass`
   - `binary_sensor.nasa_sky_hub_sky_astronomical_night`
   - `binary_sensor.nasa_sky_hub_sky_good_stargazing_conditions`
   - `camera.nasa_sky_hub_apod`

## Add Widgets to Lovelace

### Method 1: Import Pre-built Dashboards

1. **Go to your Lovelace dashboard**
2. **Click the three dots (⋮) → "Edit Dashboard"**
3. **Click the three dots again → "Dashboard settings"**
4. **Scroll down and click "Raw configuration editor"**
5. **Copy the contents from `lovelace/dashboards/space_weather.yaml`**
6. **Paste into a new dashboard or add to existing**

### Method 2: Add Individual Cards

1. **Go to your Lovelace dashboard**
2. **Click "Add Card"**
3. **Choose "Manual" or "YAML"**
4. **Copy a card from `lovelace/cards/` folder**
5. **Paste and save**

### Method 3: Use Entity Cards (Simplest)

1. **Go to your Lovelace dashboard**
2. **Click "Add Card"**
3. **Search for an entity (e.g., "NASA Sky Hub Space Weather Severity")**
4. **Add the card**

## Quick Test Card

Add this simple card to test if entities are working:

```yaml
type: entities
title: NASA Sky Hub Test
entities:
  - entity: sensor.nasa_sky_hub_space_weather_severity
  - entity: sensor.nasa_sky_hub_space_weather_flares_24h
  - entity: sensor.nasa_sky_hub_satellites_overhead
  - entity: binary_sensor.nasa_sky_hub_iss_overhead
```

## Troubleshooting

### Entities Show as "Unavailable"

- **Wait 2-3 minutes** after restart for coordinators to fetch data
- **Check logs** for errors (Settings → System → Logs)
- **Verify API key** is correct in integration settings
- **Check network connectivity** to NASA APIs

### Widgets Don't Show Data

- **Verify entity IDs match** exactly (case-sensitive)
- **Check entity state** in Developer Tools → States
- **Ensure entities are enabled** (not disabled in entity registry)

### Sky Sensors Not Working

- The Skyfield vector error has been fixed in v1.2.2
- **Restart Home Assistant** to apply the fix
- If still failing, check logs for specific errors

## Entity ID Reference

All entity IDs follow this pattern:
- Sensors: `sensor.nasa_sky_hub_{module}_{key}`
- Binary Sensors: `binary_sensor.nasa_sky_hub_{module}_{key}`
- Camera: `camera.nasa_sky_hub_{module}`

Where `{module}` is:
- `space_weather` - Space weather data
- `apod` - Astronomy Picture of the Day
- `satellites` - Satellite tracking
- `sky` - Sky visibility calculations
