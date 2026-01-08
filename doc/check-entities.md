# How to Check Which Entities Actually Exist

## Quick Check in Home Assistant

1. **Go to Developer Tools → States**
2. **In the search box, type:** `nasa_sky_hub`
3. **You'll see all entities that actually exist**

## Or Use This Template

Go to **Developer Tools → Template** and paste this:

```yaml
{% for state in states %}
  {% if 'nasa_sky_hub' in state.entity_id or 'nasa_api' in state.entity_id %}
    - **{{ state.entity_id }}**: {{ state.state }}
  {% endif %}
{% endfor %}
```

This will list all NASA Sky Hub entities and their current states.

## What to Look For

Compare the entities that exist with the entity IDs in your dashboard:

### Should Exist (if modules are enabled):
- `sensor.nasa_api_rate_remaining`
- `sensor.nasa_api_rate_status`
- `sensor.nasa_sky_hub_space_weather_severity` (if space_weather enabled)
- `sensor.nasa_sky_hub_space_weather_flares_24h` (if space_weather enabled)
- `binary_sensor.nasa_sky_hub_space_weather_solar_flare_active` (if space_weather enabled)
- `sensor.nasa_sky_hub_apod_title` (if apod enabled)
- `sensor.nasa_sky_hub_apod_date` (if apod enabled)
- `camera.nasa_sky_hub_apod` (if apod enabled)
- `sensor.nasa_sky_hub_satellites_overhead` (if satellites enabled) ✅ Works
- `sensor.nasa_sky_hub_satellites_next_pass` (if satellites enabled)
- `binary_sensor.nasa_sky_hub_satellites_iss_overhead` (if satellites enabled)
- `sensor.nasa_sky_hub_sky_visible_constellations` (if sky enabled)
- `sensor.nasa_sky_hub_sky_brightest_object` (if sky enabled)
- `sensor.nasa_sky_hub_sky_darkness_level` (if sky enabled) ✅ Works
- `sensor.nasa_sky_hub_sky_sidereal_time` (if sky enabled)
- `binary_sensor.nasa_sky_hub_sky_astronomical_night` (if sky enabled)
- `binary_sensor.nasa_sky_hub_sky_good_stargazing_conditions` (if sky enabled)

## If Entities Don't Exist

1. **Check logs** for errors during entity creation
2. **Verify modules are enabled** in integration settings
3. **Restart Home Assistant** to retry entity creation
4. **Check coordinator status** - if coordinators fail, entities might not be created

## If Entity IDs Are Wrong

If entities exist but have different IDs than expected:
1. **Note the actual entity IDs** from Developer Tools → States
2. **Update dashboard YAML** to use the correct entity IDs
3. **Refresh the dashboard**
