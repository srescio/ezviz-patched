# Installation Guide

## ⚠️ Important: Before Installing

**You must remove the original EZVIZ integration first** before installing this patched version, otherwise you'll get a "account is already configured" error.

## Step-by-Step Installation

### 1. Remove Original EZVIZ Integration

1. **Go to Settings > Devices & Services**
2. **Find the original "EZVIZ" integration**
3. **Click on it**
4. **Click the three dots menu (⋮)**
5. **Select "Delete"**
6. **Confirm deletion**

### 2. Install EZVIZ Patched via HACS

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

### 3. Configure EZVIZ Patched

1. **Go to Settings > Devices & Services**
2. **Click "Add Integration"**
3. **Search for "EZVIZ Patched"**
4. **Configure your EZVIZ account**
5. **All your sensors should now work properly!**

## Why This Happens

The original EZVIZ integration and this patched version both try to configure the same EZVIZ account. Home Assistant prevents duplicate configurations, so you need to remove the original first.

## Troubleshooting

### "Account is already configured" Error

- Make sure you've completely removed the original EZVIZ integration
- Check that no EZVIZ entities are still present in your system
- Restart Home Assistant after removing the original integration

### Integration Doesn't Appear

- Make sure HACS installation was successful
- Check that the repository URL is correct
- Restart Home Assistant after HACS installation

### Sensors Still Not Working

- Verify you're using the "EZVIZ Patched" integration (not the original)
- Check the Home Assistant logs for any errors
- Make sure your EZVIZ account credentials are correct

## Reverting Back

If you need to go back to the original EZVIZ integration:

1. **Remove EZVIZ Patched** from HACS
2. **Restart Home Assistant**
3. **Add the original EZVIZ integration** from the official integrations list
4. **Configure your account again**

## Support

For issues with this patched component, check the [Home Assistant issue #151648](https://github.com/home-assistant/core/issues/151648) for the original bug report.
