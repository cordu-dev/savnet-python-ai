import csv
from datetime import date, timedelta
from pathlib import Path


ROW_COUNT = 1_000
START_DATE = date(2026, 1, 1)
SHIFTS = ["Morning", "Evening", "Night"]
MACHINES = ["M1", "M2", "M3", "M4", "M5"]
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "production_log.csv"


def build_row(index):
    machine = MACHINES[(index - 1) % len(MACHINES)]
    shift = SHIFTS[(index - 1) % len(SHIFTS)]
    production_date = START_DATE + timedelta(days=(index - 1) // 15)
    units_produced = 420 + (index * 17) % 180
    defective_units = 5 + (index * 7) % 28

    if machine == "M3":
        defective_units += 4

    if shift == "Night":
        defective_units += 3

    return {
        "batch_id": f"B{index:04d}",
        "date": production_date.isoformat(),
        "shift": shift,
        "machine": machine,
        "units_produced": units_produced,
        "defective_units": defective_units,
    }


def main():
    fieldnames = [
        "batch_id",
        "date",
        "shift",
        "machine",
        "units_produced",
        "defective_units",
    ]

    with OUTPUT_FILE.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for index in range(1, ROW_COUNT + 1):
            writer.writerow(build_row(index))

    print(f"Created {OUTPUT_FILE} with {ROW_COUNT} rows.")


if __name__ == "__main__":
    main()
