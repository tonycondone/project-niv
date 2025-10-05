# 📧 PROJECT NIV — Email Automation Tool for Data Analysis

PROJECT NIV automates the generation and delivery of data analysis reports via email. Designed for analysts, it removes manual steps in summarizing and sharing weekly reports.

## 🔧 Features

- ✅ Auto-send reports via email (Excel + Summary)
- 📊 Generates charts and visual summaries
- ⏰ Weekly scheduling (e.g., every Monday 08:00 AM)
- 🔌 Works with CSV, Excel files
- 🔒 Secure SMTP login using app password
- 🔮 **Prescience Analytics** - Predictive insights and trend forecasting
- 🔄 **ETL Process** - Extract, Transform, Load with advanced filtering
- 📈 **ApexCharts.js Integration** - Interactive web-based visualizations
- 🌐 **Web Dashboard** - Real-time data visualization interface

## 🚀 How It Works

### Legacy Mode (Original)
1. Place data in `/data/sample.csv`
2. Configure `config.json` (email, time, recipients)
3. Run:

    ```bash
    python main.py --mode legacy    # One-time run
    python scheduler.py             # Scheduled automation
    ```

### ETL Mode (New)
1. Place data in `/data/sample.csv` or any CSV file
2. Run ETL process with filtering and transformations:

    ```bash
    # Basic ETL
    python main.py --mode etl --csv sample.csv
    
    # ETL with filters
    python main.py --mode etl --csv sample.csv --filters '{"Sales": {"min": 1000, "max": 5000}}'
    
    # ETL with transformations
    python main.py --mode etl --csv sample.csv --transformations normalize standardize
    ```

### Web Dashboard Mode
1. Run the web server:

    ```bash
    python main.py --mode web
    ```

2. Open your browser to `http://localhost:5000`
3. View interactive ApexCharts.js visualizations

## 📁 Folder Structure

```plaintext
project_niv/
├── data/                    # Source CSV or Excel files
│   ├── sample.csv          # Basic sample data
│   └── sample_detailed.csv # Detailed sample data
├── reports/                 # Auto-generated reports/charts
│   ├── charts/             # ApexCharts.js configurations
│   └── data/               # Processed data files
├── templates/              # HTML templates
│   └── chart_template.html # ApexCharts.js dashboard
├── logs/                   # Error or activity logs
├── main.py                 # Main runner script (enhanced)
├── scheduler.py            # Auto-send scheduler
├── email_utils.py          # Handles email formatting + sending
├── data_processor.py       # Legacy data processor
├── etl_processor.py        # New ETL processor
├── web_server.py           # Flask web server
├── demo_etl.py            # ETL demonstration script
├── config.json            # Email settings + schedule
└── README.md              # This file
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

## 🔄 ETL Process & ApexCharts.js Integration

PROJECT NIV now features a comprehensive ETL (Extract, Transform, Load) process with interactive ApexCharts.js visualizations:

### ETL Capabilities

- **Data Extraction**: Support for CSV files with automatic encoding detection
- **Advanced Filtering**: Range filters, value filters, and custom conditions
- **Data Transformations**: Normalization, standardization, and log transformation
- **Data Cleaning**: Duplicate removal, missing value handling, and type conversion
- **Multiple Output Formats**: Excel, CSV, JSON for different use cases

### ApexCharts.js Visualizations

- 📈 **Line Charts**: Time series and trend analysis
- 📊 **Bar Charts**: Comparative data visualization
- 📈 **Area Charts**: Filled trend representations
- 🥧 **Pie Charts**: Data distribution and proportions
- 📊 **Scatter Plots**: Correlation and relationship analysis

### Web Dashboard Features

- 🌐 **Interactive Interface**: Real-time data visualization
- 🔄 **Flow Chart**: Visual ETL process representation
- 📱 **Responsive Design**: Works on desktop and mobile
- 💾 **Data Export**: Download processed data and configurations
- 🔄 **Real-time Updates**: Live data refresh capabilities

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
