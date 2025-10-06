#!/usr/bin/env python3
"""
PROJECT NIV - Standalone KPI Dashboard Demo
Demonstrates the modern Tableau-style dashboard functionality
"""

from kpi_dashboard import KPIDashboard
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import sys
import os

console = Console()

def main():
    """Run standalone KPI dashboard demo"""
    console.clear()
    
    # Welcome header
    welcome = Panel(
        Align.center(
            Text("🎯 PROJECT NIV - KPI DASHBOARD DEMO", style="bold white on blue")
        ),
        style="bright_blue"
    )
    console.print(welcome)
    console.print()
    
    # Check if data exists
    if not os.path.exists('data/sample.csv'):
        error_panel = Panel(
            "[bold red]❌ Error: data/sample.csv not found![/bold red]\n\n"
            "[yellow]Please ensure the data file exists before running the dashboard.[/yellow]",
            title="Missing Data",
            style="red"
        )
        console.print(error_panel)
        return
    
    try:
        # Create and display dashboard
        dashboard = KPIDashboard()
        dashboard_path = dashboard.display_terminal_dashboard()
        
        # Additional info
        info_panel = Panel(
            f"""
[bold green]🎉 Dashboard Demo Completed Successfully![/bold green]

[bold blue]What was generated:[/bold blue]
• 📊 Interactive KPI cards with real-time metrics
• 📈 Tableau-style visualizations (4-panel dashboard)
• 📋 Detailed data analysis table
• 💡 Business insights and recommendations
• 📊 Performance scoring system

[bold yellow]Dashboard Features:[/bold yellow]
• Total Sales, Average Sales, Growth Rate, Performance Score
• Trend analysis with visual indicators
• Month-over-month comparison
• Professional styling similar to Tableau
• Export-ready visualizations

[bold cyan]Files Generated:[/bold cyan]
• {dashboard_path}
• Enhanced terminal output with rich formatting

[dim]This demonstrates the modern KPI dashboard integration
that enhances the automated email reporting system.[/dim]
            """,
            title="🏆 Demo Summary",
            style="green"
        )
        console.print(info_panel)
        
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Error running dashboard: {str(e)}[/bold red]\n\n"
            f"[yellow]💡 Make sure dependencies are installed:[/yellow]\n"
            f"[dim]pip install -r requirement.txt[/dim]",
            title="Error",
            style="red"
        )
        console.print(error_panel)

if __name__ == "__main__":
    main()