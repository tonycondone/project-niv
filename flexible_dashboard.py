#!/usr/bin/env python3
"""
PROJECT NIV - Flexible KPI Dashboard
Adapts to any dataset structure and generates appropriate visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich.text import Text
import time
from typing import Dict, List, Any, Optional
from data_analyzer import DataAnalyzer

console = Console()

class FlexibleDashboard:
    def __init__(self, data_path: str, config: Optional[Dict] = None):
        self.data_path = data_path
        self.config = config or {}
        self.analyzer = DataAnalyzer(data_path)
        self.df = None
        self.kpis = {}
        self.visualizations = []
        
        # Create reports directory
        os.makedirs('reports', exist_ok=True)
        
        # Set up styling
        self.setup_styling()
    
    def setup_styling(self):
        """Set up matplotlib and seaborn styling"""
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
        
        # Custom color palette
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'info': '#3498DB'
        }
    
    def load_and_analyze_data(self):
        """Load data and perform comprehensive analysis"""
        console.print("🔍 [bold blue]Loading and analyzing dataset...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Load data
            task1 = progress.add_task("📁 Loading dataset...", total=100)
            for i in range(50):
                time.sleep(0.01)
                progress.update(task1, advance=2)
            
            self.df = self.analyzer.load_data()
            
            # Analyze columns
            task2 = progress.add_task("🔍 Analyzing column types...", total=100)
            for i in range(50):
                time.sleep(0.01)
                progress.update(task2, advance=2)
            
            self.analyzer.analyze_columns()
            
            # Generate KPIs
            task3 = progress.add_task("📈 Generating KPIs...", total=100)
            for i in range(50):
                time.sleep(0.01)
                progress.update(task3, advance=2)
            
            self.kpis = self.analyzer.generate_kpis()
        
        console.print("✅ [green]Data analysis completed![/green]")
        return self.df, self.kpis
    
    def create_overview_cards(self) -> List[Panel]:
        """Create overview KPI cards based on dataset characteristics"""
        cards = []
        
        # Dataset Overview Card
        dataset_info = self.kpis['dataset_info']
        overview_card = Panel(
            Align.center(
                f"[bold white]📊 DATASET OVERVIEW[/bold white]\n"
                f"[bold cyan]{dataset_info['total_rows']:,} rows[/bold cyan]\n"
                f"[bold cyan]{dataset_info['total_columns']} columns[/bold cyan]\n"
                f"[dim]{self._get_file_size()} MB[/dim]"
            ),
            style="blue",
            width=20
        )
        cards.append(overview_card)
        
        # Data Types Card
        types_card = Panel(
            Align.center(
                f"[bold white]🏷️ DATA TYPES[/bold white]\n"
                f"[bold green]{dataset_info['numeric_columns']} numeric[/bold green]\n"
                f"[bold yellow]{dataset_info['categorical_columns']} categorical[/bold yellow]\n"
                f"[bold blue]{dataset_info['date_columns']} temporal[/bold blue]"
            ),
            style="green",
            width=20
        )
        cards.append(types_card)
        
        # Data Quality Card
        if 'data_quality' in self.kpis:
            quality = self.kpis['data_quality']
            quality_color = "green" if quality['completeness'] > 95 else "yellow" if quality['completeness'] > 80 else "red"
            
            quality_card = Panel(
                Align.center(
                    f"[bold white]✅ DATA QUALITY[/bold white]\n"
                    f"[bold {quality_color}]{quality['completeness']:.1f}% complete[/bold {quality_color}]\n"
                    f"[bold red]{quality['duplicate_rows']} duplicates[/bold red]\n"
                    f"[dim]{len(quality['columns_with_nulls'])} cols w/ nulls[/dim]"
                ),
                style=quality_color,
                width=20
            )
            cards.append(quality_card)
        
        # Primary Metric Card (most important numeric column)
        if self.analyzer.numeric_columns:
            primary_col = self._get_primary_metric_column()
            if primary_col and 'numeric_analysis' in self.kpis:
                numeric_data = self.kpis['numeric_analysis'][primary_col]
                
                primary_card = Panel(
                    Align.center(
                        f"[bold white]🎯 {primary_col.upper()}[/bold white]\n"
                        f"[bold green]{self._format_number(numeric_data['sum'])}[/bold green]\n"
                        f"[bold yellow]Avg: {self._format_number(numeric_data['mean'])}[/bold yellow]\n"
                        f"[dim]Range: {self._format_number(numeric_data['range'])}[/dim]"
                    ),
                    style="cyan",
                    width=20
                )
                cards.append(primary_card)
        
        return cards
    
    def create_data_summary_table(self) -> Table:
        """Create a comprehensive data summary table"""
        table = Table(title="📋 Dataset Summary", style="cyan")
        table.add_column("Column", style="bold yellow")
        table.add_column("Type", style="green")
        table.add_column("Key Statistics", style="blue")
        table.add_column("Quality", style="magenta")
        
        for column in self.df.columns:
            col_type = self.analyzer.column_types[column]
            
            # Generate key statistics based on column type
            if col_type == 'numeric' and 'numeric_analysis' in self.kpis:
                stats = self.kpis['numeric_analysis'][column]
                key_stats = f"Mean: {self._format_number(stats['mean'])}, Range: {self._format_number(stats['range'])}"
            
            elif col_type == 'categorical' and 'categorical_analysis' in self.kpis:
                stats = self.kpis['categorical_analysis'][column]
                key_stats = f"{stats['unique_count']} unique, Mode: {stats['most_common']}"
            
            elif col_type == 'date' and 'temporal_analysis' in self.kpis:
                stats = self.kpis['temporal_analysis'][column]
                key_stats = f"Range: {stats['date_range']['days']} days, Freq: {stats['frequency']}"
            
            else:
                unique_count = self.df[column].nunique()
                key_stats = f"{unique_count} unique values"
            
            # Quality indicator
            null_count = self.df[column].isnull().sum()
            null_pct = (null_count / len(self.df)) * 100
            
            if null_pct == 0:
                quality = "🟢 Perfect"
            elif null_pct < 5:
                quality = "🟡 Good"
            elif null_pct < 20:
                quality = "🟠 Fair"
            else:
                quality = "🔴 Poor"
            
            table.add_row(column, col_type.title(), key_stats, quality)
        
        return table
    
    def create_insights_panel(self) -> Panel:
        """Create intelligent insights based on data analysis"""
        insights = []
        recommendations = []
        
        # Data quality insights
        if 'data_quality' in self.kpis:
            quality = self.kpis['data_quality']
            if quality['completeness'] > 95:
                insights.append("🟢 Excellent data quality - minimal missing values")
            elif quality['completeness'] > 80:
                insights.append("🟡 Good data quality with some missing values")
                recommendations.append("• Consider imputation strategies for missing data")
            else:
                insights.append("🔴 Data quality needs attention - significant missing values")
                recommendations.append("• Investigate causes of missing data")
                recommendations.append("• Consider data cleaning procedures")
            
            if quality['duplicate_rows'] > 0:
                insights.append(f"⚠️ Found {quality['duplicate_rows']} duplicate rows")
                recommendations.append("• Remove or investigate duplicate entries")
        
        # Correlation insights
        if 'correlation_analysis' in self.kpis and self.kpis['correlation_analysis']['top_correlations']:
            top_corr = self.kpis['correlation_analysis']['top_correlations'][0]
            if abs(top_corr['correlation']) > 0.7:
                insights.append(f"🔗 Strong correlation found: {top_corr['column1']} ↔ {top_corr['column2']} ({top_corr['correlation']:.2f})")
                recommendations.append("• Investigate relationship between highly correlated variables")
        
        # Numeric insights
        if 'numeric_analysis' in self.kpis:
            for col, stats in self.kpis['numeric_analysis'].items():
                if stats['cv'] > 1.0:  # High coefficient of variation
                    insights.append(f"📊 High variability in {col} (CV: {stats['cv']:.2f})")
                
                if stats['std'] == 0:
                    insights.append(f"📏 {col} has constant values")
        
        # Temporal insights
        if 'temporal_analysis' in self.kpis:
            for col, stats in self.kpis['temporal_analysis'].items():
                if stats['gaps']:
                    insights.append(f"📅 Date gaps detected in {col}")
                    recommendations.append(f"• Check for missing time periods in {col}")
        
        # General recommendations
        if len(self.analyzer.numeric_columns) > 1:
            recommendations.append("• Consider correlation analysis between numeric variables")
        
        if self.analyzer.date_columns and self.analyzer.numeric_columns:
            recommendations.append("• Time series analysis could reveal trends")
        
        if not insights:
            insights.append("📊 Dataset appears well-structured for analysis")
        
        if not recommendations:
            recommendations.append("• Data is ready for advanced analytics")
        
        insights_text = "\n".join([f"{insight}" for insight in insights[:5]])
        recommendations_text = "\n".join(recommendations[:5])
        
        panel_content = f"[bold blue]🔍 KEY INSIGHTS[/bold blue]\n{insights_text}\n\n[bold green]💡 RECOMMENDATIONS[/bold green]\n{recommendations_text}"
        
        return Panel(panel_content, title="Intelligent Analysis", style="cyan")
    
    def generate_adaptive_visualizations(self) -> str:
        """Generate visualizations that adapt to the dataset structure"""
        console.print("📊 [bold blue]Generating adaptive visualizations...[/bold blue]")
        
        recommendations = self.analyzer.get_recommended_visualizations()
        
        # Determine layout based on number of visualizations
        n_viz = min(len(recommendations), 6)  # Max 6 visualizations
        
        if n_viz <= 2:
            fig, axes = plt.subplots(1, n_viz, figsize=(15, 6))
            if n_viz == 1:
                axes = [axes]
        elif n_viz <= 4:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            axes = axes.flatten()
        else:
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            axes = axes.flatten()
        
        fig.suptitle(f'Adaptive Dashboard - {os.path.basename(self.data_path)}', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Generate each recommended visualization
        for i, rec in enumerate(recommendations[:n_viz]):
            ax = axes[i]
            
            try:
                if rec['type'] == 'time_series':
                    self._create_time_series_plot(ax, rec)
                elif rec['type'] == 'bar_chart':
                    self._create_bar_chart(ax, rec)
                elif rec['type'] == 'histogram':
                    self._create_histogram(ax, rec)
                elif rec['type'] == 'correlation_heatmap':
                    self._create_correlation_heatmap(ax, rec)
                else:
                    self._create_generic_plot(ax, rec)
                
                ax.set_title(rec['title'], fontweight='bold', fontsize=11)
                
            except Exception as e:
                # Fallback visualization
                ax.text(0.5, 0.5, f"Visualization Error:\n{rec['type']}\n{str(e)[:50]}...", 
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f"Error: {rec['title']}", fontweight='bold', fontsize=11)
        
        # Hide unused subplots
        for i in range(n_viz, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        # Save dashboard
        dashboard_path = 'reports/adaptive_dashboard.png'
        plt.savefig(dashboard_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        console.print(f"✅ [green]Adaptive dashboard saved to {dashboard_path}[/green]")
        return dashboard_path
    
    def _create_time_series_plot(self, ax, rec):
        """Create time series plot"""
        date_col = rec['x_column']
        value_col = rec['y_column']
        
        # Convert date column
        dates = pd.to_datetime(self.df[date_col], errors='coerce')
        values = pd.to_numeric(self.df[value_col], errors='coerce')
        
        # Remove NaN values
        valid_mask = ~(dates.isna() | values.isna())
        dates = dates[valid_mask]
        values = values[valid_mask]
        
        if len(dates) > 0:
            # Sort by date
            sorted_indices = dates.argsort()
            dates = dates.iloc[sorted_indices]
            values = values.iloc[sorted_indices]
            
            ax.plot(dates, values, marker='o', linewidth=2, markersize=4, color=self.colors['primary'])
            ax.fill_between(dates, values, alpha=0.3, color=self.colors['primary'])
            
            ax.set_xlabel(date_col)
            ax.set_ylabel(value_col)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
    
    def _create_bar_chart(self, ax, rec):
        """Create bar chart"""
        cat_col = rec['x_column']
        value_col = rec['y_column']
        
        # Group by category and calculate mean
        grouped = self.df.groupby(cat_col)[value_col].mean().sort_values(ascending=False)
        
        # Limit to top 10 categories
        if len(grouped) > 10:
            grouped = grouped.head(10)
        
        bars = ax.bar(range(len(grouped)), grouped.values, color=self.colors['secondary'], alpha=0.8)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, grouped.values)):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(grouped.values) * 0.01,
                   f'{self._format_number(value)}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        ax.set_xticks(range(len(grouped)))
        ax.set_xticklabels(grouped.index, rotation=45, ha='right')
        ax.set_xlabel(cat_col)
        ax.set_ylabel(f'Average {value_col}')
        ax.grid(True, alpha=0.3, axis='y')
    
    def _create_histogram(self, ax, rec):
        """Create histogram"""
        column = rec['column']
        data = pd.to_numeric(self.df[column], errors='coerce').dropna()
        
        if len(data) > 0:
            ax.hist(data, bins=min(30, len(data)//2), color=self.colors['info'], alpha=0.7, edgecolor='black')
            ax.axvline(data.mean(), color=self.colors['danger'], linestyle='--', linewidth=2, label=f'Mean: {self._format_number(data.mean())}')
            ax.axvline(data.median(), color=self.colors['warning'], linestyle='--', linewidth=2, label=f'Median: {self._format_number(data.median())}')
            
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(True, alpha=0.3)
    
    def _create_correlation_heatmap(self, ax, rec):
        """Create correlation heatmap"""
        numeric_cols = rec['columns']
        numeric_df = self.df[numeric_cols].select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] > 1:
            corr_matrix = numeric_df.corr()
            
            # Create heatmap
            sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0, 
                       square=True, ax=ax, cbar_kws={'shrink': 0.8})
            
            ax.set_title('Correlation Matrix', fontweight='bold')
    
    def _create_generic_plot(self, ax, rec):
        """Create a generic plot as fallback"""
        ax.text(0.5, 0.5, f"Custom Visualization\n{rec['type']}\n{rec['description']}", 
               ha='center', va='center', transform=ax.transAxes, fontsize=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    
    def display_dashboard(self):
        """Display the complete adaptive dashboard"""
        console.clear()
        
        # Header
        header = Panel(
            Align.center(
                Text(f"🎯 ADAPTIVE DASHBOARD - {os.path.basename(self.data_path).upper()}", 
                     style="bold white on blue")
            ),
            style="bright_blue"
        )
        console.print(header)
        console.print()
        
        # Load and analyze data
        self.load_and_analyze_data()
        
        # Display overview cards
        overview_cards = self.create_overview_cards()
        console.print(Columns(overview_cards, equal=True))
        console.print()
        
        # Display data summary table
        summary_table = self.create_data_summary_table()
        console.print(summary_table)
        console.print()
        
        # Display insights
        insights_panel = self.create_insights_panel()
        console.print(insights_panel)
        console.print()
        
        # Generate visualizations
        dashboard_path = self.generate_adaptive_visualizations()
        
        # Footer with summary
        footer_content = f"""
