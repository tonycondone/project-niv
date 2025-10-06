from data_processor import generate_report
from email_utils import send_email
from kpi_dashboard import KPIDashboard
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import time

console = Console()

def main():
    """Enhanced main function with KPI dashboard integration"""
    console.clear()
    
    # Display startup header
    header = Panel(
        Align.center(
            Text("🚀 PROJECT NIV - AUTOMATED EMAIL REPORTING SYSTEM", style="bold white on blue")
        ),
        style="bright_blue"
    )
    console.print(header)
    console.print()
    
    try:
        # Step 1: Display KPI Dashboard
        console.print("📊 [bold blue]STEP 1: Generating KPI Dashboard[/bold blue]")
        dashboard = KPIDashboard()
        dashboard_path = dashboard.display_terminal_dashboard()
        
        console.print("\n⏳ [yellow]Press Enter to continue to report generation...[/yellow]")
        input()
        
        # Step 2: Generate traditional report
        console.print("\n📊 [bold blue]STEP 2: Generating Traditional Report[/bold blue]")
        report_file, summary = generate_report()
        
        # Step 3: Send email
        console.print("\n📧 [bold blue]STEP 3: Email Delivery[/bold blue]")
        send_email(report_file, summary)
        
        # Final summary
        completion_panel = Panel(
            f"""
[bold green]🎉 PROJECT NIV - ALL TASKS COMPLETED SUCCESSFULLY![/bold green]

[bold blue]Generated Outputs:[/bold blue]
• 📊 KPI Dashboard: {dashboard_path}
• 📄 Excel Report: {report_file}
• 📈 Basic Chart: reports/chart.png
• 📧 Email sent with attachments

[bold yellow]Dashboard Features:[/bold yellow]
• Real-time KPI calculations
• Tableau-style visualizations
• Performance scoring
• Growth trend analysis
• Business insights & recommendations

[dim]All work is now visible on terminal with modern UI![/dim]
            """,
            title="🏁 COMPLETION SUMMARY",
            style="green"
        )
        console.print(completion_panel)
        
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Error: {str(e)}[/bold red]\n\n"
            f"[yellow]💡 Tip: Make sure all dependencies are installed:[/yellow]\n"
            f"[dim]pip install -r requirement.txt[/dim]",
            title="Error",
            style="red"
        )
        console.print(error_panel)

if __name__ == "__main__":
    main()