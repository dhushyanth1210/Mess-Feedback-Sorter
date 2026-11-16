# MESS FEEDBACK SORTER
## Project Specification

### 1. Purpose
The Mess Feedback Sorter is a console-based Python application that organizes hostel mess feedback. It uses a Large Language Model through the Groq API to classify student comments based on category, sentiment, urgency and summary.

### 2. Input
The application reads student feedback comments from `feedback.csv`. Each comment is processed separately. Empty comments are not sent to the AI model and are marked for manual review.

### 3. Classification Rules
Each feedback comment is classified into one of the following categories:
- **Taste** – Food taste and quality.
- **Hygiene** – Cleanliness and food safety.
- **Quantity** – Food portion and availability.
- **Timing** – Food serving time.
- **Other** – Feedback that does not fit the above categories.

Sentiment must be classified as positive, negative or neutral.

The AI response must contain valid JSON with four fields: `category`, `sentiment`, `urgent` and `summary`. The `urgent` field must be Boolean (`true` or `false`). The summary must contain no more than 12 words.

### 4. Urgent Feedback Criteria
Feedback is marked urgent when it reports a possible food-safety issue, such as:
- Insects or foreign objects in food.
- Hair found in food.
- Stale, spoiled or expired food.
- Undercooked food.
- Students becoming sick after eating.

### 5. Safety Net and Validation
Python validates the AI response and checks for food-safety keywords. The safety net can increase the urgency level but must never reduce an urgent decision made by the AI. Invalid responses are retried once. If processing still fails, the comment is sent for manual review.

### 6. Expected Output and Human Checkpoint
The application generates three files:
- `results.csv` – Classified feedback.
- `urgent.csv` – Feedback marked as urgent.
- `summary.txt` – Overall feedback summary and category counts.

The warden or mess supervisor must read every comment in `urgent.csv`, verify the complaint and decide the necessary action. The AI only assists with classification; the final decision is made by a human.