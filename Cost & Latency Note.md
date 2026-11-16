# Cost & Latency Note – Mess Feedback Sorter

## 1. Model Used

- Provider: Groq
- Model: `openai/gpt-oss-120b`
- API: Groq API using the OpenAI-compatible client

## 2. Number of API Calls

The project processes 50 feedback comments.

- Each non-empty comment normally requires one API call.
- If the response is invalid, the program retries once.
- If the retry also fails, the comment is marked for manual review.
- Empty comments are not sent to the API.

Therefore:

| Situation | API calls |
|---|---:|
| Normal processing of 50 non-empty comments | 50 |
| If all 50 comments need one retry | Maximum 100 |

## 3. Estimated API Cost

Groq's published price for GPT-OSS 120B is:

- Input: $0.15 per 1 million tokens
- Output: $0.60 per 1 million tokens

For a simple estimate, assume each feedback request uses:
- 1,000 input tokens, including the system prompt and comment.
- 100 output tokens for the classification response.

For 50 comments:

| Token type | Total tokens | Estimated cost |
|---|---:|---:|
| Input | 50,000 | $0.0075 |
| Output | 5,000 | $0.0030 |
| **Total** | **55,000** | **$0.0105** |

If every comment needs one retry, the estimated cost could be approximately $0.021.

These are estimates, not actual billing figures. Actual cost depends on token usage and the number of retries.

## 4. Estimated Processing Time

The model's published token-generation speed is approximately 500 tokens per second. Actual response time also depends on network conditions, input size, and API processing time.

For planning purposes, assume around 1–3 seconds per API call.

- 50 normal calls: approximately 50–150 seconds.
- 100 calls if every comment needs a retry: approximately 100–300 seconds.

These are planning estimates, not measured results. Actual latency can be checked using the Groq Console usage and request logs.

## 5. Cost and Latency Control

The project controls unnecessary API usage by:

1. Skipping empty comments.
2. Retrying invalid responses only once.
3. Using Python for counting and percentage calculations instead of the LLM.
4. Sending failed classifications for manual review.

## 6. Conclusion

The Mess Feedback Sorter is designed to process a small daily dataset with low estimated API usage. The actual cost and processing time depend on the number of comments, token usage, and retries. The warden remains responsible for reviewing urgent feedback.