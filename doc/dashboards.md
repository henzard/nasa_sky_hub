# Quick Dashboard Setup Guide

## Quick Start: Add Cards to Your Dashboard

### Method 1: Add Individual Entities (Easiest)

1. **Go to your dashboard** → Click "Edit Dashboard" (pencil icon)
2. **Click "Add Card"** → Choose "By Entity"
3. **Select these entities** to get started:

#### Essential Cards to Add:

**Space Weather Status Card:**
- Entity: `sensor.nasa_sky_hub_space_weather_severity`
- Shows: Current space weather severity (quiet/elevated/storm/severe)

**ISS Overhead Card:**
- Entity: `binary_sensor.nasa_sky_hub_iss_overhead`
- Shows: Whether ISS is currently overhead

**APOD Camera Card:**
- Entity: `camera.nasa_sky_hub_apod`
- Shows: Today's Astronomy Picture of the Day

**Satellites Overhead:**
- Entity: `sensor.nasa_sky_hub_satellites_overhead`
- Shows: Number of satellites currently overhead

**Sky Darkness:**
- Entity: `sensor.nasa_sky_hub_sky_darkness_level`
- Shows: Sky darkness percentage (0-100%)

### Method 2: Use Pre-Built Cards (Better Looking)

#### Option A: Copy Individual Cards

1. **Go to your dashboard** → Click "Edit Dashboard"
2. **Click "Add Card"** → Choose "Manual"
3. **Copy and paste** one of these cards:

**Space Weather Overview Card:**
```yaml
type: custom:mushroom-entity-card
entity: sensor.nasa_sky_hub_space_weather_severity
name: Space Weather
icon: mdi:weather-night
tap_action:
  action: navigate
  navigation_path: /space-weather
secondary_info: last-updated
card_mod:
  style: |
    :host {
      --mushroom-state-icon-color: |
        {% if is_state('sensor.nasa_sky_hub_space_weather_severity', 'quiet') %}
          rgb(76, 175, 80);
        {% elif is_state('sensor.nasa_sky_hub_space_weather_severity', 'elevated') %}
          rgb(255, 193, 7);
        {% elif is_state('sensor.nasa_sky_hub_space_weather_severity', 'storm') %}
          rgb(255, 152, 0);
        {% elif is_state('sensor.nasa_sky_hub_space_weather_severity', 'severe') %}
          rgb(244, 67, 54);
        {% else %}
          rgb(158, 158, 158);
        {% endif %}
```

**"What's Above Me Now" Card:**
```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 🌌 What's Above Me Now
  - type: grid
    square: false
    columns: 2
    cards:
      - type: entity
        entity: binary_sensor.nasa_sky_hub_iss_overhead
        name: ISS
        icon: mdi:satellite-variant
      - type: entity
        entity: sensor.nasa_sky_hub_brightest_object_overhead
        name: Brightest
        icon: mdi:star-circle
      - type: entity
        entity: sensor.nasa_sky_hub_visible_constellations
        name: Constellations
        icon: mdi:star
      - type: entity
        entity: sensor.nasa_sky_hub_next_satellite_pass
        name: Next Pass
        icon: mdi:satellite
```

**APOD Picture Card:**
```yaml
type: picture-entity
entity: camera.nasa_sky_hub_apod
show_name: true
show_state: false
```

#### Option B: Import Full Dashboard (Best Experience)

1. **Go to Settings → Dashboards**
2. **Click three dots (⋮)** → "New Dashboard"
3. **Click three dots again** → "Raw configuration editor"
4. **Copy entire contents** from `lovelace/dashboards/space_weather.yaml`
5. **Paste and save**

Or create a new dashboard and copy one of these:

**Space Weather Dashboard** (`lovelace/dashboards/space_weather.yaml`)
- Complete space weather monitoring
- Solar flare timeline chart
- Active alerts
- Recent flares list

**Sky Overview Dashboard** (`lovelace/dashboards/sky_overview.yaml`)
- Current sky conditions
- Visible constellations
- ISS tracking
- Next satellite passes

### Method 3: Simple Entity Cards (No Custom Cards Required)

If you don't have Mushroom Cards or ApexCharts installed, use basic cards:

**Simple Space Weather:**
```yaml
type: entities
title: Space Weather
entities:
  - entity: sensor.nasa_sky_hub_space_weather_severity
    name: Current Status
  - entity: sensor.nasa_sky_hub_solar_flares_24h
    name: Solar Flares (24h)
  - entity: binary_sensor.nasa_sky_hub_solar_flare_active
    name: Flare Active
  - entity: binary_sensor.nasa_sky_hub_geomagnetic_storm_active
    name: Geomagnetic Storm
```

**Simple Sky View:**
```yaml
type: entities
title: Sky Conditions
entities:
  - entity: binary_sensor.nasa_sky_hub_astronomical_night
    name: Astronomical Night
  - entity: sensor.nasa_sky_hub_sky_darkness_level
    name: Sky Darkness
  - entity: binary_sensor.nasa_sky_hub_iss_overhead
    name: ISS Overhead
  - entity: sensor.nasa_sky_hub_satellites_overhead
    name: Satellites Overhead
```

## Recommended Dashboard Layout

### Quick View (Add to Main Dashboard)

Add these 3-4 cards to your main dashboard:

1. **Space Weather Status** (shows severity with color)
2. **ISS Overhead** (binary sensor - shows when ISS is visible)
3. **APOD Camera** (today's space image)
4. **Sky Darkness** (percentage - good for stargazing)

### Full Experience (Separate Dashboard)

Create a dedicated "Space" dashboard with:
- Space Weather Command dashboard (full)
- Sky Overview dashboard (full)
- Earth Events dashboard (APOD showcase)

## Required Custom Cards (Optional but Recommended)

For the best experience, install these HACS custom cards:

1. **Mushroom Cards** (for beautiful entity cards)
   - HACS → Frontend → Search "Mushroom"
   - Install "Mushroom Cards"

2. **ApexCharts Card** (for solar flare timeline)
   - HACS → Frontend → Search "ApexCharts"
   - Install "ApexCharts Card"

3. **Card Mod** (for custom styling)
   - HACS → Frontend → Search "Card Mod"
   - Install "Card Mod"

**Note:** The simple entity cards will work without these, but won't look as nice.

## Quick Test

After adding cards:

1. **Check entities update**: Wait 1-2 minutes, cards should show data
2. **Click on cards**: Should show more info/details
3. **Check rate limit**: Look for `sensor.nasa_api_rate_limit_remaining` - should show remaining requests

## Troubleshooting

**Cards show "Unavailable":**
- Wait 1-2 minutes for first data fetch
- Check logs for errors
- Verify integration is configured

**No data showing:**
- Check that modules are enabled in integration settings
- Verify API key is set (not DEMO_KEY if you hit limits)
- Check `sensor.nasa_api_rate_limit_remaining` value

**Custom cards not working:**
- Install required custom cards from HACS
- Or use simple entity cards instead

## Next Steps

Once cards are working:
- Create automations based on space weather alerts
- Set up notifications for ISS passes
- Add more cards as needed
- Customize colors and layouts
