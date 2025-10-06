"""
PROJECT NIV - FastAPI Backend
Professional Data Analysis & Visualization Platform
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PROJECT NIV API",
    description="Professional Data Analysis & Visualization Platform",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global ETL processor instance
class ETLProcessor:
    def __init__(self, data_dir: str = "data", output_dir: str = "reports"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.raw_data = None
        self.filtered_data = None
        self.etl_metadata = {}
        
        # Create output directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/charts", exist_ok=True)
        os.makedirs(f"{output_dir}/data", exist_ok=True)
    
    def extract(self, csv_file: str) -> pd.DataFrame:
        """Extract data from CSV file"""
        try:
            # Handle both relative and absolute paths
            if os.path.isabs(csv_file) or csv_file.startswith('./') or csv_file.startswith('../'):
                file_path = csv_file
            else:
                file_path = os.path.join(self.data_dir, csv_file)
            
            logger.info(f"Extracting data from {file_path}")
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    logger.info(f"Successfully loaded with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("Could not decode CSV file with any supported encoding")
            
            # Store metadata
            self.etl_metadata['extraction'] = {
                'file_path': file_path,
                'rows': len(df),
                'columns': len(df.columns),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Extracted {len(df)} rows and {len(df.columns)} columns")
            self.raw_data = df
            return df
            
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            raise
    
    def transform(self, filters: Optional[Dict] = None, transformations: Optional[List[str]] = None) -> pd.DataFrame:
        """Transform data with filters and transformations"""
        if self.raw_data is None:
            raise ValueError("No data to transform. Call extract() first.")
        
        logger.info("Starting data transformation")
        df = self.raw_data.copy()
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        # Apply transformations
        if transformations:
            df = self._apply_transformations(df, transformations)
        
        # Clean data
        df = self._clean_data(df)
        
        # Store metadata
        self.etl_metadata['transformation'] = {
            'filters_applied': filters,
            'transformations_applied': transformations,
            'rows_before': len(self.raw_data),
            'rows_after': len(df),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Transformation complete. {len(df)} rows remaining")
        self.filtered_data = df
        return df
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Apply filters to DataFrame"""
        for column, condition in filters.items():
            if column not in df.columns:
                logger.warning(f"Column {column} not found in data")
                continue
            
            if isinstance(condition, dict):
                if 'min' in condition and 'max' in condition:
                    df = df[(df[column] >= condition['min']) & (df[column] <= condition['max'])]
                elif 'min' in condition:
                    df = df[df[column] >= condition['min']]
                elif 'max' in condition:
                    df = df[df[column] <= condition['max']]
            elif isinstance(condition, list):
                df = df[df[column].isin(condition)]
            else:
                df = df[df[column] == condition]
        
        return df
    
    def _apply_transformations(self, df: pd.DataFrame, transformations: List[str]) -> pd.DataFrame:
        """Apply transformations to DataFrame"""
        for transformation in transformations:
            if transformation == 'normalize':
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if df[col].std() != 0:
                        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
            
            elif transformation == 'standardize':
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if df[col].std() != 0:
                        df[col] = (df[col] - df[col].mean()) / df[col].std()
            
            elif transformation == 'log_transform':
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if (df[col] > 0).all():
                        df[col] = np.log1p(df[col])
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data by removing duplicates and handling missing values"""
        initial_rows = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
        df[non_numeric_cols] = df[non_numeric_cols].fillna('Unknown')
        
        # Try to convert object columns to numeric
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_numeric(df[col], errors='raise')
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass
        
        logger.info(f"Data cleaning: {initial_rows - len(df)} duplicates removed")
        return df
    
    def load(self, output_format: str = 'excel') -> Dict[str, str]:
        """Load processed data to files"""
        if self.filtered_data is None:
            raise ValueError("No processed data to load. Call transform() first.")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_files = {}
        
        if output_format == 'excel':
            file_path = f"{self.output_dir}/processed_data_{timestamp}.xlsx"
            self.filtered_data.to_excel(file_path, index=False)
            output_files['excel'] = file_path
        
        elif output_format == 'csv':
            file_path = f"{self.output_dir}/processed_data_{timestamp}.csv"
            self.filtered_data.to_csv(file_path, index=False)
            output_files['csv'] = file_path
        
        elif output_format == 'json':
            file_path = f"{self.output_dir}/data_{timestamp}.json"
            self.filtered_data.to_json(file_path, orient='records', indent=2)
            output_files['json'] = file_path
        
        # Save metadata
        metadata_path = f"{self.output_dir}/etl_metadata_{timestamp}.json"
        with open(metadata_path, 'w') as f:
            json.dump(self.etl_metadata, f, indent=2)
        
        output_files['metadata'] = metadata_path
        logger.info(f"Data loaded to {len(output_files)} files")
        
        return output_files
    
    def generate_apexcharts_config(self, chart_type: str = 'line') -> Dict[str, Any]:
        """Generate ApexCharts configuration"""
        if self.filtered_data is None:
            raise ValueError("No processed data available")
        
        df = self.filtered_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns available for charting")
        
        base_config = {
            'chart': {
                'type': chart_type,
                'height': 350,
                'background': 'transparent',
                'foreColor': '#FFFFFF'
            },
            'theme': {
                'mode': 'dark',
                'palette': 'palette1'
            },
            'colors': ['#00D4FF', '#0099CC', '#00FF88', '#FFB800', '#FF4444']
        }
        
        if chart_type == 'line':
            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                data = df[[x_col, y_col]].head(20).to_dict('records')
                
                config = {
                    **base_config,
                    'title': {
                        'text': f'{x_col} vs {y_col} - Line Chart',
                        'style': { 'color': '#FFFFFF' }
                    },
                    'series': [{
                        'name': y_col,
                        'data': [{'x': str(row[x_col]), 'y': row[y_col]} for row in data]
                    }],
                    'xaxis': {
                        'title': { 'text': x_col },
                        'labels': { 'style': { 'colors': '#B0B0B0' } }
                    },
                    'yaxis': {
                        'title': { 'text': y_col },
                        'labels': { 'style': { 'colors': '#B0B0B0' } }
                    }
                }
            else:
                raise ValueError("Line chart requires at least 2 numeric columns")
        
        elif chart_type == 'bar':
            if len(numeric_cols) >= 1:
                col = numeric_cols[0]
                data = df[col].head(10).to_dict()
                
                config = {
                    **base_config,
                    'title': {
                        'text': f'{col} - Bar Chart',
                        'style': { 'color': '#FFFFFF' }
                    },
                    'series': [{
                        'name': col,
                        'data': list(data.values())
                    }],
                    'xaxis': {
                        'categories': list(data.keys()),
                        'labels': { 'style': { 'colors': '#B0B0B0' } }
                    }
                }
            else:
                raise ValueError("Bar chart requires at least 1 numeric column")
        
        elif chart_type == 'pie':
            if len(numeric_cols) >= 1:
                col = numeric_cols[0]
                data = df[col].head(8).to_dict()
                
                config = {
                    **base_config,
                    'title': {
                        'text': f'{col} - Pie Chart',
                        'style': { 'color': '#FFFFFF' }
                    },
                    'series': list(data.values()),
                    'labels': list(data.keys())
                }
            else:
                raise ValueError("Pie chart requires at least 1 numeric column")
        
        elif chart_type == 'area':
            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                data = df[[x_col, y_col]].head(20).to_dict('records')
                
                config = {
                    **base_config,
                    'title': {
                        'text': f'{x_col} vs {y_col} - Area Chart',
                        'style': { 'color': '#FFFFFF' }
                    },
                    'series': [{
                        'name': y_col,
                        'data': [{'x': str(row[x_col]), 'y': row[y_col]} for row in data]
                    }],
                    'xaxis': {
                        'title': { 'text': x_col },
                        'labels': { 'style': { 'colors': '#B0B0B0' } }
                    },
                    'yaxis': {
                        'title': { 'text': y_col },
                        'labels': { 'style': { 'colors': '#B0B0B0' } }
                    }
                }
            else:
                raise ValueError("Area chart requires at least 2 numeric columns")
        
        elif chart_type == 'scatter':
            if len(numeric_cols) >= 2:
                col1, col2 = numeric_cols[0], numeric_cols[1]
                data = df[[col1, col2]].head(20).to_dict('records')
                
                config = {
                    **base_config,
                    'title': {
                        'text': f'{col1} vs {col2} - Scatter Plot',
                        'style': { 'color': '#FFFFFF' }
                    },
                    'series': [{
                        'name': f'{col1} vs {col2}',
                        'data': [{'x': row[col1], 'y': row[col2]} for row in data]
                    }],
                    'xaxis': {
                        'title': { 'text': col1 },
                        'labels': { 'style': { 'colors': '#B0B0B0' } }
                    },
                    'yaxis': {
                        'title': { 'text': col2 },
                        'labels': { 'style': { 'colors': '#B0B0B0' } }
                    }
                }
            else:
                raise ValueError("Scatter plot requires at least 2 numeric columns")
        
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        return config
    
    def create_flow_chart_data(self) -> Dict[str, Any]:
        """Create flow chart data for ETL process"""
        return {
            'nodes': [
                {'id': 'extract', 'label': 'Extract Data', 'status': 'completed'},
                {'id': 'filter', 'label': 'Filter Data', 'status': 'completed'},
                {'id': 'transform', 'label': 'Transform Data', 'status': 'completed'},
                {'id': 'load', 'label': 'Load Data', 'status': 'completed'},
                {'id': 'visualize', 'label': 'Generate Charts', 'status': 'completed'}
            ],
            'edges': [
                {'from': 'extract', 'to': 'filter'},
                {'from': 'filter', 'to': 'transform'},
                {'from': 'transform', 'to': 'load'},
                {'from': 'load', 'to': 'visualize'}
            ]
        }
    
    def run_full_etl(self, csv_file: str, filters: Optional[Dict] = None, transformations: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run complete ETL process"""
        logger.info("Starting full ETL process")
        
        # Extract
        self.extract(csv_file)
        
        # Transform
        self.transform(filters, transformations)
        
        # Load
        output_files = self.load()
        
        # Generate chart configurations
        chart_configs = {}
        for chart_type in ['line', 'bar', 'area', 'pie']:
            try:
                chart_configs[chart_type] = self.generate_apexcharts_config(chart_type)
            except Exception as e:
                logger.warning(f"Could not generate {chart_type} chart: {str(e)}")
        
        # Create flow chart data
        flow_data = self.create_flow_chart_data()
        
        # Prepare results
        results = {
            'summary': {
                'original_rows': len(self.raw_data) if self.raw_data is not None else 0,
                'processed_rows': len(self.filtered_data) if self.filtered_data is not None else 0,
                'columns': len(self.filtered_data.columns) if self.filtered_data is not None else 0
            },
            'chart_configs': chart_configs,
            'flow_data': flow_data,
            'output_files': output_files,
            'metadata': self.etl_metadata
        }
        
        logger.info("ETL process completed successfully")
        return results

