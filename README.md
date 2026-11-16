# Messly — AI-Powered Hostel Mess Feedback Sorter

**Messly** is a Python-based hostel mess feedback management project with a Streamlit web interface and a console-based reporting workflow. It uses an LLM through the Groq API to classify feedback by **category**, **sentiment**, and **urgency**, then supports human review of potentially important food-safety complaints.

## Problem Statement

Hostel mess committees receive feedback about taste, cleanliness, portion sizes, and serving times. Reading every comment manually takes time, and urgent food-safety concerns may be overlooked among routine suggestions.

## Objectives

- Classify feedback into consistent categories and sentiments.
- Flag potentially urgent food-safety concerns for human review.
- Accept feedback in English, Tamil, and Tanglish through the web interface.
- Produce CSV and text reports for the mess committee.
- Support manual review rather than treating AI decisions as final.

## Technologies Used

- **Python** — application logic and validation
- **Groq API + OpenAI Python SDK** — LLM classification
- **Streamlit** — Messly web interface
- **SQLite** — local storage for web submissions
- **CSV and JSON** — input, output, and structured AI responses
- **python-dotenv** — local API key configuration
- **HTML/CSS** — custom Streamlit styling

## Classification

| Field | Possible values |
|---|---|
| Category | `taste`, `hygiene`, `quantity`, `timing`, `other` |
| Sentiment | `positive`, `negative`, `neutral` |
| Urgency | `true` / `false` |

The classifier also provides a short summary. The application applies additional Python checks and uses manual review when classification is unavailable or invalid.

## Messly Web Application

### Student Portal

- Select a meal: Breakfast, Lunch, Snacks, or Dinner.
- Submit feedback in English, Tamil, or Tanglish.
- Validate input before sending it for classification.
- Classify comments by category, sentiment, and urgency.
- Highlight possible food-safety risks and show a feedback reference ID.

### Admin Area

- Password-protected dashboard.
- Feedback totals, category and sentiment charts, and urgent-alert counts.
- Search and filter feedback by category, status, and priority.
- Accept, reject, or mark local submissions for manual review.
- Export filtered feedback as CSV.

Web submissions are stored locally in `ui_feedback.db`. Existing console reports can be viewed by the interface without being overwritten by web submissions.

## Project Files

| File | Purpose |
|---|---|
| `main.py` | Console workflow, LLM classification, validation, and safety checks |
| `app.py` | Streamlit student and admin interface |
| `messly_logo.png` | Messly branding image used by `app.py` |
| `system_prompt.txt` | AI classification instructions |
| `feedback.csv` | Sample/input feedback for console processing |
| `results.csv` | Classified console feedback |
| `urgent.csv` | Urgent console feedback |
| `summary.txt` | Console feedback statistics |
| `evaluation_results.csv` | Recorded evaluation results |
| `redteam_results.csv` | Recorded red-team test results |
| `Specification.md` | Project specification |
| `Judgment Framework.md` | AI and human decision responsibilities |
| `Cost & Latency Note.md` | API cost and latency considerations |
| `AI_Decision_Journal.md` | Project decisions and rationale |
| `Reflection.md` | Project reflection |
| `.gitignore` | Excludes local secrets and generated/private files |

`ui_feedback.db` and `.env` are **local-only** and must not be committed.

## How It Works

### Console Workflow

1. Read records from `feedback.csv`.
2. Skip empty comments and send suitable feedback to the Groq LLM API.
3. Parse and validate the structured JSON response.
4. Retry an invalid response once.
5. Apply Python safety checks for possible food-safety complaints.
6. Route unsuccessful classifications for manual review.
7. Write `results.csv`, `urgent.csv`, and `summary.txt`.

### Web Workflow

1. A student selects a meal, language, and enters feedback.
2. The interface validates the input.
3. The backend classifies the feedback and applies safety checks.
4. The result is saved to the local SQLite database.
5. An authorized admin reviews submissions and exports reports as needed.

## Installation and Running

### 1. Requirements

Install Python and open a terminal in the project folder.

```bash
pip install streamlit openai python-dotenv
```

### 2. Configure the Groq API key

Create a local `.env` file beside `main.py`:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

**Never upload `.env` or share your real API key.**

For the admin area, configure the `MESS_ADMIN_PASSWORD` environment variable before launching Streamlit. For example, in Windows PowerShell:

```powershell
$env:MESS_ADMIN_PASSWORD = "choose_a_strong_password"
```

The application reads this variable from its environment; putting it in `.env` alone is not sufficient unless your environment loads it.

### 3. Run the Messly website

```bash
streamlit run app.py
```

Open the local address displayed by Streamlit in your browser.

### 4. Run the console application

```bash
python main.py
```

### 5. Run evaluation and red-team tests

```bash
python main.py --test
python main.py --redteam
```

## Safety and Human Review

The Python safety net checks for possible food-safety risks, including foreign objects, spoiled food, undercooked food, and illness-related complaints. The safety checks are intended to prevent important complaints from being missed, but automatic detection can still make mistakes.

Urgent feedback must be verified by a human mess supervisor or warden. The system **supports** decisions; it does not make final health or disciplinary decisions.

## Testing

The repository contains recorded results for:

- **5 evaluation test cases** — recorded as 5/5 passed.
- **3 red-team test cases** — recorded as 3/3 passed.
- Structured-response validation and manual-review fallback.

These are recorded project results, not a guarantee that every possible input or future API response will be handled correctly. The deployed web interface and live API should be tested separately.

## Privacy and Security

- Store the Groq API key in local environment configuration, not in source code.
- Do not commit `.env`, `ui_feedback.db`, virtual environments, or personal student feedback.
- Review CSV exports before publishing them; sample and report data may contain user-provided comments.
- Protect admin access with a strong password.

## Limitations

- AI classification can be inaccurate or inconsistent.
- API availability, response time, and usage costs may vary.
- Input validation cannot perfectly determine whether feedback is genuine.
- Local SQLite storage is suitable for a project demonstration but is not a substitute for a production deployment plan.
- Urgent concerns require human verification and action.

## Conclusion

Messly combines LLM-assisted classification, Python validation, a food-safety checking layer, and a Streamlit interface to help organize hostel mess feedback. It is designed to make routine feedback easier to review while keeping people responsible for important decisions.
