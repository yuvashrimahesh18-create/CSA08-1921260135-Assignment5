
import sqlite3
import time
import re
from datetime import date, timedelta
from collections import Counter


# ==================================================
# 1. SENTIMENT ANALYSIS
# ==================================================

POSITIVE = {
    "good", "clean", "fast", "helpful", "improved",
    "better", "excellent", "fresh", "safe", "clear",
    "effective", "pleasant", "satisfied", "beautiful",
    "accurate", "useful", "polite"
}

NEGATIVE = {
    "bad", "dirty", "slow", "rude", "smoke",
    "broken", "polluted", "harmful", "dangerous",
    "poor", "unhealthy", "noise", "worse", "terrible"
}

NEGATORS = {"not", "never", "no"}


def score(text):
    """Calculate sentiment score using keywords and negation."""
    words = re.findall(r"\b\w+\b", text.lower())
    total = 0

    for index, word in enumerate(words):
        value = 0

        if word in POSITIVE:
            value = 1
        elif word in NEGATIVE:
            value = -1

        if index > 0 and words[index - 1] in NEGATORS:
            value *= -1

        total += value

    return total


def label(text):
    result = score(text)

    if result > 0:
        return "positive"
    elif result < 0:
        return "negative"
    else:
        return "neutral"


# ==================================================
# 2. FIFTY CITIZEN COMPLAINTS
# ==================================================

complaints = [
    "The air is clean and fresh today.",
    "Smoke from the factory is harmful.",
    "The roads are dirty and polluted.",
    "The monitoring service is helpful.",
    "The air quality is bad near the school.",
    "The bus service is fast and good.",
    "The pollution level is dangerous.",
    "The station provides clear information.",
    "The air is not good today.",
    "The environment is safe and clean.",
    "The air smells terrible near the factory.",
    "The monitoring system is excellent.",
    "The roads are not clean.",
    "The pollution is getting worse.",
    "The staff are helpful and polite.",
    "The air is fresh near the park.",
    "Smoke makes the area unhealthy.",
    "The response is slow and poor.",
    "The air quality has improved.",
    "The neighbourhood is dirty.",
    "The service is not bad.",
    "The pollution is harmful to children.",
    "The readings are clear and useful.",
    "The monitoring station is broken.",
    "The environment is pleasant today.",
    "The air is not polluted.",
    "The factory releases dangerous smoke.",
    "The service is excellent and fast.",
    "The air quality is poor.",
    "The monitoring team is helpful.",
    "The streets are clean and beautiful.",
    "The smoke causes unhealthy conditions.",
    "The response from officials is slow.",
    "The air is good near the lake.",
    "The pollution level is terrible.",
    "The station gives accurate information.",
    "The air is not bad today.",
    "The area is polluted and dirty.",
    "The service is better now.",
    "The air is harmful to public health.",
    "The team is effective and helpful.",
    "The air quality is worse today.",
    "The park is clean and pleasant.",
    "The factory smoke is dangerous.",
    "The system is not broken.",
    "The information is clear and good.",
    "The air is unhealthy near the road.",
    "The service is poor and slow.",
    "The environment is safe today.",
    "The pollution is not good."
]


# Reference labels based on reading the complaints.
# Review these labels and adjust if your own judgement differs.

manual_labels = [
    "positive", "negative", "negative", "positive", "negative",
    "positive", "negative", "positive", "negative", "positive",
    "negative", "positive", "negative", "negative", "positive",
    "positive", "negative", "negative", "positive", "negative",
    "positive", "negative", "positive", "negative", "positive",
    "positive", "negative", "positive", "negative", "positive",
    "positive", "negative", "negative", "positive", "negative",
    "positive", "positive", "negative", "positive", "negative",
    "positive", "negative", "positive", "negative", "positive",
    "positive", "negative", "negative", "positive", "negative"
]


def test_complaints():
    print("\nCITIZEN COMPLAINT SENTIMENT ANALYSIS")
    print("=" * 60)

    agreements = 0

    for index, complaint in enumerate(complaints):
        predicted = label(complaint)
        actual = manual_labels[index]

        if predicted == actual:
            agreements += 1

        print(
            f"{index + 1:02d}. {predicted:8} | "
            f"Manual: {actual:8} | {complaint}"
        )

    percentage = agreements / len(complaints) * 100

    print("\nTotal complaints:", len(complaints))
    print("Agreements:", agreements)
    print("Disagreements:", len(complaints) - agreements)
    print(f"Manual agreement: {percentage:.2f}%")

    print("\nMISCLASSIFICATION ANALYSIS")

    for index, complaint in enumerate(complaints):
        predicted = label(complaint)
        actual = manual_labels[index]

        if predicted != actual:
            print("Complaint:", complaint)
            print("Predicted:", predicted)
            print("Manual label:", actual)
            print("Reason: The keyword-based model does not understand")
            print("the complete context and meaning of the sentence.")

    return agreements


# ==================================================
# 3. EXTRACTIVE AND FIRST-K SUMMARISATION
# ==================================================

IMPORTANT_WORDS = POSITIVE | NEGATIVE | {
    "pollution", "air", "health", "factory", "station"
}