[bold green]🎉 Adaptive Dashboard Generated Successfully![/bold green]

[bold blue]📊 Analysis Summary:[/bold blue]
• Dataset: {self.kpis['dataset_info']['total_rows']:,} rows × {self.kpis['dataset_info']['total_columns']} columns
• Data Types: {self.kpis['dataset_info']['numeric_columns']} numeric, {self.kpis['dataset_info']['categorical_columns']} categorical, {self.kpis['dataset_info']['date_columns']} temporal
• Quality Score: {self.kpis['data_quality']['completeness']:.1f}% complete
• Visualizations: {len(self.analyzer.get_recommended_visualizations())} adaptive charts generated

[bold yellow]📁 Generated Files:[/bold yellow]
• Adaptive Dashboard: {dashboard_path}
• Data Analysis: Complete KPI analysis performed
• Recommendations: {len(self.analyzer.get_recommended_visualizations())} visualization suggestions

[bold cyan]🚀 Next Steps:[/bold cyan]
• View dashboard: open {dashboard_path}
• Use insights for data-driven decisions
• Apply recommendations for deeper analysis

[dim]Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]
        """
        
        footer = Panel(footer_content, title="Dashboard Summary", style="green")
        console.print(footer)
        
        return dashboard_path
    
    def _get_primary_metric_column(self) -> Optional[str]:
        """Identify the most important numeric column"""
        if not self.analyzer.numeric_columns:
            return None
        
        # Look for common business metric names
        priority_names = ['sales', 'revenue', 'amount', 'value', 'price', 'cost', 'profit', 'total']
        
        for col in self.analyzer.numeric_columns:
            col_lower = col.lower()
            if any(name in col_lower for name in priority_names):
                return col
        
        # Fall back to column with highest sum
        if 'numeric_analysis' in self.kpis:
            max_sum = 0
            primary_col = None
            for col, stats in self.kpis['numeric_analysis'].items():
                if stats['sum'] > max_sum:
                    max_sum = stats['sum']
                    primary_col = col
            return primary_col
        
        return self.analyzer.numeric_columns[0]
    
    def _format_number(self, value: float) -> str:
        """Format numbers for display"""
        if abs(value) >= 1e9:
            return f"{value/1e9:.1f}B"
        elif abs(value) >= 1e6:
            return f"{value/1e6:.1f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.1f}K"
        elif abs(value) >= 1:
            return f"{value:.1f}"
        else:
            return f"{value:.3f}"
    
    def _get_file_size(self) -> float:
        """Get file size in MB"""
        try:
            size_bytes = os.path.getsize(self.data_path)
            return round(size_bytes / (1024 * 1024), 2)
        except:
            return 0.0

def main():
    """Test the flexible dashboard"""
    dashboard = FlexibleDashboard('data/sample.csv')
    dashboard.display_dashboard()

if __name__ == "__main__":
    main()