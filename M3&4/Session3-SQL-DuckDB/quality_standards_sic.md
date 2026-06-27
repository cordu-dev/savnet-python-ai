# Station Instruction Card (SIC) — Steering Wheel Manufacturing

| Field | Value |
|---|---|
| **Document** | SIC-SW-2025-001 |
| **Revision** | A |
| **Effective date** | 2025-01-06 |
| **Approved by** | Process Engineering Lead |
| **Product lines** | PT55 Standard / PT66 Sport / PT77 Premium |

---

## Process Flow Overview

```
                              ┌─────────────────────────────────────────────────┐
Raw Materials (Mg Lingouri)   │                                                 │
        │                     │  PT55 Standard  →  MOLDING → QC → FOAMING → TAPITAT
        ▼                     │
   BATCH SETUP (66 units)     │  PT66 Sport     →  MOLDING → QC → FOAMING → CONDUCTOR → TAPITAT
        │                     │
        ▼                     │  PT77 Premium   →  MOLDING → QC → FOAMING → CONDUCTOR → LASER → TAPITAT
  Start Production            │                                                 │
                              └─────────────────────────────────────────────────┘
```

> **Key question at batch start:** *Ce materiale am?* (What materials do we have?)  
> The Production Manager must confirm stock levels before dimensioning each batch.

---

## STATION 01 — MOLDING SKELET

### Process Overview
The operator feeds **Magnesium ingots (Lingouri / Magneziu Crud)** into the injection mold press to form the steering wheel skeleton (Skelet). The Mg alloy is injected at high temperature and pressure into a precision mold. The skeleton is the structural foundation for all downstream stations.

### Roles
| Role | Responsibility |
|---|---|
| Operator | Loads ingots, sets parameters, runs the cycle |
| Process Engineer | Validates mold tool selection and parameter setup |
| Production Manager | Coordinates batch start and confirms material availability |

### Input Materials
| Material | Grade | Nominal Qty per Unit | Tolerance |
|---|---|---|---|
| Mg Ingot (Lingouri) | Grade-A | 0.500 kg | ± 0.020 kg |

### Process Parameters
| Parameter | Target | Min | Max | Unit |
|---|---|---|---|---|
| Mold temperature | 200 | **180** | **220** | °C |
| Injection pressure | 8.5 | **6.0** | **12.0** | bar |
| Ambient humidity | < 55 | — | **65** | % |
| Cycle time | 55 | 20 | 120 | sec |
| Mg quantity per cycle | 0.500 | 0.450 | 0.550 | kg |

> ⚠️ **PT77 Premium:** Target temperature is **205 °C** to improve alloy flow in the premium mold profile.

### Pass / Rework / Scrap Criteria

| Outcome | Conditions |
|---|---|
| **OK** | Temperature 180–220 °C, pressure 6–12 bar, no visible cracks or incomplete fill |
| **REWORK** | Temperature ±10 °C outside spec, minor flash (< 2 mm), borderline pressure |
| **SCRAP** | Temperature > 240 °C or < 160 °C, major crack, incomplete fill > 5%, tool damage |

### Recorded Fields
`product_id`, `batch_id`, `product_type`, `timestamp`, `shift`, `operator_id`, `mold_tool_id`, `temperature_c`, `humidity_pct`, `pressure_bar`, `mg_quantity_kg`, `duration_sec`, `cycle_result`

---

## STATION 02 — QUALITY CHECK POINT

### Process Overview
Every skeleton undergoes a dimensional and surface quality inspection before proceeding to foaming. This station is the primary gate that prevents defective skeletons from consuming downstream materials. Products that fail are routed to **Rework** or **Scrap**.

### Roles
| Role | Responsibility |
|---|---|
| Inspector | Performs all measurements and records results |
| Process Engineer | Investigates systematic failures (tooling, batch correlation) |

### Inspection Criteria

#### Dimensional Check
| Measurement | Specification | Pass | Fail → Rework | Fail → Scrap |
|---|---|---|---|---|
| Outer diameter | ± 0.3 mm from nominal | Within spec | Out by 0.3–0.8 mm | Out > 0.8 mm |
| Roundness deviation | < 0.50 mm | < 0.50 mm | 0.50–0.80 mm | > 0.80 mm |
| Spoke thickness | ± 0.5 mm | Within spec | Borderline | Structural defect |

#### Surface Check
| Defect Type | Pass | Rework | Scrap |
|---|---|---|---|
| Flash / burr | None | < 2 mm removable | > 2 mm or structural |
| Porosity / void | None | Single minor pore | Multiple or > 1 mm² |
| Cracks | None | Hairline < 5 mm | Any visible crack > 5 mm |

#### Weight Check (as proxy for material fill)
| Product Type | Target | Min | Max |
|---|---|---|---|
| PT55 Standard | 380 g | 360 g | 400 g |
| PT66 Sport | 420 g | 400 g | 440 g |
| PT77 Premium | 460 g | 440 g | 480 g |

