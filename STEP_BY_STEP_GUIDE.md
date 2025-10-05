# 📚 PROJECT NIV - Complete Step-by-Step Guide

This guide will walk you through using PROJECT NIV from installation to advanced data visualization.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Basic Usage](#basic-usage)
5. [Advanced Features](#advanced-features)
6. [Web Dashboard](#web-dashboard)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)

---

## 1. Prerequisites

### System Requirements
- **Python 3.8+** (Python 3.9+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB+ recommended for large datasets)
- **Storage**: 100MB free space

### Required Knowledge
- Basic command line usage
- Understanding of CSV file format
- Basic Python knowledge (helpful but not required)

---

## 2. Installation

### Step 1: Download/Clone the Project
```bash
# Option 1: Clone from GitHub
git clone https://github.com/tonycondone/project-niv.git
cd project-niv

# Option 2: Download ZIP and extract
# Download from: https://github.com/tonycondone/project-niv/archive/main.zip
```

### Step 2: Install Dependencies (Automatic)
```bash
# Option 1: Automatic installation (Recommended)
python3 install.py

# Option 2: Manual installation
pip install -r requirement.txt
```

### Step 3: Verify Installation
```bash
# Test the installation
python3 run_once.py --help

# Or run the interactive mode
python3 run_once.py --interactive
```

**Expected Output:**
```
======================================================================
🚀 PROJECT NIV - One-Time Data Processing
📊 ETL + ApexCharts.js Integration
======================================================================
🔍 Checking dependencies...
✅ All dependencies are already installed
usage: run_once.py [-h] [--csv CSV] [--filters FILTERS] [--transformations {normalize,log_transform,standardize} ...] [--web] [--port PORT] [--no-browser] [--interactive] [--skip-deps]

PROJECT NIV - One-Time Data Processing
```

### Automatic Dependency Installation
The `run_once.py` script automatically checks and installs dependencies:
- **First run**: Installs all required packages
- **Subsequent runs**: Skips installation if packages are already installed
- **Skip option**: Use `--skip-deps` to skip dependency check

---

## 3. Quick Start

### Method 1: One-Time Run Script (Recommended for Beginners)

#### Step 1: Prepare Your Data
Place your CSV file in the project directory or note its path.

**Example CSV structure:**
```csv
Date,Product,Category,Sales,Quantity,Region,Profit
2024-01-01,Widget A,Electronics,1500,10,North,300
2024-01-02,Widget B,Electronics,2200,15,South,440
2024-01-03,Gadget X,Electronics,1800,12,East,360
```

#### Step 2: Run the One-Time Script
```bash
# Process your CSV file
python3 run_once.py --csv your_data.csv --web
```

#### Step 3: View Results
- The script will process your data
- Open your browser to `http://localhost:5000`
- View interactive charts and visualizations

### Method 2: Interactive Mode
```bash
# Run in interactive mode for guided setup
python3 run_once.py --interactive
```

**Follow the prompts:**
1. Enter CSV file path (or press Enter for sample data)
2. Enter filters (optional)
3. Enter transformations (optional)
4. Choose whether to start web dashboard

---

## 4. Basic Usage

### Processing a Simple CSV File

#### Step 1: Basic Processing
```bash
python3 run_once.py --csv data.csv
```

**What happens:**
- Extracts data from CSV
- Cleans and validates data
- Generates Excel, CSV, and JSON outputs
- Creates ApexCharts.js configurations

#### Step 2: View Generated Files
Check the `reports/` directory:
```
reports/
├── processed_data_YYYYMMDD_HHMMSS.xlsx    # Excel report
├── data_YYYYMMDD_HHMMSS.json              # JSON data
├── etl_metadata_YYYYMMDD_HHMMSS.json      # Process metadata
└── chart_configs.json                     # Chart configurations
```

### Processing with Filters

#### Step 1: Apply Range Filters
```bash
python3 run_once.py --csv data.csv --filters '{"Sales": {"min": 1000, "max": 5000}}'
```

#### Step 2: Apply Value Filters
```bash
python3 run_once.py --csv data.csv --filters '{"Category": ["Electronics", "Hardware"]}'
```

#### Step 3: Apply Multiple Filters
```bash
python3 run_once.py --csv data.csv --filters '{"Sales": {"min": 1000}, "Region": ["North", "South"]}'
```

### Processing with Transformations

#### Step 1: Normalize Data
```bash
python3 run_once.py --csv data.csv --transformations normalize
```

#### Step 2: Standardize Data
```bash
python3 run_once.py --csv data.csv --transformations standardize
```

#### Step 3: Apply Multiple Transformations
```bash
python3 run_once.py --csv data.csv --transformations normalize standardize
```

---

## 5. Advanced Features

### Using the Main Script

#### Step 1: ETL Mode
```bash
# Basic ETL processing
python3 main.py --mode etl --csv data.csv

# ETL with filters and transformations
python3 main.py --mode etl --csv data.csv \
  --filters '{"Sales": {"min": 1000, "max": 5000}}' \
  --transformations normalize standardize
```

#### Step 2: Web Dashboard Mode
```bash
# Start web server
python3 main.py --mode web

# Access at http://localhost:5000
```

#### Step 3: Legacy Email Mode
```bash
# Traditional email reporting
python3 main.py --mode legacy
```

### Custom Filter Examples

#### Range Filters
```json
{
  "Sales": {"min": 1000, "max": 5000},
  "Quantity": {"min": 10}
}
```

#### Value Filters
```json
{
  "Category": ["Electronics", "Hardware"],
  "Region": ["North", "South"]
}
```

#### Combined Filters
```json
{
  "Sales": {"min": 1000, "max": 5000},
  "Category": ["Electronics"],
  "Region": ["North", "South"]
}
```

### Available Transformations

1. **normalize**: Min-max normalization (0-1 scale)
2. **standardize**: Z-score standardization
3. **log_transform**: Logarithmic transformation

---

## 6. Web Dashboard

### Starting the Web Server

#### Step 1: Process Data First
```bash
python3 run_once.py --csv data.csv
```

#### Step 2: Start Web Server
```bash
python3 main.py --mode web
```

#### Step 3: Access Dashboard
Open your browser to `http://localhost:5000`

### Dashboard Features

#### Interactive Charts
- **Line Charts**: Time series analysis
- **Bar Charts**: Comparative data
- **Area Charts**: Trend visualization
- **Pie Charts**: Data distribution
- **Scatter Plots**: Correlation analysis

#### Dashboard Controls
- **Refresh Charts**: Update visualizations
- **Export Data**: Download processed data
- **Toggle Flow Chart**: View ETL process
- **Real-time Updates**: Live data refresh

### API Endpoints

#### Get ETL Data
```bash
curl http://localhost:5000/api/etl-data
```

#### Run ETL Process
```bash
curl -X POST http://localhost:5000/api/run-etl \
  -H "Content-Type: application/json" \
  -d '{"csv_file": "data.csv", "filters": {"Sales": {"min": 1000}}}'
```

#### Export Data
```bash
curl http://localhost:5000/api/data/export -o exported_data.csv
```

---

## 7. Troubleshooting

### Common Issues

#### Issue 1: "python: command not found"
**Solution:**
```bash
# Use python3 instead
python3 run_once.py --csv data.csv

# Or create an alias
alias python=python3
```

#### Issue 2: "ModuleNotFoundError"
**Solution:**
```bash
# Install missing dependencies
pip install -r requirement.txt

# Or install individually
pip install pandas numpy matplotlib flask openpyxl
```

#### Issue 3: "Cannot read CSV file"
**Solutions:**
- Check file path is correct
- Ensure file is a valid CSV
- Check file permissions
- Try different encoding

#### Issue 4: "No numeric columns found"
**Solutions:**
- Ensure CSV has numeric data
- Check column names and data types
- Verify data format

#### Issue 5: Web server won't start
**Solutions:**
- Check if port 5000 is available
- Try different port: `--port 8080`
- Check firewall settings

### Debug Mode

#### Enable Verbose Logging
```bash
# Set environment variable
export PYTHONPATH=.
python3 run_once.py --csv data.csv --web
```

#### Check Logs
Look for log files in the `logs/` directory.

---

## 8. Examples

### Example 1: Sales Data Analysis

#### Data File: `sales_data.csv`
```csv
Date,Product,Category,Sales,Quantity,Region,Profit
2024-01-01,Widget A,Electronics,1500,10,North,300
2024-01-02,Widget B,Electronics,2200,15,South,440
2024-01-03,Gadget X,Electronics,1800,12,East,360
2024-01-04,Tool Y,Hardware,1200,8,West,240
2024-01-05,Widget A,Electronics,1600,11,North,320
```

#### Process with Filters
```bash
python3 run_once.py --csv sales_data.csv \
  --filters '{"Sales": {"min": 1500}, "Category": ["Electronics"]}' \
  --transformations normalize \
  --web
```

### Example 2: Financial Data Processing

#### Data File: `financial_data.csv`
```csv
Month,Revenue,Expenses,Profit,Margin
2024-01,50000,30000,20000,40
2024-02,55000,32000,23000,42
2024-03,48000,31000,17000,35
2024-04,60000,35000,25000,42
```

#### Process with Transformations
```bash
python3 run_once.py --csv financial_data.csv \
  --transformations normalize standardize \
  --web
```

### Example 3: Customer Data Analysis

#### Data File: `customers.csv`
```csv
CustomerID,Age,Income,Spending,Category,Region
C001,25,50000,1200,High,North
C002,35,75000,1800,High,South
C003,45,60000,1500,Medium,East
C004,28,45000,900,Low,West
```

#### Process with Multiple Filters
```bash
python3 run_once.py --csv customers.csv \
  --filters '{"Income": {"min": 50000}, "Spending": {"min": 1000}}' \
  --transformations normalize \
  --web
```

---

## 🎯 Quick Reference

### Essential Commands
```bash
# One-time processing with web dashboard
python3 run_once.py --csv your_data.csv --web

# Interactive mode
python3 run_once.py --interactive

# ETL processing only
python3 main.py --mode etl --csv your_data.csv

# Web dashboard only
python3 main.py --mode web

# Legacy email mode
python3 main.py --mode legacy
```

### Filter Examples
```json
# Range filter
{"Sales": {"min": 1000, "max": 5000}}

# Value filter
{"Category": ["Electronics", "Hardware"]}

# Combined filters
{"Sales": {"min": 1000}, "Region": ["North", "South"]}
```

### Transformation Options
- `normalize` - Min-max normalization
- `standardize` - Z-score standardization
- `log_transform` - Logarithmic transformation

---

## 📞 Support

### Getting Help
1. **Check this guide** for common solutions
2. **Run the demo**: `python3 demo_etl.py`
3. **Check examples**: `python3 example_usage.py`
4. **GitHub Issues**: Report bugs and request features

### Useful Resources
- **Project Repository**: https://github.com/tonycondone/project-niv
- **ApexCharts.js Documentation**: https://apexcharts.com/docs/
- **Pandas Documentation**: https://pandas.pydata.org/docs/

---

## 🎉 Congratulations!

You now have everything you need to use PROJECT NIV effectively. Start with the one-time run script for quick results, then explore the advanced features as you become more comfortable with the platform.

**Happy analyzing! 📊✨**