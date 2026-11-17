# B4 – Final Engineering Decision and AI Evaluation

**Student Name:** S.M Yuvashri  
**Register Number:** 1921260135  
**Assignment:** Assignment 5 – Data Acquisition, Cleaning, Analysis and AI Applications  
**Task:** Task09 – Part B4

## 1. Aim

To evaluate sentiment analysis and text summarisation using citizen complaints, measure SQLite query performance before and after indexing, and make an engineering decision for a larger air-quality monitoring network.

## 2. Problem Description

The city air-quality monitoring network is expected to expand by 100 additional monitoring stations. Each new station reports readings every 15 minutes. The system must process a large number of sensor readings and approximately 50,000 citizen complaints per month.

The task evaluates AI-based complaint analysis, database indexing, summarisation methods, and production-level scalability.

## 3. Sentiment Analysis of 50 Citizen Complaints

A keyword-based sentiment analysis system was implemented using Python.

### Methodology

- Positive words receive a score of +1.
- Negative words receive a score of -1.
- Negation words such as "not", "never", and "no" reverse the score of the following recognised sentiment word.
- A positive total is classified as Positive.
- A negative total is classified as Negative.
- A zero total is classified as Neutral.

### Test Results

| Metric | Result |
|---|---:|
| Total complaints | 50 |
| Agreements | 50 |
| Disagreements | 0 |
| Manual agreement | 100% |

All 50 predictions matched the reference labels used in the program.

### Limitations

The keyword-based method cannot fully understand sarcasm, complex sentence structures, or contextual meaning. For example, a sarcastic complaint may contain positive words but express a negative opinion.

A trained machine-learning sentiment model could improve contextual understanding.

## 4. Text Summarisation Comparison

Two summarisation approaches were implemented and tested using all 50 complaints.

### A. Extractive Summarisation

- Counts important words in the complete complaint text.
- Calculates sentence importance using keyword frequency.
- Selects the five highest-ranked sentences.
- Preserves the original sentences.

Execution time: **0.001066 seconds**

### B. First-K Summarisation

- Selects the first five sentences.
- Does not calculate sentence importance.
- Provides a simple and fast summarisation method.

Execution time: **0.000071 seconds**

### Comparison

| Feature | Extractive Method | First-K Method |
|---|---|---|
| Selection | Important words | First five sentences |
| Processing | Examines complete text | Stops after five sentences |
| Relevance | Uses keyword frequency | Depends on sentence order |
| Execution time | 0.001066 s | 0.000071 s |

### Observation

The extractive method considers the importance of words across all complaints. The First-K method is faster but may miss important information appearing later in the text.

Therefore, extractive summarisation is more suitable when important information must be selected from a larger collection of complaints.

## 5. SQLite Index Performance

A SQLite database containing 36,500 records was generated using 100 stations and 365 days of readings.

A query was executed 500 times before and after creating a composite index on station and day.

### SQL Index

```sql
CREATE INDEX idx_station_day
ON readings(station, day);
```

### Performance Results

| Measurement | Execution Time |
|---|---:|
| Before indexing | 1.126226 seconds |
| After indexing | 0.001569 seconds |

### Observation

The indexed query executed considerably faster than the query without an index.

The composite index improves retrieval when searching using both station and day.

An index requires additional storage and maintenance during data insertion, but it can significantly improve repeated search operations.

## 6. Production Engineering Decision

The monitoring network plans to add 100 stations reporting every 15 minutes.

### Data Volume Calculation

Readings per station per day:

96 readings

Additional readings per day:

100 × 96 = 9,600 readings

Additional readings per month:

9,600 × 30 = 288,000 readings

Existing 12 stations reporting hourly:

12 × 24 = 288 readings per day

Total daily readings, including existing stations:

9,600 + 288 = 9,888 readings

Expected citizen complaints:

50,000 per month.

### Production Recommendations

1. Store air-quality readings in SQLite with suitable indexes.
2. Validate and clean incoming CSV data before database insertion.
3. Use SQL GROUP BY for daily and monthly reports.
4. Use charts to monitor pollution trends.
5. Use a trained sentiment model for large complaint volumes.
6. Review uncertain sentiment predictions manually.
7. Retain keyword-based sentiment rules as a baseline and fallback.
8. Monitor database performance as the number of stations increases.

## 7. Algorithm

1. Read the 50 citizen complaints.
2. Calculate sentiment scores using positive and negative keywords.
3. Apply negation handling.
4. Compare predicted sentiment with reference labels.
5. Calculate the agreement percentage.
6. Generate an extractive summary using important-word frequency.
7. Generate a First-K summary using the first five sentences.
8. Compare summarisation execution times.
9. Create an SQLite readings table.
10. Insert 36,500 sample records.
11. Measure query execution time before indexing.
12. Create a composite index on station and day.
13. Measure query execution time after indexing.
14. Calculate future data requirements.
15. Print production engineering recommendations.

## 8. Complexity Analysis

| Operation | Time Complexity |
|---|---|
| Sentiment analysis | O(W) per complaint |
| Sentiment analysis for C complaints | O(C × W) |
| Extractive summarisation | O(W + S log S) |
| First-K summarisation | O(W) for this implementation |
| Database index creation | Approximately O(N log N) |
| Indexed database lookup | Approximately O(log N + R) |

Where:

- W = Number of words
- C = Number of complaints
- S = Number of sentences
- N = Number of database records
- R = Number of matching records

## 9. Screenshots

The following screenshots are included:

1. `B4_Sentiment_Analysis.png`
2. `B4_Summary_and_Index_Performance.png`

The second screenshot contains both the summarisation comparison and SQLite index performance results.

## 10. Result

The B4 program executed successfully.

Sentiment analysis was tested on 50 complaints with 100% agreement against the supplied reference labels. Extractive and First-K summarisation methods were compared using all 50 complaints. SQLite indexing improved the measured query execution time from 1.126226 seconds to 0.001569 seconds.

The production decision demonstrates how the monitoring system can accommodate 100 additional stations and 50,000 citizen complaints per month.

## 11. Conclusion

The experiment demonstrates the importance of sentiment analysis, text summarisation, database indexing, and performance evaluation in a growing air-quality monitoring network.

A combination of data cleaning, indexed database storage, SQL analysis, visualisation, and trained AI models is recommended for future production deployment.
