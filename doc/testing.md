# Testing NASA Sky Hub on Home Assistant

## Step 1: Install the Integration

### Option A: Manual Installation (Recommended for Testing)

1. **Copy the integration folder** to your Home Assistant:
   ```
   <config>/custom_components/nasa_sky_hub/
   ```
   Where `<config>` is your Home Assistant config directory (usually `/config` in Docker or `/home/homeassistant/.homeassistant` on a Pi).

2. **Verify the structure** - Make sure you have:
   ```
   custom_components/nasa_sky_hub/
   ├── __init__.py
   ├── manifest.json
   ├── config_flow.py
   ├── api_client.py
   └── ... (all other files)
   ```

3. **Restart Home Assistant**
   - Go to Settings → System → Restart
   - Or restart your HA container/service

### Option B: HACS Installation (If Available)

1. Add this repository to HACS
2. Install "NASA Sky Hub"
3. Restart Home Assistant

## Step 2: Check Installation

1. **Check Logs** after restart:
   - Go to Settings → System → Logs
   - Look for any errors related to `nasa_sky_hub`
   - You should see: `Loading integration nasa_sky_hub`

2. **Verify Integration Appears**:
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "NASA Sky Hub"
   - It should appear in the list

## Step 3: Configure the Integration

### Initial Setup

1. **Click "NASA Sky Hub"** in the Add Integration dialog

2. **Step 1: API Key**
   - Enter `DEMO_KEY` for testing (or your own API key)
   - Click "Submit"

3. **Step 2: Select Modules**
   - Select at least one module (start with "Space Weather" for testing)
   - Choose "Balanced" profile
   - Click "Submit"

4. **Step 3: Location**
   - Enter your latitude and longitude
   - Or use your HA default location
   - Click "Submit"

5. **Complete Setup**
   - You should see "Successfully configured NASA Sky Hub"

## Step 4: Verify Entities Created

1. **Go to Settings → Devices & Services**
2. **Click on "NASA Sky Hub"** integration
3. **Check "Entities" tab**
4. **You should see entities like**:
   - `sensor.nasa_api_rate_limit_remaining`
   - `sensor.nasa_sky_hub_space_weather_severity` (if space weather enabled)
   - `sensor.nasa_sky_hub_apod_title` (if APOD enabled)
   - etc.

## Step 5: Test Basic Functionality

### Test 1: Check Rate Limit Sensor

1. Go to Developer Tools → States
2. Search for `nasa_api_rate_limit_remaining`
3. Check the value - should show remaining API requests
4. State should be "normal", "warning", or "degraded"

### Test 2: Check Space Weather (if enabled)

1. Search for `sensor.nasa_sky_hub_space_weather_severity`
2. Check the state - should be "quiet", "elevated", "storm", or "severe"
3. Click on it to see attributes (flares, CMEs, storms)

### Test 3: Check APOD (if enabled)

1. Search for `camera.nasa_sky_hub_apod`
2. Click to view the image
3. Check `sensor.nasa_sky_hub_apod_title` for today's title

### Test 4: Check Satellite Tracking (if enabled)

1. Search for `binary_sensor.nasa_sky_hub_iss_overhead`
2. Check if ISS is currently overhead
3. Check `sensor.nasa_sky_hub_satellites_overhead` for count

### Test 5: Check Sky Visibility (if enabled)

1. Search for `binary_sensor.nasa_sky_hub_astronomical_night`
2. Check if it's currently astronomical night
3. Check `sensor.nasa_sky_hub_visible_constellations` for visible constellations

## Step 6: Test Services

1. **Go to Developer Tools → Services**

2. **Test Refresh All**:
   ```yaml
   service: nasa_sky_hub.refresh_all
   ```
   Click "Call Service" and check logs

3. **Test Refresh Module**:
   ```yaml
   service: nasa_sky_hub.refresh_module
   data:
    module: space_weather
   ```
   Click "Call Service"

