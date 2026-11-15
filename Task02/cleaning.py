
import csv
import math
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "cleaning_sample.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_air_quality.csv"


def fahrenheit_to_celsius(value):
    """Convert Fahrenheit temperature to Celsius."""
    return (value - 32) * 5 / 9


def is_valid_reading(value, minimum=0):
    """Check whether a sensor reading is numeric and non-negative."""
    try:
        number = float(value)
        return math.isfinite(number) and number >= minimum
    except (ValueError, TypeError):
        return False


def clean_data(rows):
    cleaned_rows = []
    seen = set()

    missing_count = 0
    invalid_count = 0
    duplicate_count = 0
    converted_count = 0

    for row in rows:

        # Handle missing sensor readings.
        required_fields = ["pm25", "pm10", "no2", "temperature"]

        if any(row[field].strip() == "" for field in required_fields):
            missing_count += 1
            continue

        # Remove duplicate records.
        record_key = (
            row["station_id"],
            row["date"],
            row["hour"]
        )

        if record_key in seen:
            duplicate_count += 1
            continue

        seen.add(record_key)

        # Reject impossible pollutant values.
        if not all(
            is_valid_reading(row[field])
            for field in ["pm25", "pm10", "no2"]
        ):
            invalid_count += 1
            continue

        temperature = float(row["temperature"])

        # Convert Fahrenheit to Celsius.
        if row["temperature_unit"].upper() == "F":
            temperature = fahrenheit_to_celsius(temperature)
            converted_count += 1
        elif row["temperature_unit"].upper() != "C":
            invalid_count += 1
            continue

        cleaned_row = {
            "station_id": row["station_id"],
            "date": row["date"],
            "hour": row["hour"],
            "pm25": float(row["pm25"]),
            "pm10": float(row["pm10"]),
            "no2": float(row["no2"]),
            "temperature": round(temperature, 2),
            "temperature_unit": "C"
        }

        cleaned_rows.append(cleaned_row)

    print("\nDATA CLEANING SUMMARY")
    print("-" * 35)
    print("Original records:", len(rows))
    print("Missing records removed:", missing_count)
    print("Invalid records removed:", invalid_count)
    print("Duplicate records removed:", duplicate_count)
    print("Fahrenheit conversions:", converted_count)
    print("Cleaned records:", len(cleaned_rows))

    return cleaned_rows


def min_max_normalisation(values):
    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [0.0 for value in values]

    return [
        (value - minimum) / (maximum - minimum)
        for value in values
    ]


def z_score_standardisation(values):
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    standard_deviation = math.sqrt(variance)

    if standard_deviation == 0:
        return [0.0 for value in values]

    return [
        (value - mean) / standard_deviation
        for value in values
    ]


def save_cleaned_data(rows):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "station_id", "date", "hour",
            "pm25", "pm10", "no2",
            "temperature", "temperature_unit"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\nCleaned data saved to:", OUTPUT_FILE.name)


def main():
    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    cleaned_rows = clean_data(rows)

    if cleaned_rows:
        pm25_values = [row["pm25"] for row in cleaned_rows]

        print("\nMIN-MAX NORMALISATION (PM2.5)")
        print(min_max_normalisation(pm25_values))

        print("\nZ-SCORE STANDARDISATION (PM2.5)")
        print(z_score_standardisation(pm25_values))

        save_cleaned_data(cleaned_rows)


if __name__ == "__main__":
    main()
