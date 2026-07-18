# Standard Operating Procedure (SOP)
## Station 100: Magnesium Skeleton Casting
**Document ID:** SOP-ST-100  
**Target Part:** Automotive Steering Wheel Armature (Skeleton)  
**Process Owner:** Foundry Quality Engineering  

---

## 1. Process Overview
The steering wheel skeleton provides the structural integrity of the final wheel. It is manufactured by injecting molten magnesium alloy (AM60B) into a precision die-casting mold under high pressure.

## 2. Standard Operating Parameters
The casting machine must maintain the following operational parameters during the cycle:

| Parameter | Sensor/Variable ID | Lower Spec Limit (LSL) | Target | Upper Spec Limit (USL) | Unit |
|---|---|---|---|---|---|
| Melt Temperature | `melt_temp` | 640 | 660 | 680 | °C |
| Clamping Force | `clamp_force` | 580 | 600 | 620 | tons |
| Injection Pressure | `injection_pressure` | 680 | 710 | 740 | bar |
| Die Temperature | `die_temp` | 200 | 215 | 230 | °C |
| Vacuum Level | `vacuum_level` | 30 | 40 | 50 | mbar |
| Cooling Time | `cooling_time` | 8.0 | 10.0 | 12.0 | seconds |
| Total Cycle Time | `cycle_time` | 35.0 | 40.0 | 45.0 | seconds |

## 3. Quality Control Inspections (QC-100)
Every cast armature must pass the automated Inspection Gate **QC-100** before being transferred to Foaming.

### 3.1 Density/Weight Check
*   **Measurement:** `casting_weight`
*   **Acceptable Limits:** 950.0 g to 1050.0 g.
*   **Action Plan (Out of Spec):** Scrap part if weight is under 950g (under-fill). Rework/trim excess flash if weight is over 1050g.

### 3.2 Porosity (Automated X-Ray)
*   **Measurement:** `porosity_pct`
*   **Acceptable Limits:** Maximum 2.0% volume porosity.
*   **Action Plan (Out of Spec):** Parts exceeding 2.0% porosity must be scrapped immediately due to structural safety hazards (brittle failure risk).
*   **Root Cause Clues:** High porosity is almost always correlated with a low vacuum level (sensor reading above 50 mbar) or worn mold seals.
