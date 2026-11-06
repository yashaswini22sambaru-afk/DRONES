"""
Drone State Management & Telemetry Streamer
Maintains drone coordinates, patrol route over isolated zones, battery, and alert history.
"""

import time
import math
import uuid
from typing import List, Dict, Any

class DroneManager:
    def __init__(self):
        # Base patrol coordinates (e.g., suburban perimeter / unlit industrial road network)
        self.drone_id = "UAV-GW-09"
        self.callsign = "Guardian Wing Alpha"
        self.base_lat = 28.5355
        self.base_lng = 77.3910
        self.current_lat = 28.5355
        self.current_lng = 77.3910
        self.altitude_m = 42.5
        self.speed_kmh = 28.0
        self.battery_pct = 88.0
        self.current_scenario = "empty_road"
        self.flight_mode = "AUTONOMOUS_PATROL"
        self.incident_history: List[Dict[str, Any]] = []
        self.alerts_active: List[Dict[str, Any]] = []
        self.operator_actions: List[Dict[str, Any]] = []
        self.spotlight_on = False
        self.siren_on = False
        self.two_way_audio_active = False

    def update_telemetry(self, step: float):
        """Simulates patrol route loop along isolated roads and battery consumption"""
        radius = 0.0035  # ~350-400m patrol radius
        self.current_lat = self.base_lat + radius * math.sin(step * 0.05)
        self.current_lng = self.base_lng + radius * math.cos(step * 0.05)
        
        # Gradual battery drain
        self.battery_pct = max(10.0, round(self.battery_pct - 0.005, 1))

    def trigger_incident(self, incident_meta: Dict[str, Any], snapshot_b64: str) -> Dict[str, Any]:
        """Creates formal incident record sent to control room"""
        incident_id = f"INC-{int(time.time())}-{uuid.uuid4().hex[:4].upper()}"
        alert_record = {
            "id": incident_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "drone_id": self.drone_id,
            "location": {
                "latitude": round(self.current_lat, 6),
                "longitude": round(self.current_lng, 6),
                "sector": "Sector 62 Outer Beltway (Isolated Bypass)"
            },
            "emergency_type": incident_meta.get("emergency_type"),
            "confidence": incident_meta.get("confidence", 0.9),
            "description": incident_meta.get("alert_description"),
            "snapshot": snapshot_b64,
            "status": "PENDING_VERIFICATION", # Verification by trained personnel
            "crowd_count": incident_meta.get("crowd_count", 0),
            "verification": {
                "verified_by": None,
                "action_taken": None,
                "verified_at": None
            }
        }
        
        # Check if already triggered recently to avoid flooding
        recent = [a for a in self.alerts_active if a["emergency_type"] == alert_record["emergency_type"]]
        if not recent:
            self.alerts_active.insert(0, alert_record)
            self.incident_history.insert(0, alert_record)
            return alert_record
        return recent[0]

    def verify_alert(self, incident_id: str, action: str, operator_name: str = "Officer Patel (Dispatch)"):
        """Trained human operator verifies incident and coordinates rescue"""
        for alert in self.alerts_active:
            if alert["id"] == incident_id:
                alert["status"] = "VERIFIED_ACTIONED" if action != "DISMISS" else "FALSE_POSITIVE"
                alert["verification"] = {
                    "verified_by": operator_name,
                    "action_taken": action,
                    "verified_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                self.operator_actions.insert(0, {
                    "timestamp": time.strftime("%H:%M:%S"),
                    "incident_id": incident_id,
                    "action": action,
                    "operator": operator_name
                })
                return alert
        return None
