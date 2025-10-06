#!/usr/bin/env python3
"""
PROJECT NIV - Production Main System
Real-time adaptive dashboard system for any dataset
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn

from data_analyzer import DataAnalyzer
from flexible_dashboard import FlexibleDashboard
from dataset_config import DatasetConfig
from data_processor import generate_report
from email_utils import send_email

console = Console()

class ProductionSystem:
    def __init__(self):
        self.config_manager = DatasetConfig()
        self.current_dataset = None
        self.current_config = None
        self.dashboard = None
        
    def display_welcome(self):
        """Display welcome screen"""
        console.clear()
        
        welcome_panel = Panel(
            Align.center(
                Text("🚀 PROJECT NIV - PRODUCTION DASHBOARD SYSTEM", style="bold white on blue")
            ),
            style="bright_blue"
        )
        console.print(welcome_panel)
        
        info_panel = Panel(
            """
[bold green]🎯 Real-time Adaptive Analytics Platform[/bold green]

[bold blue]Capabilities:[/bold blue]
• 📊 Automatic dataset analysis and type detection
• 🎨 Adaptive visualizations for any data structure
• 📈 Intelligent KPI generation
• 🔧 Configurable for different business domains
• 📧 Automated reporting and email delivery
• 🎯 Production-ready for real-world datasets

[bold yellow]Supported Data Types:[/bold yellow]
• Sales & Revenue Data
• Financial Statements
• Customer Analytics
• Inventory Management
• Web Analytics
• HR & Employee Data
• Generic Datasets

