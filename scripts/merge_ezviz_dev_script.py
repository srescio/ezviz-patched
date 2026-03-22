#!/usr/bin/env python3
"""Merge EZVIZ dev burst script into /config when HA uses script: !include scripts.yaml.

Home Assistant defaults often already have ``script: !include scripts.yaml`` with an empty
file — a second ``script:`` key is invalid YAML, so we must merge into scripts.yaml.
"""
from __future__ import annotations

import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    print("merge_ezviz_dev_script: PyYAML not installed, skip", file=sys.stderr)
    sys.exit(0)

WORKSPACE = pathlib.Path(
    sys.argv[1] if len(sys.argv) > 1 else "/workspaces/ezviz-patched"
)
FRAGMENT = WORKSPACE / ".devcontainer" / "ezviz_burst_scripts.yaml"
CONFIG = pathlib.Path("/config/configuration.yaml")
SCRIPTS = pathlib.Path("/config/scripts.yaml")


def main() -> int:
    if not FRAGMENT.is_file():
        print(f"merge_ezviz_dev_script: missing {FRAGMENT}", file=sys.stderr)
        return 0
    if not CONFIG.is_file():
        return 0

    burst = yaml.safe_load(FRAGMENT.read_text(encoding="utf-8"))
    if not isinstance(burst, dict):
        return 0

    cfg_text = CONFIG.read_text(encoding="utf-8")

    uses_scripts_yaml = bool(
        re.search(
            r"^\s*script:\s*!include\s+['\"]?scripts\.yaml['\"]?\s*$",
            cfg_text,
            re.MULTILINE,
        )
    )
    uses_ezviz_include = "ezviz_burst_scripts.yaml" in cfg_text

    if uses_ezviz_include:
        # Dedicated include; setup_devcontainer copies the file separately.
        return 0

    if not uses_scripts_yaml:
        return 0

    data: dict = {}
    if SCRIPTS.is_file() and SCRIPTS.stat().st_size > 0:
        loaded = yaml.safe_load(SCRIPTS.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data = loaded

    changed = False
    for key, value in burst.items():
        if key not in data:
            data[key] = value
            changed = True
            print(f"merge_ezviz_dev_script: added script.{key} to {SCRIPTS}")

    if changed:
        SCRIPTS.parent.mkdir(parents=True, exist_ok=True)
        SCRIPTS.write_text(
            yaml.dump(
                data,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
                width=88,
            ),
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
