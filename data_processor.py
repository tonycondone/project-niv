import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
from datetime import datetime
from typing import Tuple, Dict, List, Optional
from logger_config import logger
from config_manager import config

class DataProcessor:
    """Handles data processing, analysis, and report generation."""
    
    def __init__(self):
        self.reports_dir = config.get('reports_dir', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        self.setup_matplotlib()
    
    def setup_matplotlib(self):
        """Configure matplotlib for better chart styling."""
        plt.style.use('seaborn-v0_8')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV or Excel file with validation."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            
            if df.empty:
                raise ValueError("Data file is empty")
            
            logger.info(f"Successfully loaded data from {file_path}: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            raise
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data quality and structure."""
        try:
            # Check for required columns
            if df.shape[1] < 2:
                logger.error("Data must have at least 2 columns")
                return False
            
            # Check for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) == 0:
                logger.error("No numeric columns found in data")
                return False
            
            # Check for missing values
            missing_count = df.isnull().sum().sum()
            if missing_count > 0:
                logger.warning(f"Found {missing_count} missing values in data")
            
            logger.info("Data validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            return False
    
    def generate_summary_stats(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive summary statistics."""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns
            summary_stats = []
            
            for col in numeric_cols:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    summary_stats.append({
                        'label': f'{col} - Total',
                        'value': f"{col_data.sum():,.2f}"
                    })
                    summary_stats.append({
                        'label': f'{col} - Average',
                        'value': f"{col_data.mean():,.2f}"
                    })
                    summary_stats.append({
                        'label': f'{col} - Max',
                        'value': f"{col_data.max():,.2f}"
                    })
            
            return {
                'summary_stats': summary_stats,
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'numeric_columns': len(numeric_cols)
            }
            
        except Exception as e:
            logger.error(f"Error generating summary stats: {e}")
            return {}
    
    def create_charts(self, df: pd.DataFrame) -> str:
        """Create multiple chart types for better visualization."""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) == 0:
                logger.warning("No numeric columns for charting")
                return None
            
            # Create subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Data Analysis Dashboard', fontsize=16, fontweight='bold')
            
            # Bar chart
            if len(df) <= 20:  # Only create bar chart for small datasets
                df[numeric_cols[0]].plot(kind='bar', ax=axes[0,0], color='skyblue')
                axes[0,0].set_title('Data Distribution')
                axes[0,0].tick_params(axis='x', rotation=45)
            else:
                axes[0,0].text(0.5, 0.5, 'Dataset too large for bar chart', 
                              ha='center', va='center', transform=axes[0,0].transAxes)
                axes[0,0].set_title('Data Distribution')
            
            # Line chart
            if len(numeric_cols) >= 2:
                df[numeric_cols[0]].plot(kind='line', ax=axes[0,1], color='green', marker='o')
                axes[0,1].set_title('Trend Analysis')
            else:
                axes[0,1].text(0.5, 0.5, 'Insufficient data for trend analysis', 
                              ha='center', va='center', transform=axes[0,1].transAxes)
                axes[0,1].set_title('Trend Analysis')
            
            # Histogram
            df[numeric_cols[0]].hist(bins=min(20, len(df)//2), ax=axes[1,0], color='orange', alpha=0.7)
            axes[1,0].set_title('Data Distribution (Histogram)')
            
            # Box plot
            if len(numeric_cols) >= 2:
                df[numeric_cols].boxplot(ax=axes[1,1])
                axes[1,1].set_title('Data Comparison')
            else:
                df[numeric_cols[0]].plot(kind='box', ax=axes[1,1], color='purple')
                axes[1,1].set_title('Data Distribution (Box Plot)')
            
            plt.tight_layout()
            
            # Save chart
            chart_path = os.path.join(self.reports_dir, f'chart_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Chart saved to {chart_path}")
            return chart_path
            
        except Exception as e:
            logger.error(f"Error creating charts: {e}")
            return None
    
    def generate_excel_report(self, df: pd.DataFrame) -> str:
        """Generate comprehensive Excel report with multiple sheets."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.reports_dir, f'report_{timestamp}.xlsx')
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Main data sheet
                df.to_excel(writer, sheet_name='Data', index=False)
                
                # Summary statistics sheet
                summary_df = df.describe()
                summary_df.to_excel(writer, sheet_name='Summary')
                
                # Data info sheet
                info_data = {
                    'Metric': ['Total Rows', 'Total Columns', 'Numeric Columns', 'Text Columns', 'Missing Values'],
                    'Value': [
                        len(df),
                        len(df.columns),
                        len(df.select_dtypes(include=['number']).columns),
                        len(df.select_dtypes(include=['object']).columns),
                        df.isnull().sum().sum()
                    ]
                }
                pd.DataFrame(info_data).to_excel(writer, sheet_name='Data Info', index=False)
            
            logger.info(f"Excel report saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating Excel report: {e}")
            raise
    
    def generate_report(self, data_file: Optional[str] = None) -> Tuple[str, str, Dict]:
        """Main method to generate complete report."""
        try:
            # Use config file path or provided path
            file_path = data_file or config.get('data_file', 'data/sample.csv')
            
            # Load and validate data
            df = self.load_data(file_path)
            if not self.validate_data(df):
                raise ValueError("Data validation failed")
            
            # Generate summary statistics
            summary_stats = self.generate_summary_stats(df)
            
            # Create charts
            chart_path = self.create_charts(df)
            
            # Generate Excel report
            excel_path = self.generate_excel_report(df)
            
            # Create text summary
            summary_text = df.describe().to_string()
            
            logger.info("Report generation completed successfully")
            return excel_path, summary_text, summary_stats
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise

# Backward compatibility function
def generate_report(data_file: Optional[str] = None) -> Tuple[str, str]:
    """Legacy function for backward compatibility."""
    processor = DataProcessor()
    excel_path, summary_text, _ = processor.generate_report(data_file)
    return excel_path, summary_text