4. **Test Prefetch APOD**:
   ```yaml
   service: nasa_sky_hub.prefetch_apod_range
   data:
     start_date: "2024-01-01"
     end_date: "2024-01-03"
   ```
   Click "Call Service" (may take a while)

## Step 7: Test Lovelace Cards

### Add a Simple Card

1. Go to any dashboard
2. Click "Edit Dashboard"
3. Click "Add Card"
4. Choose "Manual" or "By Entity"
5. Select `sensor.nasa_sky_hub_space_weather_severity`
6. Save and view

### Import a Dashboard

1. Go to Settings → Dashboards
2. Click three dots → "New Dashboard"
3. Click three dots → "Raw configuration editor"
4. Copy contents from `lovelace/dashboards/space_weather.yaml`
5. Paste and save
6. View the dashboard

## Step 8: Check Logs for Issues

### Common Issues to Check

1. **Rate Limit Errors**:
   ```
   Rate limit 429 received
   ```
   - Solution: Wait a bit, or get your own API key

2. **TLE Update Errors**:
   ```
   Failed to update TLE data
   ```
   - Solution: Check internet connection

3. **API Connection Errors**:
   ```
   NASA API request failed
   ```
   - Solution: Check API key, internet connection

4. **Import Errors**:
   ```
   No module named 'skyfield'
   ```
   - Solution: Restart HA, packages should auto-install

## Step 9: Monitor Performance

### Check Update Frequency

1. Watch entities update in real-time
2. Check "Last Updated" timestamps
3. Verify updates match your selected profile:
   - Conservative: Longer intervals
   - Balanced: Medium intervals
   - Aggressive: Shorter intervals

### Check Rate Limit Usage

1. Monitor `sensor.nasa_api_rate_limit_remaining`
2. Should decrease slowly with updates
3. Should not hit zero (if it does, switch to conservative profile)

## Step 10: Test Automations

Create a simple automation to test:

```yaml
automation:
  - alias: "ISS Overhead Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.nasa_sky_hub_iss_overhead
        to: "on"
    action:
      - service: notify.persistent_notification
        data:
          message: "ISS is overhead!"
          title: "Space Alert"
```

## Troubleshooting

### Integration Not Appearing

1. Check `custom_components` folder name (must be exact)
2. Check `manifest.json` exists and is valid JSON
3. Restart HA completely
4. Check logs for import errors

### Entities Not Updating

1. Check coordinator logs for errors
2. Verify API key is valid
3. Check rate limit status
4. Try manual refresh via service

### Errors in Logs

1. **"Module not found"**: Restart HA, packages install on first use
2. **"Invalid API key"**: Check API key in config
3. **"Rate limit exceeded"**: Wait or get your own API key
4. **"Location required"**: Set location in config

### Performance Issues

1. Disable unused modules
2. Switch to conservative profile
3. Increase update intervals in options
4. Check network connectivity

## Quick Test Checklist

- [ ] Integration appears in Add Integration
- [ ] Config flow completes successfully
- [ ] Entities are created
- [ ] Rate limit sensor shows value
- [ ] At least one module sensor updates
- [ ] Services can be called
- [ ] No errors in logs
- [ ] Entities show correct data
- [ ] Lovelace cards display correctly

## Getting Help

If you encounter issues:

1. **Check Logs**: Settings → System → Logs
2. **Check Diagnostics**: Settings → Devices & Services → NASA Sky Hub → Diagnostics
3. **Review README.md**: Full documentation
4. **Check Entity States**: Developer Tools → States
5. **Test API Directly**: Try NASA API in browser

## Next Steps After Testing

Once everything works:

1. Get your own NASA API key (free at https://api.nasa.gov/)
2. Enable all modules you want
3. Import Lovelace dashboards
4. Create automations based on space weather
5. Set up notifications for ISS passes
6. Customize update intervals in options
