"""
ETL (Extract, Transform, Load) Processor for CSV Data Analysis
Integrates with ApexCharts.js for interactive visualizations
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLProcessor:
    """
    ETL Processor for handling CSV data with filtering and ApexCharts.js integration
    """
    
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
        """
        Extract data from CSV file
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            Raw DataFrame
        """
        try:
            file_path = os.path.join(self.data_dir, csv_file)
            logger.info(f"Extracting data from {file_path}")
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    logger.info(f"Successfully loaded with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("Could not read CSV with any supported encoding")
            
            # Store metadata
            self.etl_metadata['extract'] = {
                'file': csv_file,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'timestamp': datetime.now().isoformat()
            }
            
            self.raw_data = df
            logger.info(f"Extracted {len(df)} rows and {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            raise
    
    def transform(self, filters: Optional[Dict] = None, 
                  transformations: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Transform data with filtering and data processing
        
        Args:
            filters: Dictionary of filter conditions
            transformations: List of transformation operations
            
        Returns:
            Transformed DataFrame
        """
        if self.raw_data is None:
            raise ValueError("No data to transform. Run extract() first.")
        
        df = self.raw_data.copy()
        logger.info("Starting data transformation")
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        # Apply transformations
        if transformations:
            df = self._apply_transformations(df, transformations)
        
        # Data cleaning
        df = self._clean_data(df)
        
        # Store metadata
        self.etl_metadata['transform'] = {
            'filters_applied': filters,
            'transformations_applied': transformations,
            'rows_after_transform': len(df),
            'timestamp': datetime.now().isoformat()
        }
        
        self.filtered_data = df
        logger.info(f"Transformation complete. {len(df)} rows remaining")
        return df
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Apply filtering conditions to DataFrame"""
        for column, condition in filters.items():
            if column in df.columns:
                if isinstance(condition, dict):
                    # Range filter
                    if 'min' in condition:
                        df = df[df[column] >= condition['min']]
                    if 'max' in condition:
                        df = df[df[column] <= condition['max']]
                    # Value filter
                    if 'values' in condition:
                        df = df[df[column].isin(condition['values'])]
                elif isinstance(condition, list):
                    # List of values
                    df = df[df[column].isin(condition)]
                else:
                    # Single value
                    df = df[df[column] == condition]
        
        return df
    
    def _apply_transformations(self, df: pd.DataFrame, transformations: List[str]) -> pd.DataFrame:
        """Apply data transformations"""
        for transformation in transformations:
            if transformation == 'normalize':
                # Normalize numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
            
            elif transformation == 'log_transform':
                # Log transform numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = np.log1p(df[numeric_cols])
            
            elif transformation == 'standardize':
                # Standardize numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate data"""
        # Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates()
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Fill non-numeric columns with 'Unknown'
        non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
        df[non_numeric_cols] = df[non_numeric_cols].fillna('Unknown')
        
        # Convert data types more carefully
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to numeric, but only if all values can be converted
                try:
                    # Check if all values can be converted to numeric
                    pd.to_numeric(df[col], errors='raise')
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    # Keep as object if conversion fails
                    pass
        
        logger.info(f"Data cleaning: {initial_rows - len(df)} duplicates removed")
        return df
    
    def load(self, output_format: str = 'excel') -> Dict[str, str]:
        """
        Load processed data to output files
        
        Args:
            output_format: Output format ('excel', 'csv', 'json')
            
        Returns:
            Dictionary of output file paths
        """
        if self.filtered_data is None:
            raise ValueError("No data to load. Run transform() first.")
        
        output_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save processed data
        if output_format == 'excel':
            excel_path = os.path.join(self.output_dir, f"processed_data_{timestamp}.xlsx")
            self.filtered_data.to_excel(excel_path, index=False)
            output_files['excel'] = excel_path
        
        elif output_format == 'csv':
            csv_path = os.path.join(self.output_dir, f"processed_data_{timestamp}.csv")
            self.filtered_data.to_csv(csv_path, index=False)
            output_files['csv'] = csv_path
        
        # Save as JSON for ApexCharts
        json_path = os.path.join(self.output_dir, f"data_{timestamp}.json")
        self.filtered_data.to_json(json_path, orient='records', date_format='iso')
        output_files['json'] = json_path
        
        # Save metadata
        metadata_path = os.path.join(self.output_dir, f"etl_metadata_{timestamp}.json")
        with open(metadata_path, 'w') as f:
            json.dump(self.etl_metadata, f, indent=2)
        output_files['metadata'] = metadata_path
        
        logger.info(f"Data loaded to {len(output_files)} files")
        return output_files
    
    def generate_apexcharts_config(self, chart_type: str = 'line') -> Dict[str, Any]:
        """
        Generate ApexCharts.js configuration for the processed data
        
        Args:
            chart_type: Type of chart ('line', 'bar', 'area', 'pie', 'scatter')
            
        Returns:
            ApexCharts configuration dictionary
        """
        if self.filtered_data is None:
            raise ValueError("No data available. Run transform() first.")
        
        df = self.filtered_data
        
        # Get numeric columns for charting
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns found for charting")
        
        # Prepare data based on chart type
        if chart_type in ['line', 'area', 'bar']:
            # Use first categorical column as x-axis, first numeric as y-axis
            x_col = categorical_cols[0] if categorical_cols else df.index
            y_col = numeric_cols[0] if numeric_cols else None
            
            if not numeric_cols:
                raise ValueError("No numeric columns found for charting")
            
            series_data = []
            for col in numeric_cols:
                series_data.append({
                    'name': col,
                    'data': df[col].tolist()
                })
            
            config = {
                'chart': {
                    'type': chart_type,
                    'height': 350,
                    'toolbar': {
                        'show': True
                    }
                },
                'series': series_data,
                'xaxis': {
                    'categories': df[x_col].tolist() if categorical_cols else list(range(len(df)))
                },
                'title': {
                    'text': f'Data Analysis - {chart_type.title()} Chart',
                    'align': 'left'
                },
                'dataLabels': {
                    'enabled': False
                }
            }
        
        elif chart_type == 'pie':
            # Use first numeric column for pie chart
            y_col = numeric_cols[0]
            x_col = categorical_cols[0] if categorical_cols else 'Category'
            
            config = {
                'chart': {
                    'type': 'pie',
                    'height': 350
                },
                'series': df[y_col].tolist(),
                'labels': df[x_col].tolist() if categorical_cols else [f'Item {i+1}' for i in range(len(df))],
                'title': {
                    'text': f'Data Distribution - Pie Chart',
                    'align': 'left'
                }
            }
        
        elif chart_type == 'scatter':
            if len(numeric_cols) < 2:
                raise ValueError("Scatter plot requires at least 2 numeric columns")
            
            col1, col2 = numeric_cols[0], numeric_cols[1]
            config = {
                'chart': {
                    'type': 'scatter',
                    'height': 350
                },
                'series': [{
                    'name': 'Data Points',
                    'data': [[df[col1].iloc[i], df[col2].iloc[i]] for i in range(len(df))]
                }],
                'xaxis': {
                    'title': {
                        'text': col1
                    }
                },
                'yaxis': {
                    'title': {
                        'text': col2
                    }
                },
                'title': {
                    'text': f'Scatter Plot - {col1} vs {col2}',
                    'align': 'left'
                }
            }
        
        return config
    
    def create_flow_chart_data(self) -> Dict[str, Any]:
        """
        Create flow chart data showing ETL process
        
        Returns:
            Flow chart configuration for visualization
        """
        flow_data = {
            'nodes': [
                {
                    'id': 'extract',
                    'label': 'Extract',
                    'type': 'process',
                    'description': f'Data extracted from {self.etl_metadata.get("extract", {}).get("file", "unknown")}',
                    'status': 'completed' if self.raw_data is not None else 'pending'
                },
                {
                    'id': 'filter',
                    'label': 'Filter',
                    'type': 'process',
                    'description': 'Data filtering and cleaning applied',
                    'status': 'completed' if self.filtered_data is not None else 'pending'
                },
                {
                    'id': 'transform',
                    'label': 'Transform',
                    'type': 'process',
                    'description': 'Data transformations and normalization',
                    'status': 'completed' if self.filtered_data is not None else 'pending'
                },
                {
                    'id': 'visualize',
                    'label': 'Visualize',
                    'type': 'output',
                    'description': 'ApexCharts.js visualizations generated',
                    'status': 'pending'
                },
                {
                    'id': 'load',
                    'label': 'Load',
                    'type': 'output',
                    'description': 'Processed data saved to output files',
                    'status': 'pending'
                }
            ],
            'edges': [
                {'from': 'extract', 'to': 'filter'},
                {'from': 'filter', 'to': 'transform'},
                {'from': 'transform', 'to': 'visualize'},
                {'from': 'transform', 'to': 'load'},
                {'from': 'visualize', 'to': 'load'}
            ],
            'metadata': self.etl_metadata
        }
        
        return flow_data
    
    def run_full_etl(self, csv_file: str, filters: Optional[Dict] = None, 
                     transformations: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run complete ETL process
        
        Args:
            csv_file: CSV file to process
            filters: Filter conditions
            transformations: Transformation operations
            
        Returns:
            Complete ETL results
        """
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
        
        results = {
            'output_files': output_files,
            'chart_configs': chart_configs,
            'flow_data': flow_data,
            'summary': {
                'original_rows': len(self.raw_data) if self.raw_data is not None else 0,
                'processed_rows': len(self.filtered_data) if self.filtered_data is not None else 0,
                'columns': len(self.filtered_data.columns) if self.filtered_data is not None else 0
            }
        }
        
        logger.info("ETL process completed successfully")
        return results

# Example usage and testing
if __name__ == "__main__":
    # Initialize ETL processor
    etl = ETLProcessor()
    
    # Example filters
    filters = {
        'Sales': {'min': 1000, 'max': 5000}
    }
    
    # Example transformations
    transformations = ['normalize']
    
    # Run ETL process
    try:
        results = etl.run_full_etl('sample.csv', filters, transformations)
        print("ETL Process Results:")
        print(f"Output files: {results['output_files']}")
        print(f"Summary: {results['summary']}")
    except Exception as e:
        print(f"ETL process failed: {str(e)}")