def extractive_summary(text, k=5):
    """Select important sentences using keyword frequency."""

    if not text.strip():
        return ""

    sentences = re.findall(r"[^.!?]+[.!?]?", text.strip())

    word_counts = Counter(
        word for word in re.findall(r"\b\w+\b", text.lower())
        if word in IMPORTANT_WORDS
    )

    ranked = []

    for index, sentence in enumerate(sentences):
        words = re.findall(r"\b\w+\b", sentence.lower())

        sentence_score = sum(
            word_counts[word] for word in words
        )

        ranked.append((sentence_score, index, sentence.strip()))

    selected = sorted(
        ranked,
        key=lambda item: (-item[0], item[1])
    )[:k]

    selected = sorted(selected, key=lambda item: item[1])

    return " ".join(item[2] for item in selected)


def first_k_summary(text, k=5):
    """Return the first k sentences."""

    sentences = re.findall(r"[^.!?]+[.!?]?", text.strip())

    selected = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    return " ".join(selected[:k])


def test_summarisation():
    print("\nSUMMARISATION COMPARISON – 50 COMPLAINTS")
    print("=" * 60)

    sample = " ".join(complaints)

    print("Total complaints used:", len(complaints))
    print("Total words:", len(re.findall(r"\b\w+\b", sample)))

    start = time.perf_counter()
    extractive_result = extractive_summary(sample, 5)
    extractive_time = time.perf_counter() - start

    print("\nEXTRACTIVE SUMMARY (5 important sentences)")
    print(extractive_result)
    print(f"Execution time: {extractive_time:.6f} seconds")

    start = time.perf_counter()
    first_k_result = first_k_summary(sample, 5)
    first_k_time = time.perf_counter() - start

    print("\nFIRST-K SUMMARY (first 5 sentences)")
    print(first_k_result)
    print(f"Execution time: {first_k_time:.6f} seconds")

    print("\nCOMPARISON:")
    print("Extractive summarisation selects sentences using important words.")
    print("First-k summarisation selects the first five sentences.")
    print("Extractive summarisation considers the complete complaint text.")
    print("First-k summarisation stops after collecting five sentences.")


# ==================================================
# 4. SQLITE INDEX PERFORMANCE
# ==================================================

def test_database_index():
    print("\nSQLITE INDEX PERFORMANCE")
    print("=" * 60)

    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE readings (
            station TEXT,
            day TEXT,
            pm25 REAL
        )
    """)

    records = []

    for station_number in range(1, 101):
        station = f"S{station_number:03d}"

        for day_number in range(365):
            reading_date = (
                date(2026, 1, 1) + timedelta(days=day_number)
            )

            records.append((
                station,
                reading_date.isoformat(),
                20 + (day_number % 50)
            ))

    cursor.executemany(
        "INSERT INTO readings VALUES (?, ?, ?)",
        records
    )

    connection.commit()

    query = """
        SELECT AVG(pm25)
        FROM readings
        WHERE station = ? AND day = ?
    """

    parameters = ("S050", "2026-06-15")

    # Measure query time before creating the index.
    start = time.perf_counter()

    for _ in range(500):
        cursor.execute(query, parameters)
        cursor.fetchone()

    before_index = time.perf_counter() - start

    # Create a composite index.
    cursor.execute("""
        CREATE INDEX idx_station_day
        ON readings(station, day)
    """)

    connection.commit()

    # Measure query time after creating the index.
    start = time.perf_counter()

    for _ in range(500):
        cursor.execute(query, parameters)
        cursor.fetchone()

    after_index = time.perf_counter() - start

    print("Total database records:", len(records))
    print(f"Query time before index: {before_index:.6f} seconds")
    print(f"Query time after index:  {after_index:.6f} seconds")

    if after_index < before_index:
        print("Result: Index improved query performance.")
    else:
        print("Result: No improvement measured in this run.")

    print("Index created: idx_station_day")

    connection.close()


# ==================================================
# 5. PRODUCTION ENGINEERING DECISION
# ==================================================

def production_decision():
    print("\nPRODUCTION ENGINEERING DECISION")
    print("=" * 60)

    additional_stations = 100
    readings_per_station = 96

    readings_per_day = (
        additional_stations * readings_per_station
    )

    readings_per_month = readings_per_day * 30

    existing_stations = 12
    existing_daily_readings = existing_stations * 24

    total_daily_readings = (
        readings_per_day + existing_daily_readings
    )

    print("Additional stations:", additional_stations)
    print("Reporting interval: Every 15 minutes")
    print("Readings per new station per day:", readings_per_station)
    print("Additional readings per day:", readings_per_day)
    print("Additional readings per month:", readings_per_month)

    print("\nIncluding 12 existing hourly stations:")
    print("Total readings per day:", total_daily_readings)
    print("Monthly citizen complaints: 50000")

    print("\nRECOMMENDATIONS:")
    print("1. Store air-quality readings in SQLite with suitable indexes.")
    print("2. Validate and clean incoming CSV data before insertion.")
    print("3. Use SQL GROUP BY for daily and monthly reports.")
    print("4. Use charts to monitor pollution trends.")
    print("5. Use a trained sentiment model for large complaint volumes.")
    print("6. Review uncertain sentiment predictions manually.")
    print("7. Retain keyword rules as a baseline and fallback.")
    print("8. Monitor database performance as station numbers increase.")


# ==================================================
# 6. MAIN PROGRAM
# ==================================================

if __name__ == "__main__":

    test_complaints()

    test_summarisation()

    test_database_index()

    production_decision()

    print("\nTASK B4 EXECUTION COMPLETED.")