[dim]Enter your dataset path to begin analysis...[/dim]
            """,
            title="System Overview",
            style="cyan"
        )
        console.print(info_panel)
        console.print()
    
    def get_dataset_path(self) -> str:
        """Get dataset path from user"""
        while True:
            dataset_path = Prompt.ask(
                "📁 Enter dataset path (CSV file)",
                default="data/sample.csv"
            )
            
            if os.path.exists(dataset_path):
                if dataset_path.lower().endswith('.csv'):
                    return dataset_path
                else:
                    console.print("❌ [red]Please provide a CSV file[/red]")
            else:
                console.print(f"❌ [red]File not found: {dataset_path}[/red]")
                
                # Suggest files in data directory
                if os.path.exists('data'):
                    csv_files = [f for f in os.listdir('data') if f.endswith('.csv')]
                    if csv_files:
                        console.print(f"💡 [yellow]Available CSV files in data/:[/yellow]")
                        for i, file in enumerate(csv_files):
                            console.print(f"   {i+1}. data/{file}")
    
    def analyze_dataset(self, dataset_path: str) -> Dict[str, Any]:
        """Perform comprehensive dataset analysis"""
        console.print("🔍 [bold blue]Analyzing dataset...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task = progress.add_task("Loading and analyzing dataset...", total=100)
            
            # Initialize analyzer
            analyzer = DataAnalyzer(dataset_path)
            progress.update(task, advance=25)
            
            # Load data
            df = analyzer.load_data()
            progress.update(task, advance=25)
            
            # Analyze columns
            analyzer.analyze_columns()
            progress.update(task, advance=25)
            
            # Generate KPIs
            kpis = analyzer.generate_kpis()
            progress.update(task, advance=25)
        
        # Get configuration recommendations
        recommendations = self.config_manager.get_config_recommendations(df.columns.tolist())
        
        return {
            'analyzer': analyzer,
            'dataframe': df,
            'kpis': kpis,
            'recommendations': recommendations
        }
    
    def display_analysis_summary(self, analysis_results: Dict[str, Any]):
        """Display analysis summary"""
        df = analysis_results['dataframe']
        kpis = analysis_results['kpis']
        recommendations = analysis_results['recommendations']
        
        # Dataset overview
        overview_table = Table(title="📊 Dataset Overview", style="cyan")
        overview_table.add_column("Metric", style="bold yellow")
        overview_table.add_column("Value", style="green")
        
        overview_table.add_row("Rows", f"{len(df):,}")
        overview_table.add_row("Columns", str(len(df.columns)))
        overview_table.add_row("File Size", f"{self._get_file_size(self.current_dataset):.2f} MB")
        overview_table.add_row("Detected Type", recommendations['detected_type'].replace('_', ' ').title())
        overview_table.add_row("Confidence", f"{recommendations['confidence']:.1%}")
        overview_table.add_row("Data Quality", f"{kpis['data_quality']['completeness']:.1f}% complete")
        
        console.print(overview_table)
        console.print()
        
        # Column types summary
        types_table = Table(title="📋 Column Types", style="blue")
        types_table.add_column("Type", style="bold")
        types_table.add_column("Count", style="green")
        types_table.add_column("Examples", style="dim")
        
        analyzer = analysis_results['analyzer']
        
        if analyzer.numeric_columns:
            examples = ", ".join(analyzer.numeric_columns[:3])
            if len(analyzer.numeric_columns) > 3:
                examples += "..."
            types_table.add_row("Numeric", str(len(analyzer.numeric_columns)), examples)
        
        if analyzer.categorical_columns:
            examples = ", ".join(analyzer.categorical_columns[:3])
            if len(analyzer.categorical_columns) > 3:
                examples += "..."
            types_table.add_row("Categorical", str(len(analyzer.categorical_columns)), examples)
        
        if analyzer.date_columns:
            examples = ", ".join(analyzer.date_columns[:3])
            if len(analyzer.date_columns) > 3:
                examples += "..."
            types_table.add_row("Date/Time", str(len(analyzer.date_columns)), examples)
        
        if analyzer.text_columns:
            examples = ", ".join(analyzer.text_columns[:3])
            if len(analyzer.text_columns) > 3:
                examples += "..."
            types_table.add_row("Text", str(len(analyzer.text_columns)), examples)
        
        console.print(types_table)
        console.print()
    
    def configure_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Configure analysis parameters"""
        recommendations = analysis_results['recommendations']
        
        console.print("⚙️ [bold blue]Configuration Options[/bold blue]")
        
        # Show detected configuration
        config_panel = Panel(
            f"""
[bold green]🎯 Detected Configuration:[/bold green]
• Type: {recommendations['detected_type'].replace('_', ' ').title()}
• Confidence: {recommendations['confidence']:.1%}
• Description: {recommendations['config']['description']}

[bold blue]Primary Metrics:[/bold blue]
{', '.join(recommendations['config']['primary_metrics']) if recommendations['config']['primary_metrics'] else 'Auto-detected'}

[bold yellow]Visualization Focus:[/bold yellow]
{', '.join(recommendations['config']['visualization_preferences'])}
            """,
            title="Auto-Configuration",
            style="green"
        )
        console.print(config_panel)
        
        # Configuration options
        console.print("\n🛠️ [bold]Configuration Options:[/bold]")
        console.print("1. Use auto-detected configuration (recommended)")
        console.print("2. Select from predefined configurations")
        console.print("3. Create custom configuration")
        
        choice = Prompt.ask("Select option", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            self.current_config = recommendations['config']
            console.print("✅ [green]Using auto-detected configuration[/green]")
        
        elif choice == "2":
            self.config_manager.list_available_configs()
            config_types = list(self.config_manager.configs.keys())
            
            selected_type = Prompt.ask(
                "Select configuration type",
                choices=config_types,
                default=recommendations['detected_type']
            )
            
            self.current_config = self.config_manager.get_config_for_dataset(selected_type)
            console.print(f"✅ [green]Using {selected_type} configuration[/green]")
        
        elif choice == "3":
            df = analysis_results['dataframe']
            self.current_config = self.config_manager.create_custom_config(
                self.current_dataset, 
                df.columns.tolist()
            )
            console.print("✅ [green]Custom configuration created[/green]")
        
        return self.current_config
    
    def generate_dashboard(self, analysis_results: Dict[str, Any]) -> str:
        """Generate adaptive dashboard"""
        console.print("📊 [bold blue]Generating adaptive dashboard...[/bold blue]")
        
        # Create dashboard with configuration
        self.dashboard = FlexibleDashboard(self.current_dataset, self.current_config)
        
        # Use existing analysis results
        self.dashboard.analyzer = analysis_results['analyzer']
        self.dashboard.df = analysis_results['dataframe']
        self.dashboard.kpis = analysis_results['kpis']
        
        # Generate visualizations
        dashboard_path = self.dashboard.generate_adaptive_visualizations()
        
        return dashboard_path
    
    def display_results(self, dashboard_path: str, analysis_results: Dict[str, Any]):
        """Display final results"""
        kpis = analysis_results['kpis']
        
        # Create overview cards
        cards = self.dashboard.create_overview_cards()
        console.print(Columns(cards, equal=True))
        console.print()
        
        # Create summary table
        summary_table = self.dashboard.create_data_summary_table()
        console.print(summary_table)
        console.print()
        
        # Create insights panel
        insights_panel = self.dashboard.create_insights_panel()
        console.print(insights_panel)
        console.print()
        
        # Final summary
        summary_panel = Panel(
            f"""
[bold green]🎉 Production Dashboard Generated Successfully![/bold green]

[bold blue]📊 Analysis Results:[/bold blue]
• Dataset: {kpis['dataset_info']['total_rows']:,} rows × {kpis['dataset_info']['total_columns']} columns
• Quality Score: {kpis['data_quality']['completeness']:.1f}% complete
• Visualizations: {len(self.dashboard.analyzer.get_recommended_visualizations())} adaptive charts
• Configuration: {self.current_config['name']}

[bold yellow]📁 Generated Files:[/bold yellow]
• Dashboard: {dashboard_path}
• Analysis: Complete KPI analysis
• Configuration: Optimized for {self.current_config['name'].lower()}

[bold cyan]🚀 Next Steps:[/bold cyan]
• View dashboard: open {dashboard_path}
• Generate reports for email delivery
• Save configuration for future use
• Apply insights for business decisions

[dim]Ready for production use with real-world datasets![/dim]
            """,
            title="Production Results",
            style="green"
        )
        console.print(summary_panel)
        
        return dashboard_path
    
    def offer_additional_services(self, dashboard_path: str):
        """Offer additional services"""
        console.print("\n🔧 [bold blue]Additional Services Available:[/bold blue]")
        
        services = [
            ("Generate Excel Report", "Create detailed Excel report with data analysis"),
            ("Send Email Report", "Email dashboard and analysis to recipients"),
            ("Export Configuration", "Save current configuration for future use"),
            ("Batch Process Multiple Files", "Process multiple datasets with same configuration")
        ]
        
        service_table = Table()
        service_table.add_column("Option", style="bold yellow")
        service_table.add_column("Service", style="green")
        service_table.add_column("Description", style="blue")
        
        for i, (service, description) in enumerate(services, 1):
            service_table.add_row(str(i), service, description)
        
        console.print(service_table)
        
        while True:
            choice = Prompt.ask(
                "Select additional service (or 'done' to finish)",
                choices=["1", "2", "3", "4", "done"],
                default="done"
            )
            
            if choice == "done":
                break
            elif choice == "1":
                self._generate_excel_report()
            elif choice == "2":
                self._send_email_report(dashboard_path)
            elif choice == "3":
                self._export_configuration()
            elif choice == "4":
                self._batch_process()
    
    def _generate_excel_report(self):
        """Generate Excel report"""
        try:
            report_file, summary = generate_report()
            console.print(f"✅ [green]Excel report generated: {report_file}[/green]")
        except Exception as e:
            console.print(f"❌ [red]Error generating Excel report: {str(e)}[/red]")
    
    def _send_email_report(self, dashboard_path: str):
        """Send email report"""
        if not os.path.exists('reports/report.xlsx'):
            console.print("📊 [yellow]Generating Excel report first...[/yellow]")
            self._generate_excel_report()
        
        try:
            report_file = 'reports/report.xlsx'
            summary = f"Adaptive dashboard analysis for {os.path.basename(self.current_dataset)}"
            send_email(report_file, summary)
        except Exception as e:
            console.print(f"❌ [red]Error sending email: {str(e)}[/red]")
    
    def _export_configuration(self):
        """Export current configuration"""
        if self.current_config:
            config_name = Prompt.ask("Configuration name", default="custom_config")
            config_key = config_name.lower().replace(' ', '_')
            
            self.config_manager.configs[config_key] = self.current_config
            self.config_manager.save_configs()
            
            console.print(f"✅ [green]Configuration saved as '{config_key}'[/green]")
        else:
            console.print("❌ [red]No configuration to export[/red]")
    
    def _batch_process(self):
        """Batch process multiple files"""
        data_dir = Prompt.ask("Enter directory containing CSV files", default="data")
        
        if not os.path.exists(data_dir):
            console.print(f"❌ [red]Directory not found: {data_dir}[/red]")
            return
        
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        if not csv_files:
            console.print(f"❌ [red]No CSV files found in {data_dir}[/red]")
            return
        
        console.print(f"📁 [blue]Found {len(csv_files)} CSV files[/blue]")
        
        if Confirm.ask("Process all files with current configuration?"):
            for csv_file in csv_files:
                file_path = os.path.join(data_dir, csv_file)
                console.print(f"\n🔄 [yellow]Processing {csv_file}...[/yellow]")
                
                try:
                    dashboard = FlexibleDashboard(file_path, self.current_config)
                    dashboard_path = dashboard.display_dashboard()
                    console.print(f"✅ [green]Completed: {dashboard_path}[/green]")
                except Exception as e:
                    console.print(f"❌ [red]Error processing {csv_file}: {str(e)}[/red]")
    
    def _get_file_size(self, file_path: str) -> float:
        """Get file size in MB"""
        try:
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        except:
            return 0.0
    
    def run(self, dataset_path: Optional[str] = None):
        """Run the production system"""
        self.display_welcome()
        
        # Get dataset path
        if not dataset_path:
            dataset_path = self.get_dataset_path()
        
        self.current_dataset = dataset_path
        
        try:
            # Analyze dataset
            analysis_results = self.analyze_dataset(dataset_path)
            
            # Display analysis summary
            self.display_analysis_summary(analysis_results)
            
            # Configure analysis
            self.configure_analysis(analysis_results)
            
            # Generate dashboard
            dashboard_path = self.generate_dashboard(analysis_results)
            
            # Display results
            self.display_results(dashboard_path, analysis_results)
            
            # Offer additional services
            self.offer_additional_services(dashboard_path)
            
            # Final message
            console.print("\n🎉 [bold green]Production system completed successfully![/bold green]")
            console.print(f"📊 [blue]Dashboard available at: {dashboard_path}[/blue]")
            
        except KeyboardInterrupt:
            console.print("\n⚠️ [yellow]Process interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"\n❌ [red]System error: {str(e)}[/red]")
            console.print("💡 [yellow]Please check your dataset format and try again[/yellow]")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="PROJECT NIV - Production Dashboard System")
    parser.add_argument("--dataset", "-d", help="Path to CSV dataset")
    parser.add_argument("--config", "-c", help="Configuration type to use")
    parser.add_argument("--batch", "-b", help="Batch process directory")
    
    args = parser.parse_args()
    
    system = ProductionSystem()
    
    if args.batch:
        # Batch processing mode
        if os.path.exists(args.batch):
            csv_files = [f for f in os.listdir(args.batch) if f.endswith('.csv')]
            for csv_file in csv_files:
                file_path = os.path.join(args.batch, csv_file)
                console.print(f"\n🔄 Processing {csv_file}...")
                system.run(file_path)
        else:
            console.print(f"❌ Directory not found: {args.batch}")
    else:
        # Single file processing
        system.run(args.dataset)

if __name__ == "__main__":
    main()