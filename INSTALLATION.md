# Installation Guide

## ✅ Easy Installation

This custom component **automatically overrides** the built-in EZVIZ integration. You do **NOT** need to remove your existing EZVIZ integration - it will be seamlessly replaced.

## Step-by-Step Installation

### 1. Install EZVIZ Patched via HACS

1. **Open HACS** in Home Assistant
2. **Go to Integrations**
3. **Click the three dots menu (⋮)**
4. **Select "Custom repositories"**
5. **Add repository:**
   - Repository: `https://github.com/yourusername/ezviz-patched`
   - Category: `Integration`
6. **Click "Add"**
7. **Find "EZVIZ Patched"** in the store and install it
8. **Restart Home Assistant**

### 2. Automatic Override

After installation and restart:

- **Your existing EZVIZ configuration will continue to work**
- **All your cameras and sensors will remain configured**
- **The custom component will automatically take over**
- **No reconfiguration needed!**

## How Override Works

This custom component uses the same domain name (`ezviz`) as the built-in integration. Home Assistant automatically prioritizes custom components over built-in ones, so your existing configuration will seamlessly continue working with the patched version.

## Troubleshooting

### Integration Doesn't Appear

- Make sure HACS installation was successful
- Check that the repository URL is correct
- Restart Home Assistant after HACS installation

### Sensors Still Not Working

- Check the Home Assistant logs for any errors
- Make sure your EZVIZ account credentials are correct
- Verify the custom component is loaded (check logs for "Loaded ezviz from custom_components")

### Custom Component Not Loading

- Ensure the custom component files are in `custom_components/ezviz/`
- Check that `manifest.json` has a valid `version` field
- Restart Home Assistant completely

## Reverting Back

If you need to go back to the original EZVIZ integration:

1. **Remove EZVIZ Patched** from HACS
2. **Restart Home Assistant**
3. **The built-in EZVIZ integration will automatically take over again**
4. **Your existing configuration will continue working**

## Support

For issues with this patched component, check the [Home Assistant issue #151648](https://github.com/home-assistant/core/issues/151648) for the original bug report.
