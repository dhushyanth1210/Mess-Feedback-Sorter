# Mess Feedback Sorter

## Project Overview
Mess Feedback Sorter is a Python-based AI application that automatically analyzes hostel mess feedback. It classifies student comments based on category, sentiment, and urgency using an LLM API.

## Problem Statement
Hostel mess receives different types of feedback from students. Manually reading and sorting every comment takes time. Important food safety complaints may also be missed.

## Objectives
- Automatically classify student feedback.
- Identify positive, negative, and neutral sentiments.
- Detect urgent food safety complaints.
- Generate organized CSV and text reports.
- Reduce manual feedback analysis.

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
| results.csv | Classified feedback |
| urgent.csv | Urgent feedback |
| summary.txt | Feedback statistics |
| evaluation_results.csv | Evaluation test results |
| redteam_results.csv | Red-team test results |
| .env | API key configuration |
| .gitignore | Files excluded from Git |

## How It Works
1. Reads feedback from feedback.csv.
2. Sends each non-empty comment to the Groq LLM API.
3. Receives classification in JSON format.
4. Validates the AI response.
5. Applies a safety net for health-related complaints.
6. Generates results.csv, urgent.csv, and summary.txt.
7. Sends invalid or empty feedback for manual review.

## Testing
- Evaluation tests: 5/5 passed.
- Red-team tests: 3/3 passed.

## How to Run

Install dependencies:

```bash
pip install openai python-dotenv pandas
```

Run the application:

```bash
python main.py
```

Run evaluation tests:

```bash
python main.py --test
```

Run red-team tests:

```bash
python main.py --redteam
```

## API Configuration
Create a .env file and add your own Groq API key:

```text
GROQ_API_KEY=your_api_key
```

Never upload the .env file or expose your API key.

## Limitations
- AI classification may occasionally be incorrect.
- Urgent complaints require human verification.
- API availability and response time may vary.
## Security and Human Review

- API keys are stored in the `.env` file.
- The `.env` file is excluded using `.gitignore`.
- Invalid AI responses are sent for manual review.
- Urgent food safety complaints require human verification.
- AI classification supports decision-making but does not replace human judgment.
## Conclusion
Mess Feedback Sorter helps organize hostel mess feedback through AI-based classification, sentiment analysis, urgency detection, and automated report generation. It supports faster review and helps staff identify important food safety complaints.
