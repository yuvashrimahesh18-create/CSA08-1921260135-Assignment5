# A5 – AI Applications for Air-Quality Monitoring

## Student Details
- **Name:** S.M Yuvashri
- **Register Number:** 1921260135
- **Assignment:** Assignment 5 – Data Acquisition, Cleaning, Analysis and AI Applications
- **Task:** Task05 – AI Applications

## Aim
To develop simple AI-based applications for analysing citizen air-quality complaints using sentiment analysis, extractive text summarisation, and a keyword-based chatbot.

## Problem Description
Citizens submit complaints about air pollution, smoke, dust, and poor air quality. Manually analysing a large number of complaints is time-consuming. Basic natural language processing techniques can help classify complaints, identify important information, and answer common questions.

## 1. Sentiment Analysis

A lexicon-based approach is used to classify complaints into three categories:

- **Positive:** Contains favourable words such as clean, fresh, good, and safe.
- **Negative:** Contains unfavourable words such as polluted, harmful, dirty, and unhealthy.
- **Neutral:** Positive and negative scores are equal.

Negation handling is included for words such as "not", "no", and "never".

### Test Results
| Complaint | Expected sentiment | Result |
|---|---|---|
| The air is clean and fresh today. | Positive | Positive |
| The area is polluted with harmful smoke. | Negative | Negative |
| The air quality is not good. | Negative | Negative |
| The air quality is not bad. | Positive | Positive |
| The weather is normal today. | Neutral | Neutral |

## 2. Extractive Text Summarisation

The summarisation function divides a complaint into sentences and assigns scores based on the occurrence of important air-quality keywords.

The sentences with the highest scores are selected to form a short summary.

### Important Keywords
- Pollution
- Air
- PM2.5
- Smoke
- Dust
- Health
- Quality
- Harmful

### Result
The program selected two important sentences:

1. PM25 levels are harmful to public health.
2. Air pollution is increasing near the main road.

## 3. Keyword-Based Chatbot

The chatbot checks user questions for keywords and returns predefined answers.

### Test Results
| User question | Chatbot response |
|---|---|
| What is PM2.5? | Explains fine particles and their health effects |
| Tell me about air pollution | Provides information about air pollution |
| How does pollution affect health? | Explains respiratory and other health problems |
| What is a monitoring station? | Explains the monitoring network |
| What is the capital of India? | Returns an unknown-question response |

## Algorithm
1. Start the program.
2. Define positive and negative word lists.
3. Read citizen complaints.
4. Calculate positive and negative sentiment scores.
5. Apply basic negation handling.
6. Classify each complaint.
7. Split complaint text into sentences.
8. Score sentences using important keywords.
9. Select the highest-scoring sentences.
10. Read chatbot questions.
11. Match keywords and return suitable responses.
12. Display all results and stop.

## Complexity Analysis
Let n represent the number of words in a complaint and s represent the number of sentences.

- Sentiment analysis: O(n) average time using set-like keyword lookup; the current implementation uses lists, so lookup adds a lexicon-size factor.
- Text summarisation: O(n + s log s) time because sentence scores are calculated and sentences are sorted.
- Chatbot: O(1) with respect to question length for a fixed number of keyword checks, excluding the cost of scanning the question string.

## Alternative AI Approach
A machine-learning sentiment classifier could be trained using labelled citizen complaints. It may recognise context and complex language better than a fixed word list, but it requires a labelled dataset, training, testing, and additional computational resources.

A trained language model could also produce more natural summaries and chatbot responses. However, the keyword-based approach is simple, explainable, and suitable for a small demonstration.

## Result
The program successfully demonstrated sentiment classification, basic negation handling, extractive text summarisation, and keyword-based chatbot responses using Python.

## Screenshot
- A5_AI_Applications_Output.png