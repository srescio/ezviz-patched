# EZVIZ Sensor Real-Time Update Investigation

> Investigation conducted on 2026-03-19.
> Goal: determine how to receive real-time state updates from EZVIZ Zigbee sensors
> (T2C door/window contacts, water leak sensors, siren) paired to an EZVIZ A3 gateway,
> for use in a Home Assistant custom integration.

---

## Table of Contents

- [Context](#context)
- [1. EZVIZ Cloud API Polling](#1-ezviz-cloud-api-polling)
- [2. EZVIZ MQTT Push Channel](#2-ezviz-mqtt-push-channel)
- [3. ha-ezviz Beta Integration (RenierM26)](#3-ha-ezviz-beta-integration-renierM26)
- [4. EZVIZ Open Platform Message Queue](#4-ezviz-open-platform-message-queue)
- [5. A3 Gateway Local Network Probing](#5-a3-gateway-local-network-probing)
- [6. Hikvision DS-PWA32 Alarm Receiving Center](#6-hikvision-ds-pwa32-alarm-receiving-center)
- [7. Zigbee2MQTT Direct Pairing](#7-zigbee2mqtt-direct-pairing)
- [8. Passive Zigbee Sniffing](#8-passive-zigbee-sniffing)
- [9. Other Push Endpoints Investigated](#9-other-push-endpoints-investigated)
- [Conclusions](#conclusions)
- [Recommended Path Forward](#recommended-path-forward)

---

## Context

The EZVIZ A3 gateway (model CS-A3-W0-W, Hikvision OEM as DS-PWA32) acts as a Zigbee 3.0
coordinator for up to 64 sub-devices. Sensors communicate via Zigbee to the A3, which
relays state to the EZVIZ cloud. The EZVIZ mobile app and Alexa receive near-instant
notifications when sensors trigger. The question: can we get the same real-time updates
into Home Assistant?

**Devices under test:**
- 6x EZVIZ T2C (CS-T2C) door/window contact sensors
- 2x EZVIZ water leak sensors
- 1x EZVIZ siren
- 1x EZVIZ A3 gateway (IP: 192.168.0.232)

---

## 1. EZVIZ Cloud API Polling

**Endpoint:** `POST /v3/userdevices/v1/resources/pagelist` on `apiieu.ezvizlife.com`

The pagelist API returns a `FEATURE_INFO` section per device. For door/window sensors,
`FEATURE_INFO → {serial} → 0 → global → DoorMagnetic → DoorStatus` contains the
current open/closed state.

### Test Results

Polling every 5 seconds while physically opening and closing a window sensor:

```
[21:56:06] Finestra camera: OPEN
[21:56:11] Finestra camera: OPEN
[21:56:17] Finestra camera: CLOSED   ← updated within ~6 seconds of physical event
[21:56:22] Finestra camera: CLOSED
```

**Finding:** The API updates `DoorStatus` within approximately 5–6 seconds of a physical
sensor event. A full pagelist call takes ~0.3 seconds.

**Limitation:** The Home Assistant coordinator polls every 30 seconds by default, meaning
worst-case delay is ~30 seconds. Reducing the polling interval to 10–15 seconds is
viable given the low API call cost.

---

## 2. EZVIZ MQTT Push Channel

**Broker:** `pusheu.ezvizlife.com:1882` (MQTT 3.1.1, QoS 2)
**Topic:** `{MQTT_APP_KEY}/#` where `MQTT_APP_KEY = 4c6b3cc2-b5eb-4813-a592-612c1374c1fe`

The `pyezvizapi` library ([github.com/RenierM26/pyEzvizApi](https://github.com/RenierM26/pyEzvizApi))
includes an `MQTTClient` class that:

1. Registers via `POST /v1/getClientId` on pusheu.ezvizlife.com
2. Starts push via `POST /api/push/start`
3. Connects to MQTT broker on port 1882
4. Subscribes to `{MQTT_APP_KEY}/#`

### Test Results

Connected with raw MQTT client subscribing to `#` (ALL topics) with full debug logging.
Listened for 80 seconds. MQTT connection was successful:

```
MQTT connected: rc=0 session_present=0
MQTT subscribed: topic=4c6b3cc2-b5eb-4813-a592-612c1374c1fe/# mid=1 qos=(2,)
```

**Result: zero messages received in 80 seconds.** The broker disconnected us after ~60
seconds (rc=7, connection lost), which is normal for idle connections.

The MQTT message format (`EXT_FIELD_NAMES` in `mqtt.py`) is structured around camera
alarm events:

```
channel_type, time, device_serial, channel_no, alert_type_code,
default_pic_url, media_url_alt1, media_url_alt2, resource_type, ...
```

**Finding:** The EZVIZ MQTT push channel only delivers camera alarm events (motion/PIR
detection, doorbell presses). It does NOT fire for Zigbee sub-device state changes
(door open/close, water leak). Confirmed by testing and by examining the ha-ezviz
beta codebase (see section 3).

**Source:** [pyezvizapi/mqtt.py](https://github.com/RenierM26/pyEzvizApi/blob/main/pyezvizapi/mqtt.py)

---

## 3. ha-ezviz Beta Integration (RenierM26)

**Repository:** [github.com/RenierM26/ha-ezviz](https://github.com/RenierM26/ha-ezviz)

The beta ha-ezviz integration includes MQTT support (added September 2025, announced in
[issue #83](https://github.com/RenierM26/ha-ezviz/issues/83) and
[issue #19](https://github.com/RenierM26/ha-ezviz/issues/19)).

### How it uses MQTT

The `EzvizMqttHandler` class wraps the `pyezvizapi` `MQTTClient`:

```python
# From ha-ezviz/custom_components/ezviz_cloud/mqtt.py
class EzvizMqttHandler:
    def _on_message(self, event):
        serial = event["ext"]["device_serial"]
        self._coordinator.merge_mqtt_update(serial, event)
        self._hass.bus.async_fire("ezviz_push_event", event)
```

The `merge_mqtt_update` method in the coordinator ONLY updates camera-specific fields:

```python
# From ha-ezviz/custom_components/ezviz_cloud/coordinator.py
def merge_mqtt_update(self, serial, mqtt_data):
    ext = mqtt_data["ext"]
    if ext.get("image"):
        self.data[serial].update(
            last_alarm_type_code=ext.get("alert_type_code"),
            last_alarm_time=ext.get("time"),
            last_alarm_pic=ext.get("image"),
            last_alarm_type_name=mqtt_data.get("alert"),
            Motion_Trigger=True,
        )
```

**Finding:** The ha-ezviz beta MQTT integration is designed exclusively for camera
motion/alarm events. There is no handling for sensor state changes. The coordinator
still uses 30-second polling via `load_cameras` for all state data.

### Historical context from issue #19

In [issue #19](https://github.com/RenierM26/ha-ezviz/issues/19) (2021), a user tested
the MQTT CLI tool and received camera PIR events:

```
{'id': ..., 'alert': 'Front Door Doorbell PIR Event(2021-07-07 11:33:55)',
 'ezviz_alert_type': '10000', 'serial': 'xxxxxx', ...}
```

No user in the issue thread reported receiving Zigbee sensor events via MQTT.

**Sources:**
- [ha-ezviz coordinator.py](https://raw.githubusercontent.com/RenierM26/ha-ezviz/main/custom_components/ezviz_cloud/coordinator.py)
- [ha-ezviz mqtt.py](https://raw.githubusercontent.com/RenierM26/ha-ezviz/main/custom_components/ezviz_cloud/mqtt.py)
- [ha-ezviz __init__.py](https://raw.githubusercontent.com/RenierM26/ha-ezviz/main/custom_components/ezviz_cloud/__init__.py)
- [Issue #19: 10 second lag between EZViz PIR Event and HA](https://github.com/RenierM26/ha-ezviz/issues/19)
- [Issue #83: sensor.last_alarm_pic](https://github.com/RenierM26/ha-ezviz/issues/83)

---

## 4. EZVIZ Open Platform Message Queue

**URL:** [ieuopen.ezviz.com/product/message](https://ieuopen.ezviz.com/product/message) (EU)

EZVIZ has a separate **developer/enterprise platform** that offers a Message Queue service
with real-time event delivery.

### Capabilities

- **Delivery methods:** server-side subscription and webhook push
- **Latency:** 200–400ms
- **Accuracy:** 99.9% message arrival rate, up to 5 data backups
- **Supported event types:**
  - EZVIZ alarm messages (motion detection, **water leak detection**, PIR detection)
  - Device online/offline messages (heartbeat every 30 seconds)
  - ISAPI events (for industry cameras)
  - NB-IoT messages

### Access Requirements

1. Register as an EZVIZ developer at [ieuopen.ezviz.com/console/register.html](https://ieuopen.ezviz.com/console/register.html)
2. Apply for Message Queue subscription by submitting a project work order
3. Download SDK and build integration
4. **Pricing:** paid plans starting at ~$600/year for 100 devices
5. Contact: open-team@ezvizlife.com

### Why Alexa Gets Instant Updates

Alexa and Google Home integrations use EZVIZ's cloud-to-cloud server-side integration.
EZVIZ's servers push proactive state reports directly to Amazon's/Google's event gateways
via Smart Home Skill APIs. This is a server-to-server channel not available to
third-party API consumers using the mobile app API.

**Finding:** The Message Queue service is the proper way to receive real-time sensor
events. However, it's a paid enterprise service and requires a public webhook endpoint.
It would need significant integration work (webhook receiver in HA, EZVIZ developer
account, project approval).

**Sources:**
- [EZVIZ Message Queue (EU)](https://ieuopen.ezviz.com/product/message)
- [EZVIZ Developer Platform](https://www.ezviz.com/developer/index)
- [EZVIZ Cloud Developer Platform (EU)](https://ieuopen.ezviz.com/)

---

## 5. A3 Gateway Local Network Probing

**Gateway IP:** 192.168.0.232 (from pagelist `CONNECTION` section)

### Port Scan Results

Scanned ports: 22, 80, 443, 554, 1882, 1883, 5683, 5684, 6668, 7681, 7682, 8000,
8080, 8200, 8300, 8443, 8777, 8883, 8888, 9000, 9010, 9020, 9030, 9100, 34567

| Port | Status | Notes |
|------|--------|-------|
| 8000 | **OPEN** | Hikvision SDK service port |
| 9010 | CLOSED | Listed as `localCmdPort` in API but refused connections |
| All others | CLOSED | No HTTP, MQTT, or other services exposed |

### Port 8000 Investigation

- Does not respond to HTTP/ISAPI requests (connection closed without response)
- Does not respond to Hikvision NetSDK binary protocol probes
- Does not speak first on connection (passive probe: no data after 3 seconds)
- No web interface available on any port

### Cloud-Proxied ISAPI Requests

Attempted ISAPI requests proxied through the EZVIZ cloud via `/v3/devconfig/op`:

```
GetSecurityCapability → code=2009 "Device network abnormal"
GetAlarmCenter       → code=2009 "Device network abnormal"
GetZoneList          → code=2009 "Device network abnormal"
```

The cloud attempted to relay requests to the device (requests took ~11 seconds each)
but the A3 gateway did not respond. The EZVIZ consumer firmware likely strips the
ISAPI interface that exists on the Hikvision-branded equivalent.

**Finding:** The EZVIZ A3 gateway exposes no usable local API for querying sensor state
or subscribing to events. Port 8000 is open but non-functional for HTTP/ISAPI.

---

## 6. Hikvision DS-PWA32 Alarm Receiving Center

The EZVIZ A3 is an OEM version of the **Hikvision DS-PWA32** (AX Series Wireless Security
Control Panel). The Hikvision version supports:

- **Alarm Receiving Center** configuration via web interface
- Protocols: SIA-DCS, AMD-CID (Contact ID)
- Push notifications for zone alarms, tamper events, system status changes
- Configurable server address, port, account code, and secret key
- Heartbeat monitoring

### How it works (on Hikvision firmware)

1. Navigate to Communication Parameters → Alarm Receiving Center
2. Set protocol type, server address (local IP), port number
3. The panel pushes alarm events via TCP to the configured server
4. A receiver (like [alarm-server-mqtt](https://github.com/steelbrain/alarm-server-mqtt))
   parses the events and forwards to MQTT

### Applicability to EZVIZ A3

The EZVIZ A3 firmware does **not** expose the Alarm Receiving Center web interface.
Cloud-proxied ISAPI requests to configure it return error 2009 (device network abnormal).
The alarm center functionality may be disabled in the EZVIZ consumer firmware.

**Potential route:** flashing Hikvision firmware onto the A3 hardware (same SoC) could
theoretically expose ISAPI and Alarm Center configuration. This carries bricking risk
and would void warranty.

**Sources:**
- [DS-PWA32 Alarm Center Configuration Guide (PDF)](https://www.hikvision.com/content/dam/hikvision/ca/how-to-document1/alarm-products/%E3%80%902006%E3%80%91DS-PWA32-How-to-Configure-Alarm-Center-Settings.pdf)
- [alarm-server-mqtt project](https://github.com/steelbrain/alarm-server-mqtt)
- [Hikvision ISAPI alertStream discussion](https://ipcamtalk.com/threads/hikvision-isapi-event-notification-alertstream-postman.70040/)

---

## 7. Zigbee2MQTT Direct Pairing

The EZVIZ T2C sensor is **supported by Zigbee2MQTT**.

**Zigbee2MQTT page:** [zigbee2mqtt.io/devices/CS-T2C.html](https://www.zigbee2mqtt.io/devices/CS-T2C.html)

### Exposed Entities

| Property | Type | Description |
|----------|------|-------------|
| `battery` | numeric (%) | Remaining battery level |
| `contact_alarm_1` | binary | Open/closed state (alarm 1) |
| `contact_alarm_2` | binary | Open/closed state (alarm 2) |
| `tamper` | binary | Tamper detection |
| `battery_low` | binary | Low battery warning |

### Requirements

- A separate Zigbee coordinator (e.g., Sonoff Zigbee 3.0 dongle, ConBee II, SLZB-06)
- Zigbee2MQTT or ZHA addon in Home Assistant
- **Unpairing the sensors from the A3 gateway** and re-pairing to the new coordinator

### Trade-offs

- **Pro:** Instant local updates (<1 second), no cloud dependency
- **Con:** Sensors must be unpaired from the A3 gateway
- **Con:** Unpairing disables the EZVIZ security alarm system for those sensors
- **Con:** Lose EZVIZ app notifications and alarm linkage (siren, camera recording)

**Finding:** This provides the best real-time performance but requires breaking the
EZVIZ alarm ecosystem. Not suitable if the alarm system must remain functional.

**Source:** [Zigbee2MQTT CS-T2C device page](https://www.zigbee2mqtt.io/devices/CS-T2C.html)

---

## 8. Passive Zigbee Sniffing

Investigated whether a second Zigbee coordinator could passively listen to T2C messages
without unpairing from the A3.

**Finding:** Not possible. Zigbee encrypts all network traffic using the coordinator's
network key. A separate coordinator cannot decrypt messages from the A3's Zigbee network.
As stated by the Zigbee2MQTT maintainer:

> "Zigbee2mqtt cannot act as a sniffer because not all data is received by it. Not all
> zigbee commands are sent to the coordinator."
> — [zigbee2mqtt issue #3549](https://github.com/Koenkk/zigbee2mqtt/issues/3549)

A dedicated Zigbee sniffer (CC2531 with sniffer firmware + Wireshark) could capture raw
Zigbee frames, but without the A3's network key, the payload is encrypted and unusable.

**Source:** [Zigbee2MQTT: Sniff Zigbee traffic](https://www.zigbee2mqtt.io/advanced/zigbee/04_sniff_zigbee_traffic.html)

---

## 9. Other Push Endpoints Investigated

The EZVIZ cloud returns several push-related service URLs. All were probed:

| Endpoint | Address | Port | Protocol | Result |
|----------|---------|------|----------|--------|
| pushAddr | pusheu.ezvizlife.com | 1882 | MQTT | Connected. Camera events only. |
| pushAddr (HTTPS) | pusheu.ezvizlife.com | 443 | HTTP | Returns "hello!" on GET /. 401 on other paths. |
| pushDasDomain | mdev.eu.ezvizlife.com | 8777 | Unknown binary | TCP accepts connection, no HTTP or MQTT. Undocumented protocol. |
| pmsAddr | pmseu1.ezvizlife.com | 8444 | HTTPS (Tomcat) | 404 on all tested paths. |
| pmsAddr (HTTP) | pmseu1.ezvizlife.com | 8080 | HTTP (Tomcat) | Not MQTT. No known endpoints respond. |
| nodeJsAddr | meseu.ezvizlife.com | 8153 | — | DNS does not resolve. |
| ttsAddr | ttseu.ezvizlife.com | 9664 | TCP | TCP connects but unknown binary protocol. |

### pusheu.ezvizlife.com:443 Notable Finding

The `/api/push/stream` endpoint returned **HTTP 406 (Not Acceptable)** — meaning the
endpoint exists but rejects the content negotiation. Tested with Accept headers:
`application/json` (406), `text/plain` (406), `*/*` (406). The endpoint may serve a
specific internal protocol but is not documented or accessible.

The `/api/push/start` endpoint accepts additional parameters:
- `deviceType: 'Detector'` → status=200 (accepted)
- `eventType: 'sensorAlarm'` → status=200 (accepted)

These parameters are accepted but did not cause any MQTT messages to arrive for sensor
events during testing.

---

## Conclusions

| Method | Latency | Feasibility | Breaks Alarm? |
|--------|---------|-------------|---------------|
| Cloud API polling (current) | 30s worst case (configurable) | Working now | No |
| Cloud API polling (reduced interval) | 10–15s worst case | Trivial change | No |
| EZVIZ MQTT push | N/A | Does not fire for sensor events | — |
| EZVIZ Open Platform Message Queue | 200–400ms | Requires paid developer account + webhook server | No |
| Zigbee2MQTT direct pairing | <1s (local) | Requires Zigbee coordinator + unpairing | **Yes** |
| A3 local ISAPI/SDK | N/A | Firmware blocks access | — |
| Hikvision Alarm Receiving Center | Real-time | Requires Hikvision firmware on A3 | No (if it worked) |
| Passive Zigbee sniffing | N/A | Encrypted, not possible | — |

---

## Recommended Path Forward

### Short term — IMPLEMENTED (no cost, no disruption)

1. **Default polling is 30 seconds** (aligned with upstream HA EZVIZ). Configurable via
   the integration options UI (Settings → Integrations → EZVIZ → Configure). Valid range:
   5–300s. For faster Zigbee contact updates without changing the default permanently, use
   **burst mode** (`ezviz.set_polling_interval`) or set a lower interval in options (e.g.
   10–15s).

2. **Burst-mode polling service** (`ezviz.set_polling_interval`). Temporarily sets an
   aggressive polling interval and automatically restores the default after a configurable
   duration. Designed to be called from HA scripts/automations during time-critical
   windows (e.g., a script that opens a door and waits for the sensor to confirm).

   **Parameters:**
   | Parameter  | Default | Range   | Description                                    |
   |------------|---------|---------|------------------------------------------------|
   | `interval` | 1       | 1–15s   | Polling interval during the burst window         |
   | `duration` | 60      | 1–240s  | Seconds before reverting to default (max 4 min)  |

   **Example usage in HA automation/script:**
   ```yaml
   service: ezviz.set_polling_interval
   data:
     interval: 1
     duration: 60
   ```

   **How it works:**
   - Sets `DataUpdateCoordinator.update_interval` to the requested interval
   - Triggers an immediate refresh
   - After `duration` seconds, restores the configured default interval
   - Calling again while a burst is active cancels the previous timer and starts fresh

   **Rate limiting notes:**
   - No documented EZVIZ API rate limits exist, but aggressive polling (<5s) risks silent
     throttling or session blocking by the cloud
   - Each poll makes ~2–4 HTTP requests; at 2s interval that's ~1–2 req/s
   - HA-side overhead is proportional to entity count but negligible on modern hardware
   - Recommended: keep **30s** (or your chosen options default) for steady state; use
     **burst** (e.g. 2–5s) only for short windows when you need snappier sensor feedback

### Medium term (no disruption to alarm system)
3. **Register on EZVIZ Open Platform** ([ieuopen.ezviz.com](https://ieuopen.ezviz.com/console/register.html))
   and explore the Message Queue free trial (120 days, 10 devices). If approved, build a
   webhook receiver in HA for 200–400ms sensor event delivery.

### Alternative (preserves alarm system)
4. **Dual-stack approach:** keep EZVIZ sensors on the A3 for the alarm system. Add
   inexpensive Zigbee contact sensors (e.g., Aqara MCCGQ11LM, ~$8 each) paired to a
   separate Zigbee coordinator for instant HA automations. Both sensor sets monitor the
   same doors/windows independently.

### If alarm system can be sacrificed
5. **Zigbee2MQTT:** unpair T2C sensors from A3, pair to a Zigbee coordinator. Instant
   local updates, no cloud dependency. Loses EZVIZ alarm system and app integration.

### Exploratory (traffic interception)
6. **MQTT/TCP proxy scripts** are available in `scripts/mqtt_proxy.py` and
   `scripts/tcp_sniffer.py`. Use DNS override or iptables DNAT to redirect the A3
   gateway's outbound traffic through these proxies to discover what protocols and data
   the gateway actually sends to the cloud. This could reveal an undocumented push
   channel for sensor events.
