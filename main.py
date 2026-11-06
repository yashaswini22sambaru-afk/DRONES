"""
FastAPI Server for AI-Powered Surveillance Drone & Central Control Room.
Handles:
- WebSockets for continuous frame streaming & telemetry
- REST endpoints for scenario toggling, actuator triggers, and incident verification
- Privacy protection filters and coordination dispatch
"""

import asyncio
import os
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from vision_engine import VisionEngine
from drone_manager import DroneManager

app = FastAPI(title="Guardian Wing AI Drone Control Room")

vision_engine = VisionEngine()
drone_manager = DroneManager()

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open(os.path.join("templates", "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/scenario")
async def set_scenario(name: str):
    valid_scenarios = ["empty_road", "normal_patrol", "suspicious_stalking", "distress_sos", "physical_altercation"]
    if name in valid_scenarios:
        drone_manager.current_scenario = name
        return {"status": "success", "scenario": name}
    return {"status": "error", "message": "Invalid scenario name"}

@app.post("/api/privacy")
async def toggle_privacy(enabled: bool):
    vision_engine.privacy_mode_enabled = enabled
    return {"status": "success", "privacy_mode": vision_engine.privacy_mode_enabled}

@app.post("/api/actuator")
async def toggle_actuator(type: str):
    if type == "spotlight":
        drone_manager.spotlight_on = not drone_manager.spotlight_on
    elif type == "siren":
        drone_manager.siren_on = not drone_manager.siren_on
    elif type == "audio":
        drone_manager.two_way_audio_active = not drone_manager.two_way_audio_active
    
    return {
        "status": "success",
        "spotlight": drone_manager.spotlight_on,
        "siren": drone_manager.siren_on,
        "audio": drone_manager.two_way_audio_active
    }

@app.post("/api/verify-alert")
async def verify_alert(incident_id: str, action: str):
    result = drone_manager.verify_alert(incident_id, action)
    if result:
        return {"status": "success", "incident": result}
    return {"status": "error", "message": "Alert not found"}

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    tick = 0.0
    try:
        while True:
            tick += 0.2
            drone_manager.update_telemetry(tick)
            
            # Generate computer vision surveillance frame
            frame, incident_meta = vision_engine.generate_simulated_frame(
                scenario=drone_manager.current_scenario, 
                tick=tick
            )
            
            frame_b64 = vision_engine.frame_to_base64_jpeg(frame)
            
            # If emergency scenario detected, record incident snapshot
            if incident_meta["is_emergency"]:
                drone_manager.trigger_incident(incident_meta, frame_b64)

            # Build real-time telemetry payload
            payload = {
                "frame": frame_b64,
                "telemetry": {
                    "drone_id": drone_manager.drone_id,
                    "lat": drone_manager.current_lat,
                    "lng": drone_manager.current_lng,
                    "altitude": drone_manager.altitude_m,
                    "speed": drone_manager.speed_kmh,
                    "battery": drone_manager.battery_pct,
                    "flight_mode": drone_manager.flight_mode,
                    "spotlight": drone_manager.spotlight_on,
                    "siren": drone_manager.siren_on,
                    "audio": drone_manager.two_way_audio_active
                },
                "incident": incident_meta,
                "alerts": drone_manager.alerts_active[:10],
                "audit_logs": drone_manager.operator_actions[:8]
            }

            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(0.1) # ~10 FPS stream for responsive real-time client experience

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WS error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
