# EZVIZ Patched - Deployment Guide

This guide will help you deploy the EZVIZ Patched custom component to your own Git repository for HACS installation.

## 🚀 Quick Start

1. **Create a new repository on GitHub** (e.g., `ezviz-patched`)
2. **Run the setup script:**
   ```bash
   ./setup_remote.sh
   ```
3. **Follow the prompts** to add your repository URL
4. **Install in HACS** using the repository URL

## 📋 Detailed Steps

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `ezviz-patched` or `homeassistant-ezviz-patched`
3. Make it **public** (required for HACS)
4. Don't initialize with README (we already have one)

### 2. Set Up Remote Repository

```bash
# Run the setup script
./setup_remote.sh

# Enter your repository URL when prompted
# Example: https://github.com/yourusername/ezviz-patched.git
```

### 3. Install in HACS

1. **Open HACS** in Home Assistant
2. **Go to Integrations**
3. **Click the three dots menu** (⋮)
4. **Select "Custom repositories"**
5. **Add repository:**
   - Repository: `https://github.com/yourusername/ezviz-patched`
   - Category: `Integration`
6. **Click "Add"**
7. **Find "EZVIZ Patched"** in the store and install it

### 4. Create Releases (Optional)

To create versioned releases:

```bash
# Create a new release
./create_release.sh

# Enter version number (e.g., 1.0.0)
# Add release notes
# Follow the GitHub release creation steps
```

## 🔧 Repository Structure

```
ezviz-patched/
├── .gitignore              # Git ignore file
├── .git/                   # Git repository
├── hacs.json              # HACS configuration
├── info.md                # HACS info page
├── LICENSE                # MIT License
├── README.md              # Main documentation
├── manifest.json          # Home Assistant manifest
├── __init__.py            # Main integration file
├── sensor.py              # Sensor platform (with fix)
├── [other platform files] # All EZVIZ platform files
├── setup_remote.sh        # Remote setup script
└── create_release.sh      # Release creation script
```

## 📝 HACS Configuration

The `hacs.json` file contains the HACS configuration:

```json
{
  "name": "EZVIZ Patched",
  "content_in_root": true,
  "filename": "ezviz_patched",
  "country": ["US", "GB", "DE", "FR", "ES", "IT", "NL", "BE", "CH", "AT", "SE", "NO", "DK", "FI", "PL", "CZ", "HU", "RO", "BG", "HR", "SI", "SK", "LT", "LV", "EE", "IE", "PT", "GR", "CY", "MT", "LU", "IS", "LI", "MC", "SM", "VA", "AD", "AU", "CA", "NZ", "JP", "KR", "SG", "HK", "TW", "TH", "MY", "ID", "PH", "VN", "IN", "BR", "MX", "AR", "CL", "CO", "PE", "VE", "UY", "PY", "BO", "EC", "GY", "SR", "GF", "FK", "ZA", "EG", "MA", "TN", "DZ", "LY", "SD", "ET", "KE", "UG", "TZ", "GH", "NG", "CI", "SN", "ML", "BF", "NE", "TD", "CM", "CF", "CG", "CD", "AO", "ZM", "ZW", "BW", "NA", "SZ", "LS", "MG", "MU", "SC", "KM", "DJ", "SO", "ER", "RW", "BI", "MW", "MZ"],
  "homeassistant": "2025.9.0"
}
```

## ⚠️ Important Notes

- **Repository must be public** for HACS to access it
- **Content in root** is set to `true` in `hacs.json`
- **Filename** matches the domain name `ezviz_patched`
- **Home Assistant version** is set to `2025.9.0`

## 🔄 Updates

To update the component:

1. **Make changes** to the files
2. **Commit changes:**
   ```bash
   git add .
   git commit -m "Update: Description of changes"
   git push origin main
   ```
3. **HACS will automatically detect updates** and notify users

## 🐛 Troubleshooting

### HACS Can't Find the Component

- Ensure repository is **public**
- Check that `hacs.json` is in the root directory
- Verify `content_in_root` is set to `true`
- Make sure `filename` matches the domain name

### Installation Fails

- Check that all required files are present
- Verify `manifest.json` is valid
- Ensure all Python files have proper syntax

### Component Doesn't Appear

- Restart Home Assistant after installation
- Check the logs for any errors
- Verify the domain name is `ezviz_patched`

## 📞 Support

For issues with this custom component:

1. Check the [Home Assistant issue #151648](https://github.com/home-assistant/core/issues/151648)
2. Verify you're using Home Assistant 2025.9.0 or later
3. Check the Home Assistant logs for any errors

## 🎯 Next Steps

Once the official fix is merged into Home Assistant core:

1. **Remove this custom component** from HACS
2. **Use the official EZVIZ integration** instead
3. **Archive this repository** or mark it as deprecated
