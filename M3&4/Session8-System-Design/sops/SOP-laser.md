# Standard Operating Procedure (SOP)
## Station 400: Laser Surface Texturing
**Document ID:** SOP-ST-400  
**Target Part:** Textured Foam Core (Surface Activation)  
**Process Owner:** Laser Process & Robotics Engineering  

---

## 1. Process Overview
To ensure a rugged grip and improve leather bonding adhesion, the foam rim core is positioned by two synchronized robotic arms. A high-speed CO2 laser texturing system scan-ablates the polyurethane surface, creating micro-grooves and activated surface regions.

## 2. Standard Operating Parameters
The robotic arms and laser controller must maintain the following operational parameters:

| Parameter | Sensor/Variable ID | Lower Spec Limit (LSL) | Target | Upper Spec Limit (USL) | Unit |
|---|---|---|---|---|---|
| Laser Power | `laser_power` | 80 | 100 | 120 | W |
| Laser Scan Speed | `laser_scan_speed` | 800 | 900 | 1000 | mm/s |
| Pulse Frequency | `pulse_freq` | 30 | 40 | 50 | kHz |
| Robotic Alignment Offset | `robot_offset` | 0.00 | 0.05 | 0.15 | mm |
| Focal Distance | `focal_distance` | 148 | 150 | 152 | mm |

> [!CAUTION]
> **Robotic Alignment and Over-Power Damage:** If the laser power exceeds 120W or the robotic arm alignment offset drifts past 0.15mm (e.g. due to joint wear or calibration slip), the laser focal point can penetrate past the polyurethane outer skin and melt/cut the underlying copper resistive heating elements installed at Station 3. This will cause downstream electrical open-circuits in Station 5.

## 3. Quality Control Inspections (QC-400)
All textured wheels are scanned via a non-contact laser profilometer at gate **QC-400**.

### 3.1 Texture Depth Check
*   **Measurement:** `texture_depth_microns`
*   **Acceptable Limits:** 80.0 μm to 120.0 μm.
*   **Action Plan (Out of Spec):** Depth under 80μm fails to provide adequate leather adhesion (grip slip risk) -> reject for rework. Depth over 120μm indicates structural foam damage or possible wire strike -> scrap immediately.

### 3.2 Surface Roughness
*   **Measurement:** `surface_roughness_ra`
*   **Acceptable Limits:** 6.0 μm to 10.0 μm.
*   **Action Plan (Out of Spec):** Roughness out of range indicates focus drift. Calibrate focal distance.
