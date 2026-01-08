# Troubleshooting: Only Some Entities Working

## Quick Diagnostic Steps

### 1. Check Which Entities Are Registered

Go to **Settings → Devices & Services → NASA Sky Hub → Entities**

You should see entities like:
- `sensor.nasa_sky_hub_space_weather_severity`
- `sensor.nasa_sky_hub_space_weather_flares_24h`
- `sensor.nasa_sky_hub_apod_title`
- `sensor.nasa_sky_hub_apod_date`
- `sensor.nasa_sky_hub_satellites_overhead` ✅ (This one works)
- `sensor.nasa_sky_hub_satellites_next_pass`
- `sensor.nasa_sky_hub_sky_visible_constellations`
- `sensor.nasa_sky_hub_sky_brightest_object`
- `sensor.nasa_sky_hub_sky_darkness_level`
- `sensor.nasa_sky_hub_sky_sidereal_time`
- `binary_sensor.nasa_sky_hub_space_weather_solar_flare_active`
- `binary_sensor.nasa_sky_hub_satellites_iss_overhead`
- `camera.nasa_sky_hub_apod`

**Question**: Do you see these entities listed, or are they missing entirely?

### 2. Check Entity States

Go to **Developer Tools → States** and search for `nasa_sky_hub`

**Check each entity's state:**
- `unavailable` = Entity exists but coordinator failed to fetch data
- `unknown` = Entity exists but hasn't updated yet
- Missing = Entity was never created

### 3. Check Logs for Errors

Go to **Settings → System → Logs** and filter for `nasa_sky_hub`

Look for:
- `Setting up Space Weather sensors` - Should appear if module is enabled
- `Setting up APOD sensors` - Should appear if module is enabled
- `Setting up Sky sensors` - Should appear if module is enabled
- `Error fetching` - Indicates API or calculation errors
- `Failed to refresh` - Indicates coordinator setup issues

### 4. Verify Modules Are Enabled

Go to **Settings → Devices & Services → NASA Sky Hub → Configure**

Check which modules are enabled:
- ✅ Space Weather
- ✅ APOD
- ✅ Earth Events
- ✅ Satellites (this one works)
- ✅ Sky

**If modules aren't enabled**, enable them and restart Home Assistant.

### 5. Check API Key

The integration requires a NASA API key. If using `DEMO_KEY`, you may hit rate limits.

1. Get a free API key from https://api.nasa.gov/
2. Go to **Settings → Devices & Services → NASA Sky Hub → Configure**
3. Update the API key
4. Restart Home Assistant

## Common Issues

### Issue: Entities Show as "Unavailable"

**Cause**: Coordinator failed to fetch data

**Solutions**:
1. **Wait 2-3 minutes** after restart for coordinators to retry
2. **Check logs** for specific errors (API errors, calculation errors)
3. **Verify API key** is correct and not rate-limited
4. **Check network connectivity** to NASA APIs

### Issue: Entities Don't Exist at All

**Cause**: Module not enabled or setup failed silently

**Solutions**:
1. **Verify modules are enabled** in integration settings
2. **Check logs** for "Setting up [module] sensors" messages
3. **Restart Home Assistant** to retry setup
4. **Check logs** for exceptions during entity creation

### Issue: Only Satellites Work

**Possible Causes**:
1. **Other modules not enabled** - Check integration configuration
2. **API errors** - Space Weather, APOD require NASA API
3. **Calculation errors** - Sky module requires Skyfield calculations
4. **Coordinator failures** - Check logs for specific errors

**Debug Steps**:
1. Check logs for each module's setup:
   ```
   grep "Setting up" home-assistant.log | grep nasa_sky_hub
   ```
2. Check for errors:
   ```
   grep "ERROR.*nasa_sky_hub" home-assistant.log
   ```
3. Check coordinator refresh status:
   ```
   grep "coordinator.*refreshed" home-assistant.log | grep nasa_sky_hub
   ```

### Issue: Sky Entities Not Working

**Specific to Sky Module**:
- Sky calculations use Skyfield library
- Requires ephemeris file (`de421.bsp`) to be downloaded
- May fail if:
  - Network issues downloading ephemeris
  - Skyfield calculation errors (vector math)
  - Location not set correctly

**Check**:
1. Logs for "Loading ephemeris file" messages
2. Logs for Skyfield vector errors
3. Location is set in integration config

## Manual Entity Check

Run this in **Developer Tools → Template**:

```yaml
{% for state in states %}
  {% if 'nasa_sky_hub' in state.entity_id %}
    {{ state.entity_id }}: {{ state.state }}
  {% endif %}
{% endfor %}
```

This will list all NASA Sky Hub entities and their states.

## Still Not Working?

1. **Share logs** - Copy logs from Settings → System → Logs (filter: `nasa_sky_hub`)
2. **Share entity list** - Screenshot of Settings → Devices & Services → NASA Sky Hub → Entities
3. **Share configuration** - Which modules are enabled in integration settings
