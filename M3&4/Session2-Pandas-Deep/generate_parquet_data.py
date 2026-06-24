"""
Session 2 — Data Generator
Generates multiple messy Parquet files simulating real manufacturing time series data.

Each file represents one dataset slice:
  - production_log.parquet      : main production records (12 000 rows)
  - inspection_log.parquet      : quality inspection records (8 000 rows)
  - material_batches.parquet    : material batch metadata  (500 rows)

"Messy" means:
  - random missing values scattered across key columns
  - mixed date formats (some rows store dates as strings, some already parsed)
  - numeric columns occasionally contain strings like "N/A" or "err"
  - duplicate rows (about 2% of each file)
  - inconsistent category labels  (e.g. "morning" vs "Morning" vs "AM")
  - outlier values that are technically valid numbers but physically impossible
  - time gaps and irregular timestamps to simulate real sensor data

Run:
    python generate_parquet_data.py
    python generate_parquet_data.py --rows 20000 --seed 99

Requirements:
    pip install pandas pyarrow numpy
"""

import argparse
import random
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Constants — mirrors the real ZF-inspired factory domain
# ---------------------------------------------------------------------------

MACHINES = ["M01", "M02", "M03", "M04", "M05", "M06"]
SHIFTS_CLEAN = ["Morning", "Evening", "Night"]
SHIFTS_DIRTY = ["Morning", "morning", "AM", "Evening", "EVENING", "Eve", "Night", "night", "PM", "N"]
OPERATORS = [f"OP{str(i).zfill(3)}" for i in range(1, 21)]
DEFECT_TYPES_CLEAN = ["Dimensional", "Surface", "Weld", "Assembly", "Missing Part", "Contamination"]
DEFECT_TYPES_DIRTY = [
    "Dimensional", "dimensional", "DIM", "Surface", "surface", "SURFACE",
    "Weld", "WELD", "weld", "Assembly", "assembly", "ASSY",
    "Missing Part", "missing part", "MISSING", "Contamination", "contamination", "CONT",
    "None", "none", "N/A",
]
MATERIAL_SUPPLIERS = ["SupplierA", "SupplierB", "SupplierC", "SupplierD"]
PRODUCT_CODES = ["PC-1100", "PC-1200", "PC-2100", "PC-3300", "PC-4400"]

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%Y-%m-%dT%H:%M:%S",
    "%m-%d-%Y %H:%M:%S",
]


def _random_timestamp(rng: np.random.Generator, start: pd.Timestamp, periods: int) -> pd.Timestamp:
    offset_seconds = rng.integers(0, periods * 60 * 60 * 8).item()
    return start + pd.Timedelta(seconds=offset_seconds)


def _corrupt_numeric(series: pd.Series, rng: np.random.Generator, frac: float = 0.025) -> pd.Series:
    """Replace a fraction of values with strings like 'N/A' or 'err', then store the whole column as str.
    This mirrors a real SCADA/ERP export where a numeric field occasionally contains an error string,
    forcing the entire column to be stored as text. PyArrow requires homogeneous column types."""
    series = series.astype(str)
    mask = rng.random(len(series)) < frac
    replacements = rng.choice(["N/A", "err", "#VALUE!", "", "null"], size=mask.sum())
    series = series.copy()
    series.iloc[mask] = replacements
    return series


def _corrupt_dates(series: pd.Series, rng: np.random.Generator, frac: float = 0.04) -> pd.Series:
    """Re-format a fraction of timestamps into different string formats."""
    series = series.copy().astype(str)
    indices = rng.choice(len(series), size=int(len(series) * frac), replace=False)
    for idx in indices:
        try:
            ts = pd.Timestamp(series.iloc[idx])
            fmt = rng.choice(DATE_FORMATS[1:])
            series.iloc[idx] = ts.strftime(fmt)
        except Exception:
            pass
    return series


def _inject_duplicates(df: pd.DataFrame, rng: np.random.Generator, frac: float = 0.02) -> pd.DataFrame:
    """Duplicate a random fraction of rows and append them at random positions."""
    n_dupes = max(1, int(len(df) * frac))
    dupe_indices = rng.choice(df.index, size=n_dupes, replace=False)
    dupes = df.loc[dupe_indices].copy()
    combined = pd.concat([df, dupes], ignore_index=True)
    return combined.sample(frac=1, random_state=rng.integers(0, 9999).item()).reset_index(drop=True)


