# EZVIZ Patched

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A custom Home Assistant component that overrides the built-in EZVIZ integration. Used for testing changes and new features before they are submitted to [Home Assistant core](https://github.com/home-assistant/core). The component code is synced with the latest HA core EZVIZ integration and patched on top.

## Installation via HACS

1. **Open HACS** in Home Assistant
2. Go to **Integrations**
3. Click the three dots menu and select **Custom repositories**
4. Add this repository URL with category **Integration**
5. Find **EZVIZ Patched** in the store and install it
6. **Restart Home Assistant**

Your existing EZVIZ configuration will continue working automatically — no reconfiguration needed. The custom component overrides the built-in integration using the same `ezviz` domain.

## Reverting

To go back to the built-in integration:

1. Remove EZVIZ Patched from HACS
2. Restart Home Assistant

Your existing configuration will be picked up by the built-in integration automatically.

## Component Details

- **Domain**: `ezviz` (overrides built-in integration)
- **Based on**: Home Assistant core `dev` branch (synced March 2026)
- **Requirements**: `pyezvizapi==1.0.0.7`

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
