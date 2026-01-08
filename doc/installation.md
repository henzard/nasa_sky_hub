# Installation Methods

## Method 1: HACS (Recommended - Easiest)

### Prerequisites
- Home Assistant 2023.1 or later
- [HACS](https://hacs.xyz/) installed

### Installation Steps

1. **Add Custom Repository to HACS**:
   - Go to HACS → Integrations
   - Click the three dots (⋮) in the top right
   - Select "Custom repositories"
   - Add repository URL: `https://github.com/yourusername/nasa_sky_hub`
   - Category: Integration
   - Click "Add"

2. **Install Integration**:
   - Search for "NASA Sky Hub" in HACS
   - Click on it
   - Click "Download"
   - Restart Home Assistant

3. **Configure**:
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "NASA Sky Hub"
   - Follow the setup wizard

## Method 2: Direct Git Clone (For Advanced Users)

### On Home Assistant OS / Supervised

If you have SSH access to your Home Assistant:

```bash
# SSH into your Home Assistant
ssh root@your-ha-ip

# Navigate to custom_components
cd /config/custom_components

# Clone the repository
git clone https://github.com/yourusername/nasa_sky_hub.git nasa_sky_hub

# Restart Home Assistant
```

### On Docker

```bash
# Access your Home Assistant container
docker exec -it homeassistant bash

# Navigate to custom_components
cd /config/custom_components

# Clone the repository
git clone https://github.com/yourusername/nasa_sky_hub.git nasa_sky_hub

# Exit and restart container
exit
docker restart homeassistant
```

### On Linux Install

```bash
# Navigate to Home Assistant config directory
cd ~/.homeassistant/custom_components

# Clone the repository
git clone https://github.com/yourusername/nasa_sky_hub.git nasa_sky_hub

# Restart Home Assistant service
sudo systemctl restart home-assistant
```

## Method 3: Manual Download

1. **Download ZIP**:
   - Go to https://github.com/yourusername/nasa_sky_hub
   - Click "Code" → "Download ZIP"
   - Extract the ZIP file

2. **Copy Integration**:
   - Copy the `custom_components/nasa_sky_hub` folder
   - Paste it into your Home Assistant `custom_components` directory

3. **Restart Home Assistant**

## Method 4: Using HACS with Custom Repository (Before HACS Approval)

If you want to use HACS but the integration isn't in the default HACS store yet:

1. **Add as Custom Repository**:
   - HACS → Integrations → Custom repositories
   - Repository: `https://github.com/yourusername/nasa_sky_hub`
   - Category: Integration
   - Click "Add"

2. **Install**:
   - Search for "NASA Sky Hub"
   - Click "Download"
   - Restart Home Assistant

## Updating the Integration

### Via HACS
- HACS will show updates automatically
- Click "Update" when available
- Restart Home Assistant

### Via Git Clone
```bash
cd /config/custom_components/nasa_sky_hub
git pull
# Restart Home Assistant
```

## Troubleshooting Installation

### Integration Not Appearing

1. **Check Folder Structure**:
   ```
   custom_components/
   └── nasa_sky_hub/
       ├── __init__.py
       ├── manifest.json
       └── ...
   ```

2. **Verify manifest.json**:
   - Must be valid JSON
   - Domain must be `nasa_sky_hub`

3. **Check Logs**:
   - Settings → System → Logs
   - Look for errors related to `nasa_sky_hub`

4. **Restart Completely**:
   - Not just reload, but full restart

### HACS Installation Issues

1. **Clear HACS Cache**:
   - HACS → Settings → Clear cache
   - Restart Home Assistant

2. **Check Repository URL**:
   - Must be correct GitHub URL
   - Must be public repository

3. **Verify HACS Version**:
   - Update HACS if outdated

## Next Steps

After installation:
1. See [QUICKSTART.md](QUICKSTART.md) for configuration
2. See [TESTING.md](TESTING.md) for testing instructions
3. See [README.md](README.md) for full documentation
