# A2 – Data Cleaning and Normalisation

**Student Name:** Mahesh Sivaraman  
**Register Number:** 1921260135  
**Assignment:** Assignment 5 – Data Acquisition, Cleaning, Analysis and AI Applications

## 1. Aim

To clean and preprocess air-quality monitoring data by handling missing values, invalid readings, duplicate records and different temperature units. To apply Min-Max Normalisation and Z-Score Standardisation to PM2.5 readings.

## 2. Problem Description

The city air-quality monitoring network collects readings from multiple monitoring stations. The collected CSV data may contain missing values, duplicate records, impossible pollutant values and temperature readings in Fahrenheit.

These problems must be handled before the data is used for analysis.

## 3. Data Cleaning Rules

| Data issue | Cleaning method |
|---|---|
| Missing numeric readings | Remove the incomplete record |
| Duplicate readings | Identify using station ID, date and hour |
| Negative pollutant values | Reject the invalid record |
| Fahrenheit temperature | Convert to Celsius |
| Celsius temperature | Retain in Celsius |
| Numeric values | Convert to floating-point values |

The program standardises all retained temperature readings to Celsius.

## 4. Fahrenheit to Celsius Conversion

The conversion formula is:

Celsius = (Fahrenheit - 32) × 5 / 9

After conversion, the temperature unit is stored as C.

## 5. Normalisation Techniques

### 5.1 Min-Max Normalisation

Min-Max Normalisation scales values into a range between 0 and 1.

Formula:

Normalized Value = (Value - Minimum) / (Maximum - Minimum)

This method makes values easier to compare on a common scale.

### 5.2 Z-Score Standardisation

Z-Score Standardisation measures how far a value is from the mean in terms of standard deviations.

Formula:

Z = (Value - Mean) / Standard Deviation

Positive values indicate readings above the mean, while negative values indicate readings below the mean.

## 6. Algorithm

1. Start the program.
2. Read the input CSV file.
3. Identify missing numeric readings.
4. Remove records containing missing values.
5. Identify and remove duplicate readings.
6. Validate pollutant values and reject negative readings.
7. Convert Fahrenheit temperatures into Celsius.
8. Store the cleaned records.
9. Calculate Min-Max normalised PM2.5 values.
10. Calculate Z-Score standardised PM2.5 values.
11. Save the cleaned records into a new CSV file.
12. Display the cleaning summary and results.
13. Stop the program.

## 7. Complexity Analysis

Let n represent the number of input records.

- Reading and checking records: O(n)
- Duplicate detection using a set: O(n) average time
- Min-Max Normalisation: O(n)
- Z-Score Standardisation: O(n)
- Overall time complexity: O(n)
- Space complexity: O(n)

The program stores cleaned records and intermediate values in memory.

## 8. Alternative Approaches

Instead of removing incomplete records, missing numeric values could be replaced using the mean or median of valid readings.

For duplicate detection, a database table with a unique constraint on station ID, date and hour could also be used.

For larger datasets, processing records in batches can reduce memory usage.

## 9. Test Results

The sample input contained 12 records.

| Test condition | Result |
|---|---:|
| Original records | 12 |
| Missing records removed | 1 |
| Invalid records removed | 1 |
| Duplicate records removed | 1 |
| Fahrenheit conversions | 3 |
| Final cleaned records | 9 |

Both Min-Max Normalisation and Z-Score Standardisation were successfully performed on PM2.5 readings.

## 10. Output Files and Screenshots

- `cleaning.py` – Python cleaning and normalisation program.
- `cleaning_sample.csv` – Input dataset