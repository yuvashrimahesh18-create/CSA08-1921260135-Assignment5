# A4 – Debugging and Profiling

## Student Details
- **Name:** S.M yuvashri
- **Register Number:** 1921260135
- **Assignment:** Assignment 5 – Data Acquisition, Cleaning, Analysis and AI Applications
- **Task:** Task 04 – Debugging and Profiling

## Aim
To demonstrate Python debugging and profiling techniques for identifying invalid air-quality readings and measuring program execution performance.

## Problem Description
Air-quality monitoring data may contain missing PM2.5 readings and impossible negative values. Debugging techniques help identify these problems, while profiling tools measure the execution time and performance of the cleaning function.

## Tools and Techniques Used
1. **Print statements:** Display each station and its PM2.5 value during processing.
2. **Logging:** Record information, warnings, and invalid data conditions.
3. **Assertions:** Verify that cleaned PM2.5 values are non-negative.
4. **VS Code Debugger:** Supports breakpoints, variable inspection, and step-by-step execution.
5. **PDB:** Python's built-in interactive debugger.
6. **time.perf_counter():** Measures the execution time of the cleaning operation.
7. **timeit:** Measures repeated execution time.
8. **cProfile:** Profiles function calls and execution time.

## Algorithm
1. Start the program.
2. Read sample air-quality records.
3. Display each station and its PM2.5 value.
4. Log the processing information.
5. Skip missing readings.
6. Skip negative readings.
7. Validate retained values using assertions.
8. Store valid readings.
9. Measure execution time using perf_counter.
10. Measure repeated execution using timeit.
11. Profile the cleaning function using cProfile.
12. Display the results and stop.

## Test Data
The program uses six sample readings:
- Adyar – 48
- Guindy – 95
- Adyar – NA
- Guindy – -5
- Adyar – 60
- Guindy – 121

## Test Results
- Total sample records: 6
- Valid records retained: 4
- Missing readings skipped: 1
- Negative readings skipped: 1
- Assertion validation: Passed
- Profiling: Successfully executed using cProfile.

## Performance Analysis
- `time.perf_counter()` measures elapsed execution time.
- `timeit` measures repeated executions to provide a more reliable timing estimate.
- `cProfile` identifies function calls and their execution time.
- The latest profiling output reported 759 function calls in approximately 0.002 seconds. This value depends on the computer and execution environment.

## Complexity Analysis
Let n be the number of input readings.

- Cleaning operation: O(n), because each reading is examined once.
- Additional storage: O(n), because valid readings are stored in a list.
- Profiling overhead depends on the number of function calls.

## Alternative Approach
Without profiling tools, print statements and manual timing can be used. However, this approach provides less detailed performance information than timeit and cProfile.

## Result
The debugging and profiling program executed successfully. Missing and negative PM2.5 readings were identified and skipped. Valid readings passed assertion checks, and execution performance was measured using Python profiling tools.

## Screenshot
- A4_Debugging_and_Profiling.png