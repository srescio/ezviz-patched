# Home Assistant data in this dev container

## Where your account lives

- **Users / onboarding state**: `/config/.storage/` (especially `auth` and `onboarding` files)
- **Integrations & entities**: `/config/.storage/` + `/config/home-assistant_v2.db` (recorder)
- **YAML**: `/config/configuration.yaml` and includes (often **`/config/scripts.yaml`** for scripts)

The dev container mounts a **named Docker volume** `ezviz-ha-config` on `/config` (see `devcontainer.json`). That data should survive **container rebuilds** as long as the volume is not removed.

### Repo `.devcontainer/` vs what Home Assistant reads

**Home Assistant only loads `/config/…`.** Files under **`.devcontainer/`** in the git workspace are templates; editing them in the IDE does nothing until they are copied or merged into `/config`.

- **`scripts/setup_devcontainer`** runs **`scripts/merge_ezviz_dev_script.py`**: if `configuration.yaml` has **`script: !include scripts.yaml`** (the usual HA default), it **merges** the EZVIZ burst script into **`/config/scripts.yaml`**. YAML cannot have two top-level **`script:`** keys, so we cannot add a second `!include` when `scripts.yaml` is already used — an empty `scripts.yaml` meant the Scripts UI stayed empty.
- The repo template uses **`script: !include scripts.yaml`**; source definitions are in **`.devcontainer/ezviz_burst_scripts.yaml`** (also copied to **`/config/ezviz_burst_scripts.yaml`** if you prefer **`!include ezviz_burst_scripts.yaml`** instead).
- After merge, restart HA (or **Developer tools → YAML → Reload scripts**). You should see **`EZVIZ — burst polling`** under Scripts, and entity **`script.ezviz_sensor_burst_test`** under **Developer tools → States**.
- **One-shot fix** without full setup:  
  `python3 /workspaces/ezviz-patched/scripts/merge_ezviz_dev_script.py /workspaces/ezviz-patched`  
  then reload scripts / restart HA.

## Why you might see “Welcome / onboarding” again

1. **Volume was recreated or removed**  
   e.g. `docker volume rm ezviz-ha-config`, a new Docker context, or opening the project in an environment that does not attach the same volume.

2. **Home Assistant is using a different config path**  
   Always start with `hass -c /config` so it uses the mounted volume.

3. **Recorder DB was corrupt (does not delete users by itself)**  
   If logs say the recorder database was corrupt, HA renames `home-assistant_v2.db` to `*.corrupt.*` and creates a new DB. **That does not remove `.storage` auth.** If you still see onboarding, `.storage` was missing or empty for another reason.

## Backups

Use **Settings → System → Backups** in the UI, or copy `/config` (including `.storage`) while HA is stopped.

## After `postCreate` / `setup_devcontainer`

- **Initial `configuration.yaml`** is copied only when `/config/configuration.yaml` does not exist, so rebuilds do not wipe your YAML.
- Re-run `scripts/setup_devcontainer` after HA upgrades if new lazy dependencies are missing (check the log for `No module named` / `ffmpeg` errors).

## “Another Home Assistant instance is already running”

HA uses **`/config/.ha_run.lock`**. Starting **`hass -c /config`** again while one is still running (second terminal, or **reloading the task terminal** with the circular-arrow control before the old `hass` has exited) hits that error.

The task **“Run Home Assistant (8123, /config)”** should run **`scripts/run_ha_dev.sh`**. That script finds the PID in **`.ha_run.lock`**, sends **SIGTERM**, waits for it to exit, then starts HA — so a **reload** of the task panel should work without running the task twice.

If your terminal title/command still shows only `install_go2rtc_binary.sh && hass`, the editor is using an old task definition: **reload the window** or re-open the folder so **`.vscode/tasks.json`** is picked up.

To **not** stop an existing instance (fail if lock is held):  
`EZVIZ_HA_KEEP_EXISTING=1 bash scripts/run_ha_dev.sh`.

## go2rtc + DHCP in this dev image

- **`Could not find go2rtc docker binary`**: Core expects the **`go2rtc` executable** on `PATH` when `is_docker_env()` is true (same as HA OS). The setup script downloads **[AlexxIT/go2rtc](https://github.com/AlexxIT/go2rtc)** **v1.9.14** into `/usr/local/bin/go2rtc`. Bump `GO2RTC_VER` in `scripts/setup_devcontainer` if HA’s `RECOMMENDED_VERSION` changes.
- **`aiodhcpwatcher` / libpcap**: `libpcap0.8` + `libpcap0.8-dev` are installed. If you still see *“libpcap is not available”* or cannot compile filters, the runtime may need extra capabilities (e.g. `NET_RAW`) or host networking — typical for raw DHCP sniffing in Docker.
