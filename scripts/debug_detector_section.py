"""Debug: dump the DETECTOR section from EZVIZ API."""
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

raw = client._get_page_list()

for section_name in ["DETECTOR", "STATUS", "SWITCH", "FEATURE", "FEATURE_INFO"]:
    section = raw.get(section_name)
    if section:
        print("=" * 80)
        print(f"{section_name} section")
        print("=" * 80)
        for key, val in section.items():
            if "J97123910" in str(key) or "Q26" in str(key) or "Q28" in str(key) or "Q31" in str(key):
                print(f"\n--- {key} ---")
                print(json.dumps(val, indent=2, default=str))

client.close_session()
