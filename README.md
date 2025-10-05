# 📧 PROJECT NIV — Advanced Data Analysis & Visualization Platform

PROJECT NIV is a comprehensive data analysis platform that combines automated email reporting with powerful ETL (Extract, Transform, Load) capabilities and interactive ApexCharts.js visualizations. Designed for data analysts and business intelligence professionals, it streamlines the entire data processing workflow from raw CSV files to actionable insights.

## 🔧 Core Features

### 📧 Email Automation
- ✅ Auto-send reports via email (Excel + Summary)
- ⏰ Weekly scheduling (e.g., every Monday 08:00 AM)
- 🔒 Secure SMTP login using app password
- 📊 Generates charts and visual summaries

### 🔄 ETL Processing Engine
- 🔌 **Data Extraction**: Support for CSV files with automatic encoding detection
- 🎯 **Advanced Filtering**: Range filters, value filters, and custom conditions
- 🔧 **Data Transformations**: Normalization, standardization, and log transformation
- 🧹 **Data Cleaning**: Duplicate removal, missing value handling, and type conversion
- 💾 **Multiple Output Formats**: Excel, CSV, JSON for different use cases

### 📈 Interactive Visualizations
- 📊 **ApexCharts.js Integration**: Professional-grade interactive charts
- 📈 **Line Charts**: Time series and trend analysis
- 📊 **Bar Charts**: Comparative data visualization
- 📈 **Area Charts**: Filled trend representations
- 🥧 **Pie Charts**: Data distribution and proportions
- 📊 **Scatter Plots**: Correlation and relationship analysis

### 🌐 Web Dashboard
- 🖥️ **Interactive Interface**: Real-time data visualization
- 🔄 **Flow Chart**: Visual ETL process representation
- 📱 **Responsive Design**: Works on desktop and mobile
- 💾 **Data Export**: Download processed data and configurations
- 🔄 **Real-time Updates**: Live data refresh capabilities

### 🔮 Prescience Analytics
- 📈 **Predictive Modeling**: Forecast future trends based on historical data patterns
- 🎯 **Anomaly Detection**: Automatically identify unusual patterns or outliers
- ⚠️ **Alert System**: Get notified when data deviates from expected patterns
- 📊 **Confidence Intervals**: Statistical confidence levels for all predictions

## 🚀 Quick Start

### 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tonycondone/project-niv.git
   cd project-niv
   ```

2. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

3. Place your data in the `/data/` directory

### 🎯 Usage Modes

#### 1. 📧 Legacy Email Mode (Original)
For traditional email-based reporting:
```bash
# One-time report generation
python3 main.py --mode legacy

# Scheduled automation
python3 scheduler.py
```

#### 2. 🔄 ETL Processing Mode
For advanced data processing and analysis:
```bash
# Basic ETL processing
python3 main.py --mode etl --csv your_data.csv

# ETL with advanced filtering
python3 main.py --mode etl --csv your_data.csv \
  --filters '{"Sales": {"min": 1000, "max": 5000}, "Category": ["Electronics"]}'

# ETL with data transformations
python3 main.py --mode etl --csv your_data.csv \
  --transformations normalize standardize
```

#### 3. 🌐 Web Dashboard Mode
For interactive data visualization:
```bash
# Start web server
python3 main.py --mode web

# Open browser to http://localhost:5000
```

### 🧪 Demo & Examples
```bash
# Run comprehensive demo
python3 demo_etl.py

# Run usage examples
python3 example_usage.py
```

## 📁 Project Structure

```
project_niv/
├── 📁 data/                          # Data sources
│   ├── sample.csv                   # Basic sample data
│   └── sample_detailed.csv          # Enhanced sample data
├── 📁 reports/                       # Generated outputs
│   ├── 📁 charts/                   # ApexCharts.js configurations
│   ├── 📁 data/                     # Processed data files
│   ├── *.xlsx                       # Excel reports
│   ├── *.json                       # JSON data exports
│   └── *.png                        # Static chart images
├── 📁 templates/                     # Web templates
│   └── chart_template.html          # ApexCharts.js dashboard
├── 📁 logs/                         # System logs
├── 🐍 Core Scripts
│   ├── main.py                      # Main entry point (enhanced)
│   ├── etl_processor.py             # ETL processing engine
│   ├── web_server.py                # Flask web server
│   ├── data_processor.py            # Legacy data processor
│   ├── email_utils.py               # Email functionality
│   └── scheduler.py                 # Automated scheduling
├── 🧪 Demo & Examples
│   ├── demo_etl.py                  # Comprehensive demo
│   └── example_usage.py             # Usage examples
├── ⚙️ Configuration
│   ├── config.json                  # Email settings
│   └── requirement.txt              # Python dependencies
└── 📖 Documentation
    └── README.md                    # This file
```

## 📦 Dependencies

### Python Requirements
```bash
pip install -r requirement.txt
```

**Core Libraries:**
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Static chart generation
- `flask` - Web server framework
- `openpyxl` - Excel file handling
- `jinja2` - Template engine
- `schedule` - Task scheduling

### External Dependencies
- **ApexCharts.js** - Interactive charting library (loaded via CDN)
- **Mermaid.js** - Flow chart generation (loaded via CDN)

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

## 🎯 PROJECT NIV – Advanced Data Analysis Platform

**Transform your data into actionable insights with PROJECT NIV's powerful ETL engine and interactive visualizations.**

**GitHub Repository**: [https://github.com/tonycondone/project-niv](https://github.com/tonycondone/project-niv)

**License**: MIT License

**Version**: 2.0.0 (ETL + ApexCharts.js Integration)
