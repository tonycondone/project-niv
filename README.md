# 📧 PROJECT NIV — Email Automation Tool for Data Analysis

PROJECT NIV automates the generation and delivery of data analysis reports via email. Designed for analysts, it removes manual steps in summarizing and sharing weekly reports.

## 🔧 Features

- ✅ Auto-send reports via email (Excel + Summary)
- 📊 Generates charts and visual summaries
- ⏰ Weekly scheduling (e.g., every Monday 08:00 AM)
- 🔌 Works with CSV, Excel files
- 🔒 Secure SMTP login using app password
- 🔮 **Prescience Analytics** - Predictive insights and trend forecasting

## 🚀 How It Works

1. Place data in `/data/sample.csv`
2. Configure `config.json` (email, time, recipients)
3. Run:

    ```bash
    python main.py         # One-time run
    python scheduler.py    # Scheduled automation
    ```

## 📁 Folder Structure

```plaintext
project_niv/
├── data/             # Source CSV or Excel files
├── reports/          # Auto-generated reports/charts
├── templates/        # (Optional) HTML email templates
├── logs/             # Error or activity logs
├── main.py           # Main runner script
├── scheduler.py      # Auto-send scheduler
├── email_utils.py    # Handles email formatting + sending
├── data_processor.py # Reads and analyzes data
├── config.json       # Email settings + schedule
└── README.md         # This file
```

## 📦 Requirements

Install Python libraries:

```bash
pip install -r requirements.txt
```

## ✉️ Email Config (`config.json`)

```json
{
  "sender_email": "your@gmail.com",
  "password": "your_app_password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "receiver_emails": ["someone@example.com"],
  "subject": "Weekly Data Report",
  "send_time": "08:00"
}
```

> Use an app password (e.g., for Gmail) instead of your real password.

## 🧠 Example Use Case

- Sales analysts receive automated weekly reports with updated sales summaries and charts.
- Managers get a Monday 8 AM email with insights—without writing any code.

## 🔮 Prescience Analytics

PROJECT NIV now includes advanced prescience capabilities that provide:

- **Predictive Modeling**: Forecast future trends based on historical data patterns
- **Anomaly Detection**: Automatically identify unusual patterns or outliers in your data
- **Trend Analysis**: Generate forward-looking insights and recommendations
- **Risk Assessment**: Evaluate potential risks and opportunities in your datasets
- **Seasonal Forecasting**: Account for seasonal patterns and cyclical trends

### Prescience Features

- 📈 **Trend Forecasting**: Predict future values using time series analysis
- 🎯 **Pattern Recognition**: Identify recurring patterns and correlations
- ⚠️ **Alert System**: Get notified when data deviates from expected patterns
- 📊 **Confidence Intervals**: Statistical confidence levels for all predictions
- 🔍 **Root Cause Analysis**: Understand the factors driving your predictions

## 📌 Future Improvements

- Web UI (Streamlit)
- Database logging
- HTML-based email reports
- Enhanced prescience algorithms
- Real-time prediction updates

---

## 📌 PROJECT NIV – Automated Email Reporting Tool for Data Analysts

**Tech Stack:** Python, Pandas, Matplotlib, Jinja2, SMTP, Schedule

### Description

PROJECT NIV is a Python-based automation tool designed to streamline the reporting workflow for data analysts. It automates the extraction, summarization, visualization, and email delivery of analytical reports to stakeholders on a scheduled basis.

### Key Features

- **Automated Report Generation**: Processes data from CSV/Excel files and generates insightful reports.
- **Email Delivery**: Sends reports with summaries, attached Excel files, and optional charts.
- **Configurable Scheduling**: Set up automated email delivery (e.g., every Monday at 08:00 AM).
- **Secure SMTP Integration**: Supports Gmail, Outlook, and other email providers with app passwords.
- **Prescience Analytics**: Advanced predictive modeling and trend forecasting capabilities.
- **Modular Design**: Built for scalability with future UI and database integration in mind.

### Impact

PROJECT NIV eliminates repetitive manual reporting tasks, ensuring timely and consistent delivery of insights to decision-makers. It is ideal for internal reporting across industries such as business, healthcare, education, and logistics.

**GitHub Repository**: (<https://github.com/tonycondone/project-niv>)
