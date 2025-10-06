#!/usr/bin/env python3
"""
PROJECT NIV - Modern KPI Dashboard
Tableau-style dashboard for automated email reporting system
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
import time

# Set up rich console for beautiful terminal output
console = Console()

class KPIDashboard:
    def __init__(self, data_path='data/sample.csv'):
        self.data_path = data_path
        self.df = None
        self.metrics = {}
        self.setup_style()
        
    def setup_style(self):
        """Set up matplotlib and seaborn styling for professional look"""
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
    def load_data(self):
        """Load and prepare data for analysis"""
        console.print("📊 [bold blue]Loading Data...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Reading CSV data...", total=100)
            
            # Simulate loading process
            for i in range(100):
                time.sleep(0.01)
                progress.update(task, advance=1)
            
            self.df = pd.read_csv(self.data_path)
            
        console.print(f"✅ [green]Data loaded successfully![/green] Shape: {self.df.shape}")
        return self.df
        
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        console.print("📈 [bold blue]Calculating KPIs...[/bold blue]")
        
        if self.df is None:
            self.load_data()
            
        # Basic KPIs
        self.metrics = {
            'total_sales': self.df['Sales'].sum(),
            'avg_sales': self.df['Sales'].mean(),
            'max_sales': self.df['Sales'].max(),
            'min_sales': self.df['Sales'].min(),
            'growth_rate': self.calculate_growth_rate(),
            'trend': self.calculate_trend(),
            'performance_score': self.calculate_performance_score(),
            'months_analyzed': len(self.df)
        }
        
        console.print("✅ [green]KPIs calculated successfully![/green]")
        return self.metrics
        
    def calculate_growth_rate(self):
        """Calculate month-over-month growth rate"""
        if len(self.df) < 2:
            return 0
        
        first_month = self.df.iloc[0]['Sales']
        last_month = self.df.iloc[-1]['Sales']
        
        growth = ((last_month - first_month) / first_month) * 100
        return round(growth, 2)
        
    def calculate_trend(self):
        """Determine overall trend direction"""
        if len(self.df) < 2:
            return "Stable"
            
        sales_values = self.df['Sales'].values
        trend_slope = np.polyfit(range(len(sales_values)), sales_values, 1)[0]
        
        if trend_slope > 50:
            return "📈 Strong Growth"
        elif trend_slope > 0:
            return "📊 Growing"
        elif trend_slope < -50:
            return "📉 Declining"
        else:
            return "📊 Stable"
            
    def calculate_performance_score(self):
        """Calculate overall performance score (0-100)"""
        avg_sales = self.df['Sales'].mean()
        max_possible = self.df['Sales'].max() * 1.2  # 20% above max as ideal
        score = min(100, (avg_sales / max_possible) * 100)
        return round(score, 1)
        
    def create_kpi_cards(self):
        """Create KPI cards similar to Tableau dashboards"""
        if not self.metrics:
            self.calculate_kpis()
            
        # KPI Cards
        cards = []
        
        # Total Sales Card
        total_sales_card = Panel(
            Align.center(
                f"[bold white]💰 TOTAL SALES[/bold white]\n"
                f"[bold green]${self.metrics['total_sales']:,}[/bold green]\n"
                f"[dim]Across {self.metrics['months_analyzed']} months[/dim]"
            ),
            style="blue",
            width=20
        )
        
        # Average Sales Card
        avg_sales_card = Panel(
            Align.center(
                f"[bold white]📊 AVG SALES[/bold white]\n"
                f"[bold yellow]${self.metrics['avg_sales']:,.0f}[/bold yellow]\n"
                f"[dim]Per month[/dim]"
            ),
            style="yellow",
            width=20
        )
        
        # Growth Rate Card
        growth_color = "green" if self.metrics['growth_rate'] > 0 else "red"
        growth_card = Panel(
            Align.center(
                f"[bold white]📈 GROWTH[/bold white]\n"
                f"[bold {growth_color}]{self.metrics['growth_rate']:+.1f}%[/bold {growth_color}]\n"
                f"[dim]Overall trend[/dim]"
            ),
            style=growth_color,
            width=20
        )
        
        # Performance Score Card
        perf_color = "green" if self.metrics['performance_score'] > 75 else "yellow" if self.metrics['performance_score'] > 50 else "red"
        performance_card = Panel(
            Align.center(
                f"[bold white]⭐ PERFORMANCE[/bold white]\n"
                f"[bold {perf_color}]{self.metrics['performance_score']}/100[/bold {perf_color}]\n"
                f"[dim]Score[/dim]"
            ),
            style=perf_color,
            width=20
        )
        
        return [total_sales_card, avg_sales_card, growth_card, performance_card]
        
    def create_data_table(self):
        """Create a detailed data table"""
        if self.df is None:
            self.load_data()
            
        table = Table(title="📋 Sales Data Overview", style="cyan")
        table.add_column("Month", style="bold blue")
        table.add_column("Sales ($)", style="green", justify="right")
        table.add_column("vs Avg", style="yellow", justify="center")
        table.add_column("Trend", style="magenta", justify="center")
        
        avg_sales = self.df['Sales'].mean()
        
        for idx, row in self.df.iterrows():
            month = row['Month']
            sales = row['Sales']
            vs_avg = f"{((sales - avg_sales) / avg_sales * 100):+.1f}%"
            
            # Trend indicator
            if idx == 0:
                trend = "🔵"
            else:
                prev_sales = self.df.iloc[idx-1]['Sales']
                if sales > prev_sales:
                    trend = "🟢 ↗"
                elif sales < prev_sales:
                    trend = "🔴 ↘"
                else:
                    trend = "🟡 →"
            
            table.add_row(month, f"${sales:,}", vs_avg, trend)
            
        return table
        
    def create_insights_panel(self):
        """Create insights and recommendations panel"""
        if not self.metrics:
            self.calculate_kpis()
            
        insights = []
        
        # Performance insights
        if self.metrics['performance_score'] > 80:
            insights.append("🎉 Excellent performance! Sales are consistently strong.")
        elif self.metrics['performance_score'] > 60:
            insights.append("👍 Good performance with room for improvement.")
        else:
            insights.append("⚠️ Performance needs attention. Consider strategic review.")
            
        # Growth insights
        if self.metrics['growth_rate'] > 20:
            insights.append("🚀 Strong growth trajectory detected!")
        elif self.metrics['growth_rate'] > 0:
            insights.append("📈 Positive growth trend observed.")
        else:
            insights.append("📉 Declining trend requires immediate action.")
            
        # Best/Worst month
        best_month = self.df.loc[self.df['Sales'].idxmax()]
        worst_month = self.df.loc[self.df['Sales'].idxmin()]
        
        insights.append(f"🏆 Best month: {best_month['Month']} (${best_month['Sales']:,})")
        insights.append(f"📊 Lowest month: {worst_month['Month']} (${worst_month['Sales']:,})")
        
        # Recommendations
        recommendations = []
        if self.metrics['growth_rate'] < 0:
            recommendations.append("• Analyze factors causing decline")
            recommendations.append("• Implement growth strategies")
        else:
            recommendations.append("• Maintain current positive momentum")
            recommendations.append("• Explore expansion opportunities")
            
        insights_text = "\n".join([f"• {insight}" for insight in insights])
        recommendations_text = "\n".join(recommendations)
        
        panel_content = f"[bold blue]📊 KEY INSIGHTS[/bold blue]\n{insights_text}\n\n[bold green]💡 RECOMMENDATIONS[/bold green]\n{recommendations_text}"
        
        return Panel(panel_content, title="Business Intelligence", style="cyan")
        
    def generate_visualizations(self):
        """Generate Tableau-style visualizations"""
        console.print("📊 [bold blue]Generating visualizations...[/bold blue]")
        
        if self.df is None:
            self.load_data()
            
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('PROJECT NIV - Sales Analytics Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Sales Trend Line Chart
        ax1.plot(self.df['Month'], self.df['Sales'], marker='o', linewidth=3, markersize=8, color='#2E86AB')
        ax1.fill_between(self.df['Month'], self.df['Sales'], alpha=0.3, color='#2E86AB')
        ax1.set_title('Sales Trend Over Time', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Sales ($)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Bar Chart with Average Line
        bars = ax2.bar(self.df['Month'], self.df['Sales'], color='#A23B72', alpha=0.8)
        avg_line = ax2.axhline(y=self.df['Sales'].mean(), color='#F18F01', linestyle='--', linewidth=2, label=f'Average: ${self.df["Sales"].mean():,.0f}')
        ax2.set_title('Monthly Sales vs Average', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Sales ($)')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Performance Gauge (Pie chart style)
        performance_score = self.metrics['performance_score']
        remaining = 100 - performance_score
        
        colors = ['#27AE60' if performance_score > 75 else '#F39C12' if performance_score > 50 else '#E74C3C', '#ECF0F1']
        wedges, texts, autotexts = ax3.pie([performance_score, remaining], 
                                          colors=colors, 
                                          startangle=90,
                                          counterclock=False,
                                          autopct=lambda pct: f'{pct:.1f}%' if pct == performance_score else '')
        
        ax3.set_title(f'Performance Score: {performance_score}/100', fontweight='bold', fontsize=12)
        
        # 4. Growth Analysis
        months = list(range(len(self.df)))
        sales_values = self.df['Sales'].values
        
        # Scatter plot with trend line
        ax4.scatter(months, sales_values, color='#8E44AD', s=100, alpha=0.7, edgecolors='black')
        
        # Add trend line
        z = np.polyfit(months, sales_values, 1)
        p = np.poly1d(z)
        ax4.plot(months, p(months), "r--", alpha=0.8, linewidth=2)
        
        ax4.set_title('Growth Trend Analysis', fontweight='bold', fontsize=12)
        ax4.set_xlabel('Month Index')
        ax4.set_ylabel('Sales ($)')
        ax4.grid(True, alpha=0.3)
        
        # Set month labels
        ax4.set_xticks(months)
        ax4.set_xticklabels(self.df['Month'])
        
        plt.tight_layout()
        
        # Save the dashboard
        os.makedirs('reports', exist_ok=True)
        dashboard_path = 'reports/kpi_dashboard.png'
        plt.savefig(dashboard_path, dpi=300, bbox_inches='tight', facecolor='white')
        console.print(f"✅ [green]Dashboard saved to {dashboard_path}[/green]")
        
        return dashboard_path
        
    def display_terminal_dashboard(self):
        """Display the complete KPI dashboard in terminal"""
        console.clear()
        
        # Header
        header = Panel(
            Align.center(
                Text("🚀 PROJECT NIV - KPI DASHBOARD", style="bold white on blue")
            ),
            style="bright_blue"
        )
        console.print(header)
        console.print()
        
        # Load data and calculate metrics
        self.load_data()
        self.calculate_kpis()
        
        # Display KPI Cards
        kpi_cards = self.create_kpi_cards()
        console.print(Columns(kpi_cards, equal=True))
        console.print()
        
        # Display data table
        data_table = self.create_data_table()
        console.print(data_table)
        console.print()
        
        # Display insights
        insights_panel = self.create_insights_panel()
        console.print(insights_panel)
        console.print()
        
        # Generate and display visualization info
        dashboard_path = self.generate_visualizations()
        
        # Footer with actions
        footer_content = f"""
[bold green]📊 Dashboard Generated Successfully![/bold green]

[bold blue]Generated Files:[/bold blue]
• KPI Dashboard: {dashboard_path}
• Excel Report: reports/report.xlsx
• Raw Chart: reports/chart.png

[bold yellow]Next Steps:[/bold yellow]
• View dashboard: open {dashboard_path}
• Check reports folder for all outputs
• Run main.py to send email report

[dim]Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]
        """
        
        footer = Panel(footer_content, title="Summary", style="green")
        console.print(footer)
        
        return dashboard_path

def main():
    """Main function to run the KPI dashboard"""
    dashboard = KPIDashboard()
    dashboard.display_terminal_dashboard()

if __name__ == "__main__":
    main()