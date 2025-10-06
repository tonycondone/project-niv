# PROJECT NIV - Preserved Business Logic

## Critical Business Logic to Preserve

### 1. ETL Processing Engine (`etl_processor.py`)

#### Core ETL Class Structure
```python
class ETLProcessor:
    def __init__(self, data_dir: str = "data", output_dir: str = "reports")
    def extract(self, csv_file: str) -> pd.DataFrame
    def transform(self, filters: Optional[Dict], transformations: Optional[List[str]]) -> pd.DataFrame
    def load(self, output_format: str = 'excel') -> Dict[str, str]
    def run_full_etl(self, csv_file: str, filters: Optional[Dict], transformations: Optional[List[str]]) -> Dict[str, Any]
```

#### Key Business Logic
- **Data Extraction**: Robust CSV reading with encoding detection
- **Data Cleaning**: Duplicate removal, missing value imputation, type conversion
- **Advanced Filtering**: Range filters, value filters, custom conditions
- **Data Transformations**: Normalization, standardization, log transforms
- **ApexCharts Integration**: Chart configuration generation for web visualization
- **Flow Chart Generation**: SVG-based process flow visualization

#### Preserved Methods
- `_clean_data()` - Data cleaning and validation
- `_apply_filters()` - Advanced filtering logic
- `_apply_transformations()` - Data transformation pipeline
- `generate_apexcharts_config()` - Chart configuration generation
- `create_flow_chart_data()` - Process flow visualization

### 2. Data Processing Functions (`data_processor.py`)

#### Core Functionality
```python
def generate_report():
    # Read data from CSV
    # Generate summary statistics
    # Create matplotlib charts
    # Save Excel reports
    # Return file paths and summary
```

#### Business Logic
- **Report Generation**: Automated report creation with charts
- **Data Analysis**: Statistical summary generation
- **File Management**: Excel report creation and file handling
- **Chart Generation**: Matplotlib-based visualization

### 3. Email Notification System (`email_utils.py`)

#### Core Functionality
```python
def send_email(attachment_path, summary):
    # Load email configuration
    # Create email message with attachment
    # Send via SMTP
```

#### Business Logic
- **Email Configuration**: JSON-based configuration management
- **Attachment Handling**: File attachment with proper MIME types
- **SMTP Integration**: Secure email sending with authentication
- **Report Distribution**: Automated report delivery

### 4. Web Server API (`web_server.py`)

#### API Endpoints
```python
@app.route('/api/etl-data') - ETL data retrieval
@app.route('/api/run-etl') - ETL process execution
@app.route('/api/chart/<chart_type>') - Chart configuration
@app.route('/api/flow-chart') - Process flow data
@app.route('/api/data/export') - Data export
@app.route('/api/health') - Health check
```

#### Business Logic
- **RESTful API**: Standard HTTP endpoints for data operations
- **Error Handling**: Comprehensive error management and logging
- **Data Validation**: Input validation and sanitization
- **File Serving**: Static file serving for assets
- **Auto Data Loading**: Automatic sample data loading

### 5. Multi-Mode Main Script (`main.py`)

#### Execution Modes
```python
--mode legacy    # Original functionality
--mode etl       # ETL processing
--mode web       # Web server
```

#### Business Logic
- **Command Line Interface**: Argument parsing and validation
- **Mode Selection**: Different execution paths
- **Configuration Management**: JSON-based configuration
- **Error Handling**: Graceful error management

### 6. Data Validation & Type Conversion

#### Preserved Logic
- **Encoding Detection**: Automatic CSV encoding detection
- **Type Inference**: Automatic data type detection and conversion
- **Data Cleaning**: Duplicate removal and missing value handling
- **Validation**: Data quality checks and validation

### 7. Chart Configuration Generation

#### ApexCharts Integration
- **Chart Types**: Line, bar, area, pie, scatter charts
- **Data Formatting**: Proper data formatting for ApexCharts
- **Styling**: Dark theme with neon blue accents
- **Interactivity**: Zoom, pan, and selection capabilities

### 8. File Management & Export

#### Export Capabilities
- **Excel Reports**: Professional .xlsx file generation
- **JSON Data**: Structured data export
- **CSV Export**: Clean processed data export
- **Chart Images**: Static chart image generation

### 9. Process Flow Visualization

#### SVG Flow Charts
- **Node Generation**: Process step visualization
- **Status Indicators**: Real-time process status
- **Edge Connections**: Process flow connections
- **Professional Styling**: Neon blue theme integration

### 10. Configuration Management

#### JSON Configuration
- **Email Settings**: SMTP configuration
- **Data Paths**: Directory configuration
- **Processing Options**: ETL configuration
- **Chart Settings**: Visualization configuration

## Critical Algorithms to Preserve

### 1. Data Filtering Algorithm
```python
def _apply_filters(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    # Range filtering logic
    # Value filtering logic
    # Custom condition handling
    # Multiple criteria combination
```

### 2. Data Transformation Pipeline
```python
def _apply_transformations(self, df: pd.DataFrame, transformations: List[str]) -> pd.DataFrame:
    # Normalization (Min-Max scaling)
    # Standardization (Z-score)
    # Log transformation
    # Custom transformations
```

### 3. Chart Configuration Generation
```python
def generate_apexcharts_config(self, chart_type: str) -> Dict[str, Any]:
    # Chart type detection
    # Data formatting
    # Styling configuration
    # Interactive options
```

### 4. Data Cleaning Pipeline
```python
def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
    # Duplicate removal
    # Missing value imputation
    # Type conversion
    # Data validation
```

## Integration Points

### 1. Frontend-Backend Communication
- RESTful API endpoints
- JSON data exchange
- Real-time updates
- Error handling

### 2. Data Flow
- CSV input → ETL processing → Visualization → Export
- Real-time data updates
- Caching mechanisms
- Performance optimization

### 3. User Interface
- Dashboard components
- Interactive controls
- Chart rendering
- Responsive design

## Security Considerations
- Input validation and sanitization
- File upload security
- Error message sanitization
- Configuration security

## Performance Optimizations
- Chunked data processing
- Memory-efficient operations
- Caching strategies
- Parallel processing