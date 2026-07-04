# Session 3 — SQL for Data Investigators
## Steering Wheel Manufacturing · DuckDB

Hands-on SQL querying of **8 Parquet files** that simulate a real steering wheel manufacturing process.  
You write SQL directly on Parquet data using DuckDB — no database server, no CSV imports.

---

## What to Expect

You will practice SQL in the context of a real factory problem: tracing a steering wheel unit through 6 manufacturing stations, finding scrap causes, validating process tolerances, and computing yield KPIs.

**By the end of this session you will be able to:**
- Query Parquet files directly from DuckDB without loading them into Pandas first
- Aggregate production data with `GROUP BY`, `HAVING`, and `CASE WHEN`
- Join multiple station tables on a shared `product_id` key
- Use window functions (`RANK`, `SUM OVER`, `LAG`) to rank and track trends
- Translate a written quality rule (SIC) into a SQL validation query

**The data is clean and realistic** — no missing values, no corruption. The focus is entirely on SQL, not data cleaning.

---

## Prerequisites

- **Python 3.10+** on your `PATH`
- Virtual environment activated (see root `README.md`)

---

## 1 — Install Dependencies

```bash
# from the project root
source .venv/bin/activate  # or: .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 2 — Generate the Parquet Data Files

Run the generator **from inside the `Session3-SQL-DuckDB/` folder** so the files land in the correct `data/` subdirectory:

```bash
cd M3\&4/Session3-SQL-DuckDB
python generate_steering_wheel_data.py
```

This creates 8 files in `data/`:

| File | Rows (default) | Description |
|------|----------------|-------------|
| `materials_stock.parquet` | ~20 | Raw material SKUs — reference table (type × supplier × grade) |
| `materials_log.parquet` | ~36k | Material consumption (OUT) per station + warehouse restocking (IN) |
| `station_molding.parquet` | ~10k | Mg skeleton injection — all products |
| `station_quality_check.parquet` | ~10k | Dimensional + surface inspection — all products |
| `station_foaming.parquet` | ~10k | Polyurethane foam injection — all products |
| `station_conductor.parquet` | ~6k | Heating wire install — PT66 + PT77 only |
| `station_laser.parquet` | ~3k | Laser grip activation — PT77 Premium only |
| `station_tapitat.parquet` | ~10k | Leather wrapping — all products |

### Optional flags

```bash
python generate_steering_wheel_data.py --rows 20000 --seed 99
python generate_steering_wheel_data.py --output-dir my_data
```

---

## 3 — Product Types and Routing

Each unit has a `product_type` that determines which stations it visits.  
All station tables share **`product_id`** as the join key.

| Code | Name | Route | ~Share |
|---|---|---|---|
| PT55 | Standard | Molding → QC → Foaming → Tapitat | 40% |
| PT66 | Sport | Molding → QC → Foaming → **Conductor** → Tapitat | 35% |
| PT77 | Premium | Molding → QC → Foaming → **Conductor** → **Laser** → Tapitat | 25% |

> PT55 rows are **absent** from `station_conductor` and `station_laser`.  
> PT66 rows are **absent** from `station_laser`.  
> This is intentional — not missing data.

---

## 4 — Where is the Pass / Fail Result?

Each station stores its verdict in a dedicated column. **The column name and value set differ per station** — this is by design to match real factory naming conventions.

| Station | Result column | OK value | Non-OK values |
|---|---|---|---|
| `station_molding` | `cycle_result` | `OK` | `REWORK`, `SCRAP` |
| `station_quality_check` | `overall_result` | `PASS` | `REWORK`, `SCRAP` |
| `station_foaming` | `foam_result` | `OK` | `UNDERFILL`, `OVERFILL`, `SCRAP` |
| `station_conductor` | `result` | `OK` | `REWORK`, `SCRAP` |
| `station_laser` | `result` | `OK` | `REWORK`, `SCRAP` |
| `station_tapitat` | `result` | `OK` | `REWORK`, `SCRAP` |

> **Foaming note:** `UNDERFILL` and `OVERFILL` are borderline failures (volume ±0.5 ml off target).  
> `SCRAP` is only triggered at ±1.5 ml — see `quality_standards_sic.md` for full tolerances.

> **Laser note:** the table also has an `outcome` column (`Priza_la_mana` / `FAIL`) which is the grip test result specifically — separate from the station-level `result`.

---

## 5 — Read the Quality Standards (SIC)

Open `quality_standards_sic.md` before running the notebook.  
It documents the process parameters and tolerances for each station.  
The SQL queries in Section 6 of the notebook validate these rules directly.

Key rules:
- Molding temperature: **180–220 °C**
- PT55 foam volume: **8.0 ml ± 0.5 ml**
- Conductor resistance: **< 2.5 Ω** → OK, 2.5–3.0 Ω → REWORK, > 3.0 Ω → SCRAP
- Laser power: **80–120 W**; grip test must return `Priza_la_mana`

---

## 6 — Launch the Notebook

```bash
jupyter notebook
```

Open `session3_sql_duckdb.ipynb`.

Each cell follows the pattern:

```
Business question (plain English)
       ↓
SQL query
       ↓
DataFrame result → your interpretation
```

### Notebook sections

| # | Section | SQL concepts covered |
|---|---|---|
| 1 | Schema exploration | `DESCRIBE`, `UNION ALL` |
| 2 | Single-table queries | `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY` |
| 3 | Aggregation + HAVING | `HAVING`, `CASE WHEN`, `ROUND`, `STDDEV` |
| 4 | Multi-table JOINs | `JOIN`, CTE (`WITH ... AS`) |
| 5 | Window functions | `RANK() OVER`, `SUM() OVER`, `LAG()` |
| 6 | Quality validation | SIC rule checks via `CASE WHEN` + `BETWEEN` |
| 7 | Challenge questions | Write your own SQL — no answers provided |

---

## Folder Structure

```
Session3-SQL-DuckDB/
├── data/
│   ├── materials_stock.parquet
│   ├── materials_log.parquet
│   ├── station_molding.parquet
│   ├── station_quality_check.parquet
│   ├── station_foaming.parquet
│   ├── station_conductor.parquet
│   ├── station_laser.parquet
│   └── station_tapitat.parquet
├── generate_steering_wheel_data.py   ← run this first
├── quality_standards_sic.md          ← process rules + tolerances per station
├── session3_sql_duckdb.ipynb         ← main notebook
└── README.md
```

---

## Troubleshooting

- **`FileNotFoundError`** — run `generate_steering_wheel_data.py` from inside this folder first.
- **`duckdb.CatalogException`** — the notebook kernel's working directory must be `Session3-SQL-DuckDB/`. Restart the kernel from that directory.
- **`ModuleNotFoundError: duckdb`** — activate your venv, then `pip install -r requirements.txt`.
