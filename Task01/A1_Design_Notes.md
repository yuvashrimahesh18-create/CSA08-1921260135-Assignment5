# Task 1 – A1: Data Acquisition Design

## 1. Aim
To design a data acquisition system for a city air-quality monitoring network that collects air-quality readings from multiple monitoring stations, examines CSV data and stores the readings in an SQLite database.

## 2. Problem Description
The city air-quality monitoring network contains 12 monitoring stations. Each station collects hourly readings such as PM2.5, PM10, NO2 and temperature. The collected information is stored in CSV files.

The system must inspect the CSV data, identify its columns and records, and store station information and sensor readings in a structured SQLite database. The system should support future data cleaning, analysis and visualisation.

## 3. Data Acquisition and Quality Inspection

The sample CSV file contains the following fields:

| Field | Description |
|---|---|
| station_id | Unique monitoring station identifier |
| date | Date of measurement |
| hour | Hour of measurement |
| pm25 | PM2.5 concentration |
| pm10 | PM10 concentration |
| no2 | Nitrogen dioxide concentration |
| temperature | Recorded temperature |
| temperature_unit | Temperature unit (C or F) |

The Python CSV module is used to read the file and inspect its column names and records.

### Observations
- Total records in the sample CSV: 12
- Unique stations in the sample: 7
- Temperature readings use both Celsius and Fahrenheit.
- Sensor measurements are stored as text when initially read from CSV and must be converted into numeric values before analysis.
- The sample data represents only a small portion of the proposed 12-station monitoring network.

## 4. SQLite Database Design

Two tables are designed.

### Stations Table

| Column | Data type | Purpose |
|---|---|---|
| station_id | TEXT | Primary key identifying each station |

### Readings Table

| Column | Data type | Purpose |
|---|---|---|
| reading_id | INTEGER | Primary key |
| station_id | TEXT | Foreign key referencing stations |
| reading_date | TEXT | Measurement date |
| reading_hour | TEXT | Measurement hour |
| pm25 | REAL | PM2.5 value |
| pm10 | REAL | PM10 value |
| no2 | REAL | NO2 value |
| temperature | REAL | Recorded temperature |
| temperature_unit | TEXT | C or F |

The relationship between the tables is one-to-many: one monitoring station can have many readings.

## 5. CSV versus SQL

| CSV | SQL Database |
|---|---|
| Stores data in a plain-text file | Stores data in structured tables |
| Easy to create and share | Supports structured queries |
| Suitable for small datasets | Suitable for larger datasets |
| No built-in relational constraints | Supports primary and foreign keys |
| Searching may require scanning records | Indexes can improve searching |
| Concurrent updates are difficult to manage | Supports transactions |

CSV is suitable for collecting and exchanging sensor data. SQLite is suitable for structured storage, querying and analysis.

## 6. Pandas Full Scan versus Indexed SQL

| Operation | Pandas full scan | Indexed SQL |
|---|---|---|
| Load data | O(n) | Data already stored in database |
| Search one station | O(n) | Approximately O(log n) |
| Group and aggregate | O(n) | Generally O(n) without an index; index may help filtering |
| Memory usage | Often loads data into memory | Can retrieve only required records |

Here, n represents the number of records.

Pandas is convenient for in-memory data analysis. Indexed SQL is useful when the dataset is large and queries repeatedly select particular stations or dates.

## 7. Algorithm

1. Start the program.
2. Read the CSV file.
3. Inspect the column names.
4. Count and display the records.
5. Create an SQLite database.
6. Create the stations and readings tables.
7. Insert unique station identifiers.
8. Insert sensor readings using executemany().
9. Execute SQL queries to count stations and readings.
10. Calculate average PM2.5 for each station.
11. Display the results.
12. Close the database connection.
13. Stop.

## 8. SIMATS Standard Pseudocode

**Algorithm: AIR_QUALITY_DATA_ACQUISITION**

**Input:** Air-quality CSV file

**Output:** SQLite database containing station details and readings

BEGIN

1. OPEN the CSV file.
2. READ the column headings and all records.
3. DISPLAY the column headings.
4. COUNT the total number of records.
5. CONNECT to the SQLite database.
6. CREATE the Stations table if it does not exist.
7. CREATE the Readings table if it does not exist.
8. FOR each record in the CSV file:
   - INSERT the station identifier if it does not already exist.
9. END FOR
10. PREPARE all sensor reading records.
11. INSERT the readings using executemany().
12. COMMIT the database transaction.
13. EXECUTE SQL query to count stations.
14. EXECUTE SQL query to count readings.
15. EXECUTE GROUP BY query to calculate average PM2.5 per station.
16. DISPLAY the results.
17. CLOSE the database connection.

END

## 9. Result

The data acquisition program was successfully implemented and executed using Python's CSV and SQLite modules.

The sample CSV contained 12 records belonging to 7 unique monitoring stations. All 12 readings were inserted into the SQLite database successfully. The average PM2.5 concentration was calculated for each station using an SQL GROUP BY query.

## 10. Screenshots

1. A1_Data_Acquisition_Output.png – CSV inspection and record count.
2. A1_SQLite_Insertion_Output.png – Successful database insertion and station-wise PM2.5 averages.