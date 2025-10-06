import pandas as pd
import matplotlib.pyplot as plt
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
import time

console = Console()
os.makedirs('reports', exist_ok=True)

def generate_report():
    console.print("📊 [bold blue][PROJECT NIV] Starting enhanced data processing...[/bold blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        
        # Read data
        task1 = progress.add_task("📁 Reading data from data/sample.csv...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task1, advance=1)
        
        df = pd.read_csv('data/sample.csv')
        console.print(f"✅ [green]Data loaded successfully![/green] Shape: {df.shape}")
        
        # Display data preview
        data_table = Table(title="📋 Data Preview", style="cyan")
        for col in df.columns:
            data_table.add_column(col, style="bold")
        
        for _, row in df.iterrows():
            data_table.add_row(*[str(val) for val in row])
        
        console.print(data_table)
        
        # Generate summary
        task2 = progress.add_task("📈 Generating statistical summary...", total=100)
        for i in range(100):
            time.sleep(0.005)
            progress.update(task2, advance=1)
        
        summary = df.describe().to_string()
        
        # Display summary in a nice format
        summary_panel = Panel(
            f"[bold blue]Statistical Summary:[/bold blue]\n\n{summary}",
            title="📊 Data Analysis",
            style="yellow"
        )
        console.print(summary_panel)

        # Generate chart
        task3 = progress.add_task("📊 Creating visualization...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task3, advance=1)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df[df.columns[0]], df[df.columns[1]], color='#2E86AB', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                   f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Monthly Sales Report', fontsize=14, fontweight='bold')
        ax.set_ylabel('Sales ($)', fontsize=12)
        ax.set_xlabel('Month', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        chart_path = 'reports/chart.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        console.print(f"✅ [green]Chart saved to {chart_path}[/green]")

        # Save Excel report
        task4 = progress.add_task("📄 Saving Excel report...", total=100)
        for i in range(100):
            time.sleep(0.005)
            progress.update(task4, advance=1)
        
        output_file = 'reports/report.xlsx'
        
        # Enhanced Excel with formatting
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Sales Data', index=False)
            df.describe().to_excel(writer, sheet_name='Summary Statistics')
        
        console.print(f"✅ [green]Excel report saved to {output_file}[/green]")
    
    success_panel = Panel(
        "[bold green]🎉 Data processing completed successfully![/bold green]\n\n"
        f"[blue]Generated files:[/blue]\n"
        f"• Excel Report: {output_file}\n"
        f"• Visualization: {chart_path}",
        title="✅ Processing Complete",
        style="green"
    )
    console.print(success_panel)
    
    return output_file, summary