# Global ETL processor instance
etl_processor = ETLProcessor(data_dir='data')

@app.get("/")
async def root():
    return {"message": "PROJECT NIV API", "version": "4.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "etl_processor": "ready",
        "data_available": etl_processor.filtered_data is not None
    }

@app.get("/api/etl-data")
async def get_etl_data():
    """Get ETL data and chart configurations"""
    try:
        # Check if we have processed data, if not try to load sample data
        if etl_processor.filtered_data is None:
            # Try to load sample data automatically
            sample_files = ['data/sample_detailed.csv', 'data/sample.csv']
            for sample_file in sample_files:
                if os.path.exists(sample_file):
                    logger.info(f"Auto-loading sample data from {sample_file}")
                    etl_processor.run_full_etl(sample_file)
                    break
            else:
                raise HTTPException(status_code=400, detail="No ETL data available and no sample data found. Please upload a CSV file first.")
        
        # Generate chart configurations
        chart_configs = {}
        for chart_type in ['line', 'bar', 'area', 'pie']:
            try:
                chart_configs[chart_type] = etl_processor.generate_apexcharts_config(chart_type)
            except Exception as e:
                logger.warning(f"Could not generate {chart_type} chart: {str(e)}")
        
        # Create flow chart data
        flow_data = etl_processor.create_flow_chart_data()
        
        # Prepare response
        response = {
            'chart_configs': chart_configs,
            'flow_data': flow_data,
            'summary': {
                'original_rows': len(etl_processor.raw_data) if etl_processor.raw_data is not None else 0,
                'processed_rows': len(etl_processor.filtered_data) if etl_processor.filtered_data is not None else 0,
                'columns': len(etl_processor.filtered_data.columns) if etl_processor.filtered_data is not None else 0
            },
            'metadata': etl_processor.etl_metadata
        }
        
        return response
    
    except Exception as e:
        logger.error(f"Error getting ETL data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/run-etl")
