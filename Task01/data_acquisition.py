
import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "sample_air_quality.csv"
DATABASE_FILE = BASE_DIR / "air_quality.db"


def inspect_csv(filename):
    print("AIR QUALITY DATA ACQUISITION")
    print("-" * 40)

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        print("CSV Columns:", reader.fieldnames)
        print("Total records:", len(rows))

    return rows


def create_database():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.execute("PRAGMA foreign_keys = ON")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            station_id TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT,
            reading_date TEXT,
            reading_hour TEXT,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            temperature REAL,
            temperature_unit TEXT,
            FOREIGN KEY (station_id) REFERENCES stations(station_id)
        )
    """)

    connection.commit()
    return connection


def insert_data(rows, connection):
    cursor = connection.cursor()

    # Clear previous readings so rerunning does not duplicate records.
    cursor.execute("DELETE FROM readings")

    # Insert unique station IDs.
    stations = [(row["station_id"],) for row in rows]

    cursor.executemany("""
        INSERT OR IGNORE INTO stations (station_id)
        VALUES (?)
    """, stations)

    # Prepare reading records.
    readings = [
        (
            row["station_id"],
            row["date"],
            row["hour"],
            float(row["pm25"]),
            float(row["pm10"]),
            float(row["no2"]),
            float(row["temperature"]),
            row["temperature_unit"]
        )
        for row in rows
    ]

    # Insert all readings using executemany.
    cursor.executemany("""
        INSERT INTO readings (
            station_id, reading_date, reading_hour,
            pm25, pm10, no2, temperature, temperature_unit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, readings)

    connection.commit()
    print("\nCSV records inserted into SQLite successfully.")


def verify_database(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM stations")
    station_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM readings")
    reading_count = cursor.fetchone()[0]

    print("Total stations:", station_count)
    print("Total readings:", reading_count)

    cursor.execute("""
        SELECT station_id, AVG(pm25)
        FROM readings
        GROUP BY station_id
        ORDER BY station_id
    """)

    print("\nAverage PM2.5 by station:")
    for station_id, average in cursor.fetchall():
        print(f"{station_id}: {average:.2f}")


def main():
    rows = inspect_csv(CSV_FILE)
    connection = create_database()

    try:
        insert_data(rows, connection)
        verify_database(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
