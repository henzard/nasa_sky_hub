# Logo Submission Guide

## Why No Logo Shows

Home Assistant custom integrations **cannot display logos from local files**. Logos must be submitted to the [Home Assistant Brands repository](https://github.com/home-assistant/brands) to be displayed in the UI.

## Current Status

- ✅ **Icon**: Added `"icon": "mdi:rocket-launch"` to `manifest.json` (shows a Material Design icon as fallback)
- ✅ **Logo file**: `logo.png` exists in `custom_components/nasa_sky_hub/` (for HACS display)
- ❌ **Brand logo**: Not yet submitted to Home Assistant Brands repository

## How to Submit Logo to Home Assistant Brands

### Step 1: Prepare Your Logo

1. **Logo Requirements**:
   - Format: PNG
   - Size: 128x128 pixels (recommended)
   - Background: Transparent
   - File name: `logo.png`

2. **Verify your logo**:
   - Located at: `custom_components/nasa_sky_hub/logo.png`
   - Should be square (128x128 recommended)

### Step 2: Fork the Brands Repository

1. Go to: https://github.com/home-assistant/brands
2. Click "Fork" to create your own copy

### Step 3: Add Your Logo

1. **Navigate to the custom integrations folder**:
   ```
   brands/custom_integrations/
   ```

2. **Create a folder** named after your domain:
   ```
   brands/custom_integrations/nasa_sky_hub/
   ```

3. **Add your logo**:
   - Copy `logo.png` to `brands/custom_integrations/nasa_sky_hub/logo.png`
   - The logo should be 128x128 pixels

4. **Create `icon.png`** (optional but recommended):
   - Create a smaller icon version (32x32 or 64x64 pixels)
   - Save as `brands/custom_integrations/nasa_sky_hub/icon.png`

### Step 4: Create Pull Request

1. **Commit your changes**:
   ```bash
   git add brands/custom_integrations/nasa_sky_hub/
   git commit -m "Add logo for nasa_sky_hub integration"
   git push origin your-branch-name
   ```

2. **Create Pull Request**:
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill out the PR description
   - Submit the PR

### Step 5: Wait for Approval

- Home Assistant maintainers will review your PR
- Once merged, your logo will appear in Home Assistant UI
- This may take a few days to weeks

## Alternative: Use Icon (Current Solution)

Until the logo is approved, the integration uses:
- **Icon**: `mdi:rocket-launch` (Material Design icon)
- This appears as a rocket icon in the integration card

## References

- [Home Assistant Brands Repository](https://github.com/home-assistant/brands)
- [Brand Guidelines](https://developers.home-assistant.io/docs/brand/)
- [Integration Branding Documentation](https://developers.home-assistant.io/docs/brand/integration_branding/)
