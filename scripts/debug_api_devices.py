"""Debug script: dump all devices from EZVIZ API to see categories and data."""
import json
import sys
sys.path.insert(0, "/usr/local/lib/python3.14/site-packages")

from pyezvizapi.client import EzvizClient

with open("/config/.storage/core.config_entries") as f:
    data = json.load(f)

ezviz_entry = next(
    e for e in data["data"]["entries"] if e["domain"] == "ezviz"
)
token = {
    "session_id": ezviz_entry["data"]["session_id"],
    "rf_session_id": ezviz_entry["data"]["rf_session_id"],
    "username": ezviz_entry["title"],
    "api_url": ezviz_entry["data"]["url"],
}

client = EzvizClient(token=token)
client.login()

print("=" * 80)
print("RAW PAGELIST - ALL DEVICES (before category filtering)")
print("=" * 80)

raw = client._get_page_list()

print(f"\nTop-level keys in pagelist response: {list(raw.keys())}\n")

print("-" * 80)
print("ALL deviceInfos entries:")
print("-" * 80)
for i, dev in enumerate(raw.get("deviceInfos", [])):
    serial = dev.get("deviceSerial", "???")
    name = dev.get("deviceName") or dev.get("name", "???")
    category = dev.get("deviceCategory", "???")
    sub_cat = dev.get("deviceSubCategory", "???")
    model = dev.get("deviceType", "???")
    status = dev.get("status", "???")
    print(f"\n  [{i}] Serial: {serial}")
    print(f"      Name: {name}")
    print(f"      Category: {category}")
    print(f"      SubCategory: {sub_cat}")
    print(f"      Model/Type: {model}")
    print(f"      Status: {status}")
    print(f"      hik: {dev.get('hik')}")

print("\n")
print("=" * 80)
print("FULL deviceInfos JSON (for deep inspection)")
print("=" * 80)
for dev in raw.get("deviceInfos", []):
    serial = dev.get("deviceSerial", "???")
    print(f"\n--- {serial} ---")
    print(json.dumps(dev, indent=2, default=str))

if raw.get("DETECTOR"):
    print("\n")
    print("=" * 80)
    print("DETECTOR section (sub-devices like sensors)")
    print("=" * 80)
    print(json.dumps(raw["DETECTOR"], indent=2, default=str))

if raw.get("FEATURE"):
    print("\n")
    print("=" * 80)
    print("FEATURE section")
    print("=" * 80)
    for serial, feat in raw["FEATURE"].items():
        print(f"\n--- {serial} ---")
        print(json.dumps(feat, indent=2, default=str))

client.close_session()
