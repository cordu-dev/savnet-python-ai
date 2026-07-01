"""
Session 4 — Shared data helpers
================================

This module is the "data layer" for the whole session. Every script and the
notebook import from here so we write the loading + KPI logic ONCE and reuse it.

Why a separate file?
    A clean Streamlit app has three layers:
        1. DATA      -> load + shape the data          (this file)
        2. PROCESS   -> compute KPIs / aggregations     (this file)
        3. DISPLAY   -> draw widgets and charts         (the 0X_*.py scripts)
    Keeping the data layer separate means the display code stays short and
    readable, and you can test the numbers without opening a browser.

The data itself lives in Session 3 (single source of truth). We reference it
with a relative path instead of copying the files.
"""

from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Where is the data?
# ---------------------------------------------------------------------------
# __file__ is the path to THIS file. .parent walks up one folder at a time.
#   this file      -> .../Session4-Visualization-Streamlit/data_utils.py
#   .parent        -> .../Session4-Visualization-Streamlit/
#   .parent.parent -> .../M3&4/
# From M3&4 we can hop into the Session 3 data folder. This works no matter
# what directory you launch `streamlit run` from.
DATA_DIR = Path(__file__).parent.parent / "Session3-SQL-DuckDB" / "data"

# The six production stations, in the order a wheel moves through the factory.
# Not every product visits every station (see the routing dict below).
STATIONS = ["molding", "quality_check", "foaming", "conductor", "laser", "tapitat"]

# Which stations each product type actually passes through.
# PT55 Standard skips the conductor + laser; PT66 Sport skips only the laser.
PRODUCT_ROUTES = {
    "PT55": ["molding", "quality_check", "foaming", "tapitat"],
    "PT66": ["molding", "quality_check", "foaming", "conductor", "tapitat"],
    "PT77": ["molding", "quality_check", "foaming", "conductor", "laser", "tapitat"],
}

# The column that holds the pass/fail verdict is named differently per table.
RESULT_COLUMNS = {
    "molding": "cycle_result",
    "quality_check": "overall_result",
    "foaming": "foam_result",
    "conductor": "result",
    "laser": "result",
    "tapitat": "result",
}

# Foam volume targets from the SIC (ml of polyurethane). Used for spec checks.
FOAM_TARGETS = {"PT55": 8.0, "PT66": 10.0, "PT77": 12.0}

# Values that count as "good on the first try" for First Pass Yield.
PASS_VALUES = {"OK", "PASS", "Priza_la_mana"}


# ---------------------------------------------------------------------------
# 2. Loading helpers
# ---------------------------------------------------------------------------
def load_station(name: str) -> pd.DataFrame:
    """Read one station's Parquet file into a DataFrame.

    Example: load_station("molding") -> reads station_molding.parquet
    """
    path = DATA_DIR / f"station_{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path.name}. Run generate_steering_wheel_data.py in "
            f"Session3-SQL-DuckDB first."
        )
    return pd.read_parquet(path)


def load_all() -> dict[str, pd.DataFrame]:
    """Load every station table into a dict keyed by station name.

    Returns something like {"molding": df, "quality_check": df, ...}.
    A dict is handy because we can loop over stations by name.
    """
    return {name: load_station(name) for name in STATIONS}


def load_materials_log() -> pd.DataFrame:
    """Material consumption + restock time-series (used for waste KPIs)."""
    return pd.read_parquet(DATA_DIR / "materials_log.parquet")


# ---------------------------------------------------------------------------
# 3. Small shaping helpers (reusable building blocks)
# ---------------------------------------------------------------------------
def add_is_scrap(df: pd.DataFrame, result_col: str) -> pd.DataFrame:
    """Add a boolean `is_scrap` column so we can average it into a rate.

    Trick: the mean of a boolean column IS the proportion of True values.
    So df["is_scrap"].mean() == the scrap RATE. We use this everywhere.
    """
    df = df.copy()  # copy so we never mutate the caller's DataFrame
    df["is_scrap"] = df[result_col] == "SCRAP"
    return df


def scrap_rate_by(df: pd.DataFrame, group_col: str, result_col: str) -> pd.DataFrame:
    """Scrap rate (%) grouped by any column (shift, operator, product_type...).

    Returns a tidy DataFrame with the group column + a `scrap_rate_pct` column,
    ready to hand straight to Seaborn.
    """
    df = add_is_scrap(df, result_col)
    out = (
        df.groupby(group_col)["is_scrap"]
        .mean()                       # proportion scrapped per group
        .mul(100)                     # -> percentage
        .round(2)
        .reset_index(name="scrap_rate_pct")
    )
    return out


