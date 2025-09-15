# Troubleshooting Guide

## Integration Not Appearing in HACS

### Check Repository Structure
Make sure your repository has this structure:
```
ezviz-patched/
├── hacs.json                    # HACS configuration
├── info.md                      # HACS info page
├── README.md                    # Documentation
├── LICENSE                      # License file
└── custom_components/
    └── ezviz_patched/           # Component directory
        ├── manifest.json        # Home Assistant manifest
        ├── __init__.py          # Main integration file
        ├── sensor.py            # Sensor platform
        └── [other files]        # All other component files
```

### Verify HACS Configuration
Check that `hacs.json` contains:
```json
{
  "name": "EZVIZ Patched",
  "content_in_root": false,
  "filename": "ezviz_patched",
  "country": ["US", "GB", "DE", "FR", "ES", "IT", "NL", "BE", "CH", "AT", "SE", "NO", "DK", "FI", "PL", "CZ", "HU", "RO", "BG", "HR", "SI", "SK", "LT", "LV", "EE", "IE", "PT", "GR", "CY", "MT", "LU", "IS", "LI", "MC", "SM", "VA", "AD", "AU", "CA", "NZ", "JP", "KR", "SG", "HK", "TW", "TH", "MY", "ID", "PH", "VN", "IN", "BR", "MX", "AR", "CL", "CO", "PE", "VE", "UY", "PY", "BO", "EC", "GY", "SR", "GF", "FK", "ZA", "EG", "MA", "TN", "DZ", "LY", "SD", "ET", "KE", "UG", "TZ", "GH", "NG", "CI", "SN", "ML", "BF", "NE", "TD", "CM", "CF", "CG", "CD", "AO", "ZM", "ZW", "BW", "NA", "SZ", "LS", "MG", "MU", "SC", "KM", "DJ", "SO", "ER", "RW", "BI", "MW", "MZ"],
  "homeassistant": "2025.9.0"
}
```

### Common Issues

1. **Repository not public**: HACS can only access public repositories
2. **Wrong repository URL**: Make sure you're using the correct GitHub URL
3. **HACS not updated**: Update HACS to the latest version
4. **Home Assistant not restarted**: Restart Home Assistant after HACS installation

## Integration Not Appearing in Home Assistant

### Check Installation
1. Verify the integration was installed successfully in HACS
2. Check that the files are in the correct location:
   - `custom_components/ezviz_patched/` directory exists
   - `manifest.json` is present and valid
   - All Python files are present

### Check Logs
Look for errors in the Home Assistant logs:
1. Go to Settings > System > Logs
2. Look for any errors related to `ezviz_patched`
3. Check for import errors or missing dependencies

### Verify Manifest
The `manifest.json` should contain:
```json
{
  "domain": "ezviz_patched",
  "name": "EZVIZ Patched",
  "documentation": "https://www.home-assistant.io/integrations/ezviz",
  "requirements": ["pyEzviz==0.2.0.4"],
  "codeowners": ["@baqs"],
  "version": "2025.9.0-patched",
  "iot_class": "cloud_polling"
}
```

## "Account Already Configured" Error

This happens when the original EZVIZ integration is still configured. You must:

1. **Remove the original EZVIZ integration**:
   - Go to Settings > Devices & Services
   - Find "EZVIZ" integration
   - Click on it → Three dots menu (⋮) → Delete
   - Confirm deletion

2. **Restart Home Assistant**

3. **Add EZVIZ Patched**:
   - Go to Settings > Devices & Services
   - Click "Add Integration"
   - Search for "EZVIZ Patched"

## Sensors Still Not Working

1. **Verify you're using the patched version**:
   - Check that the integration name is "EZVIZ Patched"
   - Look for the domain `ezviz_patched` in the logs

2. **Check sensor configuration**:
   - Verify your EZVIZ account credentials
   - Check that the integration is properly configured

3. **Check for errors**:
   - Look at the Home Assistant logs
   - Check for any KeyError messages

## Still Having Issues?

1. **Check the original issue**: [Home Assistant issue #151648](https://github.com/home-assistant/core/issues/151648)
2. **Verify Home Assistant version**: This fix is for Home Assistant 2025.9.0
3. **Check EZVIZ account**: Make sure your EZVIZ account is working
4. **Try manual installation**: If HACS doesn't work, try manual installation

## Manual Installation

If HACS installation fails, you can install manually:

1. **Download the repository**
2. **Extract the `custom_components/ezviz_patched` folder**
3. **Copy it to your Home Assistant `custom_components` directory**
4. **Restart Home Assistant**
5. **Add the integration through the UI**
