# Standard Operating Procedure (SOP)
## Station 300: Conductor & Wiring Assembly
**Document ID:** SOP-ST-300  
**Target Part:** Steering Wheel Heating & Wiring Assembly  
**Process Owner:** Electrical Assembly Quality Engineering  

---

## 1. Process Overview
At this station, resistive heating wire is wound around the rim core, and the NTC temperature thermistor is embedded flush into the polyurethane surface. Electrical harnesses for the horn, multi-function switches, and airbag connections are routed and crimped to connectors.

## 2. Standard Operating Parameters
The automated winding and crimping machines must hold the following limits:

| Parameter | Sensor/Variable ID | Lower Spec Limit (LSL) | Target | Upper Spec Limit (USL) | Unit |
|---|---|---|---|---|---|
| Heater Winding Tension | `winding_tension` | 12 | 14 | 16 | N |
| Element Embedding Pressing Force | `pressing_force` | 80 | 90 | 100 | N |
| Connector Crimp Force | `crimp_force` | 1.2 | 1.35 | 1.5 | kN |

> [!WARNING]
> **Heater Winding Tension:** Tension exceeding 16.0 N can introduce microscopic necking and structural weakness to the micro-resistive wire. Though it may pass initial electrical tests at QC-300, it is prone to breaking during downstream mechanical wrapping or laser bombardment.

## 3. Quality Control Inspections (QC-300)
All assemblies must pass automated electrical verification at checkpoint **QC-300**.

### 3.1 Initial Heater Circuit Test
*   **Measurement:** `heater_resistance_ohms`
*   **Acceptable Limits:** 2.10 Ω to 2.50 Ω.
*   **Action Plan (Out of Spec):** Reject and scrap/rework. Infinite resistance indicates wire break or open crimp. Low resistance indicates short-circuit.

### 3.2 Thermistor Sensor Check
*   **Measurement:** `thermistor_resistance_kohm`
*   **Acceptable Limits:** 9.50 kΩ to 10.50 kΩ (at ambient temperature ~25°C).
*   **Action Plan (Out of Spec):** Out of spec indicates a faulty or wrong thermistor component. Scrap batch and check supplier lot trace.