def scrap_rate_by_station(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Overall scrap rate (%) for each station, as one tidy table.

    Loops over every station table, computes its scrap rate, and stacks the
    results. Answers: "which station bleeds the most scrap?"
    """
    rows = []
    for name, df in frames.items():
        result_col = RESULT_COLUMNS[name]
        rate = (df[result_col] == "SCRAP").mean() * 100
        rows.append({"station": name, "scrap_rate_pct": round(rate, 2)})
    return pd.DataFrame(rows).sort_values("scrap_rate_pct", ascending=False)


def weekly_scrap_trend(df: pd.DataFrame, result_col: str) -> pd.DataFrame:
    """Scrap rate (%) per calendar week — answers "is quality drifting?".

    `resample("W")` groups rows into weekly buckets using the timestamp index.
    """
    df = add_is_scrap(df, result_col)
    df = df.set_index("timestamp")
    trend = (
        df["is_scrap"]
        .resample("W")           # one bucket per week
        .mean()
        .mul(100)
        .round(2)
        .reset_index(name="scrap_rate_pct")
    )
    return trend


# ---------------------------------------------------------------------------
# 4. Filtering (shared by the interactive scripts)
# ---------------------------------------------------------------------------
def apply_filters(
    df: pd.DataFrame,
    product_types: list[str] | None = None,
    shifts: list[str] | None = None,
) -> pd.DataFrame:
    """Keep only rows matching the chosen product types and/or shifts.

    `None` (or empty list) means "no filter on this dimension". Some station
    tables (e.g. foaming) have no `shift` column, so we check first.
    """
    out = df
    if product_types and "product_type" in out.columns:
        out = out[out["product_type"].isin(product_types)]
    if shifts and "shift" in out.columns:
        out = out[out["shift"].isin(shifts)]
    return out


# ---------------------------------------------------------------------------
# 5. The three "headline" KPIs for the final dashboard
# ---------------------------------------------------------------------------
def first_pass_yield(
    frames: dict[str, pd.DataFrame],
    product_types: list[str] | None = None,
) -> float:
    """First Pass Yield (%) — the gold-standard quality KPI.

    Definition: the share of individual wheels (product_id) that passed EVERY
    station on their route on the first try (no REWORK / SCRAP / UNDERFILL...).

    How we compute it:
        1. For each station table, mark each product_id as good/not-good.
        2. A product is "first pass" only if it is good at ALL of the stations
           on its own product-type route.
    Because routes differ per product type, we evaluate one type at a time.
    """
    types = product_types or list(PRODUCT_ROUTES.keys())
    good_ids: set[str] = set()
    total_ids = 0

    for ptype in types:
        route = PRODUCT_ROUTES[ptype]
        # Start with the set of all product_ids of this type (from molding).
        molding = frames["molding"]
        ids_of_type = set(molding.loc[molding["product_type"] == ptype, "product_id"])
        total_ids += len(ids_of_type)

        # Intersect down: keep only ids that were "good" at every route station.
        passing = ids_of_type
        for station in route:
            df = frames[station]
            result_col = RESULT_COLUMNS[station]
            good_here = set(df.loc[df[result_col].isin(PASS_VALUES), "product_id"])
            passing = passing & good_here  # set intersection

        good_ids |= passing

    if total_ids == 0:
        return 0.0
    return round(len(good_ids) / total_ids * 100, 2)


def out_of_spec_rate(
    frames: dict[str, pd.DataFrame],
    product_types: list[str] | None = None,
) -> float:
    """Out-of-Spec Rate (%) — process parameters that breach SIC tolerances.

    This is DIFFERENT from the scrap rate: a reading can be out of spec even if
    the operator still logged the unit as OK. We check three SIC rules:
        - Molding temperature must stay within 180-220 C.
        - Foam volume must stay within target +/- 0.5 ml (target per type).
        - Conductor resistance must stay below 2.5 Ohm.
    We count how many checked readings breach their rule, across all three.
    """
    breaches = 0
    checks = 0

    # --- Molding temperature ---
    mol = apply_filters(frames["molding"], product_types)
    temp_bad = (mol["temperature_c"] < 180) | (mol["temperature_c"] > 220)
    breaches += int(temp_bad.sum())
    checks += len(mol)

    # --- Foam volume vs per-type target ---
    foam = apply_filters(frames["foaming"], product_types)
    target = foam["product_type"].map(FOAM_TARGETS)
    foam_bad = (foam["foam_volume_ml"] - target).abs() > 0.5
    breaches += int(foam_bad.sum())
    checks += len(foam)

    # --- Conductor resistance (only PT66/PT77 exist in this table) ---
    cond = apply_filters(frames["conductor"], product_types)
    res_bad = cond["resistance_ohm"] >= 2.5
    breaches += int(res_bad.sum())
    checks += len(cond)

    if checks == 0:
        return 0.0
    return round(breaches / checks * 100, 2)


def daily_throughput(
    molding: pd.DataFrame,
    product_types: list[str] | None = None,
    shifts: list[str] | None = None,
) -> pd.DataFrame:
    """Units produced per calendar day (capacity KPI).

    Returns a tidy DataFrame with `date` + `units` columns. Callers can take
    the mean of `units` for the headline number, or plot it as a trend line.
    We count molding rows because every wheel starts at the molding station.
    """
    df = apply_filters(molding, product_types, shifts)
    per_day = (
        df.set_index("timestamp")
        .resample("D")                       # one bucket per day
        .size()                              # count rows in each day
        .reset_index(name="units")
    )
    per_day = per_day.rename(columns={"timestamp": "date"})
    return per_day


# ---------------------------------------------------------------------------
# 6. Manual smoke test — run this file directly to sanity-check the data layer
#     python data_utils.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    frames = load_all()
    print("Loaded station tables:")
    for name, df in frames.items():
        print(f"  {name:<14} {len(df):>7,} rows")

    print(f"\nFirst Pass Yield : {first_pass_yield(frames)} %")
    print(f"Out-of-Spec Rate : {out_of_spec_rate(frames)} %")
    tp = daily_throughput(frames['molding'])
    print(f"Daily Throughput : {tp['units'].mean():.0f} units/day (avg)")
    print("\nScrap rate by station:")
    print(scrap_rate_by_station(frames).to_string(index=False))
