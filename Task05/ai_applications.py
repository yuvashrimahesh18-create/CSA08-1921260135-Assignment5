
# Task 05 - AI Applications
# Sentiment Analysis of Citizen Air-Quality Complaints

def analyse_sentiment(complaint):
    """Classify a complaint as Positive, Negative, or Neutral."""

    positive_words = ["good", "clean", "fresh", "improved", "better", "safe"]
    negative_words = ["bad", "polluted", "dirty", "smoke", "dust", "harmful",
                      "poor", "unhealthy", "terrible"]

    words = complaint.lower().replace(".", "").replace(",", "").split()

    positive_score = 0
    negative_score = 0
    negation_words = ["not", "no", "never"]

    for index, word in enumerate(words):
        # Check whether the current word is affected by negation
        negated = index > 0 and words[index - 1] in negation_words

        if word in positive_words:
            if negated:
                negative_score += 1
            else:
                positive_score += 1

        elif word in negative_words:
            if negated:
                positive_score += 1
            else:
                negative_score += 1

    if positive_score > negative_score:
        return "Positive"
    elif negative_score > positive_score:
        return "Negative"
    else:
        return "Neutral"


# Test complaints
complaints = [
    "The air is clean and fresh today.",
    "The area is polluted with harmful smoke.",
    "The air quality is not good.",
    "The air quality is not bad.",
    "The weather is normal today."
]

print("SENTIMENT ANALYSIS RESULTS")

for complaint in complaints:
    result = analyse_sentiment(complaint)
    print(f"Complaint: {complaint}")
    print(f"Sentiment: {result}\n")

# Extractive Text Summarisation

def extractive_summary(text, number_of_sentences=2):
    """Select the most important sentences using keyword frequency."""

    sentences = text.split(".")

    keywords = [
        "pollution", "air", "pm25", "smoke",
        "dust", "health", "quality", "harmful"
    ]

    sentence_scores = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            score = 0
            words = sentence.lower().split()

            for word in words:
                if word.strip(",.!?") in keywords:
                    score += 1

            sentence_scores.append((score, sentence))

    sentence_scores.sort(key=lambda item: item[0], reverse=True)

    selected = sentence_scores[:number_of_sentences]

    return ". ".join(sentence for score, sentence in selected)


# Test summarisation
complaint_text = (
    "The city is crowded today. "
    "Air pollution is increasing near the main road. "
    "PM25 levels are harmful to public health. "
    "People are enjoying the weekend."
)

print("\nEXTRACTIVE TEXT SUMMARISATION")
print("Original complaint:")
print(complaint_text)

print("\nSummary:")
print(extractive_summary(complaint_text))

# Keyword-Based Air Quality Chatbot

def air_quality_chatbot(question):
    """Answer common air-quality questions using keywords."""

    question = question.lower()

    if "pm25" in question or "pm2.5" in question:
      return "PM2.5 refers to fine particles that can affect human health."

    elif "health" in question:
      return "Poor air quality can cause respiratory and other health problems."

    elif "pollution" in question or "air quality" in question:
      return "Air pollution should be monitored regularly to protect public health."

    elif "station" in question:
      return "The monitoring network collects readings from multiple stations."

    elif "temperature" in question:
        return "Temperature readings help analyse environmental conditions."

    else:
        return "Sorry, I do not have an answer for that question."


# Test chatbot
print("\nAIR QUALITY CHATBOT")

questions = [
    "What is PM2.5?",
    "Tell me about air pollution",
    "How does pollution affect health?",
    "What is a monitoring station?",
    "What is the capital of India?"
]

for question in questions:
    print("User:", question)
    print("Chatbot:", air_quality_chatbot(question))
    print()
