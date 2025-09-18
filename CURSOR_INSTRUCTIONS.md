# Cursor Instructions: Override Home Assistant Core Component

## Cursor-Specific Workflow for Custom Component Override

**Cursor Context**: This guide is optimized for Cursor IDE workflows, including AI-assisted development, real-time testing, and iterative development cycles.

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
  "domain": "ezviz", // Must match core component domain exactly
  "name": "EZVIZ Patched", // Display name
  "version": "2025.9.0-patched",
  "requirements": ["pyezvizapi==1.0.0.7"],
  "config_flow": true, // Match core component
  "dependencies": ["ffmpeg"] // Match core component
}
```

### 3. **Key Override Principles**

- **Domain Must Match**: `domain` in manifest.json must exactly match core component
- **Copy Core Files**: Copy all files from `homeassistant/components/[domain]/` to `custom_components/[domain]/`
- **Preserve Config**: Existing integrations will automatically use custom component
- **No Restart Required**: Changes take effect after Home Assistant restart

### 4. **Cursor-Specific Testing Workflow**

**Critical for Cursor**: Always test in running instance before syncing to repository.

1. **Apply to Running Instance**: Copy changes to `/config/custom_components/[domain]/` in your Home Assistant container
2. **Restart Home Assistant**: Verify changes work in the UI
3. **Iterate with AI**: Use Cursor's AI to fix issues and test again
4. **Sync to Repository**: Only after confirming it works, copy changes to repo
5. **Commit & Push**: Update repository with tested version

**Cursor Advantage**: AI can help debug issues in real-time while testing.

### 5. **Cursor-Specific Common Issues**

- **Domain Mismatch**: Ensure manifest.json domain exactly matches core component
- **Missing Dependencies**: Install all requirements from core component
- **Import Errors**: Check all imports match core component structure
- **Translation Issues**: Use simple translation keys, avoid complex structures
- **AI Debugging**: Use Cursor's AI to analyze error logs and suggest fixes
- **Real-time Testing**: Test changes immediately in running Home Assistant instance

### 6. **Enhanced Features (Optional)**

- **Repairs Platform**: Add user notifications with GitHub links
- **System Health**: Provide component status information
- **Issue Monitoring**: Track external issue status automatically

### 7. **Installation Methods**

- **Manual**: Copy to `custom_components/[domain]/`
- **HACS**: Use Git repository URL for community installation
- **Docker**: Mount custom_components directory

## Cursor vs Copilot Differences

### **Cursor-Specific Advantages:**
- **Real-time Testing**: Test changes immediately in running Home Assistant instance
- **AI Debugging**: Use Cursor's AI to analyze error logs and suggest fixes
- **Iterative Development**: Make changes, test, fix, repeat - all in one IDE
- **Container Integration**: Direct access to running Docker containers
- **Live Error Analysis**: AI can read Home Assistant logs and suggest solutions

### **Copilot Differences:**
- **Code Completion Focus**: More focused on code suggestions rather than full workflow
- **Limited Testing Integration**: May require manual testing setup
- **Less Container Awareness**: May not be as integrated with running environments

### **Cursor Workflow Example:**
1. Make code changes in Cursor
2. Copy to running Home Assistant container
3. Use Cursor AI to analyze any error logs
4. Iterate until working
5. Sync to repository

## Example: EZVIZ Override

This repository demonstrates overriding the core `ezviz` component with a patched version that fixes GitHub issue #151648, includes repair notifications, and provides GitHub issue links for user guidance. The development process used Cursor's AI-assisted workflow for real-time testing and debugging.
