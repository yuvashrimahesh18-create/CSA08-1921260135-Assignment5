
import csv
import sqlite3
import time
import cProfile
import pstats
import io

from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "generated_air_quality.csv"


def generate_dataset(station_count):
    """Generate 8760 hourly readings per station."""
    records = []

    for station_number in range(1, station_count + 1):
        station_id = f"S{station_number:03d}"

        for hour_number in range(8760):
            day_number = hour_number // 24 + 1
            pm25 = 20 + (hour_number % 50)

            records.append((station_id, day_number, pm25))

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["station_id", "day", "pm25"])
        writer.writerows(records)

    return records


def calculate_using_loops(records):
    """Calculate daily averages using Python dictionaries."""
    totals = defaultdict(float)
    counts = defaultdict(int)

    for station_id, day, pm25 in records:
        key = (station_id, day)
        totals[key] += pm25
        counts[key] += 1

    averages = {}

    for key in totals:
        averages[key] = totals[key] / counts[key]

    return averages


def calculate_using_sql(records):
    """Calculate daily averages using SQLite GROUP BY."""
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE readings (
            station_id TEXT,
            day INTEGER,
            pm25 REAL
        )
    """)

    cursor.executemany(
        "INSERT INTO readings VALUES (?, ?, ?)",
        records
    )

    cursor.execute("""
        SELECT station_id, day, AVG(pm25)
        FROM readings
        GROUP BY station_id, day
    """)

    results = cursor.fetchall()
    connection.close()

    return results


def benchmark():
    print("LOOPS VS SQLITE PERFORMANCE COMPARISON")
    print("=" * 50)

    for station_count in [1, 12, 120]:
        print(f"\nSTATIONS: {station_count}")

        start = time.perf_counter()
        records = generate_dataset(station_count)
        generation_time = time.perf_counter() - start

        start = time.perf_counter()
        loop_results = calculate_using_loops(records)
        loop_time = time.perf_counter() - start

        start = time.perf_counter()
        sql_results = calculate_using_sql(records)
        sql_time = time.perf_counter() - start

        print("Generated readings:", len(records))
        print("Daily groups using loops:", len(loop_results))
        print("Daily groups using SQL:", len(sql_results))
        print(f"Dataset generation time: {generation_time:.4f} seconds")
        print(f"Python loop time: {loop_time:.4f} seconds")
        print(f"SQLite GROUP BY time: {sql_time:.4f} seconds")

        assert len(loop_results) == len(sql_results)
        print("Validation: Both methods produced the same number of groups.")

    print("\nPERFORMANCE COMPARISON COMPLETED.")


def profile_performance():
    """Profile the Python loop implementation using cProfile."""
    print("\nCPROFILE PERFORMANCE ANALYSIS")
    print("=" * 50)

    records = generate_dataset(12)

    profiler = cProfile.Profile()
    profiler.enable()

    calculate_using_loops(records)

    profiler.disable()

    output = io.StringIO()
    stats = pstats.Stats(profiler, stream=output)
    stats.sort_stats("cumulative")
    stats.print_stats(10)

    print(output.getvalue())


if __name__ == "__main__":
    benchmark()
    profile_performance()
