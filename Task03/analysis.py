
import csv
import sqlite3
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR.parent / "Task02" / "cleaned_air_quality.csv"
DATABASE_FILE = BASE_DIR / "air_quality_analysis.db"


def read_data():
    """Read cleaned air-quality records from CSV."""
    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def create_database(rows):
    """Store readings in SQLite for SQL-based analysis."""
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS readings")

    cursor.execute("""
        CREATE TABLE readings (
            station_id TEXT,
            reading_date TEXT,
            reading_hour TEXT,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            temperature REAL
        )
    """)

    data = [
        (
            row["station_id"],
            row["date"],
            row["hour"],
            float(row["pm25"]),
            float(row["pm10"]),
            float(row["no2"]),
            float(row["temperature"])
        )
        for row in rows
    ]

    cursor.executemany("""
        INSERT INTO readings
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)

    connection.commit()
    return connection


def analyse_data(connection):
    cursor = connection.cursor()

    print("\nDAILY AIR QUALITY SUMMARY")
    print("-" * 45)

    cursor.execute("""
        SELECT reading_date,
               COUNT(*),
               ROUND(AVG(pm25), 2),
               ROUND(AVG(pm10), 2),
               ROUND(AVG(no2), 2)
        FROM readings
        GROUP BY reading_date
    """)

    for result in cursor.fetchall():
        print(
            f"Date: {result[0]} | Records: {result[1]} | "
            f"Average PM2.5: {result[2]} | "
            f"Average PM10: {result[3]} | "
            f"Average NO2: {result[4]}"
        )

    print("\nSTATION-WISE PM2.5 COMPARISON")
    print("-" * 45)

    cursor.execute("""
        SELECT station_id, ROUND(AVG(pm25), 2)
        FROM readings
        GROUP BY station_id
        ORDER BY AVG(pm25) DESC
    """)

    station_results = cursor.fetchall()

    for station, average in station_results:
        print(f"{station}: {average}")

    print("\nAVERAGE PM2.5 BY HOUR")
    print("-" * 45)

    cursor.execute("""
        SELECT reading_hour, ROUND(AVG(pm25), 2)
        FROM readings
        GROUP BY reading_hour
        ORDER BY reading_hour
    """)

    hour_results = cursor.fetchall()

    for hour, average in hour_results:
        print(f"{hour}: {average}")

    if hour_results:
        worst_hour = max(hour_results, key=lambda item: item[1])
        print(
            f"\nHighest average PM2.5 hour: "
            f"{worst_hour[0]} ({worst_hour[1]})"
        )

    return station_results, hour_results


def generate_charts(rows, station_results, hour_results):
    """Generate five air-quality visualisations."""

    # 1. PM2.5 trend by hour
    times = [row["hour"] for row in rows]
    pm25_values = [float(row["pm25"]) for row in rows]

    plt.figure(figsize=(9, 5))
    plt.plot(times, pm25_values, marker="o")
    plt.title("PM2.5 Readings by Hour")
    plt.xlabel("Hour")
    plt.ylabel("PM2.5")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(BASE_DIR / "A3_PM25_Trend.png")
    plt.close()

    # 2. Station-wise PM2.5 comparison
    stations = [item[0] for item in station_results]
    averages = [item[1] for item in station_results]

    plt.figure(figsize=(9, 5))
    plt.bar(stations, averages)
    plt.title("Average PM2.5 by Monitoring Station")
    plt.xlabel("Station")
    plt.ylabel("Average PM2.5")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "A3_Station_Comparison.png")
    plt.close()

    # 3. Temperature and PM2.5 relationship
    temperatures = [float(row["temperature"]) for row in rows]

    plt.figure(figsize=(8, 5))
    plt.scatter(temperatures, pm25_values)
    plt.title("Temperature vs PM2.5")
    plt.xlabel("Temperature (Celsius)")
    plt.ylabel("PM2.5")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(BASE_DIR / "A3_Temperature_Relationship.png")
    plt.close()

    # 4. PM2.5 distribution histogram
    plt.figure(figsize=(8, 5))
    plt.hist(pm25_values, bins=5, edgecolor="black")
    plt.title("Distribution of PM2.5 Readings")
    plt.xlabel("PM2.5")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "A3_PM25_Histogram.png")
    plt.close()

    # 5. Box plot of PM2.5 by station
    station_values = defaultdict(list)

    for row in rows:
        station_values[row["station_id"]].append(
            float(row["pm25"])
        )

    plt.figure(figsize=(9, 5))
    plt.boxplot(
        list(station_values.values()),
        tick_labels=list(station_values.keys())
    )
    plt.title("PM2.5 Distribution by Station")
    plt.xlabel("Station")
    plt.ylabel("PM2.5")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "A3_Station_Boxplot.png")
    plt.close()

    print("\nFive visualisation charts generated successfully!")


def main():
    rows = read_data()
    print("Total cleaned readings:", len(rows))

    connection = create_database(rows)

    station_results, hour_results = analyse_data(connection)

    generate_charts(rows, station_results, hour_results)

    connection.close()


if __name__ == "__main__":
    main()
