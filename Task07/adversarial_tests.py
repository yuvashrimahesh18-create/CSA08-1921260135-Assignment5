import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "adversarial_data.csv"


def test_missing_column():
    print("\nTEST 1: MISSING COLUMN")

    bad_file = BASE_DIR / "missing_column.csv"

    bad_file.write_text(
        "station_id,date,hour,pm25,pm10\n"
        "S01,2026-11-01,00:00,45,78\n",
        encoding="utf-8"
    )

    try:
        with open(bad_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            required = {
                "station_id", "date", "hour",
                "pm25", "pm10", "no2"
            }

            if not required.issubset(reader.fieldnames or []):
                raise ValueError("Required CSV column is missing.")

            print("All required columns are present.")

    except ValueError as error:
        print("Error:", error)

def test_wrong_delimiter():
    print("\nTEST 2: WRONG DELIMITER")

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            required = {"station_id", "date", "hour", "pm25", "pm10", "no2"}

            if not required.issubset(reader.fieldnames or []):
                raise ValueError("Wrong delimiter or invalid CSV header.")

            print("Delimiter is correct.")

    except ValueError as error:
        print("Error:", error)


def test_empty_file():
    print("\nTEST 3: EMPTY FILE")

    empty_file = BASE_DIR / "empty.csv"
    empty_file.write_text("", encoding="utf-8")

    try:
        with open(empty_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("CSV file is empty.")

    except ValueError as error:
        print("Error:", error)


def test_encoding():
    print("\nTEST 4: ENCODING")

    bad_file = BASE_DIR / "invalid_encoding.csv"

    bad_file.write_bytes(
        b"station_id,date,hour\nS01,2026-11-01,00:00\n\xff"
    )

    try:
        with open(bad_file, "r", encoding="utf-8") as file:
            file.read()

        print("File successfully read using UTF-8.")

    except UnicodeDecodeError:
        print("Error: Invalid UTF-8 encoding detected.")
def test_sql_injection():
    print("\nTEST 5: SQL INJECTION")

    import sqlite3

    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE stations (
            station_id TEXT,
            station_name TEXT
        )
    """)

    cursor.executemany(
        "INSERT INTO stations VALUES (?, ?)",
        [
            ("S01", "Central Station"),
            ("S02", "North Station")
        ]
    )

    user_input = "S01' OR '1'='1"

    # Unsafe query using string concatenation
    unsafe_query = (
        "SELECT * FROM stations WHERE station_id = '"
        + user_input + "'"
    )

    cursor.execute(unsafe_query)
    unsafe_results = cursor.fetchall()

    print("Unsafe query result count:", len(unsafe_results))

    # Safe query using a parameterized statement
    cursor.execute(
        "SELECT * FROM stations WHERE station_id = ?",
        (user_input,)
    )

    safe_results = cursor.fetchall()

    print("Parameterized query result count:", len(safe_results))

    connection.close()
def analyse_adversarial_sentiment(text):
    positive_words = {"good", "clean", "fresh", "great"}
    negative_words = {"bad", "toxic", "harmful", "pollution"}

    words = text.lower().replace(",", "").replace(".", "").replace("!", "").split()

    positive = 0
    negative = 0

    for index, word in enumerate(words):
        if word in positive_words:
            if index > 1 and words[index - 1] == "not" and words[index - 2] == "not":
                positive += 1
            elif index > 0 and words[index - 1] == "not":
                negative += 1
            else:
                positive += 1

        elif word in negative_words:
            if index > 0 and words[index - 1] == "not":
                positive += 1
            else:
                negative += 1

    if positive > negative:
        return "Positive"
    elif negative > positive:
        return "Negative"
    else:
        return "Neutral"


def test_adversarial_sentiment():
    print("\nTEST 6: ADVERSARIAL SENTIMENT")

    complaints = [
        "Great, another day breathing toxic air!",
        "The air is not not good.",
        "The air is clean but pollution is harmful."
    ]

    for complaint in complaints:
        result = analyse_adversarial_sentiment(complaint)
        print("Complaint:", complaint)
        print("Sentiment:", result)

def test_executemany_comparison():
    print("\nTEST 7: EXECUTE VS EXECUTEMANY")

    import sqlite3
    import time

    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE loop_data (
            station_id TEXT,
            pm25 REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE batch_data (
            station_id TEXT,
            pm25 REAL
        )
    """)

    records = [
        (f"S{i:04d}", float(i))
        for i in range(1000)
    ]

    # Individual execute() insertions
    start = time.perf_counter()

    for record in records:
        cursor.execute(
            "INSERT INTO loop_data VALUES (?, ?)",
            record
        )

    loop_time = time.perf_counter() - start

    # Batch executemany() insertion
    start = time.perf_counter()

    cursor.executemany(
        "INSERT INTO batch_data VALUES (?, ?)",
        records
    )

    batch_time = time.perf_counter() - start

    loop_count = cursor.execute(
        "SELECT COUNT(*) FROM loop_data"
    ).fetchone()[0]

    batch_count = cursor.execute(
        "SELECT COUNT(*) FROM batch_data"
    ).fetchone()[0]

    print("Records inserted using execute():", loop_count)
    print("Records inserted using executemany():", batch_count)
    print(f"Individual insertion time: {loop_time:.6f} seconds")
    print(f"Batch insertion time: {batch_time:.6f} seconds")

    connection.close()

if __name__ == "__main__":
     test_missing_column()
     test_wrong_delimiter()
     test_empty_file()
     test_encoding()
     test_sql_injection()
     test_adversarial_sentiment()
     test_executemany_comparison()