# 📧 PROJECT NIV — Enhanced Email Automation Tool for Data Analysis

PROJECT NIV is a comprehensive Python-based automation tool that streamlines the reporting workflow for data analysts. It automates the extraction, summarization, visualization, and email delivery of analytical reports to stakeholders on a scheduled basis.

## ✨ Enhanced Features

- 🎨 **Beautiful HTML Email Templates** - Professional, responsive email designs
- 📊 **Advanced Chart Generation** - Multiple chart types with improved styling
- 🔧 **Comprehensive Configuration** - Environment variables and validation
- 📝 **Robust Logging System** - File rotation and detailed error tracking
- 🚀 **Enhanced CLI Interface** - Easy-to-use command-line tools
- 🔄 **Retry Logic** - Automatic retry on email failures
- 📈 **Data Validation** - Comprehensive data quality checks
- 🎯 **Flexible Scheduling** - Daily, weekly, or monthly reports
- 📎 **Multiple Attachments** - Excel reports + charts in emails
- 🛡️ **Error Handling** - Graceful error recovery and reporting

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/tonycondone/project-niv.git
cd project-niv

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit `config.json` with your email settings:

```json
{
  "sender_email": "your@gmail.com",
  "password": "your_app_password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "receiver_emails": ["recipient1@example.com", "recipient2@example.com"],
  "subject": "Weekly Data Report",
  "send_time": "08:00",
  "data_file": "data/sample.csv",
  "reports_dir": "reports",
  "schedule_type": "weekly",
  "day_of_week": "monday"
}
```

### 3. Test Configuration

```bash
python cli.py test
```

### 4. Send Report

```bash
# Send report immediately
python cli.py send

# Or use the main script
python main.py
```

### 5. Schedule Reports

```bash
# Daily reports at 9 AM
python cli.py schedule --daily 09:00

# Weekly reports on Monday at 8 AM
python cli.py schedule --weekly monday 08:00

# Monthly reports at 8 AM
python cli.py schedule --monthly 08:00
```

## 📁 Enhanced Project Structure

```plaintext
project_niv/
├── data/                    # Source CSV or Excel files
├── reports/                 # Auto-generated reports and charts
├── templates/               # HTML email templates
│   └── email_template.html  # Professional email template
├── logs/                    # Application logs with rotation
├── main.py                  # Main runner script
├── cli.py                   # Enhanced command-line interface
├── scheduler.py             # Advanced scheduler with retry logic
├── email_utils.py           # HTML email sender with templates
├── data_processor.py        # Enhanced data processing and validation
├── config_manager.py        # Configuration management with validation
├── logger_config.py         # Logging configuration
├── config.json              # Application configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🎯 CLI Commands

### Send Reports
```bash
python cli.py send                    # Send report immediately
python cli.py send --data-file data/my_data.csv  # Use specific data file
```

### Test & Validate
```bash
python cli.py test                    # Test configuration and email
python cli.py status                  # Show application status
python cli.py logs --lines 100       # View recent logs
```

### Configuration Management
```bash
python cli.py config show             # Show current configuration
python cli.py config set sender_email user@example.com  # Update config
```

### Scheduling
```bash
python cli.py schedule --daily 09:00           # Daily at 9 AM
python cli.py schedule --weekly friday 17:00   # Weekly on Friday at 5 PM
python cli.py schedule --monthly 08:00         # Monthly at 8 AM
```

## 🔧 Advanced Configuration

### Environment Variables

You can override configuration using environment variables:

```bash
export SENDER_EMAIL="your@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export RECEIVER_EMAILS="user1@example.com,user2@example.com"
export DATA_FILE="data/production_data.csv"
export SCHEDULE_TYPE="daily"
export SEND_TIME="09:00"
```

### Email Providers

The tool supports various email providers:

- **Gmail**: `smtp.gmail.com:587`
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Configure your own server

## 📊 Enhanced Features

### HTML Email Templates

Professional, responsive email templates with:
- Modern design with gradients and cards
- Summary statistics display
- Chart previews
- Mobile-friendly layout
- Fallback to plain text

### Advanced Chart Generation

- Multiple chart types (bar, line, histogram, box plot)
- High-resolution output (300 DPI)
- Automatic chart selection based on data size
- Professional styling with seaborn themes

### Data Validation

- File format validation (CSV, Excel)
- Data quality checks
- Missing value detection
- Numeric column validation
- Empty dataset detection

### Logging System

- File rotation (10MB max, 5 backups)
- Console and file output
- Configurable log levels
- Detailed error tracking
- Performance metrics

## 🛠️ Development

### Running Tests

```bash
python cli.py test
```

### Adding New Features

The codebase is modular and extensible:

- `DataProcessor`: Add new analysis methods
- `EmailSender`: Customize email templates
- `ReportScheduler`: Add new scheduling options
- `ConfigManager`: Add new configuration options

## 📈 Use Cases

- **Sales Analytics**: Automated weekly sales reports with trends and insights
- **Financial Reporting**: Monthly financial summaries with charts
- **Marketing Metrics**: Campaign performance reports
- **Operations Data**: Daily operational dashboards
- **Research Data**: Automated research findings distribution

## 🔒 Security

- App password authentication (no real passwords)
- Environment variable support
- Secure SMTP connections (TLS)
- Input validation and sanitization
- Error message sanitization

## 📌 Future Enhancements

- [ ] Web UI with Streamlit
- [ ] Database integration
- [ ] Multiple data source support
- [ ] Advanced analytics (ML insights)
- [ ] Email template editor
- [ ] Report customization dashboard
- [ ] API endpoints
- [ ] Docker containerization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Tech Stack:** Python, Pandas, Matplotlib, Jinja2, SMTP, Schedule, OpenPyXL

**GitHub Repository**: [https://github.com/tonycondone/project-niv](https://github.com/tonycondone/project-niv)
