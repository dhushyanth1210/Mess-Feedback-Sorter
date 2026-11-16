# Mess Feedback Sorter

## Project Overview

Mess Feedback Sorter is a Python-based AI application that analyzes hostel mess feedback. It uses a Large Language Model (LLM) through the Groq API to classify student comments based on category, sentiment, urgency and a short summary.

## Problem Statement

Hostel mess receives different types of feedback from students. Manually reading and sorting every comment takes time. Important food safety complaints may also be missed.

## Objectives

- Automatically classify student feedback.
- Identify positive, negative and neutral sentiments.
- Detect urgent food safety complaints.
- Generate organized CSV and text reports.
- Support faster manual feedback review.

## Technologies Used

- Python
- Groq API
- OpenAI Python SDK
- CSV
- JSON
- python-dotenv

## Categories

- Taste
- Hygiene
- Quantity
- Timing
- Other

## Sentiment

- Positive
- Negative
- Neutral

## Project Files

| File | Purpose |
|---|---|
| main.py | Main Python application |
| feedback.csv | Input feedback data |
| system_prompt.txt | AI classification instructions |
| Specification.md | Project specification |
| Judgment Framework.md | AI and human decision responsibilities |
| Cost & Latency Note.md | API cost and processing-time considerations |
| AI_Decision_Journal.md | Records important project decisions |
| Reflection.md | Project learning and reflection |
| evaluation_results.csv | Evaluation test results |
| redteam_results.csv | Red-team test results |
| results.csv | Classified feedback output |
| urgent.csv | Urgent feedback output |
| summary.txt | Feedback statistics |
| .gitignore | Files excluded from Git |

## How It Works

1. Reads feedback from `feedback.csv`.
2. Skips empty comments.
3. Sends non-empty comments to the Groq LLM API.
4. Receives classification in JSON format.
5. Validates the AI response.
6. Retries invalid responses once.
7. Applies a Python safety net for possible food safety complaints.
8. Sends failed classifications for manual review.
9. Generates `results.csv`, `urgent.csv` and `summary.txt`.

## Safety and Human Review

The Python safety net checks for possible food safety issues such as insects, foreign objects, spoiled food and sickness after eating.

The safety net can increase urgency but cannot reduce an urgent decision made by the AI.

The warden or mess supervisor must review every comment in `urgent.csv` and decide the appropriate action. AI classification is only a support tool.

## Testing

The project includes:

- 5 evaluation test cases.
- 3 red-team test cases.
- JSON response validation.
- Empty feedback handling.
- Manual review fallback.

Recorded test results: Evaluation 5/5 passed and Red-team 3/3 passed.

## How to Run

### 1. Install Dependencies

```bash
pip install openai python-dotenv
```

### 2. Configure API Key

Create a local `.env` file in the project folder:

```text
GROQ_API_KEY=your_api_key
```

Never upload `.env` or expose your API key.

### 3. Run the Application

```bash
python main.py
```

### 4. Run Evaluation Tests

```bash
python main.py --test
```

### 5. Run Red-Team Tests

```bash
python main.py --redteam
```

## Limitations

- AI classification may occasionally be incorrect.
- API availability and response time may vary.
- API usage may involve costs depending on token consumption.
- Urgent complaints require human verification.

## Conclusion

Mess Feedback Sorter helps organize hostel mess feedback through AI-based classification, sentiment analysis, urgency detection and automated report generation. It combines AI capabilities with Python validation and human review to support better feedback management.