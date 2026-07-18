# Standard Operating Procedure (SOP)
## Station 200: Polyurethane Foaming
**Document ID:** SOP-ST-200  
**Target Part:** Steering Wheel Polyurethane Core  
**Process Owner:** Plastics Quality Engineering  

---

## 1. Process Overview
The cast magnesium skeleton is placed into the foaming mold cavity. High-pressure dispensing heads inject a precise, fast-curing mixture of Polyol and Isocyanate. The chemicals expand, forming a soft, microcellular cushioning layer around the metal armature.

## 2. Standard Operating Parameters
The foaming machine (Hennecke/KraussMaffei) must maintain the following parameters:

| Parameter | Sensor/Variable ID | Lower Spec Limit (LSL) | Target | Upper Spec Limit (USL) | Unit |
|---|---|---|---|---|---|
| Mold Temperature | `mold_temp` | 45 | 50 | 55 | °C |
| Polyol Temperature | `polyol_temp` | 22 | 23.5 | 25 | °C |
| Isocyanate Temperature | `iso_temp` | 22 | 23.5 | 25 | °C |
| Polyol Flow Rate | `polyol_flow_rate` | 98.0 | 100.0 | 102.0 | g/s |
| Isocyanate Flow Rate | `iso_flow_rate` | 104.0 | 106.0 | 108.0 | g/s |
| Injection Pressure | `injection_pressure` | 140 | 150 | 160 | bar |
| Demolding/Curing Time | `demold_time` | 110.0 | 120.0 | 130.0 | seconds |

### 2.1 Chemical Formulation Control
*   **Mixing Ratio (Polyol:Iso):** Target ratio is 100:106.
*   **Formula Calculation:** `mixing_ratio = (iso_flow_rate / polyol_flow_rate) * 100`
*   **Operational Range:** 104.0 to 108.0.
*   **Crucial Alert:** If the ratio shifts outside 100:104 to 100:108, the polyurethane will either fail to cure fully (soft/sticky skin) or become too rigid.

## 3. Quality Control Inspections (QC-200)
All foamed cores must be inspected at checkpoint **QC-200**.

### 3.1 Hardness Test
*   **Measurement:** `foam_hardness_shore_a`
*   **Acceptable Limits:** 40.0 to 60.0 Shore A.
*   **Action Plan (Out of Spec):** Soft foam (under 40.0) is scraped. Check for Isocyanate flow drops or ratio imbalance.

### 3.2 Foamed Core Weight Check
*   **Measurement:** `foam_weight`
*   **Acceptable Limits:** 300.0 g to 350.0 g.
*   **Action Plan (Out of Spec):** Weight under 300.0g indicates internal voids, large air pockets, or an incomplete fill ("short mold"). Check for low mold temperature or under-injection.
