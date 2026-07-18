# Standard Operating Procedure (SOP)
## Station 500: Leather Wrapping & Final Assembly
**Document ID:** SOP-ST-500  
**Target Part:** Completed Steering Wheel Assembly  
**Process Owner:** Assembly & Finishing Quality Engineering  

---

## 1. Process Overview
At this station, polyurethane-laser-textured steering wheel rims are wrapped with custom-cut leather. Hot-melt adhesive is applied, and operators stitch the leather seams. The final assembly involves mounting switches, bezels, paddle shifters, and the airbag housing, followed by final quality audit checks.

## 2. Standard Operating Parameters
Assembly tools and processes must maintain these limits:

| Parameter | Sensor/Variable ID | Lower Spec Limit (LSL) | Target | Upper Spec Limit (USL) | Unit |
|---|---|---|---|---|---|
| Leather Wrapping Tension | `wrapping_tension` | 20 | 22.5 | 25 | N |
| Adhesive Dispense Weight | `glue_weight` | 15.0 | 20.0 | 25.0 | g |
| Adhesive Temperature | `glue_temp` | 120 | 130 | 140 | °C |
| Trim Screws Torque | `screw_torque` | 2.4 | 2.6 | 2.8 | Nm |

> [!WARNING]
> **Adhesive Temperature Control:** If `glue_temp` falls below 110°C, the adhesive viscosity increases, causing poor surface bonding. This yields loose leather patches or cosmetic "wrinkling" within 24 hours.
> 
> **Excessive Wrapping Tension:** If wrapping tension spikes above 30N (often due to manual operator pull or mechanical tensioner calibration error), it stretches the leather excessively. This tension is transmitted directly to the underlying heater wire. If the wire has been previously weakened (e.g. by laser scoring or high winding tension), it will snap under this final tension, causing a complete electrical open-circuit.

## 3. Quality Control Inspections (QC-500 - End of Line)
Every finished steering wheel must pass the End-of-Line (EOL) electrical and mechanical test **QC-500**.

### 3.1 Final Heater Resistance (Critical safety & comfort)
*   **Measurement:** `final_heater_resistance_ohms`
*   **Acceptable Limits:** 2.10 Ω to 2.50 Ω.
*   **Action Plan (Out of Spec):** Infinite/extremely high resistance (e.g., > 10.0 Ω or `999.9` Ω) indicates a wire break. The part must be scrapped and investigated.
*   **Investigation Path:** Cross-reference `heater_resistance_ohms` at QC-300. If it was PASS (e.g. 2.3 Ω) but QC-500 is FAIL, the wire was broken during Station 4 (Laser) or Station 5 (Wrapping). Look for high laser power/robot offset at Station 4 or excessive wrapping tension at Station 5.

### 3.2 Airbag Circuit Resistance (Safety critical)
*   **Measurement:** `airbag_resistance_ohms`
*   **Acceptable Limits:** 1.80 Ω to 2.20 Ω.
*   **Action Plan (Out of Spec):** Scrap module, quarantine airbag harness batch.

### 3.3 Switch Continuity
*   **Measurement:** `switch_continuity_resistance_ohms`
*   **Acceptable Limits:** Maximum 0.50 Ω.
