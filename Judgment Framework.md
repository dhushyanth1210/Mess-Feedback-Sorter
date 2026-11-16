# Judgment Framework – Mess Feedback Sorter

## 1. Purpose

The Mess Feedback Sorter uses an LLM to classify student mess feedback. Python validates the results and applies safety rules. The tool only organizes feedback. The warden makes the final decisions.

## 2. Decision-Making Framework

| Part of the Tool | What decision is made? | Who or what makes the decision? | Who checks the decision? |
|---|---|---|---|
| Category | Which category does the feedback belong to? | LLM | Python validates the category; a person can review doubtful cases. |
| Sentiment | Is the feedback positive, negative, or neutral? | LLM | Python checks whether the value is valid. |
| Urgent flag | Does the comment mention a possible health risk? | LLM and Python safety net | Warden checks every comment in urgent.csv. |
| Summary | What is the main point of the comment in 12 words or fewer? | LLM | Python checks the word limit. |
| JSON validation | Does the LLM response contain the correct fields and values? | Python | The program retries once and sends failed responses for manual review. |
| Empty comment | Should an empty comment be sent to the LLM? | Python | The program directly marks it for manual review. |
| Final action | What should be done about the feedback? | Warden | The warden is responsible for the final decision. |

## 3. Special Attention: Urgent Flag

The urgent flag is used only for possible health-related risks, such as insects in food, hair in food, expired or spoiled food, undercooked food, or students becoming sick after eating.

Taste, quantity, and timing complaints must not be marked urgent just because the student is angry.

The LLM initially identifies whether a comment is urgent. Python then checks for known health-risk keywords. If a keyword is found, Python can change the urgent flag from false to true.

The safety net can only increase urgency. It cannot change an urgent result from true to false.

## 4. Human Checkpoint

The warden must read every comment in `urgent.csv` and decide what action is required. The tool does not automatically take action against the mess staff or make food-safety decisions.

Comments that fail validation are marked for manual review instead of being treated as successfully classified.

## 5. Responsibility

The LLM is responsible for suggesting classifications. Python is responsible for validation, safety checks, and counting. The warden is responsible for reviewing urgent feedback and deciding the next action.

**Final principle:** AI assists with organizing feedback, but humans remain responsible for important decisions.