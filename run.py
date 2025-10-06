#!/usr/bin/env python3
"""
PROJECT NIV - Easy Run Script
Simple entry point to run the production system
"""

import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import pandas
        import matplotlib
        import rich
        import seaborn
        import numpy
        import openpyxl
        return True
    except ImportError as e:
        console.print(f"❌ [red]Missing dependency: {str(e)}[/red]")
        return False

def install_dependencies():
    """Install Python dependencies"""
    console.print("📦 [blue]Installing Python dependencies...[/blue]")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirement.txt"])
        console.print("✅ [green]Dependencies installed successfully![/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"❌ [red]Failed to install dependencies: {e}[/red]")
        return False

def show_usage():
    """Show usage instructions"""
    console.clear()
    
    header = Panel(
        "🚀 PROJECT NIV - PRODUCTION DASHBOARD SYSTEM\n\n"
        "This is a Python-based adaptive analytics platform that works with any CSV dataset.",
        title="Welcome",
        style="bold blue"
    )
    console.print(header)
    
    usage_table = Table(title="🎯 Available Commands", style="cyan")
    usage_table.add_column("Command", style="bold yellow")
    usage_table.add_column("Description", style="green")
    usage_table.add_column("Example", style="blue")
    
    commands = [
        ("python run.py", "Show this help menu", "python run.py"),
        ("python production_main.py", "Run the main production system", "python production_main.py --dataset data/sample.csv"),
        ("python demo_flexibility.py", "Demo system flexibility with multiple datasets", "python demo_flexibility.py"),
        ("python dashboard_demo.py", "Run standalone dashboard demo", "python dashboard_demo.py"),
        ("python main.py", "Run original enhanced system", "python main.py"),
        ("npm run backend", "Run via npm (calls Python)", "npm run backend"),
        ("npm run demo", "Run demo via npm", "npm run demo")
    ]
    
    for command, description, example in commands:
        usage_table.add_row(command, description, example)
    
    console.print(usage_table)
    
    setup_panel = Panel(
        """
[bold blue]🔧 Setup Instructions:[/bold blue]

[bold yellow]1. Install Python Dependencies:[/bold yellow]
   pip install -r requirement.txt
   [dim]OR[/dim]
   npm run install

[bold yellow]2. Run the System:[/bold yellow]
   python production_main.py
   [dim]OR[/dim]
   npm run backend

[bold yellow]3. Try the Demo:[/bold yellow]
   python demo_flexibility.py
   [dim]OR[/dim]
   npm run demo

[bold green]✅ The system will automatically:[/bold green]
• Analyze any CSV dataset
• Generate adaptive KPI dashboards
• Create professional visualizations
• Provide business intelligence insights
        """,
        title="Quick Start",
        style="green"
    )
    console.print(setup_panel)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--install":
            install_dependencies()
            return
        elif sys.argv[1] == "--check":
            if check_dependencies():
                console.print("✅ [green]All dependencies are installed![/green]")
            else:
                console.print("❌ [red]Some dependencies are missing. Run: python run.py --install[/red]")
            return
    
    # Check if dependencies are installed
    if not check_dependencies():
        console.print("⚠️ [yellow]Some dependencies are missing.[/yellow]")
        if input("Install dependencies now? (y/n): ").lower().startswith('y'):
            if install_dependencies():
                console.print("🚀 [green]Ready to run! Use: python production_main.py[/green]")
            return
        else:
            console.print("💡 [blue]Run 'python run.py --install' to install dependencies later.[/blue]")
    
    show_usage()

if __name__ == "__main__":
    main()