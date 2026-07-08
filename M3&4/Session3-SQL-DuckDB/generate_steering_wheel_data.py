"""
Session 3 — Steering Wheel Data Generator
Generates clean Parquet files simulating a real steering wheel manufacturing process.

Stations (one Parquet per station):
  materials_stock.parquet       : Raw material inventory reference   (~300 rows)
  materials_log.parquet         : Material consumption time series   (~15k rows)
  station_molding.parquet       : Skeleton molding — all products    (~10k rows)
  station_quality_check.parquet : Dimensional + surface inspection   (~10k rows)
  station_foaming.parquet       : Polyurethane foam injection        (~10k rows)
  station_conductor.parquet     : Heating conductor install          (~6k rows, PT66+PT77)
  station_laser.parquet         : Laser bombardment / grip           (~3k rows, PT77 only)
  station_tapitat.parquet       : Leather wrapping                   (~10k rows)

Product routing:
  PT55 Standard : Molding → QC → Foaming → Tapitat
  PT66 Sport    : Molding → QC → Foaming → Conductor → Tapitat
  PT77 Premium  : Molding → QC → Foaming → Conductor → Laser → Tapitat

Run:
    python generate_steering_wheel_data.py
    python generate_steering_wheel_data.py --rows 10000 --seed 42
    python generate_steering_wheel_data.py --rows 20000 --seed 99 --output-dir my_data

Requirements:
    pip install pandas pyarrow numpy
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# ---------------------------------------------------------------------------
# Metadata Spec
# ---------------------------------------------------------------------------
METADATA_SPEC = {
    "materials_stock": {
        "description": "Current raw materials stock, inventory levels, and reorder thresholds",
        "columns": {
            "material_id": "Unique identifier for the material SKU",
            "material_name": "Full descriptive name of the material",
            "material_type": "Broad category of the material",
            "grade": "Grade quality classification of the material (e.g. Grade-A, Grade-B, Standard)",
            "unit": "Unit of measurement for inventory quantities",
            "quantity_in_stock": "Current quantity of the material in stock",
            "reorder_threshold": "Stock level below which a reorder is triggered",
            "supplier": "Name of the supplier who provides this material",
            "last_updated": "Timestamp when the stock level was last updated",
        }
    },
    "materials_log": {
        "description": "Audit log of material transactions, tracking when materials were used and by which operator",
        "columns": {
            "log_id": "Unique identifier for the material log entry",
            "timestamp": "Timestamp of the material consumption/transaction",
            "material_type": "Type of material used (e.g. Mg_ingot, foam_polyurethane, leather, conductor_wire, adhesive, dye)",
            "batch_id": "Production batch identifier associated with this material log",
            "transaction_type": "Type of transaction (e.g. CONSUMED, WASTED)",
            "quantity_used": "Quantity of material used or wasted in this transaction",
            "unit": "Unit of measurement (e.g. kg, L, dm2, m)",
            "operator_id": "Identifier of the operator who handled the material",
            "station_id": "Station identifier where the material was consumed",
        }
    },
    "station_molding": {
        "description": "Molding station parameters for Mg (magnesium) skeleton injection molding",
        "columns": {
            "product_id": "Unique product identifier of the steering wheel",
            "batch_id": "Batch identifier of the steering wheel",
            "product_type": "Product model/type (PT55, PT66, PT77)",
            "timestamp": "Timestamp when the skeleton molding completed",
            "shift": "Working shift name (Morning, Evening, Night)",
            "operator_id": "Identifier of the molding station operator",
            "mold_tool_id": "Identifier of the mold tool used",
            "temperature_c": "Molding mold temperature in degrees Celsius",
            "humidity_pct": "Relative ambient humidity in percent",
            "pressure_bar": "Injection pressure in bar",
            "mg_quantity_kg": "Quantity of magnesium alloy used in kilograms",
            "duration_sec": "Molding cycle duration in seconds",
            "cycle_result": "Molding cycle status result (OK or REWORK)",
        }
    },
    "station_quality_check": {
        "description": "Quality control check parameters, measurements, and status for finished products",
        "columns": {
            "qc_id": "Unique identifier for the quality check inspection entry",
            "product_id": "Unique product identifier of the steering wheel",
            "batch_id": "Batch identifier of the steering wheel",
            "product_type": "Product model/type (PT55, PT66, PT77)",
            "timestamp": "Timestamp of the inspection check",
            "inspector_id": "Identifier of the quality inspector",
            "dimensional_check": "Dimensional inspection outcome (PASS or FAIL)",
            "surface_check": "Surface finish inspection outcome (PASS or FAIL)",
            "weight_g": "Measured weight of the molded skeleton in grams",
            "roundness_mm": "Roundness tolerance measurement deviation in millimeters",
            "overall_result": "Overall quality check inspection outcome (PASS or FAIL)",
            "notes": "Inspector's comments or notes",
        }
    },
    "station_foaming": {
        "description": "Polyurethane foaming parameters and results for steering wheel padding",
        "columns": {
            "product_id": "Unique product identifier of the steering wheel",
            "batch_id": "Batch identifier of the steering wheel",
            "product_type": "Product model/type (PT55, PT66, PT77)",
            "timestamp": "Timestamp when the foaming process completed",
            "operator_id": "Identifier of the foaming machine operator",
            "foam_volume_ml": "Volume of polyurethane foam injected in milliliters",
            "foam_density_gcm3": "Density of the foam in grams per cubic centimeter",
            "temperature_c": "Temperature of the foaming mold in degrees Celsius",
            "humidity_pct": "Relative ambient humidity in percent",
            "pressure_bar": "Injection pressure in bar",
            "cure_time_sec": "Curing duration inside the mold in seconds",
            "foam_result": "Foam injection result flag (e.g. OK, UNDERFILL, OVERFILL)",
        }
    },
    "station_conductor": {
        "description": "Conductor wire installation and electrical testing parameters",
        "columns": {
            "product_id": "Unique product identifier of the steering wheel",
            "batch_id": "Batch identifier of the steering wheel",
            "product_type": "Product model/type (PT55, PT66, PT77)",
            "timestamp": "Timestamp when the conductor installation completed",
            "operator_id": "Identifier of the operator at the conductor station",
            "wire_gauge_mm": "Diameter/gauge of the installation conductor wire in millimeters",
            "resistance_ohm": "Measured electrical resistance of the wire in ohms",
            "voltage_test_v": "Voltage applied during the electrical safety test in volts",
            "installation_duration_sec": "Duration of the wire installation process in seconds",
            "conductor_layout": "Conductor layout scheme (e.g. Single_Zone, Dual_Zone)",
            "result": "Result of the conductor station quality check (OK or REWORK)",
        }
    },
    "station_laser": {
        "description": "Laser engraving power parameters and grip conductivity checks",
        "columns": {
            "product_id": "Unique product identifier of the steering wheel",
            "batch_id": "Batch identifier of the steering wheel",
            "timestamp": "Timestamp when laser engraving completed",
            "operator_id": "Identifier of the laser station operator",
            "laser_power_w": "Laser beam power setting in watts",
            "burn_duration_sec": "Laser burning duration in seconds",
            "burning_pattern": "Engraving pattern (e.g. Geometric_Grip, Ergonomic_Wave, Sport_Cross)",
            "surface_temp_c": "Surface temperature after laser treatment in degrees Celsius",
            "grip_conductivity_test": "Conductivity verification status (PASS or FAIL)",
            "outcome": "Visual outcome of the grip surface (e.g. Priza_la_mana)",
            "result": "Laser station overall status result (OK or REWORK)",
        }
    },
    "station_tapitat": {
        "description": "Upholstery station parameters for leather wrapping, stitching, and adhesive",
        "columns": {
            "product_id": "Unique product identifier of the steering wheel",
            "batch_id": "Batch identifier of the steering wheel",
            "product_type": "Product model/type (PT55, PT66, PT77)",
            "timestamp": "Timestamp when the upholstery wrapping completed",
            "operator_id": "Identifier of the upholstery operator",
            "leather_type": "Type/quality of leather used (e.g. Standard, Premium, Sport)",
            "leather_quantity_dm2": "Amount of leather used in square decimeters",
            "stitching_pattern": "Stitching pattern applied (e.g. Classic, Double_Stitch, Sport_Diamond, Premium_Hand)",
            "adhesive_ml": "Volume of adhesive used in milliliters",
            "tapitat_duration_min": "Duration of the upholstering process in minutes",
            "result": "Upholstery station result status (OK or REWORK)",
        }
    }
}



# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PRODUCT_TYPES = ["PT55", "PT66", "PT77"]
PRODUCT_TYPE_WEIGHTS = [0.40, 0.35, 0.25]   # 40% standard, 35% sport, 25% premium

SHIFTS = ["Morning", "Evening", "Night"]

OPERATORS = [f"OP{str(i).zfill(3)}" for i in range(1, 21)]
INSPECTORS = [f"INS{str(i).zfill(2)}" for i in range(1, 9)]
MOLD_TOOLS = [f"MT{str(i).zfill(3)}" for i in range(1, 13)]

MATERIAL_SUPPLIERS = {
    "Mg_ingot":           ["MetalWorks RO", "AlphaAlloys DE", "SteelCore HU"],
    "foam_polyurethane":  ["FoamTech PL", "PolyFlex CZ"],
    "leather":            ["LeatherCraft IT", "PremiumHide PT", "SportTex DE"],
    "conductor_wire":     ["WirePro SK", "ElectraFlex RO"],
    "adhesive":           ["BondTech DE", "AdhesivePro HU"],
    "dye":                ["ColorFlex PL", "DyeWorks CZ"],
}

MATERIAL_UNITS = {
    "Mg_ingot": "kg",
    "foam_polyurethane": "kg",
    "leather": "dm2",
    "conductor_wire": "m",
    "adhesive": "kg",
    "dye": "L",
}

STITCHING_PATTERNS_PT55 = ["Classic", "Double_Stitch"]
STITCHING_PATTERNS_PT66 = ["Sport_Diamond", "Double_Stitch"]
STITCHING_PATTERN_PT77  = "Premium_Hand"

BURNING_PATTERNS = ["Geometric_Grip", "Ergonomic_Wave", "Sport_Cross"]
CONDUCTOR_LAYOUTS = ["Single_Zone", "Dual_Zone"]

BATCH_SIZE = 66   # from diagram: Setup Batch 66

# Foam volume targets by product type (ml of polyurethane)
FOAM_TARGETS = {"PT55": 8.0, "PT66": 10.0, "PT77": 12.0}

# Weight targets by product type (grams)
WEIGHT_TARGETS = {"PT55": 380, "PT66": 420, "PT77": 460}

PRODUCTION_START = pd.Timestamp("2025-01-06 06:00:00")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assign_shifts(timestamps: pd.DatetimeIndex) -> list:
    """Assign shift label based on hour of day."""
    def _shift(ts):
        h = ts.hour
        if 6 <= h < 14:
            return "Morning"
        elif 14 <= h < 22:
            return "Evening"
        else:
            return "Night"
    return [_shift(ts) for ts in timestamps]


def _batch_ids_for(n: int) -> list:
    """Assign sequential batch IDs using the factory batch size of 66."""
    return [f"BATCH{str((i // BATCH_SIZE) + 1).zfill(4)}" for i in range(n)]


# ---------------------------------------------------------------------------
# Product pool — shared across all station tables
# ---------------------------------------------------------------------------

def generate_product_pool(n_products: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Master list of product_ids.
    Every station table joins back to this via product_id.
    """
    product_types = rng.choice(PRODUCT_TYPES, size=n_products, p=PRODUCT_TYPE_WEIGHTS)
    return pd.DataFrame({
        "product_id":   [f"PID{str(i).zfill(6)}" for i in range(1, n_products + 1)],
        "product_type": product_types,
        "batch_id":     _batch_ids_for(n_products),
    })


