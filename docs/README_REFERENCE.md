# PROJECT NIV - README Analysis Reference

## Project Overview
**PROJECT NIV** is a professional data analysis and visualization platform that combines powerful ETL processing with a modern TypeScript/TSX dashboard interface. The platform is designed for data analysts, business intelligence professionals, and developers.

## Core Goals
- Transform raw data into actionable insights
- Provide a complete data pipeline with ETL processing
- Offer interactive visualizations powered by ApexCharts.js
- Deliver a professional dashboard with black, white, and light neon blue theme
- Enable one-click data processing with automatic dependency installation

## Main Features

### 1. Professional TSX Dashboard
- Modern TypeScript/TSX interface
- Black, white, and light neon blue color scheme (#00D4FF)
- Real-time data processing and visualization updates
- Responsive design for desktop, tablet, and mobile
- Interactive ApexCharts.js visualizations

### 2. Complete ETL Pipeline
- **Extract**: CSV support with automatic encoding detection
- **Transform**: Advanced filtering and data transformations
- **Load**: Multiple output formats (Excel, JSON, CSV)

### 3. Advanced Filtering System
- Range filters: `{"Sales": {"min": 1000, "max": 5000}}`
- Value filters: `{"Category": ["Electronics", "Hardware"]}`
- Custom conditions with complex boolean logic
- Multiple criteria combination

### 4. Data Transformations
- Normalization (Min-max scaling 0-1)
- Standardization (Z-score normalization)
- Log transformation
- Extensible transformation pipeline

### 5. Interactive Visualizations
- Line charts for time series analysis
- Bar charts for comparative analysis
- Area charts for filled trends
- Pie charts for distribution analysis
- Scatter plots for correlation analysis

### 6. Web Server & API
- Flask-based web server
- RESTful API endpoints
- Real-time data refresh
- Export functionality
- SVG flow charts with status indicators

## Data Sources
- CSV files with automatic encoding detection
- Sample data included (sample.csv, sample_detailed.csv)
- Support for various data formats and structures

## Target Users
- Data analysts
- Business intelligence professionals
- Developers
- Enterprise applications
- Data science teams

## Use Cases
- Sales analytics and revenue analysis
- Financial reporting and KPI monitoring
- ETL pipelines and data processing workflows
- Data exploration and pattern identification
- Report automation and scheduled insights
- Departmental reporting and compliance monitoring
- Executive dashboards and strategic metrics

## Technical Architecture
- **Backend**: Python 3.8+, Flask, Pandas, NumPy
- **Frontend**: TypeScript/TSX, HTML5, CSS3, ApexCharts.js
- **Data Processing**: Pandas, NumPy, OpenPyXL
- **Visualization**: ApexCharts.js, SVG, Matplotlib
- **Web Server**: Flask with static file serving

## Performance Characteristics
- Small datasets (< 1K rows): < 1 second
- Medium datasets (1K-10K rows): 1-5 seconds
- Large datasets (10K+ rows): 5-30 seconds
- Memory efficient with chunked processing
- Parallel processing capabilities
- Intelligent caching for repeated operations

## Key Differentiators
- Professional TSX dashboard with modern design
- One-click processing with zero setup
- Advanced ETL capabilities with real-time updates
- Interactive visualizations with dark theme
- Responsive design for all devices
- Comprehensive API for programmatic access