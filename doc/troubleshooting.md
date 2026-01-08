# Fix "Entity Not Found" Error

## The Problem
You see "Entity not found" for all NASA Sky Hub entities. This means the entities haven't been created yet.

## Quick Fixes (Try These in Order)

### Fix 1: Check Integration is Configured

1. Go to **Settings → Devices & Services**
2. Look for **"NASA Sky Hub"** in the list
3. If you DON'T see it:
   - Click **"Add Integration"** (bottom right)
   - Search for **"NASA Sky Hub"**
   - Follow the setup wizard
   - Enter your API key (use `DEMO_KEY` for testing)
   - Select modules to enable
   - Set your location

### Fix 2: Check Modules Are Enabled

1. Go to **Settings → Devices & Services**
2. Click on **"NASA Sky Hub"**
3. Click **"Configure"** (or the three dots → Configure)
4. Make sure modules are checked:
   - ✅ Space Weather
   - ✅ APOD
   - ✅ Satellites
   - ✅ Sky Visibility
5. Save if you made changes

### Fix 3: Restart Home Assistant

After configuring the integration:
1. Go to **Settings → System**
2. Click **"Restart"** (top right)
3. Wait for Home Assistant to restart (2-5 minutes)
4. Go back to your dashboard

### Fix 4: Check Entities Were Created

1. Go to **Developer Tools → States** (left sidebar)
2. In the search box, type: `nasa`
3. You should see entities like:
   - `sensor.nasa_sky_hub_space_weather_severity`
   - `binary_sensor.nasa_sky_hub_iss_overhead`
   - `camera.nasa_sky_hub_apod`
   - etc.

**If you see them here:** The card will work, just wait a minute for data

**If you DON'T see them:** Integration isn't set up correctly - go back to Fix 1

### Fix 5: Check Logs for Errors

1. Go to **Settings → System → Logs**
2. Look for errors containing `nasa_sky_hub`
3. Common errors:
   - **"Invalid API key"**: Check your API key
   - **"Rate limit exceeded"**: Wait a few minutes or get your own API key
   - **"Module not found"**: Restart HA to install Python packages

## Step-by-Step: First Time Setup

If you haven't set up the integration yet:

1. **Settings → Devices & Services**
2. **Click "Add Integration"** (bottom right)
3. **Search: "NASA Sky Hub"**
4. **Click it**
5. **Enter API Key**: `DEMO_KEY` (or your own key)
6. **Click Submit**
7. **Select Modules**: Check at least "Space Weather"
8. **Select Profile**: "Balanced"
9. **Click Submit**
10. **Set Location**: Enter your latitude/longitude
11. **Click Submit**
12. **Restart Home Assistant**
13. **Wait 2-3 minutes**
14. **Go back to dashboard** - entities should work now!

## Verify It's Working

After setup and restart:

1. **Developer Tools → States**
2. **Search: `nasa`**
3. **You should see entities** with values (not "unavailable")

If you see entities with values, your dashboard card will work!

## Still Not Working?

1. **Check integration shows in Devices & Services**
2. **Check entities exist in Developer Tools → States**
3. **Check logs for errors**
4. **Try restarting Home Assistant again**
5. **Wait 5 minutes** (first data fetch can take time)

## Quick Test

Once entities exist, test with this simple card:

```yaml
type: entities
title: NASA Test
entities:
  - sensor.nasa_api_rate_limit_remaining
```

This should ALWAYS work if integration is installed. If this shows "not found", the integration isn't configured.
