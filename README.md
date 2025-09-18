# EZVIZ Patched

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A custom component that overrides the built-in EZVIZ integration. This component is identical to the current Home Assistant core EZVIZ integration and includes all the latest fixes, including the resolution for the `KeyError: 'mode'` bug that occurred in Home Assistant 2025.9.0.

## ✅ What's Included

- **Latest EZVIZ integration code**: Identical to current Home Assistant core
- **All bug fixes**: Includes the fix for the 'mode' sensor KeyError from [PR #151848](https://github.com/home-assistant/core/pull/151848)
- **Full functionality**: All sensors, cameras, and features work properly

## 📦 Installation via HACS

✅ **Easy Installation**: This component automatically overrides the built-in EZVIZ integration. Your existing configuration will continue working seamlessly.

### Install EZVIZ Patched

1. **Open HACS** in Home Assistant
2. **Go to Integrations**
3. **Click the three dots menu** (⋮)
4. **Select "Custom repositories"**
5. **Add repository:**
   - Repository: `https://github.com/yourusername/ezviz_patched`
   - Category: `Integration`
6. **Click "Add"**
7. **Find "EZVIZ Patched"** in the store and install it
8. **Restart Home Assistant**

### Automatic Override

After installation and restart:

- ✅ **Your existing EZVIZ configuration continues to work**
- ✅ **All your cameras and sensors remain configured**
- ✅ **The custom component automatically takes over**
- ✅ **No reconfiguration needed!**

## 🚀 Usage

This custom component works exactly like the original EZVIZ integration but with the bug fixes applied. You can:

1. Add it through the integrations UI
2. Configure your EZVIZ cameras and sensors
3. All sensors should now work properly without the KeyError

## ⚠️ Important Notes

- This component **overrides the built-in EZVIZ integration** using the same domain name (`ezviz`)
- It contains the **latest code from Home Assistant core** with all current fixes
- The fix for the `KeyError: 'mode'` bug from [PR #151848](https://github.com/home-assistant/core/pull/151848) is included

## 🔗 Original Issue

This component includes the fix for [Home Assistant issue #151648](https://github.com/home-assistant/core/issues/151648) where EZVIZ sensors were becoming unavailable after updating to Home Assistant 2025.9.0 due to a missing 'mode' sensor type definition.

## 📝 Component Details

- **Domain**: `ezviz` (overrides built-in integration)
- **Version**: `2025.9.0-patched`
- **Requirements**: `pyezvizapi==1.0.0.7`
- **Identical to**: Current Home Assistant core EZVIZ integration

## 📋 Version

- Based on Home Assistant 2025.9.0
- Patched version: 2025.9.0-patched

## 🤝 Contributing

This is a temporary fix. For the official fix, please contribute to the [Home Assistant Core repository](https://github.com/home-assistant/core).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