# ---------------------------------------------------------------------------
# Materials tables
# ---------------------------------------------------------------------------

def generate_materials_stock(rng: np.random.Generator) -> pd.DataFrame:
    """
    Reference snapshot of raw material inventory.
    One row per material SKU (type × supplier × grade combination).
    """
    records = []
    mat_id = 1

    for mat_type, suppliers in MATERIAL_SUPPLIERS.items():
        grades = ["Grade-A", "Grade-B"] if mat_type in ("Mg_ingot", "leather") else ["Standard"]
        unit = MATERIAL_UNITS[mat_type]

        for supplier in suppliers:
            for grade in grades:
                qty = round(float(rng.uniform(300, 5000)), 1)
                reorder = round(qty * float(rng.uniform(0.10, 0.20)), 1)
                last_updated = PRODUCTION_START - pd.Timedelta(days=int(rng.integers(1, 14)))

                records.append({
                    "material_id":        f"MAT{str(mat_id).zfill(4)}",
                    "material_name":      f"{mat_type.replace('_', ' ').title()} {grade} — {supplier}",
                    "material_type":      mat_type,
                    "grade":              grade,
                    "unit":               unit,
                    "quantity_in_stock":  qty,
                    "reorder_threshold":  reorder,
                    "supplier":           supplier,
                    "last_updated":       last_updated,
                })
                mat_id += 1

    return pd.DataFrame(records)


