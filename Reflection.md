# Project Reflection – Mess Feedback Sorter

Developing the Mess Feedback Sorter helped me understand how Artificial Intelligence can solve a real-world problem. I selected the hostel mess feedback system because students regularly experience issues related to food taste, hygiene, quantity and serving time. Managing many feedback comments manually can be difficult. My aim was to build an application that organizes feedback and identifies important complaints.

I used Python and a Large Language Model through the Groq API. The application reads student comments from a CSV file and sends non-empty comments to the AI model for classification. The model identifies the category, sentiment, urgency and a short summary. I selected five categories: taste, hygiene, quantity, timing and other.

One important decision was to separate AI classification from Python validation. An AI response may contain incorrect or unexpected information. Therefore, I added JSON parsing and validation. The program checks whether the response contains the required fields and valid values. If the response is invalid, it retries once. If processing still fails, the feedback is marked for manual review.

Another important feature was the safety net. I wanted food safety complaints to receive attention. Therefore, I included keyword checks for issues such as insects, hair, spoiled food and students becoming sick. The safety net can increase the urgency level but cannot reduce an urgent decision made by the AI. This helps prevent important safety complaints from being overlooked.

I also included Tanglish feedback examples because students may not always write in formal English. This helped me understand the importance of designing AI systems for the language used by actual users.

Testing was an important part of the project. I created five evaluation tests and three red-team tests to check the system's behaviour. I also generated separate CSV reports for classified feedback and urgent complaints, along with a summary report.I learned to document assumptions and verify results before presenting my work.

During this project, I learned about API integration, prompt engineering, CSV processing, JSON validation, error handling and testing. I also understood that AI should not be trusted blindly. Human review is necessary, especially when food safety is involved.

Overall, this project improved my practical understanding of AI-based application development. It showed me how an AI model and traditional programming can work together to solve a practical problem. In the future, the application can be improved with a user-friendly interface, additional language support and a dashboard for mess administrators.