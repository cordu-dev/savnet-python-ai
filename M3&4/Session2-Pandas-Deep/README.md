# Session 2 — Pandas Deep Dive

Hands-on exploration of real-world, messy manufacturing data using **Pandas** and **Parquet**.  
You will clean, reshape, and analyse three interlinked datasets that simulate a factory production environment.

---

## Prerequisites

- **Python 3.10+** installed and available on your `PATH`
- Basic familiarity with the terminal / command line

---

## 1 — Create a Virtual Environment

From the **project root** (`savnet-python-ai/`):

```bash
python -m venv .venv
```

Activate it:

| Platform | Command |
|----------|---------|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

Your prompt should now show `(.venv)` — you're inside the virtual environment.

---

## 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

Key packages pulled in for this session:

| Package | Why it's needed |
|---------|-----------------|
| `pandas` | Core data manipulation |
| `pyarrow` | Read / write Parquet files |
| `numpy` | Numerical operations & random data generation |
| `jupyter` | Interactive notebook environment |

> If you only want the bare minimum for this session you can also run:
> ```bash
> pip install pandas pyarrow numpy jupyter
> ```

---

## 3 — Generate the Parquet Data Files

Navigate into this session folder and run the data generator:

```bash
python generate_parquet_data.py
```

This creates three files inside the `data/` directory:

| File | Rows (approx.) | Description |
|------|---------------|-------------|
| `production_log.parquet` | ~12 240 | Main production cycles — mixed formats, outliers, duplicates |
| `inspection_log.parquet` | ~8 160 | Quality inspection events linked to production batches |
| `material_batches.parquet` | ~505 | Material batch reference table with supplier info |

### Optional flags

```bash
# Custom row count and random seed
python generate_parquet_data.py --rows 20000 --seed 99

# Write files to a different directory
python generate_parquet_data.py --output-dir my_data
```

---

## 4 — Launch Jupyter Notebook

From the **session folder**:

```bash
jupyter notebook
```

This opens the Jupyter interface in your browser. Open:

```
session2_pandas_deep.ipynb
```

> **Tip:** If your browser doesn't open automatically, look for a URL like  
> `http://127.0.0.1:8888/?token=...` in the terminal output and paste it into your browser.

---

## Folder Structure

```
Session2-Pandas-Deep/
├── data/
│   ├── production_log.parquet
│   ├── inspection_log.parquet
│   └── material_batches.parquet
├── generate_parquet_data.py   # Run this first to (re)generate data
├── session2_pandas_deep.ipynb # Main notebook — start here
├── rolling_window_explainer.png
└── README.md
```

---

## Troubleshooting

- **`ModuleNotFoundError: pyarrow`** — make sure your virtual environment is activated and `pip install -r requirements.txt` completed without errors.
- **`FileNotFoundError` inside the notebook** — run `generate_parquet_data.py` first so the `data/` files exist.
- **Jupyter command not found** — confirm your venv is active.
  - macOS / Linux: `which jupyter` should point inside `.venv/bin/`
  - Windows: `where jupyter` should point inside `.venv\Scripts\`
