import io
from contextlib import redirect_stdout
import pstats
import logging
import time
import timeit
import cProfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

# Sample air-quality readings
SAMPLE = [
    {"station": "Adyar", "pm25": "48"},
    {"station": "Guindy", "pm25": "95"},
    {"station": "Adyar", "pm25": "NA"},
    {"station": "Guindy", "pm25": "-5"},
    {"station": "Adyar", "pm25": "60"},
    {"station": "Guindy", "pm25": "121"}
]


def clean_readings(records):
    """Clean missing and negative PM2.5 readings."""

    cleaned = []

    for row in records:
        value = row["pm25"]

        # Print statement for debugging
        print(f"Checking {row['station']}: {value}")

        # Logging for program monitoring
        logging.info("Processing station %s", row["station"])

        if value == "" or value.upper() == "NA":
            logging.warning("Missing reading skipped")
            continue

        pm25 = float(value)

        if pm25 < 0:
            logging.warning("Negative reading skipped")
            continue

        # Assertion to validate cleaned data
        assert pm25 >= 0, "Invalid negative PM2.5 value"

        cleaned.append((row["station"], pm25))

    return cleaned


def profile_workload():
    """Workload used by cProfile."""
    total = 0
    for i in range(10000):
        total += i
    return total


def main():

    print("\n--- DEBUGGING USING PRINT AND LOGGING ---")

    start = time.perf_counter()
    cleaned = clean_readings(SAMPLE)
    end = time.perf_counter()

    print("\nCLEANED DATA:")
    print(cleaned)

    print("\n--- ASSERTION TEST ---")
    assert all(value >= 0 for _, value in cleaned)
    print("Assertion passed: All readings are non-negative.")

    print("\n--- PERF_COUNTER TIMING ---")
    print(f"Cleaning execution time: {end - start:.6f} seconds")

    print("\n--- TIMEIT MEASUREMENT ---")

    with redirect_stdout(io.StringIO()):
     elapsed = timeit.timeit(
        lambda: clean_readings(SAMPLE),
        number=10
    )

    print(f"10 executions took: {elapsed:.6f} seconds")
    print("\n--- CPROFILE RESULTS ---")

profiler = cProfile.Profile()

with redirect_stdout(io.StringIO()):
    profiler.enable()
    clean_readings(SAMPLE)
    profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats()

print("\nAll debugging and profiling demonstrations completed.")