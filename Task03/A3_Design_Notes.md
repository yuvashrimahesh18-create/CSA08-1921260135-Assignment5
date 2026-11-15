# Task 3 – Data Analysis and Visualisation (A3)

**Student Name:** Mahesh Sivaraman  
**Register Number:** 1921260135  
**Course Outcome:** CO5

## 1. Aim
To analyse cleaned air-quality data using Python and SQLite and generate visualisations to understand pollution trends, station-wise pollution levels, and the relationship between temperature and PM2.5.

## 2. Problem Description
The city air-quality monitoring network collects readings from multiple stations. The collected data must be analysed to identify daily pollution levels, compare stations, examine temperature relationships, and identify hours with higher PM2.5 concentrations.

## 3. Tools and Technologies
- Python 3.15.0
- SQLite3
- CSV module
- Matplotlib 3.11.2
- VS Code

## 4. Analysis Performed
1. Imported cleaned air-quality readings from Task 2.
2. Stored the readings in an SQLite database.
3. Calculated daily averages for PM2.5, PM10, and NO2.
4. Compared average PM2.5 levels across monitoring stations.
5. Calculated average PM2.5 values by hour and identified the highest average hour.

## 5. Visualisations Generated
- PM2.5 Trend – shows PM2.5 readings across the collected records.
- Station Comparison – compares average PM2.5 levels across stations.
- Temperature Relationship – examines the relationship between temperature and PM2.5.
- PM2.5 Histogram – displays the distribution of PM2.5 readings.
- Station Boxplot – compares the distribution and spread of PM2.5 readings.

## 6. SQL Operations
The program uses SQL `CREATE TABLE`, `INSERT`, and `SELECT` statements. It uses `GROUP BY` and aggregate functions such as `COUNT()` and `AVG()` to summarise the readings.

## 7. Algorithm
1. Read the cleaned CSV file.
2. Connect to SQLite and create the readings table.
3. Insert the cleaned records using `executemany()`.
4. Execute SQL queries for daily, station-wise, and hourly summaries.
5. Extract the required values for visualisation.
6. Generate and save five charts using Matplotlib.
7. Display the analysis results.

## 8. Complexity Analysis
- Reading N CSV records: O(N).
- Inserting N records: O(N) for the batch operation, excluding database index overhead.
- Grouping and aggregating N records: approximately O(N) for a full scan, with database overhead.
- Generating charts: depends on the number of records and chart type; most plotted data preparation is O(N).

SQL `GROUP BY` is useful for performing aggregation within the database instead of manually calculating every group in Python.

## 9. Result
The cleaned air-quality data was successfully analysed using Python and SQLite. Daily averages, station-wise PM2.5 comparisons, and hourly averages were calculated. Five visualisation charts were generated successfully.

## 10. Output Files
- `air_quality_analysis.db`
- `A3_PM25_Trend.png`
- `A3_Station_Comparison.png`
- `A3_Temperature_Relationship.png`
- `A3_PM25_Histogram.png`
- `A3_Station_Boxplot.png`

## 11. Conclusion
The analysis successfully summarised the cleaned air-quality readings and presented the results through five charts. SQLite aggregation and Matplotlib visualisations helped identify pollution patterns and compare monitoring stations.