### Pass / Rework / Scrap Criteria Summary
| Outcome | Condition |
|---|---|
| **PASS** | All dimensional checks pass, surface OK, weight within range, roundness < 0.50 mm |
| **REWORK** | Single minor defect correctable without remolding |
| **SCRAP** | Multiple failures, or any single critical failure (structural crack, severe dimensional) |

### Recorded Fields
`qc_id`, `product_id`, `batch_id`, `product_type`, `timestamp`, `inspector_id`, `dimensional_check`, `surface_check`, `weight_g`, `roundness_mm`, `overall_result`, `notes`

---

## STATION 03 — FOAMING SPUMA

### Process Overview
The skeleton is placed in a foaming jig and **polyurethane foam** is injected to form the comfortable grip layer. Foam volume is precisely controlled by product type. The station operator monitors temperature, humidity, and pressure — all of which affect foam expansion rate and final density.

### Critical Rule — Product Type #55
> **PT55 Standard requires exactly 8.0 ml of polyurethane (tolerance: ± 0.5 ml)**  
> Source: Standard Guidelines, reference from diagram notation.

### Foam Volume Specification
| Product Type | Target Volume | Min (UNDERFILL threshold) | Max (OVERFILL threshold) | Scrap threshold |
|---|---|---|---|---|
| **PT55 Standard** | **8.0 ml** | 7.5 ml | 8.5 ml | < 6.5 ml or > 9.5 ml |
| **PT66 Sport** | **10.0 ml** | 9.5 ml | 10.5 ml | < 8.5 ml or > 11.5 ml |
| **PT77 Premium** | **12.0 ml** | 11.5 ml | 12.5 ml | < 10.5 ml or > 13.5 ml |

### Process Parameters
| Parameter | Target | Min | Max | Unit |
|---|---|---|---|---|
| Foam volume | Per table above | See above | See above | ml |
| Foam density | 1.05 | 0.90 | 1.20 | g/cm³ |
| Ambient temperature | 25 | **18** | **32** | °C |
| Ambient humidity | < 55 | — | **65** | % |
| Injection pressure | 6.5 | 4.0 | 10.0 | bar |
| Cure time | 210 | 150 | 300 | sec |

> ⚠️ **Humidity sensitivity:** Polyurethane reacts with moisture. Humidity > 65% causes foam voids and inconsistent density. **Stop foaming if humidity exceeds 65%** and notify the process engineer.

### Pass / Rework / Scrap Criteria
| Outcome | Condition |
|---|---|
| **OK** | Foam volume within ± 0.5 ml of target, no visible voids, cure complete |
| **UNDERFILL** | Foam volume below target by 0.5–1.5 ml — grip feel insufficient |
| **OVERFILL** | Foam volume above target by 0.5–1.5 ml — dimensional failure possible |
| **SCRAP** | Volume deviation > 1.5 ml from target, visible void, foam collapse, or cure failure |

### Recorded Fields
`product_id`, `batch_id`, `product_type`, `timestamp`, `operator_id`, `foam_volume_ml`, `foam_density_gcm3`, `temperature_c`, `humidity_pct`, `pressure_bar`, `cure_time_sec`, `foam_result`

---

## STATION 04 — CONDUCTOR INCALZIRE VOLAN

> **Applies to: PT66 Sport and PT77 Premium only.**  
> PT55 Standard does not include a heating conductor. Skip to Station 05.

### Process Overview
A resistance heating wire is routed around the steering wheel rim and connected to the vehicle's 12V system. The conductor enables the heated steering wheel function. The key quality gate is **electrical resistance** — too high means poor thermal performance or a connection fault.

### Wire Specification
| Product Type | Wire Gauge | Conductor Layout | Resistance Spec |
|---|---|---|---|
| PT66 Sport | 0.50 mm | Single Zone | < 2.5 Ω |
| PT77 Premium | 0.75 mm | Single Zone or Dual Zone | < 2.5 Ω |

### Process Parameters
| Parameter | Target | Min | Max | Unit |
|---|---|---|---|---|
| Resistance | 1.8 | — | **2.5** | Ω |
| Voltage test | 12.0 | 10.5 | 13.5 | V |
| Installation time | 210 | 90 | 380 | sec |

### Pass / Rework / Scrap Criteria
| Outcome | Condition |
|---|---|
| **OK** | Resistance < 2.5 Ω, voltage test nominal, no visible wire damage |
| **REWORK** | Resistance 2.5–3.0 Ω — re-crimp connector, re-route if loose |
| **SCRAP** | Resistance > 3.0 Ω, wire break, insulation damage, voltage test fail |

### Recorded Fields
`product_id`, `batch_id`, `product_type`, `timestamp`, `operator_id`, `wire_gauge_mm`, `resistance_ohm`, `voltage_test_v`, `installation_duration_sec`, `conductor_layout`, `result`

---

## STATION 05 — LASER BOMBARDMENT

> **Applies to: PT77 Premium only.**  
> This station is skipped for PT55 and PT66.

### Process Overview
A high-power laser creates a micro-textured grip surface on the leather layer (or foam layer prior to tapitat). The laser burning pattern determines the **tactile feel (Priză la mână — grip feel)**. After laser treatment, a **conductivity test** verifies that the grip surface is properly activated.