def generate_materials_log(
    molding:   pd.DataFrame,
    foaming:   pd.DataFrame,
    conductor: pd.DataFrame,
    tapitat:   pd.DataFrame,
    rng:       np.random.Generator,
) -> pd.DataFrame:
    """
    Time-series material consumption log.
    OUT rows are derived from each station's activity.
    IN rows simulate periodic warehouse restocking.
    """
    n_mol  = len(molding)
    n_foam = len(foaming)
    n_cond = len(conductor)
    n_tap  = len(tapitat)

    log_counter = [1]  # mutable counter shared across frames

    def _ids(n):
        start = log_counter[0]
        log_counter[0] += n
        return [f"LOG{str(i).zfill(7)}" for i in range(start, start + n)]

    # Mg ingot consumption from molding
    df_mol = pd.DataFrame({
        "log_id":          _ids(n_mol),
        "timestamp":       molding["timestamp"].values,
        "material_type":   "Mg_ingot",
        "batch_id":        molding["batch_id"].values,
        "transaction_type":"OUT",
        "quantity_used":   molding["mg_quantity_kg"].values.round(4),
        "unit":            "kg",
        "operator_id":     molding["operator_id"].values,
        "station_id":      "MOLDING",
    })

    # Polyurethane foam consumption
    df_foam = pd.DataFrame({
        "log_id":          _ids(n_foam),
        "timestamp":       foaming["timestamp"].values,
        "material_type":   "foam_polyurethane",
        "batch_id":        foaming["batch_id"].values,
        "transaction_type":"OUT",
        "quantity_used":   (foaming["foam_volume_ml"].values / 1000).round(6),
        "unit":            "kg",
        "operator_id":     foaming["operator_id"].values,
        "station_id":      "FOAMING",
    })

    # Conductor wire consumption
    df_cond = pd.DataFrame({
        "log_id":          _ids(n_cond),
        "timestamp":       conductor["timestamp"].values,
        "material_type":   "conductor_wire",
        "batch_id":        conductor["batch_id"].values,
        "transaction_type":"OUT",
        "quantity_used":   (conductor["wire_gauge_mm"].values * 2.5).round(3),
        "unit":            "m",
        "operator_id":     conductor["operator_id"].values,
        "station_id":      "CONDUCTOR",
    })

    # Leather consumption
    df_tap = pd.DataFrame({
        "log_id":          _ids(n_tap),
        "timestamp":       tapitat["timestamp"].values,
        "material_type":   "leather",
        "batch_id":        tapitat["batch_id"].values,
        "transaction_type":"OUT",
        "quantity_used":   tapitat["leather_quantity_dm2"].values,
        "unit":            "dm2",
        "operator_id":     tapitat["operator_id"].values,
        "station_id":      "TAPITAT",
    })

    # Periodic IN receipts (warehouse restocking)
    receipt_rows = []
    for mat_type in MATERIAL_SUPPLIERS:
        unit = MATERIAL_UNITS[mat_type]
        n_receipts = int(rng.integers(15, 30))
        for _ in range(n_receipts):
            receipt_ts = PRODUCTION_START + pd.Timedelta(days=int(rng.integers(0, 90)))
            receipt_rows.append({
                "log_id":          f"LOG{str(log_counter[0]).zfill(7)}",
                "timestamp":       receipt_ts,
                "material_type":   mat_type,
                "batch_id":        f"RECV{str(log_counter[0]).zfill(5)}",
                "transaction_type":"IN",
                "quantity_used":   round(float(rng.uniform(300, 2000)), 1),
                "unit":            unit,
                "operator_id":     str(rng.choice(OPERATORS)),
                "station_id":      "WAREHOUSE",
            })
            log_counter[0] += 1

    df_recv = pd.DataFrame(receipt_rows)

    df = pd.concat([df_mol, df_foam, df_cond, df_tap, df_recv], ignore_index=True)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Station generators
