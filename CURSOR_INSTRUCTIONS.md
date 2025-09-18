# Cursor Instructions: Override Home Assistant Core Component

## Quick Setup for Custom Component Override

### 1. **File Structure**
```
custom_components/
└── [domain_name]/          # Must match core component domain
    ├── __init__.py         # Entry point
    ├── manifest.json       # Component metadata
    ├── [other files...]    # Copy from core component
    └── translations/
        └── en.json         # Optional translations
```

### 2. **Critical manifest.json Settings**
```json
{
  "domain": "ezviz",           // Must match core component domain exactly
  "name": "EZVIZ Patched",     // Display name
  "version": "2025.9.0-patched",
  "requirements": ["pyezvizapi==1.0.0.7"],
  "config_flow": true,         // Match core component
  "dependencies": ["ffmpeg"]   // Match core component
}
```

### 3. **Key Override Principles**
- **Domain Must Match**: `domain` in manifest.json must exactly match core component
- **Copy Core Files**: Copy all files from `homeassistant/components/[domain]/` to `custom_components/[domain]/`
- **Preserve Config**: Existing integrations will automatically use custom component
- **No Restart Required**: Changes take effect after Home Assistant restart

### 4. **Testing Workflow**
1. **Test in Running Instance First**: Apply changes to `/config/custom_components/[domain]/`
2. **Restart Home Assistant**: Verify changes work
3. **Sync to Repository**: Copy working changes to repo
4. **Commit & Push**: Update repository with working version

### 5. **Common Issues**
- **Domain Mismatch**: Ensure manifest.json domain exactly matches core component
- **Missing Dependencies**: Install all requirements from core component
- **Import Errors**: Check all imports match core component structure
- **Translation Issues**: Use simple translation keys, avoid complex structures

### 6. **Enhanced Features (Optional)**
- **Repairs Platform**: Add user notifications with GitHub links
- **System Health**: Provide component status information
- **Issue Monitoring**: Track external issue status automatically

### 7. **Installation Methods**
- **Manual**: Copy to `custom_components/[domain]/`
- **HACS**: Use Git repository URL for community installation
- **Docker**: Mount custom_components directory

## Example: EZVIZ Override
This repository demonstrates overriding the core `ezviz` component with a patched version that fixes GitHub issue #151648, includes repair notifications, and provides GitHub issue links for user guidance.
