# B2 – Adversarial Data and SQL Injection Testing

**Student Name:** S.M Yuvashri  
**Register Number:** 1921260135  
**Course:** Python Programming  
**Assignment:** Assignment 5 – Data Acquisition, Cleaning, Analysis and AI Applications

## 1. Aim

To test an air-quality data processing system using adversarial inputs, identify errors in CSV files, demonstrate SQL injection risks, evaluate sentiment-analysis limitations, and compare SQLite insertion methods.

## 2. CSV Adversarial Testing

The following input problems were tested:

| Test | Expected result | Actual result |
|---|---|---|
| Missing column | Detect missing column | Detected |
| Wrong delimiter | Detect invalid header | Detected |
| Empty file | Detect empty CSV | Detected |
| Invalid UTF-8 | Detect encoding error | Detected |

The program successfully identified all four CSV problems.

## 3. SQL Injection Testing

A SQLite in-memory database was created with two station records.

Test input:

`S01' OR '1'='1`

The unsafe query used string concatenation. This allowed the injected condition to return both records.

The parameterized query used a `?` placeholder and treated the input as a single value.

| Method | Records returned |
|---|---:|
| Unsafe string concatenation | 2 |
| Parameterized query | 0 |

**Conclusion:** Parameterized queries prevent this SQL injection attempt by separating SQL instructions from user-supplied values.

## 4. Adversarial Sentiment Analysis

Three challenging complaint statements were tested.

| Complaint | Result |
|---|---|
| Great, another day breathing toxic air! | Neutral |
| The air is not not good. | Positive |
| The air is clean but pollution is harmful. | Negative |

The double-negation handling was improved to recognise the phrase "not not good" as positive.

The sarcasm example was classified as neutral because the rule-based method cannot understand the intended sarcastic meaning. The mixed statement was classified as negative because negative keywords outweighed positive keywords.

**Limitation:** This simple lexicon-based method cannot reliably understand sarcasm, complex negation, or context. A trained machine-learning or natural-language-processing model could improve accuracy.

## 5. Execute vs Executemany Comparison

A total of 1,000 records were inserted into two SQLite tables using different methods.

| Method | Records inserted | Observed time |
|---|---:|---:|
| Individual execute() | 1,000 | 0.001414 seconds |
| executemany() | 1,000 | 0.000833 seconds |

In this test, `executemany()` completed faster than repeated `execute()` calls.

**Conclusion:** `executemany()` is convenient and can reduce Python-to-database call overhead when inserting multiple records. Actual performance depends on the dataset, database configuration, and system.

## 6. Algorithm

1. Create adversarial CSV test files.
2. Check for missing columns, wrong delimiters, empty files, and invalid encoding.
3. Create an SQLite database and insert sample station records.
4. Compare unsafe SQL string concatenation with parameterized queries.
5. Test sentiment analysis with sarcasm, double negation, and mixed sentiment.
6. Insert 1,000 records using `execute()` and `executemany()`.
7. Count inserted records and compare execution times.

## 7. Complexity Analysis

- CSV validation: O(n), where n is the number of CSV records.
- Sentiment analysis: O(w), where w is the number of words in a complaint.
- Individual insertion: O(n) database insertion operations.
- Batch insertion: O(n) records submitted through one `executemany()` call.

## 8. Files and Screenshots

- `adversarial_tests.py`
- `adversarial_data.csv`
- `missing_column.csv` – generated test input
- `empty.csv` – generated test input
- `invalid_encoding.csv` – generated test input
- `B2_CSV_Adversarial_Tests.png`
- `B2_SQL_Injection_Test.png`
- `B2_Adversarial_Sentiment.png`
- `B2_Execute_vs_Executemany.png`

## 9. Result

The adversarial tests successfully detected CSV input errors, demonstrated the risk of SQL injection, evaluated sentiment-analysis limitations, and compared SQLite insertion methods. Parameterized queries provided protection against the tested SQL injection input, and both insertion methods successfully stored 1,000 records.

## 10. Conclusion

The experiment demonstrated the importance of validating untrusted input, using parameterized SQL queries, testing AI applications with challenging examples, and evaluating database performance. The results also highlighted the limitations of simple rule-based sentiment analysis.