import pandas as pd


production_data = [
    {
        "batch_id": "B001",
        "date": "2026-01-05",
        "shift": "Morning",
        "machine": "M1",
        "units_produced": 500,
        "defective_units": 12,
    },
    {
        "batch_id": "B002",
        "date": "2026-01-05",
        "shift": "Morning",
        "machine": "M2",
        "units_produced": 460,
        "defective_units": 18,
    },
    {
        "batch_id": "B003",
        "date": "2026-01-05",
        "shift": "Evening",
        "machine": "M1",
        "units_produced": 520,
        "defective_units": 9,
    },
    {
        "batch_id": "B004",
        "date": "2026-01-06",
        "shift": "Night",
        "machine": "M3",
        "units_produced": 430,
        "defective_units": 25,
    },
]


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    print_section("Lesson 1 — Why Pandas for Manufacturing Data?")
    print("Manufacturing data usually comes as tables: batches, machines, shifts,")
    print("produced units, defective units, inspections, and process measurements.")
    print("Pandas helps engineers turn those tables into practical questions.")

    df = pd.DataFrame(production_data)

    print_section("1. First look at the production table")
    print(df)

    print_section("2. What does one row represent?")
    print("One row represents one production batch record.")

    print_section("3. Practical questions engineers can ask")
    print("Question A: Which machine has the highest number of defective units?")
    machine_defects = df.groupby("machine")["defective_units"].sum()
    print(machine_defects)
    print("Answer:", machine_defects.idxmax())

    print("\nQuestion B: Which shift has the highest number of defective units?")
    shift_defects = df.groupby("shift")["defective_units"].sum()
    print(shift_defects)
    print("Answer:", shift_defects.idxmax())

    print("\nQuestion C: Which batch should be reviewed first?")
    batch_to_review = df.sort_values("defective_units", ascending=False).iloc[0]
    print(batch_to_review[["batch_id", "machine", "shift", "defective_units"]])

    print_section("4. Key lesson")
    print("Pandas is like a smart spreadsheet inside Python.")
    print("It helps engineers inspect production data, ask better questions,")
    print("and find where investigation should start.")

    print_section("5. Mini challenge")
    print("Try changing one defective_units value and run the file again.")
    print("Does the machine or shift answer change?")


if __name__ == "__main__":
    main()
