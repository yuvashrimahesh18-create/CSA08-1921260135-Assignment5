# B1 – Complete Data Cleaning Pipeline

**Student Name:** S.M Yuvashri  
**Register Number:** 1921260135  
**Course:** Python Programming  
**Assignment:** Assignment 5 – Data Acquisition, Cleaning, Analysis and AI Applications

## 1. Aim

To develop a Python-based air-quality data-cleaning pipeline that reads raw CSV data, identifies and handles data-quality problems, converts temperature units, stores cleaned readings in SQLite, and verifies the pipeline using a large dataset.

## 2. Problem Description

The city air-quality monitoring network collects readings from multiple monitoring stations. The raw data may contain missing values, invalid pollutant readings, duplicate records, and temperature values recorded in Fahrenheit.

The objective is to clean and standardise the data and store the valid records in a structured SQLite database.

## 3. Software and Libraries Used

- Python 3.15.0
- CSV module
- SQLite3 module
- pathlib module
- time module

## 4. Input Dataset

The input file is `raw_air_quality.csv`.

The dataset contains:
- Station ID
- Date
- Hour
- PM2.5
- PM10
- NO2
- Temperature
- Temperature unit

## 5. Data Cleaning Operations

| Data issue | Cleaning method |
|---|---|
| Missing values | Remove incomplete records |
| Invalid numeric values | Reject records containing invalid numbers |
| Negative pollutant values | Remove invalid records |
| Duplicate readings | Identify using station ID, date and hour |
| Fahrenheit temperature | Convert into Celsius |
| Valid readings | Retain in cleaned CSV |

### Fahrenheit Conversion

Temperature conversion formula:

°C = (°F − 32) × 5 / 9

## 6. SQLite Database

The cleaned records are stored in an SQLite database named `air_quality.db`.

The readings table contains:
- ID
- Station ID
- Date
- Hour
- PM2.5
- PM10
- NO2
- Temperature
- Temperature unit

The `executemany()` method is used for inserting multiple records efficiently.

A SQL `GROUP BY` query calculates station-wise average PM2.5 values.

## 7. Algorithm

1. Start the program.
2. Read the input CSV file.
3. Verify required columns.
4. Identify and remove missing records.
5. Convert numeric values.
6. Reject invalid and negative pollutant readings.
7. Convert Fahrenheit temperatures into Celsius.
8. Remove duplicate readings.
9. Save cleaned records into a new CSV file.
10. Create the SQLite database and readings table.
11. Insert cleaned records using `executemany()`.
12. Execute SQL queries to calculate station-wise averages.
13. Test the program with 1,200 readings.
14. Display the execution time and results.
15. Stop.

## 8. Test Results

### Data Cleaning Test

| Operation | Result |
|---|---:|
| Missing records removed | 1 |
| Invalid records removed | 1 |
| Duplicate records removed | 1 |
| Fahrenheit conversions | 2 |
| Cleaned records | 8 |
| Database readings | 8 |

### Station-wise Average PM2.5

| Station | Average PM2.5 |
|---|---:|
| S01 | 48.5 |
| S02 | 38.0 |
| S03 | 31.5 |
| S04 | 60.0 |
| S11 | 48.0 |
| S12 | 25.0 |

### Large Dataset Test

| Test | Result |
|---|---:|
| Generated readings | 1,200 |
| Readings stored in SQLite | 1,200 |
| Test status | Successful |

## 9. Performance and Complexity Analysis

Let n represent the number of input records.

- CSV reading and validation: O(n)
- Duplicate detection using a set: O(n) average
- CSV writing: O(n)
- SQLite batch insertion: O(n) overall
- Station-wise SQL aggregation: depends on the database query plan and number of records.

Using `executemany()` reduces repeated Python-to-SQLite execution overhead compared with executing each insertion separately.

## 10. Output Files

- `data_pipeline.py`
- `raw_air_quality.csv`
- `cleaned_air_quality.csv`
- `air_quality.db`
- `B1_Data_Cleaning_Output.png`
- `B1_Large_Dataset_Test.png`

## 11. Result

The data-cleaning pipeline was successfully implemented and tested. It removed missing, invalid, and duplicate readings, converted Fahrenheit temperatures into Celsius, stored the cleaned data in SQLite, and successfully inserted 1,200 records during the large dataset test.

## 12. Conclusion

The project demonstrates how Python's built-in CSV and SQLite modules can be used to build a reliable data-cleaning and storage pipeline. Batch insertion and SQL aggregation provide a practical approach for handling larger air-quality datasets.