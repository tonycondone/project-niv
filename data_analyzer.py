#!/usr/bin/env python3
"""
PROJECT NIV - Intelligent Data Analyzer
Automatically detects dataset structure and generates appropriate KPIs
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import Dict, List, Tuple, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class DataAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.column_types = {}
        self.numeric_columns = []
        self.date_columns = []
        self.categorical_columns = []
        self.text_columns = []
        self.analysis_results = {}
        
    def load_data(self) -> pd.DataFrame:
        """Load data and perform initial analysis"""
        try:
            # Try different encodings and separators
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            separators = [',', ';', '\t', '|']
            
            for encoding in encodings:
                for sep in separators:
                    try:
                        self.df = pd.read_csv(self.file_path, encoding=encoding, sep=sep)
                        if self.df.shape[1] > 1:  # Valid if more than 1 column
                            console.print(f"✅ [green]Data loaded successfully![/green] Encoding: {encoding}, Separator: '{sep}'")
                            break
                    except:
                        continue
                if self.df is not None and self.df.shape[1] > 1:
                    break
            
            if self.df is None or self.df.shape[1] <= 1:
                raise ValueError("Could not parse the CSV file with any common format")
                
            console.print(f"📊 Dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
            return self.df
            
        except Exception as e:
            console.print(f"❌ [red]Error loading data: {str(e)}[/red]")
            raise
    
    def analyze_columns(self) -> Dict[str, str]:
        """Analyze each column to determine its type and characteristics"""
        if self.df is None:
            self.load_data()
        
        console.print("🔍 [blue]Analyzing column types...[/blue]")
        
        for column in self.df.columns:
            col_data = self.df[column].dropna()
            
            if len(col_data) == 0:
                self.column_types[column] = 'empty'
                continue
            
            # Check if numeric
            if pd.api.types.is_numeric_dtype(col_data):
                self.column_types[column] = 'numeric'
                self.numeric_columns.append(column)
            
            # Check if date/time
            elif self._is_date_column(col_data):
                self.column_types[column] = 'date'
                self.date_columns.append(column)
            
            # Check if categorical (limited unique values)
            elif self._is_categorical_column(col_data):
                self.column_types[column] = 'categorical'
                self.categorical_columns.append(column)
            
            # Default to text
            else:
                self.column_types[column] = 'text'
                self.text_columns.append(column)
        
        # Display analysis results
        self._display_column_analysis()
        return self.column_types
    
    def _is_date_column(self, col_data: pd.Series) -> bool:
        """Check if column contains date/time data"""
        # Try to parse a sample of the data as dates
        sample_size = min(10, len(col_data))
        sample = col_data.head(sample_size)
        
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\w{3}\s+\d{4}',      # Jan 2023
            r'\w{3}-\d{4}',        # Jan-2023
        ]
        
        for value in sample:
            value_str = str(value).strip()
            if any(re.match(pattern, value_str) for pattern in date_patterns):
                try:
                    pd.to_datetime(value_str)
                    return True
                except:
                    continue
        
        return False
    
    def _is_categorical_column(self, col_data: pd.Series) -> bool:
        """Check if column is categorical"""
        unique_count = col_data.nunique()
        total_count = len(col_data)
        
        # If less than 20 unique values or less than 50% unique, consider categorical
        return unique_count < 20 or (unique_count / total_count) < 0.5
    
    def _display_column_analysis(self):
        """Display column analysis results"""
        table = Table(title="📋 Column Analysis Results", style="cyan")
        table.add_column("Column", style="bold yellow")
        table.add_column("Type", style="green")
        table.add_column("Unique Values", style="blue")
        table.add_column("Null Count", style="red")
        table.add_column("Sample Values", style="dim")
        
        for column in self.df.columns:
            col_type = self.column_types[column]
            unique_count = self.df[column].nunique()
            null_count = self.df[column].isnull().sum()
            
            # Get sample values
            sample_values = self.df[column].dropna().head(3).tolist()
            sample_str = ", ".join([str(v)[:20] for v in sample_values])
            if len(sample_str) > 50:
                sample_str = sample_str[:47] + "..."
            
            table.add_row(
                column,
                col_type,
                str(unique_count),
                str(null_count),
                sample_str
            )
        
        console.print(table)
    
    def generate_kpis(self) -> Dict[str, Any]:
        """Generate KPIs based on detected column types"""
        if not self.column_types:
            self.analyze_columns()
        
        console.print("📈 [blue]Generating dynamic KPIs...[/blue]")
        
        kpis = {
            'dataset_info': {
                'total_rows': len(self.df),
                'total_columns': len(self.df.columns),
                'numeric_columns': len(self.numeric_columns),
                'date_columns': len(self.date_columns),
                'categorical_columns': len(self.categorical_columns)
            }
        }
        
        # Generate numeric KPIs
        if self.numeric_columns:
            kpis['numeric_analysis'] = self._analyze_numeric_columns()
        
        # Generate categorical KPIs
        if self.categorical_columns:
            kpis['categorical_analysis'] = self._analyze_categorical_columns()
        
        # Generate date-based KPIs
        if self.date_columns:
            kpis['temporal_analysis'] = self._analyze_date_columns()
        
        # Generate correlation analysis
        if len(self.numeric_columns) > 1:
            kpis['correlation_analysis'] = self._analyze_correlations()
        
        # Generate data quality metrics
        kpis['data_quality'] = self._analyze_data_quality()
        
        self.analysis_results = kpis
        return kpis
    
    def _analyze_numeric_columns(self) -> Dict[str, Any]:
        """Analyze numeric columns"""
        numeric_analysis = {}
        
        for col in self.numeric_columns:
            col_data = self.df[col].dropna()
            
            numeric_analysis[col] = {
                'count': len(col_data),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()) if len(col_data) > 1 else 0,
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'sum': float(col_data.sum()),
                'range': float(col_data.max() - col_data.min()),
                'cv': float(col_data.std() / col_data.mean()) if col_data.mean() != 0 else 0
            }
        
        return numeric_analysis
    
    def _analyze_categorical_columns(self) -> Dict[str, Any]:
        """Analyze categorical columns"""
        categorical_analysis = {}
        
        for col in self.categorical_columns:
            col_data = self.df[col].dropna()
            value_counts = col_data.value_counts()
            
            categorical_analysis[col] = {
                'unique_count': len(value_counts),
                'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_common_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                'distribution': dict(value_counts.head(10).to_dict()),
                'entropy': self._calculate_entropy(value_counts)
            }
        
        return categorical_analysis
    
    def _analyze_date_columns(self) -> Dict[str, Any]:
        """Analyze date columns"""
        temporal_analysis = {}
        
        for col in self.date_columns:
            try:
                date_series = pd.to_datetime(self.df[col], errors='coerce').dropna()
                
                temporal_analysis[col] = {
                    'date_range': {
                        'start': date_series.min().strftime('%Y-%m-%d'),
                        'end': date_series.max().strftime('%Y-%m-%d'),
                        'days': (date_series.max() - date_series.min()).days
                    },
                    'frequency': self._detect_frequency(date_series),
                    'gaps': self._detect_date_gaps(date_series)
                }
            except Exception as e:
                console.print(f"⚠️ [yellow]Could not analyze date column {col}: {str(e)}[/yellow]")
        
        return temporal_analysis
    
    def _analyze_correlations(self) -> Dict[str, Any]:
        """Analyze correlations between numeric columns"""
        numeric_df = self.df[self.numeric_columns].select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {}
        
        correlation_matrix = numeric_df.corr()
        
        # Find strongest correlations
        correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                col1 = correlation_matrix.columns[i]
                col2 = correlation_matrix.columns[j]
                corr_value = correlation_matrix.iloc[i, j]
                
                if not np.isnan(corr_value):
                    correlations.append({
                        'column1': col1,
                        'column2': col2,
                        'correlation': float(corr_value),
                        'strength': self._correlation_strength(abs(corr_value))
                    })
        
        # Sort by absolute correlation value
        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            'top_correlations': correlations[:5],
            'correlation_matrix': correlation_matrix.to_dict()
        }
    
    def _analyze_data_quality(self) -> Dict[str, Any]:
        """Analyze data quality metrics"""
        total_cells = self.df.shape[0] * self.df.shape[1]
        null_cells = self.df.isnull().sum().sum()
        
        quality_metrics = {
            'completeness': float((total_cells - null_cells) / total_cells * 100),
            'null_percentage': float(null_cells / total_cells * 100),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'columns_with_nulls': list(self.df.columns[self.df.isnull().any()]),
            'data_types_consistent': self._check_data_consistency()
        }
        
        return quality_metrics
    
    def _calculate_entropy(self, value_counts: pd.Series) -> float:
        """Calculate entropy for categorical distribution"""
        probabilities = value_counts / value_counts.sum()
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return float(entropy)
    
    def _detect_frequency(self, date_series: pd.Series) -> str:
        """Detect frequency of date series"""
        if len(date_series) < 2:
            return "insufficient_data"
        
        date_series_sorted = date_series.sort_values()
        differences = date_series_sorted.diff().dropna()
        
        if len(differences) == 0:
            return "single_date"
        
        mode_diff = differences.mode()
        if len(mode_diff) == 0:
            return "irregular"
        
        avg_diff = mode_diff.iloc[0].days
        
        if avg_diff == 1:
            return "daily"
        elif 6 <= avg_diff <= 8:
            return "weekly"
        elif 28 <= avg_diff <= 32:
            return "monthly"
        elif 88 <= avg_diff <= 95:
            return "quarterly"
        elif 360 <= avg_diff <= 370:
            return "yearly"
        else:
            return f"custom_{avg_diff}_days"
    
    def _detect_date_gaps(self, date_series: pd.Series) -> List[Dict]:
        """Detect gaps in date series"""
        if len(date_series) < 2:
            return []
        
        date_series_sorted = date_series.sort_values()
        differences = date_series_sorted.diff().dropna()
        
        # Find unusually large gaps (more than 2x the median difference)
        if len(differences) == 0:
            return []
        
        median_diff = differences.median()
        large_gaps = differences[differences > median_diff * 2]
        
        gaps = []
        for idx, gap in large_gaps.items():
            gaps.append({
                'start_date': date_series_sorted.loc[idx - 1].strftime('%Y-%m-%d'),
                'end_date': date_series_sorted.loc[idx].strftime('%Y-%m-%d'),
                'gap_days': gap.days
            })
        
        return gaps[:5]  # Return top 5 gaps
    
    def _correlation_strength(self, corr_value: float) -> str:
        """Classify correlation strength"""
        if corr_value >= 0.8:
            return "very_strong"
        elif corr_value >= 0.6:
            return "strong"
        elif corr_value >= 0.4:
            return "moderate"
        elif corr_value >= 0.2:
            return "weak"
        else:
            return "very_weak"
    
    def _check_data_consistency(self) -> bool:
        """Check if data types are consistent within columns"""
        inconsistencies = 0
        
        for column in self.df.columns:
            if self.column_types[column] == 'numeric':
                # Check if all values can be converted to numeric
                try:
                    pd.to_numeric(self.df[column], errors='raise')
                except:
                    inconsistencies += 1
        
        return inconsistencies == 0
    
    def get_recommended_visualizations(self) -> List[Dict[str, str]]:
        """Recommend appropriate visualizations based on data types"""
        recommendations = []
        
        # Time series plots for date + numeric combinations
        if self.date_columns and self.numeric_columns:
            for date_col in self.date_columns:
                for num_col in self.numeric_columns:
                    recommendations.append({
                        'type': 'time_series',
                        'x_column': date_col,
                        'y_column': num_col,
                        'title': f'{num_col} Over Time',
                        'description': f'Shows trend of {num_col} across {date_col}'
                    })
        
        # Bar charts for categorical + numeric combinations
        if self.categorical_columns and self.numeric_columns:
            for cat_col in self.categorical_columns:
                for num_col in self.numeric_columns:
                    recommendations.append({
                        'type': 'bar_chart',
                        'x_column': cat_col,
                        'y_column': num_col,
                        'title': f'{num_col} by {cat_col}',
                        'description': f'Compares {num_col} across different {cat_col} categories'
                    })
        
        # Histograms for numeric columns
        for num_col in self.numeric_columns:
            recommendations.append({
                'type': 'histogram',
                'column': num_col,
                'title': f'Distribution of {num_col}',
                'description': f'Shows the frequency distribution of {num_col} values'
            })
        
        # Correlation heatmap for multiple numeric columns
        if len(self.numeric_columns) > 2:
            recommendations.append({
                'type': 'correlation_heatmap',
                'columns': self.numeric_columns,
                'title': 'Correlation Matrix',
                'description': 'Shows correlations between all numeric variables'
            })
        
        return recommendations[:6]  # Return top 6 recommendations

def main():
    """Test the data analyzer"""
    analyzer = DataAnalyzer('data/sample.csv')
    analyzer.load_data()
    analyzer.analyze_columns()
    kpis = analyzer.generate_kpis()
    
    # Display results
    console.print("\n📊 [bold blue]Generated KPIs:[/bold blue]")
    console.print(Panel(str(kpis), title="Analysis Results", style="green"))
    
    recommendations = analyzer.get_recommended_visualizations()
    console.print(f"\n💡 [bold blue]Visualization Recommendations: {len(recommendations)}[/bold blue]")
    for rec in recommendations:
        console.print(f"• {rec['type']}: {rec['title']}")

if __name__ == "__main__":
    main()