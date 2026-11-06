# Guardian Wing: AI-Powered Surveillance Drone for Women's Safety & Isolated Area Assistance

## Project Overview
Guardian Wing is an AI-driven smart surveillance drone prototype engineered to protect citizens (with special emphasis on women's safety) across isolated roads, unlit bypasses, and low-density areas. 

The system leverages:
1. **Edge-Level / Simulated AI Vision**: Real-time road density estimation, pedestrian behavior tracking, harassment/altercation detection, and SOS gesture recognition.
2. **Citizen Privacy by Design**: Automated facial & pedestrian anonymization/blurring during normal patrols. Unmasking only occurs during high-confidence incident alerts or authorized dispatch override.
3. **Control Room C4I Dashboard**: Live low-latency video feed, live GPS telemetry and interactive Leaflet map, evidence snapshot inspection, and human-in-the-loop alert verification with rapid rescue dispatch.
4. **On-Drone Active Deterrents**: Remote high-lumen spotlights, 110dB deterrent siren, and two-way voice communication intercom.

---

## Directory Structure
- [main.py](file:///d:/DRONES/main.py): FastAPI application running the WebSocket streaming server and REST API for drone control & rescue dispatch.
- [vision_engine.py](file:///d:/DRONES/vision_engine.py): Computer vision engine with scenario simulations, behavioral heuristics, and privacy-preserving blurring.
- [drone_manager.py](file:///d:/DRONES/drone_manager.py): Flight telemetry manager, GPS loop simulator, actuator status, and incident verification queue.
- [templates/index.html](file:///d:/DRONES/templates/index.html): Real-time web dashboard featuring telemetry, map, interactive scenario injector, and verification panel.

---

## How to Run & Access

1. **Start the server**:
   ```bash
   python main.py
   ```
   *The server starts on `http://127.0.0.1:8000`.*

2. **Open the Control Room**:
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

3. **Interactive Scenario Testing**:
   Click on the scenario buttons at the bottom of the feed:
   - **Empty Road**: Verifies low-density detection and isolated area tracking.
   - **Normal Solo**: Demonstrates routine escort surveillance with privacy blurring enabled.
   - **Stalking/Shadow**: Triggers a proximity warning when someone follows a solo pedestrian.
   - **SOS Wave**: Triggers a distress signal alert when hands are waved overhead.
   - **Harassment**: Triggers a high-priority emergency alert when grappling or restraint is identified.

4. **Human-in-the-Loop Verification**:
   - When an alert triggers, review the evidence snapshot in the **Verification & Rescue Queue**.
   - Click **"Dispatch Rescue"** to log emergency crew coordination, or **"Dismiss"** for false alarms.
   - Trigger the **Spotlight**, **Siren**, or **Voice Intercom** to deter aggressors while emergency units are en route.
