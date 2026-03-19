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

## Development

This repo includes a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) setup for developing and testing changes locally.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [VS Code](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/) with the **Dev Containers** extension

### Getting started

1. Open this repo in VS Code / Cursor
2. When prompted, click **Reopen in Container** (or run `Dev Containers: Reopen in Container` from the command palette)
3. Wait for the container to build — it installs Home Assistant core and symlinks the component into `/config/custom_components/ezviz`
4. Run `Tasks: Run Task` > **Run Home Assistant on port 9123**
5. Open `http://localhost:9123` to access the test instance

### Available tasks

| Task | Description |
|---|---|
| Run Home Assistant on port 9123 | Start HA with the custom component loaded |
| Run Home Assistant configuration against /config | Validate the HA configuration |
| Upgrade Home Assistant to latest dev | Install HA core from the `dev` branch |
| Install a specific version of Home Assistant | Install a pinned HA release |
| Resync config from .devcontainer | Copy `configuration.yaml` back to `/config` |

### Debugging

Enable step-by-step debugging by uncommenting `debugpy:` in `.devcontainer/configuration.yaml`, starting HA via the task, then attaching with the **Python: Attach Local** launch configuration.

### Configuration

The test instance uses `.devcontainer/configuration.yaml`. Debug logging for `custom_components.ezviz` is enabled by default.

## Component Details

- **Domain**: `ezviz` (overrides built-in integration)
- **Based on**: Home Assistant core `dev` branch (synced March 2026)
- **Requirements**: `pyezvizapi==1.0.0.7`

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
