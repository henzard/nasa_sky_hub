#!/bin/bash
# Quick test script for NASA Sky Hub integration

echo "=== NASA Sky Hub Integration Test ==="
echo ""

# Check if we're in the right directory
if [ ! -d "custom_components/nasa_sky_hub" ]; then
    echo "❌ Error: custom_components/nasa_sky_hub directory not found"
    echo "   Run this script from the project root"
    exit 1
fi

echo "✅ Found integration directory"

# Check for required files
REQUIRED_FILES=(
    "custom_components/nasa_sky_hub/__init__.py"
    "custom_components/nasa_sky_hub/manifest.json"
    "custom_components/nasa_sky_hub/config_flow.py"
    "custom_components/nasa_sky_hub/api_client.py"
    "custom_components/nasa_sky_hub/rate_limiter.py"
    "custom_components/nasa_sky_hub/sensor.py"
    "custom_components/nasa_sky_hub/binary_sensor.py"
    "custom_components/nasa_sky_hub/camera.py"
)

echo ""
echo "Checking required files..."
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ Missing: $file"
    fi
done

# Check manifest.json syntax
echo ""
echo "Validating manifest.json..."
if python3 -m json.tool custom_components/nasa_sky_hub/manifest.json > /dev/null 2>&1; then
    echo "✅ manifest.json is valid JSON"
else
    echo "❌ manifest.json has syntax errors"
fi

# Check Python syntax
echo ""
echo "Checking Python syntax..."
python3 -m py_compile custom_components/nasa_sky_hub/__init__.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Python syntax OK"
else
    echo "❌ Python syntax errors found"
fi

# Check for coordinators
echo ""
echo "Checking coordinators..."
if [ -d "custom_components/nasa_sky_hub/coordinators" ]; then
    echo "✅ Coordinators directory exists"
    COORDINATORS=(
        "coordinators/space_weather.py"
        "coordinators/apod.py"
        "coordinators/satellites.py"
        "coordinators/sky.py"
    )
    for coord in "${COORDINATORS[@]}"; do
        if [ -f "custom_components/nasa_sky_hub/$coord" ]; then
            echo "  ✅ $coord"
        else
            echo "  ❌ Missing: $coord"
        fi
    done
else
    echo "❌ Coordinators directory missing"
fi

# Check Lovelace dashboards
echo ""
echo "Checking Lovelace dashboards..."
if [ -d "lovelace/dashboards" ]; then
    echo "✅ Lovelace dashboards directory exists"
    DASHBOARDS=(
        "lovelace/dashboards/space_weather.yaml"
        "lovelace/dashboards/sky_overview.yaml"
        "lovelace/dashboards/earth_events.yaml"
    )
    for dashboard in "${DASHBOARDS[@]}"; do
        if [ -f "$dashboard" ]; then
            echo "  ✅ $dashboard"
        else
            echo "  ❌ Missing: $dashboard"
        fi
    done
else
    echo "⚠️  Lovelace dashboards directory not found (optional)"
fi

echo ""
echo "=== Test Complete ==="
echo ""
echo "Next steps:"
echo "1. Copy custom_components/nasa_sky_hub to your HA config directory"
echo "2. Restart Home Assistant"
echo "3. Add integration via Settings → Devices & Services"
echo "4. See TESTING.md for detailed testing instructions"
