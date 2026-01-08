# How to Get Logs and Diagnostics for Troubleshooting

## Method 1: Get Full Diagnostics (Easiest - Shows Everything)

1. **Go to Settings → Devices & Services**
2. **Click on "NASA Sky Hub"** integration
3. **Click the three dots (⋮)** in the top right
4. **Click "Download diagnostics"**
5. **A JSON file will download** - this contains ALL the info I need!

**What's in diagnostics:**
- All configuration settings
- All entities and their states
- Rate limiter status
- Coordinator statuses
- API status
- Everything!

---

## Method 2: Get Logs from Home Assistant

1. **Go to Settings → System → Logs**
2. **In the filter box**, type: `nasa_sky_hub`
3. **Copy all the log entries** that show up
4. **Or click "Download"** to get full log file

**What to look for:**
- Errors (red text)
- Warnings (yellow text)
- Info messages starting with "NASA Sky Hub"

---

## Method 3: Get Specific Entity States

1. **Go to Developer Tools → States**
2. **Search for: `nasa`**
3. **Take a screenshot** of all the entities
4. **Or copy the entity IDs** and their states

---

## Method 4: Get Configuration Screenshot

1. **Go to Settings → Devices & Services**
2. **Click on "NASA Sky Hub"**
3. **Click "Configure"** (or three dots → Configure)
4. **Take a screenshot** of the configuration screen

This shows:
- Which modules are enabled
- API key status (masked)
- Location settings
- Profile settings

---

## What to Send Me

For best troubleshooting, send me:

1. **Diagnostics file** (Method 1) - This is the most helpful!
2. **Screenshot of config screen** (Method 4)
3. **Screenshot of entities** (Method 3) - if entities aren't showing
4. **Any error logs** (Method 2) - if there are errors

---

## Quick Diagnostic Check

Run this in Developer Tools → Services to test:

```yaml
service: system_log.write
data:
  message: "NASA Sky Hub Diagnostic Test"
  level: info
```

Then check logs to confirm logging is working.

---

## Enable Debug Logging (For More Details)

Add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.nasa_sky_hub: debug
```

Then restart Home Assistant. This will give MUCH more detailed logs.

---

## Common Issues to Check in Logs

**"Entity not found" errors:**
- Look for "Setting up sensors" messages
- Check if coordinators are being created
- Verify modules are enabled

**API errors:**
- Look for "NASA API request failed"
- Check rate limit messages
- Verify API key is set

**No data:**
- Check coordinator refresh messages
- Look for "async_config_entry_first_refresh" messages
- Verify location is set correctly

---

## Export Everything at Once

1. **Diagnostics**: Settings → Devices & Services → NASA Sky Hub → Download diagnostics
2. **Logs**: Settings → System → Logs → Download
3. **Screenshot**: Config screen and entity list

Send me all three and I can diagnose any issue!