### Process Parameters
| Parameter | Target | Min | Max | Unit |
|---|---|---|---|---|
| Laser power | 100 | **80** | **120** | W |
| Burn duration | 9.0 | 4.0 | 20.0 | sec |
| Surface temperature | 55 | 38 | 78 | °C |

### Burning Patterns
| Pattern | Description |
|---|---|
| `Geometric_Grip` | Regular grid pattern — maximum grip area |
| `Ergonomic_Wave` | Contoured wave following hand position — comfort-focused |
| `Sport_Cross` | Diagonal cross-hatch — visual and tactile sport accent |

### Quality Gate — Grip Test (Priză la Mână)
The grip conductivity test measures whether the laser surface treatment achieved the required tactile activation.

| Outcome | `grip_conductivity_test` | `outcome` |
|---|---|---|
| Surface properly activated | `PASS` | `Priza_la_mana` |
| Surface not activated | `FAIL` | `FAIL` |

### Pass / Rework / Scrap Criteria
| Outcome | Condition |
|---|---|
| **OK** | Grip test PASS, laser power 80–120 W, even burn pattern, no deep damage |
| **REWORK** | Minor burn inconsistency, borderline power, pattern incomplete |
| **SCRAP** | Grip conductivity test FAIL, laser power out of spec, leather/foam damage |

### Recorded Fields
`product_id`, `batch_id`, `timestamp`, `operator_id`, `laser_power_w`, `burn_duration_sec`, `burning_pattern`, `surface_temp_c`, `grip_conductivity_test`, `outcome`, `result`

---

## STATION 06 — TAPITAT PIELE (Leather Wrapping)

### Process Overview
The steering wheel is wrapped with the final leather layer and stitched according to product specifications. Leather grade, stitching pattern, and adhesive quantity are determined by product type. This is the final value-add station before packaging.

### Leather Specification
| Product Type | Leather Type | Area Target | Stitching Pattern |
|---|---|---|---|
| PT55 Standard | Standard | 2.60 dm² ± 0.16 | Classic or Double_Stitch |
| PT66 Sport | Sport (perforated) | 2.90 dm² ± 0.16 | Sport_Diamond or Double_Stitch |
| PT77 Premium | Premium (full grain) | 3.20 dm² ± 0.16 | Premium_Hand (hand-stitched) |

### Process Parameters
| Parameter | Target | Min | Max | Unit |
|---|---|---|---|---|
| Leather area | Per table above | −0.30 dm² | +0.30 dm² | dm² |
| Adhesive quantity | 20 | 10 | 35 | ml |
| Process duration | 32 | 15 | 60 | min |

### Pass / Rework / Scrap Criteria
| Outcome | Condition |
|---|---|
| **OK** | Full leather coverage, clean stitching, no gaps or bubbles, adhesive well-distributed |
| **REWORK** | Minor stitch defect (< 3 stitches), small air bubble (< 5 mm²) — correctable |
| **SCRAP** | Leather tear, coverage gap > 10%, stitching line failure, adhesive contamination visible |

### Recorded Fields
`product_id`, `batch_id`, `product_type`, `timestamp`, `operator_id`, `leather_type`, `leather_quantity_dm2`, `stitching_pattern`, `adhesive_ml`, `tapitat_duration_min`, `result`

---

## Material Stock Reference

### Raw Materials Required for Production
| Material | Used At Station | Unit | Reorder Alert |
|---|---|---|---|
| Mg Ingot (Lingouri) | Molding | kg | Trigger when stock < 20% |
| Polyurethane Foam | Foaming | kg | Trigger when stock < 20% |
| Conductor Wire | Conductor | m | Trigger when stock < 20% |
| Leather (Standard / Sport / Premium) | Tapitat | dm² | Trigger when stock < 20% |
| Adhesive | Tapitat | kg | Trigger when stock < 20% |
| Dye | Tapitat (finish) | L | Trigger when stock < 20% |

### Batch Start Checklist
Before dimensioning a new batch, the Production Manager must confirm:

- [ ] Mg ingots in stock ≥ `batch_size × 0.500 kg × 1.10` (10% safety margin)
- [ ] Polyurethane foam in stock ≥ `batch_size × max_foam_per_type_ml × 1.10`
- [ ] Leather in stock ≥ `batch_size × max_leather_per_type_dm2 × 1.10`
- [ ] Conductor wire in stock ≥ `count_PT66_PT77 × wire_length_per_unit × 1.10`
- [ ] All material certificates valid (supplier grade confirmed)

---

## Scrap & Rework Decision Tree

```
Product fails any station check
        │
        ├── Single minor defect, correctable?
        │           │
        │           YES → REWORK — return to station, fix, re-inspect
        │           │
        │           NO  → SCRAP — remove from flow, log root cause
        │
        └── Critical failure (structural / electrical / safety)?
                    │
                    YES → SCRAP immediately, escalate to process engineer
```

---

## Revision History

| Rev | Date | Change | Author |
|---|---|---|---|
| A | 2025-01-06 | Initial release for PT55 / PT66 / PT77 | Process Engineering |
