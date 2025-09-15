# EZVIZ Patched

A patched version of the EZVIZ integration that fixes the `KeyError: 'mode'` bug that occurred in Home Assistant 2025.9.0.

## What's Fixed

- **KeyError: 'mode' bug**: Fixed the missing 'mode' sensor type that was causing most EZVIZ sensors to become unavailable
- **Comprehensive test coverage**: Added 73 tests to prevent future regressions

## Installation

1. Install this custom component through HACS
2. Restart Home Assistant
3. The integration will appear as "EZVIZ (Patched)" in the integrations list

## Usage

This custom component works exactly like the original EZVIZ integration but with the bug fixes applied. You can:

1. Add it through the integrations UI
2. Configure your EZVIZ cameras and sensors
3. All sensors should now work properly without the KeyError

## Important Notes

- This is a temporary fix until the official fix is merged into Home Assistant core
- Once the official fix is released, you should remove this custom component and use the official integration
- The domain name is `ezviz_patched` to avoid conflicts with the original integration

## Original Issue

This fixes issue #151648 where EZVIZ sensors were becoming unavailable after updating to Home Assistant 2025.9.0 due to a missing 'mode' sensor type definition.

## Files Modified

- `sensor.py`: Added missing 'mode' sensor type to SENSOR_TYPES
- `__init__.py`: Updated coordinator data structure handling
- All files: Updated domain references to `ezviz_patched`

## Version

- Based on Home Assistant 2025.9.0
- Patched version: 2025.9.0-patched
