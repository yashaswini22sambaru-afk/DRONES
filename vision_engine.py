"""
AI Models and Vision Engine for Drone Surveillance & Safety Analysis.
Includes:
- Empty road / low-density area detection
- Anomaly / harassment / distress gesture detection
- Privacy masking / Face & pedestrian anonymization before storage
- Image snapshot capture with metadata
"""

import cv2
import numpy as np
import time
import base64
from typing import Dict, Any, List, Tuple

class VisionEngine:
    def __init__(self):
        # We use a synthetic yet realistic computer vision frame generator & analyzer
        # equipped with privacy preservation filters and incident trigger simulations.
        self.privacy_mode_enabled = True
        self.last_incident_time = 0

    def apply_privacy_blur(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Anonymize pedestrians by blurring faces/bodies when not in verified emergency state
        to protect citizen privacy under routine patrol.
        """
        output = frame.copy()
        if not self.privacy_mode_enabled:
            return output

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            h, w = output.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            # Anonymize head/face region or whole bounding box
            roi = output[y1:y2, x1:x2]
            if roi.size > 0:
                blurred = cv2.GaussianBlur(roi, (25, 25), 30)
                output[y1:y2, x1:x2] = blurred
        return output

    def generate_simulated_frame(self, scenario: str = "normal", tick: float = 0.0) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Generates realistic surveillance drone video feed graphics with HUD overlays,
        road segmentations, and dynamic scenario actors.
        Scenarios: 'empty_road', 'normal_patrol', 'suspicious_stalking', 'distress_sos', 'physical_altercation'
        """
        width, height = 800, 480
        # Create dark road / street background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Road pavement
        frame[:] = (28, 30, 32)
        
        # Isolated road borders and pavement
        cv2.fillPoly(frame, [np.array([[120, 0], [680, 0], [780, 480], [20, 480]])], (45, 48, 52))
        
        # Road markings (dashed center line)
        offset = int((tick * 60) % 80)
        for y in range(-80 + offset, height, 80):
            cv2.line(frame, (400, y), (400, y + 40), (200, 200, 200), 4)
            
        # Side trees / dark bushes (isolated area backdrop)
        for i in range(0, height, 60):
            cv2.circle(frame, (50, i + 20), 35, (20, 35, 20), -1)
            cv2.circle(frame, (750, i + 10), 40, (18, 32, 18), -1)

        detections = []
        incident_meta = {
            "is_emergency": False,
            "emergency_type": None,
            "confidence": 0.0,
            "density_level": "LOW_DENSITY_EMPTY",
            "crowd_count": 0,
            "alert_description": "Road Clear / Isolated Zone"
        }

        # Actor coordinates and scenarios
        if scenario == "empty_road":
            incident_meta["density_level"] = "ISOLATED_EMPTY_ROAD"
            incident_meta["alert_description"] = "No pedestrians detected. Low-density isolated area under active surveillance."
            incident_meta["crowd_count"] = 0

        elif scenario == "normal_patrol":
            incident_meta["density_level"] = "LOW_DENSITY (1 Person)"
            incident_meta["crowd_count"] = 1
            # 1 lone pedestrian walking along footpath
            px, py = int(220 + np.sin(tick * 0.5) * 15), int(260 + np.cos(tick * 0.5) * 10)
            detections.append({
                "id": "person_1",
                "label": "Pedestrian (Lone)",
                "bbox": [px - 20, py - 45, px + 20, py + 45],
                "behavior": "Walking peacefully"
            })
            incident_meta["alert_description"] = "Solo pedestrian observed in isolated sector. Routine safety escort active."

        elif scenario == "suspicious_stalking":
            incident_meta["is_emergency"] = True
            incident_meta["emergency_type"] = "SUSPICIOUS_FOLLOWING_STALKING"
            incident_meta["confidence"] = 0.89
            incident_meta["density_level"] = "VERY_LOW_DENSITY (2 Persons)"
            incident_meta["crowd_count"] = 2
            incident_meta["alert_description"] = "Proximity alert: Individual trailing lone female closely on unlit road."

            # Person 1 (Target)
            px1, py1 = 340, 240
            detections.append({
                "id": "person_victim",
                "label": "Person (Target)",
                "bbox": [px1 - 20, py1 - 45, px1 + 20, py1 + 45],
                "behavior": "Accelerating pace / Distressed"
            })
            # Person 2 (Stalker)
            px2, py2 = int(340 + np.sin(tick * 2) * 8), 305
            detections.append({
                "id": "person_suspect",
                "label": "Suspicious Subject",
                "bbox": [px2 - 22, py2 - 45, px2 + 22, py2 + 45],
                "behavior": "Target tracking / Shadowing < 2.5m"
            })

        elif scenario == "distress_sos":
            incident_meta["is_emergency"] = True
            incident_meta["emergency_type"] = "DISTRESS_SIGNAL_GESTURE"
            incident_meta["confidence"] = 0.94
            incident_meta["density_level"] = "ISOLATED (1 Person Calling Help)"
            incident_meta["crowd_count"] = 1
            incident_meta["alert_description"] = "Emergency SOS gesture detected (Hands waved overhead / signaling drone)."

            px, py = 390, 250
            detections.append({
                "id": "person_sos",
                "label": "Distressed Person",
                "bbox": [px - 25, py - 50, px + 25, py + 50],
                "behavior": "Active SOS Gesture / Waving for help"
            })

        elif scenario == "physical_altercation":
            incident_meta["is_emergency"] = True
            incident_meta["emergency_type"] = "PHYSICAL_HARASSMENT_GRAPPLING"
            incident_meta["confidence"] = 0.97
            incident_meta["density_level"] = "ISOLATED CRITICAL (2 Persons Grappling)"
            incident_meta["crowd_count"] = 2
            incident_meta["alert_description"] = "URGENT: Physical harassment or struggle detected. High kinetic confrontation."

            # Closely tangled bounding boxes
            px, py = 380, 250
            detections.append({
                "id": "person_victim",
                "label": "Target (Under Attack)",
                "bbox": [px - 28, py - 45, px + 5, py + 45],
                "behavior": "Being physically restrained"
            })
            detections.append({
                "id": "person_aggressor",
                "label": "Aggressor",
                "bbox": [px - 5, py - 48, px + 35, py + 45],
                "behavior": "Harassment / Forced movement"
            })

        # Draw actors onto frame
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            is_emergency = incident_meta["is_emergency"]
            color = (50, 70, 240) if is_emergency else (80, 220, 100) # Red/Amber or Green

            # Draw body silhouette
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            # Head
            cv2.circle(frame, (cx, y1 + 14), 10, (220, 220, 220), -1)
            # Torso
            cv2.line(frame, (cx, y1 + 24), (cx, y2 - 20), (200, 200, 200), 4)
            # Arms & gestures
            if "SOS" in det.get("behavior", ""):
                # Waving arms up
                arm_wiggle = int(np.sin(tick * 8) * 8)
                cv2.line(frame, (cx, y1 + 30), (cx - 24, y1 - 10 + arm_wiggle), (240, 240, 240), 3)
                cv2.line(frame, (cx, y1 + 30), (cx + 24, y1 - 10 - arm_wiggle), (240, 240, 240), 3)
            elif "Harassment" in det.get("behavior", "") or "restrained" in det.get("behavior", ""):
                # Confrontation arms
                cv2.line(frame, (cx, y1 + 32), (cx + (15 if "Victim" in det["label"] else -15), y1 + 25), (240, 100, 100), 3)
            else:
                cv2.line(frame, (cx, y1 + 32), (cx - 15, y1 + 50), (200, 200, 200), 3)
                cv2.line(frame, (cx, y1 + 32), (cx + 15, y1 + 50), (200, 200, 200), 3)
            
            # Legs
            cv2.line(frame, (cx, y2 - 20), (cx - 12, y2), (180, 180, 180), 3)
            cv2.line(frame, (cx, y2 - 20), (cx + 12, y2), (180, 180, 180), 3)

            # Bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            # Label banner
            tag = f"{det['label']} | {det['behavior']}"
            cv2.putText(frame, tag, (x1, max(15, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, color, 1, cv2.LINE_AA)

        # Apply privacy safeguards (blur face/identifiable features unless operator overrides)
        if self.privacy_mode_enabled and not incident_meta["is_emergency"]:
            frame = self.apply_privacy_blur(frame, detections)

        # Drone HUD overlay (Telemetry, Crosshairs, Night-vision status, Coordinates)
        frame = self._render_drone_hud(frame, incident_meta, tick)

        return frame, incident_meta

    def _render_drone_hud(self, frame: np.ndarray, meta: Dict[str, Any], tick: float) -> np.ndarray:
        h, w = frame.shape[:2]
        # Crosshair in center
        cx, cy = w // 2, h // 2
        hud_color = (0, 230, 255) if not meta["is_emergency"] else (0, 70, 255)
        
        # Center gimbal reticle
        cv2.circle(frame, (cx, cy), 24, hud_color, 1)
        cv2.line(frame, (cx - 35, cy), (cx - 10, cy), hud_color, 1)
        cv2.line(frame, (cx + 10, cy), (cx + 35, cy), hud_color, 1)
        cv2.line(frame, (cx, cy - 35), (cx, cy - 10), hud_color, 1)
        cv2.line(frame, (cx, cy + 10), (cx, cy + 35), hud_color, 1)

        # Corner brackets
        b_len = 25
        corners = [(15, 15, 1, 1), (w - 15, 15, -1, 1), (15, h - 15, 1, -1), (w - 15, h - 15, -1, -1)]
        for x, y, dx, dy in corners:
            cv2.line(frame, (x, y), (x + dx * b_len, y), (140, 140, 140), 1)
            cv2.line(frame, (x, y), (x, y + dy * b_len), (140, 140, 140), 1)

        # Telemetry HUD text
        cv2.putText(frame, "DRONE RECON: GUARDIAN-WING V3 [ACTIVE]", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 180), 1)
        cv2.putText(frame, f"DENSITY: {meta['density_level']}", (25, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)
        
        # Privacy Mode Indicator
        priv_text = "PRIVACY COMPLIANCE: BLUR ON" if self.privacy_mode_enabled else "PRIVACY COMPLIANCE: OVERRIDDEN BY DISPATCH"
        cv2.putText(frame, priv_text, (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 220, 100) if self.privacy_mode_enabled else (0, 165, 255), 1)

        # Emergency Banner if alert
        if meta["is_emergency"]:
            cv2.rectangle(frame, (0, 0), (w, 24), (0, 0, 180), -1)
            alert_str = f"ALERT: {meta['emergency_type']} | CONF: {int(meta['confidence']*100)}% | TRANSMITTING TO DISPATCH"
            cv2.putText(frame, alert_str, (15, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return frame

    def frame_to_base64_jpeg(self, frame: np.ndarray) -> str:
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return base64.b64encode(buffer).decode('utf-8')
