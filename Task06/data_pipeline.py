import csv
import sqlite3
from pathlib import Path
from time import perf_counter

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "raw_air_quality.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_air_quality.csv"
DATABASE_FILE = BASE_DIR / "air_quality.db"


def clean_data():
    cleaned_records = []
    seen_records = set()

    missing_count = 0
    invalid_count = 0
    duplicate_count = 0
    fahrenheit_count = 0

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "station_id", "date", "hour", "pm25",
            "pm10", "no2", "temperature", "temp_unit"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV is missing required columns.")

        for row in reader:
            numeric_fields = ["pm25", "pm10", "no2", "temperature"]

            if any(
                row[field] is None or row[field].strip() in ("", "NA", "N/A")
                for field in numeric_fields
            ):
                missing_count += 1
                continue

            try:
                pm25 = float(row["pm25"])
                pm10 = float(row["pm10"])
                no2 = float(row["no2"])
                temperature = float(row["temperature"])
            except ValueError:
                invalid_count += 1
                continue

            if min(pm25, pm10, no2) < 0:
                invalid_count += 1
                continue

            if row["temp_unit"].strip().upper() == "F":
                temperature = (temperature - 32) * 5 / 9
                fahrenheit_count += 1

            key = (
                row["station_id"],
                row["date"],
                row["hour"]
            )

            if key in seen_records:
                duplicate_count += 1
                continue

            seen_records.add(key)

            cleaned_records.append({
                "station_id": row["station_id"],
                "date": row["date"],
                "hour": row["hour"],
                "pm25": pm25,
                "pm10": pm10,
                "no2": no2,
                "temperature": round(temperature, 2),
                "temp_unit": "C"
            })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "station_id", "date", "hour", "pm25",
            "pm10", "no2", "temperature", "temp_unit"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_records)

    return cleaned_records, missing_count, invalid_count, duplicate_count, fahrenheit_count


def save_to_database(records):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT,
            date TEXT,
            hour TEXT,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            temperature REAL,
            temp_unit TEXT,
            UNIQUE(station_id, date, hour)
        )
    """)

    cursor.executemany("""
        INSERT OR IGNORE INTO readings
        (station_id, date, hour, pm25, pm10, no2, temperature, temp_unit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            r["station_id"], r["date"], r["hour"],
            r["pm25"], r["pm10"], r["no2"],
            r["temperature"], r["temp_unit"]
        )
        for r in records
    ])

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM readings")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT station_id, ROUND(AVG(pm25), 2)
        FROM readings
        GROUP BY station_id
        ORDER BY station_id
    """)

    print("\nSTATION-WISE AVERAGE PM2.5")
    for station, average in cursor.fetchall():
        print(f"{station}: {average}")

    connection.close()
    return total
def test_large_dataset():
    test_records = []

    for i in range(1200):
        test_records.append({
            "station_id": f"S{i % 12 + 1:02d}",
            "date": "2026-11-02",
            "hour": f"{i // 60:02d}:{i % 60:02d}",
            "pm25": 30 + (i % 50),
            "pm10": 60 + (i % 50),
            "no2": 15 + (i % 20),
            "temperature": 28.0,
            "temp_unit": "C"
        })

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM readings")

    cursor.executemany("""
        INSERT INTO readings
        (station_id, date, hour, pm25, pm10, no2, temperature, temp_unit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            r["station_id"], r["date"], r["hour"],
            r["pm25"], r["pm10"], r["no2"],
            r["temperature"], r["temp_unit"]
        )
        for r in test_records
    ])

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM readings")
    count = cursor.fetchone()[0]

    print("\nLARGE DATASET TEST")
    print("Generated readings:", len(test_records))
    print("Readings stored in SQLite:", count)

    connection.close()

def main():
    start = perf_counter()

    records, missing, invalid, duplicates, converted = clean_data()

    print("DATA CLEANING SUMMARY")
    print("Missing records removed:", missing)
    print("Invalid records removed:", invalid)
    print("Duplicate records removed:", duplicates)
    print("Fahrenheit conversions:", converted)
    print("Cleaned records:", len(records))

    total = save_to_database(records)

    elapsed = perf_counter() - start

    print("\nDATABASE SUMMARY")
    print("Total readings stored:", total)
    print("Cleaned CSV saved to:", OUTPUT_FILE)
    print("Database saved to:", DATABASE_FILE)
    print(f"Execution time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
    test_large_dataset()