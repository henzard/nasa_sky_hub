# Lovelace Dashboard Dependencies

## Required Cards (Built-in)

All dashboards now use **standard Home Assistant cards** that work out of the box:
- `markdown` - For headers and text
- `entities` - For displaying entity lists
- `vertical-stack` - For stacking cards vertically
- `grid` - For grid layouts
- `picture-elements` - For overlaying elements on images
- `conditional` - For conditional card display

## Optional Cards (HACS)

Some dashboards include **optional** cards that enhance the experience but aren't required:

### ApexCharts Card (Optional)
- **Used in**: `space_weather.yaml`, `flare_timeline.yaml`
- **Purpose**: Beautiful charts for solar flare activity
- **Installation**: HACS → Frontend → Search "ApexCharts Card"
- **If not installed**: The chart cards will show an error, but other cards will work fine

### Mushroom Cards (Optional - Not Used Anymore)
- **Status**: Removed from all dashboards
- **Previous use**: Enhanced entity cards with better styling
- **Current**: All dashboards use standard `entities` cards instead

## Installation Instructions

### For Standard Dashboards (No Extra Cards Needed)

1. Copy dashboard YAML from `lovelace/dashboards/`
2. Paste into your Lovelace dashboard
3. **That's it!** Everything works with built-in cards

### For Enhanced Dashboards (With Charts)

1. Install ApexCharts Card via HACS:
   - Go to HACS → Frontend
   - Search "ApexCharts Card"
   - Click Install
   - Restart Home Assistant

2. Copy dashboard YAML from `lovelace/dashboards/`
3. Paste into your Lovelace dashboard

## Dashboard Files

- **`space_weather.yaml`** - Space weather monitoring (requires ApexCharts for charts)
- **`sky_overview.yaml`** - Night sky conditions (no dependencies)
- **`earth_events.yaml`** - Earth events and APOD (no dependencies)

## Card Files

- **`whats_above.yaml`** - Quick "what's above" card (no dependencies)
- **`flare_overview.yaml`** - Space weather overview card (no dependencies)
- **`flare_timeline.yaml`** - Flare timeline chart (requires ApexCharts)

## Troubleshooting

### "Custom element doesn't exist" Error

If you see this error:
1. **Check which card is missing** (error message will tell you)
2. **If it's `apexcharts-card`**: Install via HACS (optional)
3. **If it's `mushroom-*`**: Update to latest dashboard files (already fixed)
4. **If it's something else**: Check the dashboard YAML for typos

### Cards Not Showing Data

1. **Verify entities exist**: Settings → Devices & Services → NASA Sky Hub → Entities
2. **Check entity IDs match**: Entity IDs are case-sensitive
3. **Wait 2-3 minutes**: After restart, coordinators need time to fetch data
4. **Check logs**: Settings → System → Logs for errors