async def run_etl(
    csv_file: str = "sample_detailed.csv",
    filters: Optional[Dict] = None,
    transformations: Optional[List[str]] = None
):
    """Run ETL process"""
    try:
        results = etl_processor.run_full_etl(csv_file, filters, transformations)
        return {
            'success': True,
            'message': 'ETL process completed successfully',
            'results': results
        }
    except Exception as e:
        logger.error(f"Error running ETL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chart/{chart_type}")
async def get_chart_config(chart_type: str):
    """Get specific chart configuration"""
    try:
        if etl_processor.filtered_data is None:
            raise HTTPException(status_code=400, detail="No data available")
        
        config = etl_processor.generate_apexcharts_config(chart_type)
        return config
    except Exception as e:
        logger.error(f"Error getting chart config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/flow-chart")
async def get_flow_chart():
    """Get flow chart data"""
    try:
        flow_data = etl_processor.create_flow_chart_data()
        return flow_data
    except Exception as e:
        logger.error(f"Error getting flow chart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/export")
async def export_data():
    """Export processed data"""
    try:
        if etl_processor.filtered_data is None:
            raise HTTPException(status_code=400, detail="No data available")
        
        # Save data to temporary file
        output_file = 'reports/exported_data.csv'
        os.makedirs('reports', exist_ok=True)
        etl_processor.filtered_data.to_csv(output_file, index=False)
        
        return FileResponse(
            output_file, 
            media_type='text/csv',
            filename='etl_export.csv'
        )
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)