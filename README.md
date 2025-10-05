<div align="center">

# 📊 PROJECT NIV

### Advanced Data Analysis & Visualization Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-green.svg)](https://pandas.pydata.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com)
[![ApexCharts](https://img.shields.io/badge/ApexCharts.js-Interactive-orange.svg)](https://apexcharts.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen.svg)](https://github.com/tonycondone/project-niv)

*Transform your data into actionable insights with powerful ETL processing and interactive visualizations*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🔧 Features](#-core-features) • [💼 Use Cases](#-use-cases) • [🤝 Contributing](#-contributing)

</div>

---

PROJECT NIV is a comprehensive data analysis platform that combines automated email reporting with powerful ETL (Extract, Transform, Load) capabilities and interactive ApexCharts.js visualizations. Designed for data analysts and business intelligence professionals, it streamlines the entire data processing workflow from raw CSV files to actionable insights.

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🔧 Core Features](#-core-features)
- [📁 Project Structure](#-project-structure)
- [📦 Dependencies](#-dependencies)
- [💼 Use Cases](#-use-cases)
- [🔄 ETL Process Deep Dive](#-etl-process-deep-dive)
- [🌐 Web Dashboard Features](#-web-dashboard-features)
- [🔮 Prescience Analytics](#-prescience-analytics)
- [🚀 Advanced Usage Examples](#-advanced-usage-examples)
- [🔧 Configuration Options](#-configuration-options)
- [📈 Performance & Scalability](#-performance--scalability)
- [🛠️ Development & Contributing](#️-development--contributing)
- [📞 Support & Documentation](#-support--documentation)

---

## 🔧 Core Features

### 📧 Email Automation
<table>
<tr>
<td width="50%">

- 📧 **Auto-send reports** via email (Excel + Summary)
- ⏰ **Weekly scheduling** (e.g., every Monday 08:00 AM)
- 🔒 **Secure SMTP** login using app password
- 📊 **Chart generation** and visual summaries

</td>
<td width="50%">

- 📈 **Professional reports** with insights
- 🎯 **Configurable recipients** and timing
- 📱 **Multi-format support** (Excel, PDF, HTML)
- 🔔 **Notification system** for delivery status

</td>
</tr>
</table>

### 🔄 ETL Processing Engine
<table>
<tr>
<td width="50%">

- 🔌 **Data Extraction** - CSV files with automatic encoding detection
- 🎯 **Advanced Filtering** - Range, value, and custom conditions
- 🔧 **Data Transformations** - Normalization, standardization, log transform
- 🧹 **Data Cleaning** - Duplicate removal, missing value handling

</td>
<td width="50%">

- 💾 **Multiple Output Formats** - Excel, CSV, JSON for different use cases
- 📦 **Auto-Installation** - Dependencies installed automatically
- 🔍 **Data Validation** - Type checking and error handling
- 📊 **Metadata Tracking** - Complete process documentation

</td>
</tr>
</table>

### 📈 Interactive Visualizations
<table>
<tr>
<td width="50%">

- 📊 **ApexCharts.js Integration** - Professional-grade interactive charts
- 📈 **Line Charts** - Time series and trend analysis
- 📊 **Bar Charts** - Comparative data visualization
- 📈 **Area Charts** - Filled trend representations

</td>
<td width="50%">

- 🥧 **Pie Charts** - Data distribution and proportions
- 📊 **Scatter Plots** - Correlation and relationship analysis
- 🎨 **Custom Styling** - Professional themes and colors
- 📱 **Responsive Design** - Works on all devices

</td>
</tr>
</table>

### 🌐 Web Dashboard
<table>
<tr>
<td width="50%">

- 🖥️ **Interactive Interface** - Real-time data visualization
- 🔄 **Flow Chart** - Visual ETL process representation
- 📱 **Responsive Design** - Works on desktop and mobile
- 💾 **Data Export** - Download processed data and configurations

</td>
<td width="50%">

- 🔄 **Real-time Updates** - Live data refresh capabilities
- 🎛️ **Interactive Controls** - Filter and customize views
- 📊 **Summary Statistics** - Key metrics at a glance
- 🔗 **API Endpoints** - Programmatic access

</td>
</tr>
</table>

### 🔮 Prescience Analytics
<table>
<tr>
<td width="50%">

- 📈 **Predictive Modeling** - Forecast future trends
- 🎯 **Anomaly Detection** - Identify unusual patterns
- ⚠️ **Alert System** - Notifications for data deviations
- 📊 **Confidence Intervals** - Statistical confidence levels

</td>
<td width="50%">

- 🔍 **Root Cause Analysis** - Understand prediction drivers
- 📈 **Trend Forecasting** - Time series analysis
- 🎲 **Risk Assessment** - Statistical risk evaluation
- 🔄 **Model Validation** - Cross-validation and accuracy metrics

</td>
</tr>
</table>

## 🚀 Quick Start

<div align="center">

### Get up and running in under 2 minutes! ⚡

</div>

### 📦 Installation Options

<table>
<tr>
<td width="33%" align="center">

#### 🎯 **Option 1: Automatic** 
*Recommended for beginners*

```bash
git clone https://github.com/tonycondone/project-niv.git
cd project-niv
python3 install.py
```

✅ **Zero configuration**  
✅ **Dependencies auto-installed**  
✅ **Sample data included**

</td>
<td width="33%" align="center">

#### 🔧 **Option 2: Manual**
*For advanced users*

```bash
git clone https://github.com/tonycondone/project-niv.git
cd project-niv
pip install -r requirement.txt
```

✅ **Full control**  
✅ **Custom setup**  
✅ **Development ready**

</td>
<td width="33%" align="center">

#### ⚡ **Option 3: One-Click**
*Instant processing*

```bash
git clone https://github.com/tonycondone/project-niv.git
cd project-niv
python3 run_once.py --interactive
```

✅ **Immediate results**  
✅ **Auto-installation**  
✅ **Interactive guide**

</td>
</tr>
</table>

### 🎯 Usage Modes

<table>
<tr>
<td width="33%" align="center">

#### 📧 **Legacy Email Mode**
*Traditional reporting*

```bash
# One-time report
python3 main.py --mode legacy

# Scheduled automation
python3 scheduler.py
```

📧 **Email reports**  
⏰ **Scheduled delivery**  
📊 **Excel attachments**

</td>
<td width="33%" align="center">

#### 🔄 **ETL Processing Mode**
*Advanced data processing*

```bash
# Basic ETL
python3 main.py --mode etl --csv data.csv

# With filters & transforms
python3 main.py --mode etl --csv data.csv \
  --filters '{"Sales": {"min": 1000}}' \
  --transformations normalize
```

🎯 **Advanced filtering**  
🔧 **Data transformations**  
💾 **Multiple outputs**

</td>
<td width="33%" align="center">

#### 🌐 **Web Dashboard Mode**
*Interactive visualization*

```bash
# Start web server
python3 main.py --mode web

# Visit http://localhost:5000
```

📊 **Interactive charts**  
🖥️ **Web dashboard**  
📱 **Responsive design**

</td>
</tr>
</table>

### 🧪 Demo & Examples

<div align="center">

#### Try it out with these examples! 🚀

</div>

<table>
<tr>
<td width="50%">

#### 🚀 **One-Time Run Script**
*Perfect for beginners*

```bash
# Process any CSV file
python3 run_once.py --csv your_data.csv --web

# Interactive guided mode
python3 run_once.py --interactive

# With filters and transformations
python3 run_once.py --csv data.csv \
  --filters '{"Sales": {"min": 1000}}' \
  --transformations normalize --web
```

</td>
<td width="50%">

#### 📚 **Learning Examples**
*Comprehensive demos*

```bash
# Quick start examples
python3 quick_start.py

# Comprehensive ETL demo
python3 demo_etl.py

# Advanced usage examples
python3 example_usage.py
```

</td>
</tr>
</table>

## 📁 Project Structure

<div align="center">

### Clean, organized, and developer-friendly structure 📂

</div>

```
project_niv/
├── 📁 data/                          # 📊 Data sources
│   ├── sample.csv                   # Basic sample data
│   └── sample_detailed.csv          # Enhanced sample data
├── 📁 reports/                       # 📈 Generated outputs
│   ├── 📁 charts/                   # ApexCharts.js configurations
│   ├── 📁 data/                     # Processed data files
│   ├── *.xlsx                       # Excel reports
│   ├── *.json                       # JSON data exports
│   └── *.png                        # Static chart images
├── 📁 templates/                     # 🎨 Web templates
│   └── chart_template.html          # ApexCharts.js dashboard
├── 📁 logs/                         # 📝 System logs
├── 🐍 Core Scripts
│   ├── main.py                      # Main entry point (enhanced)
│   ├── etl_processor.py             # ETL processing engine
│   ├── web_server.py                # Flask web server
│   ├── data_processor.py            # Legacy data processor
│   ├── email_utils.py               # Email functionality
│   └── scheduler.py                 # Automated scheduling
├── 🧪 Demo & Examples
│   ├── run_once.py                  # One-time processing script
│   ├── quick_start.py               # Quick start examples
│   ├── demo_etl.py                  # Comprehensive demo
│   └── example_usage.py             # Usage examples
├── ⚙️ Configuration
│   ├── config.json                  # Email settings
│   └── requirement.txt              # Python dependencies
└── 📖 Documentation
    ├── README.md                    # This file
    └── STEP_BY_STEP_GUIDE.md        # Complete tutorial
## 📦 Dependencies

<div align="center">

### Modern tech stack with automatic installation 🔧

</div>

<table>
<tr>
<td width="50%">

#### 🐍 **Python Libraries**
*Core data processing*

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** - Static chart generation
- **flask** - Web server framework
- **openpyxl** - Excel file handling
- **jinja2** - Template engine
- **schedule** - Task scheduling

</td>
<td width="50%">

#### 🌐 **External Dependencies**
*Frontend visualization*

- **ApexCharts.js** - Interactive charting library
- **Mermaid.js** - Flow chart generation
- **CDN Integration** - No local installation needed
- **Responsive Design** - Mobile-friendly UI

</td>
</tr>
</table>

### 🚀 Installation

```bash
# Automatic installation (Recommended)
pip install -r requirement.txt

# Or install individually
pip install pandas numpy matplotlib flask openpyxl jinja2 schedule
```

## 💼 Use Cases

<div align="center">

### Perfect for data professionals across industries 🎯

</div>

<table>
<tr>
<td width="33%" align="center">

#### 📊 **Business Intelligence**
*Data-driven decisions*

- **Sales Analytics** - Track performance
- **Financial Reporting** - Automated summaries
- **KPI Monitoring** - Real-time tracking
- **Trend Analysis** - Pattern identification

</td>
<td width="33%" align="center">

#### 🔬 **Data Science & Analytics**
*Advanced data processing*

- **ETL Pipelines** - Large dataset processing
- **Data Exploration** - Interactive discovery
- **Statistical Analysis** - Built-in tools
- **Report Automation** - Generate & distribute

</td>
<td width="33%" align="center">

#### 🏢 **Enterprise Applications**
*Scalable solutions*

- **Departmental Reporting** - Custom reports
- **Compliance Monitoring** - Quality checks
- **Executive Dashboards** - High-level insights
- **Data Integration** - Seamless workflows

</td>
</tr>
</table>

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

## 💼 Use Cases

### 📊 Business Intelligence
- **Sales Analytics**: Track sales performance with interactive dashboards
- **Financial Reporting**: Automated monthly/quarterly financial summaries
- **KPI Monitoring**: Real-time tracking of key performance indicators
- **Trend Analysis**: Identify patterns and forecast future performance

### 🔬 Data Science & Analytics
- **ETL Pipelines**: Process large datasets with advanced filtering and transformations
- **Data Exploration**: Interactive visualizations for data discovery
- **Statistical Analysis**: Built-in normalization and standardization tools
- **Report Automation**: Generate and distribute analytical reports automatically

### 🏢 Enterprise Applications
- **Departmental Reporting**: Custom reports for different business units
- **Compliance Monitoring**: Automated data quality and compliance checks
- **Executive Dashboards**: High-level insights for decision makers
- **Data Integration**: Seamless integration with existing data sources

## 🔄 ETL Process Deep Dive

### Data Extraction
- **Multi-format Support**: CSV files with automatic encoding detection
- **Error Handling**: Robust error handling for malformed data
- **Metadata Tracking**: Comprehensive logging of extraction process
- **Data Validation**: Automatic data type detection and validation

### Data Transformation
- **Filtering Options**:
  - Range filters: `{"Sales": {"min": 1000, "max": 5000}}`
  - Value filters: `{"Category": ["Electronics", "Hardware"]}`
  - Custom conditions: Complex boolean logic
- **Transformation Functions**:
  - `normalize`: Min-max normalization (0-1 scale)
  - `standardize`: Z-score standardization
  - `log_transform`: Logarithmic transformation
- **Data Cleaning**:
  - Duplicate removal
  - Missing value imputation
  - Data type conversion
  - Outlier detection

### Data Loading
- **Output Formats**: Excel (.xlsx), CSV, JSON
- **Chart Configurations**: ApexCharts.js ready JSON
- **Metadata Export**: Complete ETL process documentation
- **Flow Visualization**: Mermaid.js flow charts

## 🌐 Web Dashboard Features

### Interactive Visualizations
- **Real-time Charts**: ApexCharts.js powered interactive visualizations
- **Multiple Chart Types**: Line, Bar, Area, Pie, and Scatter plots
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Custom Styling**: Professional, modern UI with customizable themes

### Dashboard Capabilities
- **Live Data Refresh**: Real-time data updates without page reload
- **Export Functionality**: Download data and chart configurations
- **Flow Visualization**: Interactive ETL process flow charts
- **Summary Statistics**: Key metrics and data insights at a glance

### API Endpoints
- `GET /api/etl-data` - Retrieve processed ETL data
- `POST /api/run-etl` - Execute ETL process via API
- `GET /api/chart/<type>` - Get specific chart configuration
- `GET /api/flow-chart` - Retrieve flow chart data
- `GET /api/data/export` - Export processed data
- `GET /api/health` - Health check endpoint

## 🔮 Prescience Analytics

### Predictive Capabilities
- **Trend Forecasting**: Time series analysis and future value prediction
- **Anomaly Detection**: Automatic identification of unusual data patterns
- **Pattern Recognition**: Machine learning-based pattern identification
- **Risk Assessment**: Statistical risk evaluation and opportunity analysis
- **Seasonal Analysis**: Cyclical pattern detection and forecasting

### Advanced Features
- **Confidence Intervals**: Statistical confidence levels for predictions
- **Alert System**: Automated notifications for data deviations
- **Root Cause Analysis**: Deep dive into prediction drivers
- **Model Validation**: Cross-validation and accuracy metrics

## 🚀 Advanced Usage Examples

### Complex ETL Pipeline
```bash
# Multi-step ETL with filters and transformations
python3 main.py --mode etl \
  --csv sales_data.csv \
  --filters '{"Sales": {"min": 1000}, "Region": ["North", "South"]}' \
  --transformations normalize standardize
```

### Web Dashboard with Custom Data
```bash
# Process data and start web server
python3 main.py --mode etl --csv custom_data.csv
python3 main.py --mode web
```

### Automated Reporting
```bash
# Schedule automated ETL processing
python3 scheduler.py
```

## 🔧 Configuration Options

### ETL Configuration
- **Filter Types**: Range, value, regex, custom functions
- **Transformations**: Normalize, standardize, log, custom
- **Output Formats**: Excel, CSV, JSON, Parquet
- **Chart Types**: Line, Bar, Area, Pie, Scatter, Heatmap

### Web Server Configuration
- **Port**: Default 5000, configurable
- **Host**: Local or network accessible
- **Debug Mode**: Development vs production settings
- **CORS**: Cross-origin resource sharing settings

## 📈 Performance & Scalability

### Data Processing
- **Memory Efficient**: Handles large datasets with chunked processing
- **Parallel Processing**: Multi-threaded data transformation
- **Caching**: Intelligent caching for repeated operations
- **Progress Tracking**: Real-time progress monitoring

### Web Performance
- **CDN Integration**: ApexCharts.js and Mermaid.js via CDN
- **Lazy Loading**: On-demand chart generation
- **Responsive Design**: Optimized for all screen sizes
- **Caching**: Browser and server-side caching

## 🛠️ Development & Contributing

### Tech Stack
- **Backend**: Python 3.8+, Flask, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript, ApexCharts.js
- **Visualization**: ApexCharts.js, Mermaid.js, Matplotlib
- **Data Processing**: Pandas, NumPy, OpenPyXL

### Getting Started for Developers
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Run tests: `python3 -m pytest`
5. Submit a pull request

## 📞 Support & Documentation

- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive inline documentation
- **Examples**: Extensive example scripts and demos
- **API Reference**: Complete API documentation

---

<div align="center">

## 🎯 PROJECT NIV

### Advanced Data Analysis Platform

**Transform your data into actionable insights with powerful ETL processing and interactive visualizations**

---

### 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/tonycondone/project-niv?style=social)
![GitHub forks](https://img.shields.io/github/forks/tonycondone/project-niv?style=social)
![GitHub issues](https://img.shields.io/github/issues/tonycondone/project-niv)
![GitHub pull requests](https://img.shields.io/github/issues-pr/tonycondone/project-niv)
![GitHub last commit](https://img.shields.io/github/last-commit/tonycondone/project-niv)

### 🚀 Quick Links

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/tonycondone/project-niv)
[![Documentation](https://img.shields.io/badge/Documentation-Guide-blue?style=for-the-badge&logo=read-the-docs)](STEP_BY_STEP_GUIDE.md)
[![Issues](https://img.shields.io/badge/Issues-Report%20Bug-red?style=for-the-badge&logo=github)](https://github.com/tonycondone/project-niv/issues)
[![Discussions](https://img.shields.io/badge/Discussions-Community-green?style=for-the-badge&logo=github)](https://github.com/tonycondone/project-niv/discussions)

### 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Version**: 2.0.0 (ETL + ApexCharts.js Integration)  
**Python**: 3.8+  
**Status**: Production Ready ✅

---

### 💡 Made with ❤️ by [Tony Condone](https://github.com/tonycondone)

*Star ⭐ this repository if you find it helpful!*

</div>