def _inject_missing(df: pd.DataFrame, rng: np.random.Generator, columns: list, frac: float = 0.04):
    """Set a random fraction of values to NaN for the listed columns."""
    for col in columns:
        if col not in df.columns:
            continue
        mask = rng.random(len(df)) < frac
        df.loc[mask, col] = np.nan
    return df


# ---------------------------------------------------------------------------
# Table generators
# ---------------------------------------------------------------------------

def generate_production_log(n_rows: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Main production log — one row per production cycle.
    Intentionally messy: mixed date formats, dirty shift labels,
    numeric corruption, missing values, and ~2% duplicates.
    """
    start = pd.Timestamp("2025-01-01 06:00:00")
    timestamps = sorted([_random_timestamp(rng, start, n_rows // 3) for _ in range(n_rows)])

    machines = rng.choice(MACHINES, size=n_rows)
    shifts = rng.choice(SHIFTS_DIRTY, size=n_rows)
    operators = rng.choice(OPERATORS, size=n_rows)
    product_codes = rng.choice(PRODUCT_CODES, size=n_rows)

    units_produced = rng.integers(300, 650, size=n_rows).astype(float)
    defective_units = (units_produced * rng.uniform(0.01, 0.12, size=n_rows)).astype(int).astype(float)

    # Inject physically impossible outliers in ~0.5% of rows
    outlier_mask = rng.random(n_rows) < 0.005
    units_produced[outlier_mask] = rng.integers(5000, 99999, size=outlier_mask.sum()).astype(float)

    cycle_time_sec = rng.normal(loc=45, scale=8, size=n_rows).clip(5, 300)
    temperature_c = rng.normal(loc=72, scale=6, size=n_rows).clip(20, 200)
    pressure_bar = rng.normal(loc=8.5, scale=1.2, size=n_rows).clip(2, 30)

    df = pd.DataFrame({
        "batch_id": [f"B{str(i).zfill(5)}" for i in range(1, n_rows + 1)],
        "timestamp": [str(ts) for ts in timestamps],
        "machine_id": machines,
        "shift": shifts,
        "operator_id": operators,
        "product_code": product_codes,
        "units_produced": units_produced,
        "defective_units": defective_units,
        "cycle_time_sec": cycle_time_sec.round(2),
        "temperature_c": temperature_c.round(2),
        "pressure_bar": pressure_bar.round(3),
        "material_batch_id": [
            f"MB{str(rng.integers(1, 501).item()).zfill(4)}" for _ in range(n_rows)
        ],
    })

    # Corrupt numeric columns to include string garbage
    df["units_produced"] = _corrupt_numeric(df["units_produced"], rng, frac=0.02)
    df["defective_units"] = _corrupt_numeric(df["defective_units"], rng, frac=0.015)
    df["cycle_time_sec"] = _corrupt_numeric(df["cycle_time_sec"], rng, frac=0.01)

    # Corrupt some timestamps to mixed formats
    df["timestamp"] = _corrupt_dates(df["timestamp"], rng, frac=0.04)

    # Inject structural missing values
    df = _inject_missing(df, rng, ["operator_id", "temperature_c", "pressure_bar", "material_batch_id"], frac=0.05)

    # Inject duplicates last so they carry all the noise
    df = _inject_duplicates(df, rng, frac=0.02)

    return df


def generate_inspection_log(n_rows: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Quality inspection records — one row per inspection event.
    Linked to production_log via batch_id (many inspections per batch).
    Contains dirty defect type labels and some missing inspectors.
    """
    start = pd.Timestamp("2025-01-01 07:00:00")
    timestamps = sorted([_random_timestamp(rng, start, n_rows // 3) for _ in range(n_rows)])

    # Many inspections reference a batch that also appears in production log
    batch_pool = [f"B{str(i).zfill(5)}" for i in range(1, 12001)]
    batch_ids = rng.choice(batch_pool, size=n_rows)

    inspectors = [f"INS{str(rng.integers(1, 11).item()).zfill(2)}" for _ in range(n_rows)]
    defect_types = rng.choice(DEFECT_TYPES_DIRTY, size=n_rows)
    severity = rng.choice(["Low", "Medium", "High", "Critical", "low", "HIGH", "med", "MEDIUM"], size=n_rows)
    passed = pd.array(rng.choice(["True", "False", "1", "0", "yes", "no", "N/A"], size=n_rows), dtype="string")
    units_inspected = rng.integers(10, 150, size=n_rows).astype(float)
    units_rejected = (units_inspected * rng.uniform(0, 0.2, size=n_rows)).astype(int).astype(float)

    inspection_duration_min = rng.exponential(scale=12, size=n_rows).clip(1, 120).round(1)

    df = pd.DataFrame({
        "inspection_id": [f"INS{str(i).zfill(6)}" for i in range(1, n_rows + 1)],
        "timestamp": [str(ts) for ts in timestamps],
        "batch_id": batch_ids,
        "inspector_id": inspectors,
        "defect_type": defect_types,
        "severity": severity,
        "passed": passed,
        "units_inspected": units_inspected,
        "units_rejected": units_rejected,
        "inspection_duration_min": inspection_duration_min,
        "notes": rng.choice([
            "OK", "Check weld seam", "Re-inspect required", "Supplier fault suspected",
            "Machine drift detected", "", "", "operator error noted",
        ], size=n_rows),
    })

    df["timestamp"] = _corrupt_dates(df["timestamp"], rng, frac=0.05)
    df = _inject_missing(df, rng, ["inspector_id", "defect_type", "severity", "notes"], frac=0.06)
    df["units_rejected"] = _corrupt_numeric(df["units_rejected"], rng, frac=0.02)
    df = _inject_duplicates(df, rng, frac=0.02)

    return df


def generate_material_batches(n_rows: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Material batch reference table — one row per material batch.
    Linked to production_log via material_batch_id.
    Contains supplier info, material grade, and receipt date.
    """
    suppliers = rng.choice(MATERIAL_SUPPLIERS, size=n_rows, p=[0.4, 0.3, 0.2, 0.1])
    grades = rng.choice(["Grade-A", "Grade-B", "Grade-C", "grade-a", "GRADE-B", "B", "A", "C"], size=n_rows)
    receipt_dates = pd.date_range("2024-10-01", periods=n_rows, freq="2h")

    df = pd.DataFrame({
        "material_batch_id": [f"MB{str(i).zfill(4)}" for i in range(1, n_rows + 1)],
        "supplier": suppliers,
        "material_grade": grades,
        "receipt_date": receipt_dates.strftime("%Y-%m-%d"),
        "quantity_kg": rng.normal(loc=500, scale=80, size=n_rows).clip(50, 2000).round(1),
        "certificate_ok": pd.array(rng.choice([True, False, None], size=n_rows, p=[0.85, 0.10, 0.05]), dtype="boolean"),
    })

    df = _inject_missing(df, rng, ["supplier", "material_grade", "certificate_ok"], frac=0.04)
    df = _inject_duplicates(df, rng, frac=0.01)

    return df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate messy manufacturing Parquet files for Session 2.")
    parser.add_argument("--rows", type=int, default=12000, help="Base row count for production_log (default: 12000)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory (default: ./data)")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    configs = [
        ("production_log.parquet", generate_production_log, args.rows),
        ("inspection_log.parquet", generate_inspection_log, int(args.rows * 0.65)),
        ("material_batches.parquet", generate_material_batches, 500),
    ]

    for filename, generator_fn, n in configs:
        print(f"  Generating {filename} ({n:,} base rows)...", end="", flush=True)
        df = generator_fn(n, rng)
        path = output_dir / filename
        df.to_parquet(path, index=False, engine="pyarrow")
        print(f"  done → {len(df):,} rows  ({path.stat().st_size / 1024:.1f} KB)")

    print(f"\nAll files written to '{output_dir.resolve()}'")
    print("Run the Session 2 Jupyter notebook to explore them.")


if __name__ == "__main__":
    main()