# ---------------------------------------------------------------------------

def generate_station_molding(pool: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Skeleton molding — all products.
    Input: Mg ingots. Key params: temperature, pressure, humidity, cycle time.
    Pass window: temperature 180–220 °C, pressure 6–12 bar.
    """
    n = len(pool)
    timestamps = pd.date_range(PRODUCTION_START, periods=n, freq="3min") + \
                 pd.to_timedelta(rng.integers(0, 120, size=n), unit="s")
    shifts = _assign_shifts(timestamps)

    # PT77 premium runs slightly hotter for better alloy flow
    temp_target = np.where(pool["product_type"].values == "PT77", 205.0, 195.0)
    temperature_c = (rng.normal(0, 6, n) + temp_target).clip(155, 255).round(2)
    pressure_bar  = rng.normal(8.5, 0.9, n).clip(3.5, 15.0).round(3)
    humidity_pct  = rng.normal(52, 7, n).clip(28, 82).round(1)
    mg_qty_kg     = rng.normal(0.500, 0.022, n).clip(0.410, 0.590).round(4)
    duration_sec  = rng.normal(55, 8, n).clip(18, 125).round(1)

    temp_ok     = (temperature_c >= 180) & (temperature_c <= 220)
    pressure_ok = (pressure_bar  >= 6.0) & (pressure_bar  <= 12.0)
    rand        = rng.random(n)
    cycle_result = np.where(
        temp_ok & pressure_ok & (rand > 0.06),
        "OK",
        np.where(rand > 0.02, "REWORK", "SCRAP"),
    )

    return pd.DataFrame({
        "product_id":    pool["product_id"].values,
        "batch_id":      pool["batch_id"].values,
        "product_type":  pool["product_type"].values,
        "timestamp":     timestamps,
        "shift":         shifts,
        "operator_id":   rng.choice(OPERATORS, size=n),
        "mold_tool_id":  rng.choice(MOLD_TOOLS, size=n),
        "temperature_c": temperature_c,
        "humidity_pct":  humidity_pct,
        "pressure_bar":  pressure_bar,
        "mg_quantity_kg":mg_qty_kg,
        "duration_sec":  duration_sec,
        "cycle_result":  cycle_result,
    })


def generate_station_quality_check(pool: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Dimensional + surface inspection — all products.
    Checks: weight, roundness deviation, dimensional tolerance, surface appearance.
    """
    n = len(pool)
    timestamps = pd.date_range(PRODUCTION_START + pd.Timedelta(minutes=1), periods=n, freq="3min") + \
                 pd.to_timedelta(rng.integers(0, 60, size=n), unit="s")

    weight_target = np.array([WEIGHT_TARGETS[pt] for pt in pool["product_type"].values])
    weight_g       = (rng.normal(0, 9, n) + weight_target).clip(315, 525).round(1)
    roundness_mm   = rng.normal(0.14, 0.09, n).clip(0.01, 0.85).round(3)
    dimensional_ok = rng.random(n) > 0.05
    surface_ok     = rng.random(n) > 0.06

    dimensional_check = np.where(dimensional_ok, "PASS", "FAIL")
    surface_check     = np.where(surface_ok, "PASS", "FAIL")

    all_ok = dimensional_ok & surface_ok & (roundness_mm < 0.50)
    rand   = rng.random(n)
    overall_result = np.where(
        all_ok, "PASS",
        np.where(rand > 0.30, "REWORK", "SCRAP"),
    )

    notes_pool = [
        "All OK", "Minor surface scratch", "Dimensional borderline",
        "Weight within spec", "Re-check roundness", "", "OK — proceed",
        "Tool wear suspected", "Operator flag — manual re-measure",
        "Slight flash on rim", "Surface finish marginal",
    ]

    return pd.DataFrame({
        "qc_id":            [f"QC{str(i).zfill(7)}" for i in range(1, n + 1)],
        "product_id":       pool["product_id"].values,
        "batch_id":         pool["batch_id"].values,
        "product_type":     pool["product_type"].values,
        "timestamp":        timestamps,
        "inspector_id":     rng.choice(INSPECTORS, size=n),
        "dimensional_check":dimensional_check,
        "surface_check":    surface_check,
        "weight_g":         weight_g,
        "roundness_mm":     roundness_mm,
        "overall_result":   overall_result,
        "notes":            rng.choice(notes_pool, size=n),
    })


def generate_station_foaming(pool: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Polyurethane foam injection — all products.
    Volume target: PT55=8 ml, PT66=10 ml, PT77=12 ml (±0.5 ml tolerance).
    """
    n = len(pool)
    timestamps = pd.date_range(PRODUCTION_START + pd.Timedelta(minutes=2), periods=n, freq="3min") + \
                 pd.to_timedelta(rng.integers(0, 90, size=n), unit="s")

    foam_target    = np.array([FOAM_TARGETS[pt] for pt in pool["product_type"].values])
    foam_volume_ml = (rng.normal(0, 0.38, n) + foam_target).round(2)
    foam_density   = rng.normal(1.05, 0.03, n).clip(0.88, 1.22).round(4)
    temperature_c  = rng.normal(25.0, 1.6, n).clip(17.0, 33.0).round(2)
    humidity_pct   = rng.normal(48, 6, n).clip(22, 76).round(1)
    pressure_bar   = rng.normal(6.5, 0.55, n).clip(3.5, 11.0).round(3)
    cure_time_sec  = rng.normal(210, 16, n).clip(145, 305).round(1)

    underfill = foam_volume_ml < (foam_target - 0.5)
    overfill  = foam_volume_ml > (foam_target + 0.5)
    severe    = (foam_volume_ml < (foam_target - 1.5)) | (foam_volume_ml > (foam_target + 1.5))

    foam_result = np.where(
        severe, "SCRAP",
        np.where(underfill, "UNDERFILL",
                 np.where(overfill, "OVERFILL", "OK")),
    )

    return pd.DataFrame({
        "product_id":       pool["product_id"].values,
        "batch_id":         pool["batch_id"].values,
        "product_type":     pool["product_type"].values,
        "timestamp":        timestamps,
        "operator_id":      rng.choice(OPERATORS, size=n),
        "foam_volume_ml":   foam_volume_ml,
        "foam_density_gcm3":foam_density,
        "temperature_c":    temperature_c,
        "humidity_pct":     humidity_pct,
        "pressure_bar":     pressure_bar,
        "cure_time_sec":    cure_time_sec,
        "foam_result":      foam_result,
    })


def generate_station_conductor(pool: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Heating conductor installation — PT66 and PT77 only.
    Spec: resistance < 2.5 Ω → OK; 2.5–3.0 Ω → REWORK; > 3.0 Ω → SCRAP.
    """
    sub = pool[pool["product_type"].isin(["PT66", "PT77"])].reset_index(drop=True)
    n = len(sub)
    timestamps = pd.date_range(PRODUCTION_START + pd.Timedelta(minutes=3), periods=n, freq="5min") + \
                 pd.to_timedelta(rng.integers(0, 120, size=n), unit="s")

    # PT77 uses thicker wire (0.75 mm vs 0.50 mm for PT66)
    wire_gauge_mm     = np.where(sub["product_type"].values == "PT77", 0.75, 0.50)
    resistance_ohm    = rng.normal(1.80, 0.38, n).clip(0.40, 5.50).round(3)
    voltage_test_v    = rng.normal(12.0, 0.28, n).clip(10.0, 14.0).round(2)
    install_dur_sec   = rng.normal(210, 32, n).clip(85, 380).round(1)
    conductor_layout  = np.where(
        sub["product_type"].values == "PT77",
        rng.choice(CONDUCTOR_LAYOUTS, size=n),
        "Single_Zone",
    )

    result = np.where(
        resistance_ohm < 2.5, "OK",
        np.where(resistance_ohm < 3.0, "REWORK", "SCRAP"),
    )

    return pd.DataFrame({
        "product_id":              sub["product_id"].values,
        "batch_id":                sub["batch_id"].values,
        "product_type":            sub["product_type"].values,
        "timestamp":               timestamps,
        "operator_id":             rng.choice(OPERATORS, size=n),
        "wire_gauge_mm":           wire_gauge_mm,
        "resistance_ohm":          resistance_ohm,
        "voltage_test_v":          voltage_test_v,
        "installation_duration_sec":install_dur_sec,
        "conductor_layout":        conductor_layout,
        "result":                  result,
    })


def generate_station_laser(pool: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Laser bombardment / grip activation — PT77 Premium only.
    Creates the tactile grip surface (Priză la mână).
    Spec: laser power 80–120 W; grip conductivity test PASS required.
    """
    sub = pool[pool["product_type"] == "PT77"].reset_index(drop=True)
    n = len(sub)
    timestamps = pd.date_range(PRODUCTION_START + pd.Timedelta(minutes=5), periods=n, freq="10min") + \
                 pd.to_timedelta(rng.integers(0, 180, size=n), unit="s")

    laser_power_w    = rng.normal(100, 8, n).clip(65, 140).round(1)
    burn_duration_sec= rng.normal(9.0, 1.6, n).clip(3.5, 22.0).round(1)
    surface_temp_c   = rng.normal(55, 4, n).clip(36, 82).round(1)
    burning_pattern  = rng.choice(BURNING_PATTERNS, size=n)

    grip_pass              = rng.random(n) > 0.07
    grip_conductivity_test = np.where(grip_pass, "PASS", "FAIL")
    outcome                = np.where(grip_pass, "Priza_la_mana", "FAIL")

    power_ok = (laser_power_w >= 80) & (laser_power_w <= 120)
    rand     = rng.random(n)
    result   = np.where(
        grip_pass & power_ok, "OK",
        np.where(rand > 0.40, "REWORK", "SCRAP"),
    )

    return pd.DataFrame({
        "product_id":           sub["product_id"].values,
        "batch_id":             sub["batch_id"].values,
        "timestamp":            timestamps,
        "operator_id":          rng.choice(OPERATORS, size=n),
        "laser_power_w":        laser_power_w,
        "burn_duration_sec":    burn_duration_sec,
        "burning_pattern":      burning_pattern,
        "surface_temp_c":       surface_temp_c,
        "grip_conductivity_test":grip_conductivity_test,
        "outcome":              outcome,
        "result":               result,
    })


def generate_station_tapitat(pool: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Leather wrapping — all products.
    Leather grade and stitching pattern differ per product type.
    """
    n = len(pool)
    timestamps = pd.date_range(PRODUCTION_START + pd.Timedelta(minutes=4), periods=n, freq="4min") + \
                 pd.to_timedelta(rng.integers(0, 120, size=n), unit="s")

    pt77_mask = pool["product_type"].values == "PT77"
    pt66_mask = pool["product_type"].values == "PT66"

    leather_type = np.where(pt77_mask, "Premium",
                            np.where(pt66_mask, "Sport", "Standard"))

    # Leather area: premium > sport > standard
    base_area = np.where(pt77_mask, 3.20, np.where(pt66_mask, 2.90, 2.60))
    leather_qty_dm2 = (rng.normal(0, 0.16, n) + base_area).clip(1.90, 4.60).round(2)

    stitching_pattern = np.where(
        pt77_mask,
        STITCHING_PATTERN_PT77,
        np.where(
            pt66_mask,
            rng.choice(STITCHING_PATTERNS_PT66, size=n),
            rng.choice(STITCHING_PATTERNS_PT55, size=n),
        ),
    )

    adhesive_ml    = rng.normal(20, 2.6, n).clip(9, 36).round(1)
    duration_min   = rng.normal(32, 5, n).clip(14, 62).round(1)
    rand           = rng.random(n)
    result         = np.where(rand > 0.07, "OK", np.where(rand > 0.02, "REWORK", "SCRAP"))

    return pd.DataFrame({
        "product_id":          pool["product_id"].values,
        "batch_id":            pool["batch_id"].values,
        "product_type":        pool["product_type"].values,
        "timestamp":           timestamps,
        "operator_id":         rng.choice(OPERATORS, size=n),
        "leather_type":        leather_type,
        "leather_quantity_dm2":leather_qty_dm2,
        "stitching_pattern":   stitching_pattern,
        "adhesive_ml":         adhesive_ml,
        "tapitat_duration_min":duration_min,
        "result":              result,
    })


def save_parquet_with_metadata(df: pd.DataFrame, path: Path, table_name: str):
    """Convert DataFrame to PyArrow Table, attach metadata to schema and fields, and write."""
    # Convert to Arrow Table
    table = pa.Table.from_pandas(df, preserve_index=False)
    
    # Get metadata for table and columns
    spec = METADATA_SPEC.get(table_name, {})
    table_desc = spec.get("description", "")
    col_specs = spec.get("columns", {})
    
    # Update schema-level metadata
    existing_meta = table.schema.metadata or {}
    new_meta = {**existing_meta}
    if table_desc:
        new_meta[b"description"] = table_desc.encode("utf-8")
        
    # Update column-level metadata
    new_fields = []
    for field in table.schema:
        col_desc = col_specs.get(field.name)
        if col_desc:
            field_meta = {b"description": col_desc.encode("utf-8")}
            if field.metadata:
                field_meta.update(field.metadata)
            new_fields.append(field.with_metadata(field_meta))
        else:
            new_fields.append(field)
            
    # Apply schema and write
    new_schema = pa.schema(new_fields, metadata=new_meta)
    table = table.cast(new_schema)
    pq.write_table(table, path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate steering wheel manufacturing Parquet files for Session 3."
    )
    parser.add_argument("--rows",       type=int, default=10000,
                        help="Number of products / molding rows (default: 10000)")
    parser.add_argument("--seed",       type=int, default=42,
                        help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--output-dir", type=str, default="data",
                        help="Output directory (default: ./data)")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating steering wheel data — {args.rows:,} products, seed={args.seed}\n")

    # 1. Product pool
    pool = generate_product_pool(args.rows, rng)
    type_counts = pool["product_type"].value_counts().to_dict()
    print(f"  Product mix: {type_counts}")

    # 2. Station tables
    print("\n  Building station tables...")
    molding   = generate_station_molding(pool, rng)
    qc        = generate_station_quality_check(pool, rng)
    foaming   = generate_station_foaming(pool, rng)
    conductor = generate_station_conductor(pool, rng)
    laser     = generate_station_laser(pool, rng)
    tapitat   = generate_station_tapitat(pool, rng)

    # 3. Material tables
    print("  Building material tables...")
    stock   = generate_materials_stock(rng)
    mat_log = generate_materials_log(molding, foaming, conductor, tapitat, rng)

    # 4. Write Parquet files
    configs = [
        ("materials_stock.parquet",       stock),
        ("materials_log.parquet",         mat_log),
        ("station_molding.parquet",       molding),
        ("station_quality_check.parquet", qc),
        ("station_foaming.parquet",       foaming),
        ("station_conductor.parquet",     conductor),
        ("station_laser.parquet",         laser),
        ("station_tapitat.parquet",       tapitat),
    ]

    print()
    for filename, df in configs:
        path = output_dir / filename
        table_name = filename.replace(".parquet", "")
        save_parquet_with_metadata(df, path, table_name)
        print(f"  {filename:<40} → {len(df):>7,} rows  ({path.stat().st_size / 1024:.1f} KB)")

    print(f"\nAll files written to '{output_dir.resolve()}'")
    print("Run the Session 3 Jupyter notebook to start querying with DuckDB.")


if __name__ == "__main__":
    main()
