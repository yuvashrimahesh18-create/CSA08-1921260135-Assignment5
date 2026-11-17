# B3 – Performance Comparison: Python Loops vs SQLite

**Student Name:** S.M Yuvashri  
**Register Number:** 1921260135  
**Assignment:** 5 – Data Acquisition, Cleaning, Analysis and AI Applications  
**Task:** B3 – Performance Comparison

## 1. Aim

To compare the performance of Python loops and SQLite GROUP BY for calculating daily average PM2.5 readings using datasets of different sizes.

## 2. Problem Description

The city air-quality monitoring network collects hourly readings from multiple monitoring stations. Daily average PM2.5 values must be calculated efficiently as the number of stations and readings increases.

This task compares Python dictionary-based loops with SQLite aggregation.

## 3. Tools and Libraries

- Python 3.15.0
- csv – generating CSV datasets
- sqlite3 – database operations and GROUP BY
- time – measuring execution time
- cProfile and pstats – profiling program execution
- collections.defaultdict – storing totals and counts

Pandas was considered as an alternative, but it could not be executed in the current Windows environment because of an Application Control policy blocking its required library.

## 4. Dataset Generation

The program generates 8760 hourly readings per station, representing one year.

| Number of stations | Total readings |
|---:|---:|
| 1 | 8,760 |
| 12 | 105,120 |
| 120 | 1,051,200 |

## 5. Methods Compared

### Method 1: Python Loops

- Uses dictionaries to store total PM2.5 and reading counts.
- Groups readings using station ID and day.
- Calculates daily averages using total divided by count.

### Method 2: SQLite GROUP BY

- Creates an SQLite readings table.
- Inserts records using executemany().
- Uses SQL GROUP BY to calculate daily averages.

## 6. Performance Results

| Stations | Readings | Python loops (seconds) | SQLite GROUP BY (seconds) |
|---:|---:|---:|---:|
| 1 | 8,760 | 0.0036 | 0.0154 |
| 12 | 105,120 | 0.0404 | 0.2554 |
| 120 | 1,051,200 | 0.2780 | 1.6724 |

Both methods produced the same number of daily groups.

## 7. Complexity Analysis

Let n represent the total number of readings.

- Python loops: O(n) time for aggregation and O(g) additional storage, where g is the number of station-day groups.
- SQLite GROUP BY: typically O(n log n) for grouping without a suitable index, with database-dependent performance and storage overhead.
- Dataset generation: O(n).

## 8. cProfile Analysis

The cProfile module was used to analyse the Python loop implementation with 12 stations.

Observed profiling result:

- Function analysed: calculate_using_loops()
- Function calls: 2
- Total execution time: approximately 0.029 seconds.

The profiler identified calculate_using_loops() as the main function in the measured workload.

## 9. Comparison and Discussion

In this particular in-memory benchmark, Python dictionary-based loops were faster than SQLite GROUP BY.

Python loops are simple and effective for direct aggregation in memory. SQLite is useful when data must be stored persistently, queried repeatedly, filtered, or shared across applications.

Pandas groupby() is another possible approach for data analysis, but it was not benchmarked because Pandas could not be loaded in this environment.

The results are specific to this program and computer; they do not prove that Python loops are always faster than SQL.

## 10. Result

Successfully generated datasets containing 8,760, 105,120, and 1,051,200 readings. Compared Python loops with SQLite GROUP BY and verified that both methods generated matching group counts. Used cProfile to inspect the Python aggregation function.

## 11. Conclusion

The experiment demonstrates how aggregation performance can change as dataset size increases. Python loops performed faster in this test, while SQLite provides persistent storage and flexible querying capabilities. The appropriate method depends on dataset size, storage requirements, and application needs.

## 12. Screenshot Files

1. B3_Performance_Comparison.png
2. B3_CProfile_Analysis.png