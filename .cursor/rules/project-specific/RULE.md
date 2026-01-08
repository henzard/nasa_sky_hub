---
description: "NASA Sky Hub project-specific rules and conventions"
alwaysApply: true
---

# NASA Sky Hub Project Rules

## Project Structure

- Integration code: `custom_components/nasa_sky_hub/`
- Documentation: `doc/` folder
- Lovelace dashboards: `lovelace/dashboards/`
- Lovelace cards: `lovelace/cards/`
- Root files: `README.md`, `hacs.json`, `logo.png`, `.gitignore`

## Module Organization

- Each module has its own coordinator in `coordinators/`
- Module names match constants in `const.py`
- Enable/disable modules via config flow
- Each module should be independently testable

## Entity Naming

- Format: `{platform}.nasa_sky_hub_{module}_{name}`
- Examples:
  - `sensor.nasa_sky_hub_space_weather_severity`
  - `binary_sensor.nasa_sky_hub_iss_overhead`
  - `camera.nasa_sky_hub_apod`

## Rate Limiting

- All API calls go through centralized rate limiter
- Rate limiter tracks remaining requests
- Degrade gracefully when limits are low
- Log rate limit status for debugging

## Data Flow

1. Config Entry → Creates API Client & Rate Limiter
2. Platform Setup → Creates Coordinators
3. Coordinators → Fetch data via API Client
4. Entities → Display coordinator data

## Logging Strategy

- Setup: INFO level (major steps)
- Operations: DEBUG level (detailed flow)
- Errors: ERROR level (with context)
- Rate limits: WARNING level (recoverable)

## Testing Checklist

Before committing:
- [ ] Version bumped (ONLY if code changed, NOT for docs/rules)
- [ ] All modules work independently
- [ ] Rate limiting functions correctly
- [ ] Entities created for enabled modules
- [ ] No errors in logs
- [ ] HACS compatibility verified
- [ ] No temporary/compliance files created (check `git status`)

## Git Workflow - MANDATORY

**After making ANY changes:**
1. ✅ Check status: `git status`
2. ✅ **Update version in `manifest.json`** (ONLY if code changed in `custom_components/nasa_sky_hub/`)
   - ✅ Code changes: bump version
   - ❌ Documentation/rules: do NOT bump version
3. ✅ Stage changes: `git add .`
4. ✅ Commit immediately: `git commit -m "type: description"`
5. ✅ Push immediately: `git push`
6. ✅ **MANDATORY: Create git tag** (ONLY if version was bumped): `git tag v{VERSION} -m "Version {VERSION}: description"`
7. ✅ **MANDATORY: Push tag** (ONLY if version was bumped): `git push origin v{VERSION}`

**Never leave uncommitted changes.** All file modifications must be committed, pushed, AND tagged in the same session.

## HACS Version Display - CRITICAL

**HACS requires GitHub Releases to display versions correctly.**

Without GitHub Releases:
- HACS shows commit hashes (e.g., "4b79009") instead of "v1.1.5"
- Version comparison fails
- Update notifications break

**Every version bump MUST include:**
1. Git tag creation and push
2. **GitHub Release creation** (HACS reads releases, not just tags!)

**GitHub Release Steps:**
- GitHub → Releases → Draft a new release
- Select tag: `v{VERSION}`
- Title: `Version {VERSION}`
- Publish release

## Files to Never Create

**Never create these types of files:**
- Compliance reports (`*_COMPLIANCE_*.md`, `*_REPORT_*.md`)
- Status check files (`*_CHECK_*.md`)
- Meta-documentation about project compliance
- Temporary tracking files

**Use git commands instead:**
- `git status` - Check what changed
- `git diff` - Review changes
- Don't create files to track compliance - check rules directly

## Common Patterns

### Coordinator Pattern
```python
class MyCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_client, update_interval=1800):
        super().__init__(hass, _LOGGER, name="my_module")
        self.api_client = api_client
        
    async def _async_update_data(self):
        return await self.api_client.get_data()
```

### Entity Pattern
```python
class MySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, description):
        super().__init__(coordinator)
        self.entity_description = description
```

## Dependencies

- `aiohttp>=3.8.0` - HTTP client
- `pyephem>=4.1` - Astronomical calculations
- `skyfield>=1.42` - Satellite tracking

Keep dependencies minimal and well-justified.
