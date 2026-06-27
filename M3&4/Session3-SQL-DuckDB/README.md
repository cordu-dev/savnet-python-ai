# Session 3 — SQL for Data Investigators
## Steering Wheel Manufacturing · DuckDB

Hands-on SQL querying of **8 Parquet files** that simulate a real steering wheel manufacturing process.  
You will write SQL directly on Parquet data using DuckDB — no database server needed.

---

## Prerequisites

- **Python 3.10+** on your `PATH`
- Virtual environment activated (see root `README.md`)

---

## 1 — Install Dependencies

```bash
pip install pandas pyarrow numpy duckdb jupyter
```

---

## 2 — Generate the Parquet Data Files

```bash
python generate_steering_wheel_data.py
```

This creates 8 files in `data/`:

| File | Rows (approx.) | Description |
|------|----------------|-------------|
| `materials_stock.parquet` | ~300 | Raw material inventory snapshot |
| `materials_log.parquet` | ~28k | Material consumption time series (OUT) + restocking (IN) |
| `station_molding.parquet` | ~10k | Skeleton molding — all products |
| `station_quality_check.parquet` | ~10k | Dimensional + surface inspection — all products |
| `station_foaming.parquet` | ~10k | Polyurethane foam injection — all products |
| `station_conductor.parquet` | ~6k | Heating conductor — PT66 + PT77 only |
| `station_laser.parquet` | ~3k | Laser bombardment / grip — PT77 only |
| `station_tapitat.parquet` | ~10k | Leather wrapping — all products |

### Optional flags

```bash
python generate_steering_wheel_data.py --rows 20000 --seed 99
python generate_steering_wheel_data.py --output-dir my_data
```

---

## 3 — Read the Quality Standards (SIC)

Open `quality_standards_sic.md` to understand the process:
- What each station does
- Process parameter tolerances
- Pass / Rework / Scrap criteria

These rules are the ones you will **validate with SQL** in the notebook.

---

## 4 — Launch the Notebook

```bash
jupyter notebook
```

Open `session3_sql_duckdb.ipynb`.

The notebook is structured as **docDB blocks** — each cell is:

```
Business question (plain English)
       ↓
SQL query
       ↓
DataFrame result → your interpretation
```

### Notebook sections

| Section | SQL concepts |
|---|---|
| 1. Schema exploration | `DESCRIBE`, `UNION ALL` |
| 2. Single-table queries | `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY` |
| 3. Aggregation + HAVING | `HAVING`, `CASE WHEN`, `ROUND`, `STDDEV` |
| 4. Multi-table JOINs | `JOIN`, `CTE` (`WITH`) |
| 5. Window functions | `RANK()`, `SUM() OVER`, `LAG()` |
| 6. Quality validation | SIC rule checks via `CASE WHEN` |
| 7. Challenge questions | Write your own SQL |

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
├── quality_standards_sic.md          ← process rules + tolerances
├── session3_sql_duckdb.ipynb         ← main notebook
└── README.md
```

---

## Product Types

| Code | Name | Stations |
|---|---|---|
| PT55 | Standard | Molding → QC → Foaming → Tapitat |
| PT66 | Sport | Molding → QC → Foaming → Conductor → Tapitat |
| PT77 | Premium | Molding → QC → Foaming → Conductor → Laser → Tapitat |

All station tables share `product_id` as the join key.

---

## Troubleshooting

- **`FileNotFoundError`** — run `generate_steering_wheel_data.py` first.
- **`duckdb.CatalogException`** — make sure the notebook is run from the `Session3-SQL-DuckDB/` directory.
- **`ModuleNotFoundError: duckdb`** — run `pip install duckdb` with your venv active.
