# Entity ID Reference

## How Entity IDs Are Generated

Entity IDs in Home Assistant are generated from:
- **Domain**: `sensor`, `binary_sensor`, or `camera`
- **Unique ID**: Generated as `{coordinator.name}_{description.key}`

The final entity ID format is: `{domain}.{domain}_{unique_id}`

## Complete Entity ID List

### Rate Limit Sensors (Always Enabled)
- `sensor.nasa_api_rate_remaining` (unique_id: `nasa_api_rate_remaining`)
- `sensor.nasa_api_rate_status` (unique_id: `nasa_api_rate_status`)

### Space Weather Sensors
- `sensor.nasa_sky_hub_space_weather_severity` (unique_id: `space_weather_severity`)
- `sensor.nasa_sky_hub_space_weather_flares_24h` (unique_id: `space_weather_flares_24h`)

### Space Weather Binary Sensors
- `binary_sensor.nasa_sky_hub_space_weather_solar_flare_active` (unique_id: `space_weather_solar_flare_active`)
- `binary_sensor.nasa_sky_hub_space_weather_geomagnetic_storm_active` (unique_id: `space_weather_geomagnetic_storm_active`)
- `binary_sensor.nasa_sky_hub_space_weather_radiation_storm_active` (unique_id: `space_weather_radiation_storm_active`)

### APOD Sensors
- `sensor.nasa_sky_hub_apod_title` (unique_id: `apod_title`)
- `sensor.nasa_sky_hub_apod_date` (unique_id: `apod_date`)

### APOD Camera
- `camera.nasa_sky_hub_apod` (unique_id: `nasa_sky_hub_apod`)

### Satellite Sensors
- `sensor.nasa_sky_hub_satellites_overhead` (unique_id: `satellites_satellites_overhead`)
- `sensor.nasa_sky_hub_satellites_next_pass` (unique_id: `satellites_next_pass`)

### Satellite Binary Sensors
- `binary_sensor.nasa_sky_hub_satellites_iss_overhead` (unique_id: `satellites_iss_overhead`)
- `binary_sensor.nasa_sky_hub_satellites_visible_satellite_pass` (unique_id: `satellites_visible_satellite_pass`)

### Sky Sensors
- `sensor.nasa_sky_hub_sky_visible_constellations` (unique_id: `sky_visible_constellations`)
- `sensor.nasa_sky_hub_sky_brightest_object` (unique_id: `sky_brightest_object`)
- `sensor.nasa_sky_hub_sky_darkness_level` (unique_id: `sky_darkness_level`)
- `sensor.nasa_sky_hub_sky_sidereal_time` (unique_id: `sky_sidereal_time`)

### Sky Binary Sensors
- `binary_sensor.nasa_sky_hub_sky_astronomical_night` (unique_id: `sky_astronomical_night`)
- `binary_sensor.nasa_sky_hub_sky_good_stargazing_conditions` (unique_id: `sky_good_stargazing_conditions`)

### Asteroid Sensors (if enabled)
- `sensor.nasa_sky_hub_asteroids_sentry_total_threats` (unique_id: `asteroids_sentry_total_threats`)
- `sensor.nasa_sky_hub_asteroids_sentry_max_palermo_scale` (unique_id: `asteroids_sentry_max_palermo_scale`)
- `sensor.nasa_sky_hub_asteroids_cad_total_approaches` (unique_id: `asteroids_cad_total_approaches`)
- `sensor.nasa_sky_hub_asteroids_cad_next_approach` (unique_id: `asteroids_cad_next_approach`)

## Verifying Entity IDs

To check which entities actually exist in your Home Assistant:

1. **Go to Developer Tools → States**
2. **Search for `nasa_sky_hub`**
3. **Compare the list with the entity IDs in your dashboard**

Or use this template in Developer Tools → Template:

```yaml
{% for state in states %}
  {% if 'nasa_sky_hub' in state.entity_id or 'nasa_api' in state.entity_id %}
    {{ state.entity_id }}
  {% endif %}
{% endfor %}
```

## Common Issues

### Entity ID Mismatch
If an entity shows "Entity not found", verify:
1. The entity exists in Developer Tools → States
2. The entity ID in the dashboard matches exactly (case-sensitive)
3. The entity is not disabled in Settings → Devices & Services → Entities

### Entity Not Created
If an entity doesn't exist at all:
1. Check logs for "Setting up [module] sensors" messages
2. Verify the module is enabled in integration settings
3. Check if coordinator setup failed silently
4. Restart Home Assistant to retry entity creation
