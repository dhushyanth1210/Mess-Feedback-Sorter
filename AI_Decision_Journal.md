# AI Decision Journal – Mess Feedback Sorter

## Project Overview
The Mess Feedback Sorter is a Python-based application that uses an LLM API to classify hostel mess feedback and identify urgent food safety complaints.

## Decision 1: Choosing the Domain
**Decision:** Food and hostel mess feedback.

**Reason:** Students regularly provide feedback about food taste, hygiene, quantity and serving time. Automatically organizing this feedback can help mess management identify important issues.

## Decision 2: Choosing the AI Model
**Decision:** Groq API with the `openai/gpt-oss-120b` model.

**Reason:** It supports an OpenAI-compatible API, allowing the model to be connected using the Python OpenAI library.

## Decision 3: Choosing Input and Output
**Decision:** CSV files.

**Reason:** CSV files are simple to read and process using Python. The application accepts feedback from `feedback.csv` and generates separate report files.

## Decision 4: Designing the Classification System
**Decision:** Five categories: taste, hygiene, quantity, timing and other. Three sentiments: positive, negative and neutral.

**Reason:** These labels help organize different types of student feedback consistently.

## Decision 5: Identifying Urgent Feedback
**Decision:** Urgent status is used for clear food safety risks.

**Reason:** Complaints involving insects, hair, spoiled food or students becoming sick require human attention. Python's safety net can increase urgency but cannot reduce it.

## Decision 6: Prompt Design
**Decision:** A structured system prompt using Authority, Exemplar, Constraint, Rubric and Metadata.

**Reason:** This gives the model clear instructions, examples, restrictions and output requirements. Tanglish examples were also included.

## Decision 7: Validation and Testing
**Decision:** Python validates the model's JSON response and retries invalid responses once. Failed responses are sent for manual review.

**Reason:** This reduces the chance of invalid data entering the final reports.

**Testing Evidence:**
- Evaluation tests: 5/5 passed.
- Red-team tests: 3/3 passed.

## Final Decision
The application combines AI classification with Python validation and human review. It is designed to support mess management, not replace human decisions.