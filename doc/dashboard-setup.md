# Super Simple Dashboard Setup

## Method 1: Add Entities (Easiest - What You're Looking At Now)

You're already in the right place! Here's exactly what to do:

### Step-by-Step:

1. **You're on "By entity" tab** ✅ (you're already here!)

2. **In the search box**, type: `nasa`

3. **You'll see entities like:**
   - `sensor.nasa_sky_hub_space_weather_severity`
   - `binary_sensor.nasa_sky_hub_iss_overhead`
   - `camera.nasa_sky_hub_apod`
   - `sensor.nasa_sky_hub_satellites_overhead`

4. **Click the checkbox** next to the ones you want:
   - ✅ `sensor.nasa_sky_hub_space_weather_severity` (Space Weather)
   - ✅ `binary_sensor.nasa_sky_hub_iss_overhead` (ISS Overhead)
   - ✅ `camera.nasa_sky_hub_apod` (Today's Space Picture)

5. **Click "ADD"** at the bottom

6. **Done!** Cards will appear on your dashboard

---

## Method 2: Add a Manual Card (For Better Looking Cards)

### Step-by-Step:

1. **Click the "By card" tab** (top of the screen)

2. **Type "manual" in the search box**

3. **Click on "Manual"** card

4. **A code box will appear** - Delete everything in it

5. **Copy and paste this EXACT code:**

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 🌌 Space Status
  - type: grid
    square: false
    columns: 2
    cards:
      - type: entity
        entity: sensor.nasa_sky_hub_space_weather_severity
        name: Space Weather
      - type: entity
        entity: binary_sensor.nasa_sky_hub_iss_overhead
        name: ISS Overhead
      - type: entity
        entity: sensor.nasa_sky_hub_satellites_overhead
        name: Satellites
      - type: entity
        entity: sensor.nasa_sky_hub_sky_darkness_level
        name: Sky Darkness
  - type: picture-entity
    entity: camera.nasa_sky_hub_apod
    show_name: true
```

6. **Click "SAVE"**

7. **Done!** You'll see a nice card with all the space info

---

## What Each Entity Shows:

- **Space Weather Severity**: quiet/elevated/storm/severe
- **ISS Overhead**: Yes/No if International Space Station is above you
- **Satellites Overhead**: Number of satellites currently visible
- **Sky Darkness**: 0-100% (higher = darker = better for stargazing)
- **APOD Camera**: Today's Astronomy Picture of the Day

---

## Quick Test:

After adding cards, wait 1-2 minutes, then:
- Cards should show data (not "unavailable")
- Click on cards to see more details
- Space Weather should show "quiet" or another status

---

## Troubleshooting:

**If entities show "unavailable":**
- Wait 2-3 minutes (first data fetch takes time)
- Check Settings → Devices & Services → NASA Sky Hub
- Make sure integration is configured

**If you don't see any NASA entities:**
- Make sure the integration is installed and configured
- Restart Home Assistant
- Check that modules are enabled in integration settings

---

## That's It!

Start with Method 1 (By Entity) - it's the easiest. Just check the boxes and click ADD!
