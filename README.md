### 6. Run Messly Web Application

Messly provides a Streamlit-based web interface for collecting and managing hostel mess feedback.

```bash
streamlit run app.py
```

The application opens in a web browser.

### Messly Web Application Features

**Student Portal**
- Submit feedback about breakfast, lunch, snacks and dinner.
- Supports English, Tamil and Tanglish.
- Validates feedback before processing.
- Uses AI to classify feedback by category, sentiment and urgency.
- Highlights possible food safety concerns.

**Admin Dashboard**
- Password-protected access.
- View feedback statistics and category-wise insights.
- Search and filter submitted feedback.
- Review, accept or reject feedback.
- Export feedback reports as CSV.

**Data Storage**

The web application uses a local SQLite database (`ui_feedback.db`) for new submissions. Existing console-generated reports remain separate.

The database and API credentials are excluded from GitHub to protect private information.

### Human Oversight

Messly assists with feedback classification and prioritization. Important complaints require review by the mess supervisor or warden before action is taken.
