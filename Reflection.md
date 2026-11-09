# Project Reflection – Mess Feedback Sorter

Developing the Mess Feedback Sorter helped me understand how Artificial Intelligence can be used to solve a real-world problem. I selected the hostel mess feedback system because students regularly experience issues related to food taste, hygiene, quantity and serving time. Managing many feedback comments manually can be difficult. My aim was to build a simple application that organizes feedback and identifies important complaints.

I used Python and a Large Language Model through the Groq API. The application reads student comments from a CSV file and sends them to the AI model for classification. The model identifies the category, sentiment, urgency and a short summary. I selected five categories: taste, hygiene, quantity, timing and other. This made the feedback easier to organize.

One important decision was to separate AI classification from Python validation. An AI response can sometimes contain incorrect or unexpected information. Therefore, I added JSON parsing and validation functions. The program checks whether the response contains the required fields and valid values. If the response is invalid, it retries once. If it still fails, the feedback is marked for manual review.

Another important feature was the safety net. I wanted food safety complaints to receive attention. Therefore, I added keyword-based checks for issues such as insects, hair, spoiled food and students becoming sick. The safety net can increase the urgency level but cannot reduce it. This helps prevent a clear safety complaint from being ignored by the automated system.

I also included Tanglish feedback examples because students may not always write in formal English. This helped me understand the importance of designing AI systems for the language used by actual users.

Testing was an important part of the project. I created five evaluation tests and three red-team tests. All eight tests passed during my testing. I also generated separate CSV reports for classified feedback and urgent complaints, along with a summary report.

During this project, I learned about API integration, prompt engineering, CSV processing, JSON validation, error handling and testing. I also understood that AI should not be trusted blindly. Human review is still necessary, especially when food safety is involved.

Overall, this project improved my practical understanding of AI-based application development. It showed me how an AI model and traditional programming can work together to solve a practical problem. In the future, the application can be improved with a user-friendly interface, more language support and a dashboard for mess administrators.