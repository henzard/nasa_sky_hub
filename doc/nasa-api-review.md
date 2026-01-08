# NASA API Implementation Review

This document reviews each NASA API from the official catalog (https://api.nasa.gov/) and verifies our implementation against the official documentation.

## ✅ Implemented APIs

### 1. APOD (Astronomy Picture of the Day)
- **Status**: ✅ Correctly Implemented
- **Endpoint**: `GET https://api.nasa.gov/planetary/apod`
- **Parameters**: 
  - `date` (YYYY-MM-DD, optional, default: today)
  - `start_date`, `end_date` (for date ranges)
  - `count` (for random images)
  - `thumbs` (bool, for video thumbnails)
  - `api_key` (required)
- **Our Implementation**: Uses `/planetary/apod` with optional `date` parameter ✅
- **Notes**: Currently experiencing service outage per NASA docs, but implementation is correct

### 2. DONKI (Space Weather Database)
- **Status**: ✅ Correctly Implemented
- **Endpoints Used**:
  - `/DONKI/FLR` - Solar Flares
  - `/DONKI/CME` - Coronal Mass Ejections
  - `/DONKI/GST` - Geomagnetic Storms
- **Parameters**: 
  - `startDate` (YYYY-MM-DD, default: 30 days prior)
  - `endDate` (YYYY-MM-DD, default: current UTC date)
  - `api_key` (required)
- **Our Implementation**: ✅ Correctly uses all three endpoints with `startDate` and `endDate` parameters
- **Additional DONKI Endpoints Available** (not currently implemented):
  - `/DONKI/CMEAnalysis` - CME Analysis with advanced filtering
  - `/DONKI/IPS` - Interplanetary Shocks
  - `/DONKI/SEP` - Solar Energetic Particles
  - `/DONKI/MPC` - Magnetopause Crossings
  - `/DONKI/RBE` - Radiation Belt Enhancements
  - `/DONKI/HSS` - High Speed Streams
  - `/DONKI/WSAEnlilSimulations` - WSA+Enlil Simulations
  - `/DONKI/notifications` - Combined notifications

### 3. EONET (Earth Observatory Natural Event Tracker)
- **Status**: ✅ Correctly Implemented (Fixed)
- **Endpoint**: `GET https://eonet.gsfc.nasa.gov/api/v3/events`
- **Parameters**: 
  - `days` (int, default: 30)
  - No API key required
- **Our Implementation**: ✅ Fixed to use correct endpoint `eonet.gsfc.nasa.gov/api/v3/events` (not `api.nasa.gov/EONET/events`)
- **Notes**: EONET is accessed directly, not through `api.nasa.gov`. It does not require an API key.

### 4. NeoWs (Near Earth Object Web Service)
- **Status**: ✅ Correctly Implemented
- **Endpoints**:
  - `/neo/rest/v1/feed` - Asteroid feed by date range
  - `/neo/rest/v1/neo/{asteroid_id}` - Lookup specific asteroid
  - `/neo/rest/v1/neo/browse` - Browse all asteroids
- **Parameters**:
  - `start_date` (YYYY-MM-DD, required)
  - `end_date` (YYYY-MM-DD, default: 7 days after start_date)
  - `api_key` (required)
- **Our Implementation**: ✅ Uses `/neo/rest/v1/feed` with `start_date` and `end_date` parameters
- **Notes**: We only implement the feed endpoint. Lookup and browse endpoints are available but not used.

## ❌ Not Implemented APIs

### 5. EPIC (Earth Polychromatic Imaging Camera)
- **Status**: ❌ Not Implemented
- **Endpoint**: `GET https://api.nasa.gov/EPIC/api/{type}/{path}`
- **Types**: `natural`, `enhanced`
- **Paths**: `images`, `date/{YYYY-MM-DD}`, `all`, `available`
- **Parameters**: `api_key` (required)
- **Use Case**: Full disc imagery of Earth from DSCOVR satellite
- **Potential Value**: Could add Earth imagery camera entity

### 6. Exoplanet Archive
- **Status**: ❌ Not Implemented
- **Endpoint**: Various endpoints for exoplanet data
- **Use Case**: Programmatic access to NASA's Exoplanet Archive database
- **Potential Value**: Could add exoplanet discovery sensors

### 7. GIBS (Global Imagery Browse Services)
- **Status**: ❌ Not Implemented
- **Endpoint**: WMTS/WMS tile services
- **Use Case**: Standardized web services for global satellite imagery
- **Potential Value**: Could add Earth imagery layers

### 8. Insight Mars Weather
- **Status**: ❌ Not Implemented
- **Endpoint**: `GET https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0`
- **Parameters**: 
  - `api_key` (required)
  - `feedtype` (string, default: "json")
  - `ver` (float, default: 1.0)
- **Use Case**: Mars weather measurements (temperature, wind, pressure) from InSight lander
- **Rate Limit**: 2,000 requests per hour per IP
- **Potential Value**: ⚠️ **Limited Value** - Has significant missing data due to power management issues on Mars. Last updated 3/30/2021. Could add Mars weather sensors but data reliability is questionable.
- **Notes**: Service has gaps due to InSight needing to manage power use during Martian winter/dust storms

### 9. NASA Image and Video Library
- **Status**: ❌ Not Implemented
- **Endpoint**: Various endpoints for searching NASA media
- **Use Case**: Access to NASA Image and Video Library at images.nasa.gov
- **Potential Value**: ⚠️ **Low Priority** - Media search doesn't align with real-time space awareness focus

### 10. Open Science Data Repository
- **Status**: ❌ Not Implemented
- **Use Case**: Programmatic interface for Open Science Data Repository website
- **Potential Value**: ❌ **Not Relevant** - Research data access doesn't fit space awareness use case

### 11. Satellite Situation Center (SSC)
- **Status**: ❌ Not Implemented
- **Endpoint**: `POST https://sscweb.gsfc.nasa.gov/WS/sscr/2/{endpoint}`
- **Endpoints**:
  - `/locations` - Get spacecraft locations with geophysical region mapping
  - `/graphs` - Generate orbit plots
  - `/conjunctions` - Find magnetic/radial conjunctions between satellites
- **Use Case**: System to cast geocentric spacecraft location information into geophysical regions (magnetosphere, plasmasphere, etc.)
- **Parameters**: Complex XML/JSON requests with satellite IDs, time intervals, coordinate systems, magnetic field models
- **Potential Value**: ⚠️ **Moderate Value** - Could enhance satellite tracking with geophysical region context (e.g., "ISS is in nightside magnetosphere"), but:
  - Very complex API (requires XML schema knowledge, magnetic field models)
  - JSON support is "less stable and may change"
  - Primarily designed for scientific research, not real-time monitoring
  - Would add significant complexity for moderate value
- **Recommendation**: Skip for now - too complex for the value it provides

### 12. SSD/CNEOS (Solar System Dynamics / Center for Near-Earth Object Studies)
- **Status**: ❌ Not Implemented
- **Base URL**: `https://ssd-api.jpl.nasa.gov/`
- **APIs Available**:
  
  #### 12a. CAD (Close Approach Data) API ✅ **HIGH VALUE**
  - **Endpoint**: `GET https://ssd-api.jpl.nasa.gov/cad.api`
  - **Use Case**: Close approach data for asteroids and comets (when they pass near Earth/planets)
  - **Key Parameters**:
    - `date-min`, `date-max` - Date range (default: now to +60 days)
    - `dist-max` - Maximum approach distance (default: 0.05 AU)
    - `body` - Target body (Earth, Moon, Mars, etc., default: Earth)
    - `neo` - Filter to NEOs only (default: true)
    - `pha` - Filter to Potentially Hazardous Asteroids
    - `sort` - Sort by date, distance, velocity, etc.
  - **Returns**: Detailed close approach data including:
    - Approach distance (nominal, min, max with 3-sigma uncertainty)
    - Velocity (relative and infinity)
    - Object diameter, absolute magnitude
    - Approach date/time
  - **Potential Value**: ✅ **VERY HIGH** - Perfect complement to NeoWs feed:
    - Provides detailed close approach predictions (when asteroids will be closest)
    - Includes uncertainty ranges (3-sigma)
    - Can filter by distance, size, velocity
    - Can query approaches to Moon, Mars, etc. (not just Earth)
  - **Recommendation**: **Implement this** - Would add significant value for asteroid tracking
  
  #### 12b. Fireball Data API ⚠️ **MODERATE VALUE**
  - **Endpoint**: `GET https://ssd-api.jpl.nasa.gov/fireball.api`
  - **Use Case**: Fireball (bright meteor) data from CNEOS sensors
  - **Key Parameters**:
    - `date-min`, `date-max` - Date range
    - `energy-min`, `energy-max` - Total radiated energy filter
    - `impact-e-min`, `impact-e-max` - Impact energy filter (kilotons)
    - `req-loc`, `req-alt` - Require location/altitude data
  - **Returns**: Fireball events with:
    - Date/time, location (lat/lon), altitude
    - Total radiated energy (×10¹⁰ joules)
    - Estimated impact energy (kilotons)
    - Entry velocity components (vx, vy, vz)
  - **Potential Value**: ⚠️ **MODERATE** - Interesting but:
    - Historical data (fireballs that already happened)
    - Not predictive (can't predict future fireballs)
    - Useful for "recent fireball events" sensor but limited real-time value
  - **Recommendation**: Consider for future - Nice-to-have but not critical
  
  #### 12c. Sentry API ✅ **HIGH VALUE**
  - **Endpoint**: `GET https://ssd-api.jpl.nasa.gov/sentry.api`
  - **Use Case**: Impact risk assessment for asteroids (CNEOS Sentry system)
  - **Modes**:
    - **Mode O** - Object-specific details (query by asteroid designation)
    - **Mode S** - Summary table (all Sentry objects)
    - **Mode V** - Virtual Impactor (VI) table
    - **Mode R** - Removed objects (previously tracked, now removed)
  - **Key Parameters**:
    - `des` or `spk` - Asteroid designation/SPK-ID (Mode O)
    - `ip-min` - Minimum impact probability filter
    - `ps-min` - Minimum Palermo Scale filter
    - `h-max` - Maximum absolute magnitude (size filter)
    - `days` - Days since last observation
  - **Returns**: Impact risk data including:
    - Impact probability (cumulative and per-event)
    - Palermo Scale (hazard rating)
    - Torino Scale (hazard rating, <100 years only)
    - Impact energy (Megatons TNT)
    - Impact dates
    - Object diameter, mass, velocity
  - **Potential Value**: ✅ **VERY HIGH** - Critical for asteroid threat monitoring:
    - Provides impact risk assessment (which asteroids could hit Earth)
    - Includes hazard scales (Palermo, Torino)
    - Shows impact probabilities and dates
    - Can track objects removed from Sentry (no longer threats)
  - **Recommendation**: **Implement this** - Essential for comprehensive asteroid threat awareness
  
  #### 12d. Other SSD APIs
  - **NHATS** (Near-Earth Object Human Space Flight Accessible Targets Study) - Mission design data
  - **Scout** - Real-time impact assessment for newly discovered objects
  - **Mission Design** - Trajectory design tools
  - **Potential Value**: ⚠️ **Low** - Specialized mission planning tools, not general space awareness

### 13. Techport
- **Status**: ❌ Not Implemented
- **Endpoint**: RESTful API at https://techport.nasa.gov/help/articles/api
- **Use Case**: NASA technology project data (active and completed projects)
- **Potential Value**: ❌ **Not Relevant** - Technology project tracking doesn't fit space awareness use case

### 14. TechTransfer
- **Status**: ❌ Not Implemented
- **Endpoint**: `GET https://api.nasa.gov/techtransfer/patent/` (and `/software/`, `/spinoff/`)
- **Parameters**: 
  - `patent` (string) - Search patents
  - `patent_issued` (string) - Filter by issue date
  - `software` (string) - Search software
  - `Spinoff` (string) - Search spinoff examples
  - `api_key` (required)
- **Use Case**: Patents, Software, and Tech Transfer Reports
- **Potential Value**: ❌ **Not Relevant** - Patent/technology search doesn't fit space awareness use case

### 15. TLE API
- **Status**: ✅ **Correctly Using Alternative** (Celestrak)
- **Endpoint**: `GET http://tle.ivanstanojevic.me/api/tle` (NOT api.nasa.gov)
- **Endpoints**:
  - `/api/tle?search={q}` - Search by satellite name
  - `/api/tle/{q}` - Get TLE by satellite number
- **Use Case**: Two line element data for earth-orbiting objects (JSON format)
- **Our Approach**: ✅ We use Celestrak directly (`https://celestrak.org/NORAD/elements/stations.txt`) which is:
  - More comprehensive (includes all satellites, not just searchable ones)
  - More reliable (primary source)
  - Already integrated and working
- **Notes**: NASA's TLE API is actually hosted at `tle.ivanstanojevic.me` (not api.nasa.gov) and gets data from Celestrak anyway. Our direct Celestrak approach is optimal.

### 16. Vesta/Moon/Mars Trek WMTS
- **Status**: ❌ Not Implemented
- **Use Case**: Web Map Tile Service (WMTS) for Vesta, Moon, and Mars imagery
- **Potential Value**: ⚠️ **Low Priority** - Planetary map tiles are interesting but complex to integrate and don't align with real-time space awareness focus

## Implementation Summary

### Correctly Implemented ✅
1. **APOD** - Astronomy Picture of the Day
2. **DONKI FLR/CME/GST** - Space Weather (3 of 11 available endpoints)
3. **EONET** - Earth Events (fixed endpoint)
4. **NeoWs Feed** - Near Earth Objects (1 of 3 available endpoints)

### Issues Fixed
- **EONET Endpoint**: Fixed from incorrect `api.nasa.gov/EONET/events` to correct `eonet.gsfc.nasa.gov/api/v3/events`

### Potential Enhancements (Ranked by Value)

#### Critical High Value Additions ✅ **IMPLEMENT THESE**
1. **SSD/CNEOS Sentry API** - Impact risk assessment for asteroids
   - Provides impact probabilities, hazard scales (Palermo/Torino)
   - Shows which asteroids pose threats to Earth
   - Essential for comprehensive asteroid threat monitoring
   - **Priority**: **HIGHEST** - Critical safety data

2. **SSD/CNEOS CAD API** - Close Approach Data
   - Detailed close approach predictions (when asteroids pass closest)
   - Includes uncertainty ranges, velocities, sizes
   - Can query approaches to Earth, Moon, Mars, etc.
   - **Priority**: **HIGH** - Perfect complement to NeoWs feed

#### High Value Additions ✅
3. **EPIC**: Add Earth imagery camera entity (full disc Earth from DSCOVR)
4. **DONKI Additional Endpoints**: Add SEP, IPS, RBE for comprehensive space weather monitoring

#### Moderate Value ⚠️
5. **SSD/CNEOS Fireball API** - Recent fireball events (historical data, not predictive)
6. **NeoWs Lookup/Browse**: Add asteroid lookup and browse endpoints for detailed asteroid info
7. **Satellite Situation Center**: Add geophysical region context to satellite tracking (complex, moderate value)

#### Low Priority / Not Recommended ❌
6. **Insight Mars Weather**: Has significant data gaps, unreliable for real-time monitoring
7. **Vesta/Moon/Mars Trek WMTS**: Complex integration, doesn't fit real-time focus
8. **Techport/TechTransfer**: Not relevant for space awareness use case
9. **NASA Image/Video Library**: Media search doesn't align with real-time monitoring
10. **Open Science Data Repository**: Research data doesn't fit use case

## Rate Limits

All `api.nasa.gov` APIs share the same rate limits:
- **API Key**: 1,000 requests per hour
- **DEMO_KEY**: 30 requests per hour, 50 requests per day

**EONET** (separate service):
- No API key required
- No documented rate limits (but should be used responsibly)

## Key Findings

### ✅ Correct Implementation Verified
- All implemented APIs match official NASA documentation exactly
- EONET endpoint corrected (was using wrong base URL)
- TLE data source verified (Celestrak is optimal choice)

### 🎯 Recommended Next Additions (Priority Order)
1. **SSD/CNEOS Sentry API** - **CRITICAL** - Impact risk assessment (which asteroids threaten Earth)
2. **SSD/CNEOS CAD API** - **HIGH** - Close approach predictions (when asteroids pass closest)
3. **EPIC** - High value for Earth imagery camera entity
4. **DONKI SEP/IPS/RBE** - High value for comprehensive space weather
5. **SSD/CNEOS Fireball API** - Moderate value for recent fireball events (historical)

### ⚠️ APIs Not Recommended
- **Insight**: Data reliability issues (power management gaps)
- **Techport/TechTransfer**: Not relevant to space awareness
- **NASA Image Library**: Doesn't fit real-time monitoring focus

## References

- Official NASA API Portal: https://api.nasa.gov/
- APOD API: https://api.nasa.gov/#apod
- DONKI API: https://api.nasa.gov/#donki
- EONET API: https://api.nasa.gov/#eonet (actual endpoint: https://eonet.gsfc.nasa.gov/api/v3/events)
- NeoWs API: https://api.nasa.gov/#neows
- EPIC API: https://api.nasa.gov/#epic
- Insight API: https://api.nasa.gov/#insight
- TechTransfer API: https://api.nasa.gov/#techtransfer
- TLE API: http://tle.ivanstanojevic.me (not api.nasa.gov)
- Celestrak: https://celestrak.org/ (our TLE source)
- SSD/CNEOS APIs: https://ssd-api.jpl.nasa.gov/
  - CAD API: https://ssd-api.jpl.nasa.gov/doc/cad.html
  - Fireball API: https://ssd-api.jpl.nasa.gov/doc/fireball.html
  - Sentry API: https://ssd-api.jpl.nasa.gov/doc/sentry.html
- Satellite Situation Center: https://sscweb.gsfc.nasa.gov/WebServices/REST/json/
