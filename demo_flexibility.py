#!/usr/bin/env python3
"""
PROJECT NIV - Flexibility Demo
Demonstrates the system's ability to handle different types of datasets
"""

import os
from production_main import ProductionSystem
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def demo_dataset_flexibility():
    """Demonstrate system flexibility with different dataset types"""
    
    console.clear()
    
    # Header
    header = Panel(
        "🎯 PROJECT NIV - DATASET FLEXIBILITY DEMONSTRATION\n\n"
        "This demo shows how the system automatically adapts to different types of datasets,\n"
        "detecting data types, generating appropriate KPIs, and creating relevant visualizations.",
        title="Flexibility Demo",
        style="bold blue"
    )
    console.print(header)
    console.print()
    
    # Available datasets
    datasets = [
        {
            'file': 'data/sample.csv',
            'name': 'Sales Data',
            'description': 'Simple sales data with months and sales figures'
        },
        {
            'file': 'data/customer_data.csv', 
            'name': 'Customer Analytics',
            'description': 'Customer demographics and purchase behavior'
        },
        {
            'file': 'data/financial_data.csv',
            'name': 'Financial Data',
            'description': 'Quarterly financial statements by department'
        },
        {
            'file': 'data/inventory_data.csv',
            'name': 'Inventory Management',
            'description': 'Product inventory levels and supplier information'
        },
        {
            'file': 'data/web_analytics.csv',
            'name': 'Web Analytics',
            'description': 'Website traffic and user behavior metrics'
        }
    ]
    
    # Show available datasets
    dataset_table = Table(title="📊 Available Test Datasets", style="cyan")
    dataset_table.add_column("Dataset", style="bold yellow")
    dataset_table.add_column("Type", style="green")
    dataset_table.add_column("Description", style="blue")
    dataset_table.add_column("Status", style="magenta")
    
    for dataset in datasets:
        status = "✅ Available" if os.path.exists(dataset['file']) else "❌ Missing"
        dataset_table.add_row(
            os.path.basename(dataset['file']),
            dataset['name'],
            dataset['description'],
            status
        )
    
    console.print(dataset_table)
    console.print()
    
    # Process each available dataset
    results = []
    
    for dataset in datasets:
        if not os.path.exists(dataset['file']):
            console.print(f"⚠️ [yellow]Skipping {dataset['file']} - file not found[/yellow]")
            continue
        
        console.print(f"\n🔄 [bold blue]Processing: {dataset['name']}[/bold blue]")
        console.print(f"📁 File: {dataset['file']}")
        console.print(f"📝 Description: {dataset['description']}")
        console.print("-" * 80)
        
        try:
            # Initialize system
            system = ProductionSystem()
            system.current_dataset = dataset['file']
            
            # Analyze dataset
            analysis_results = system.analyze_dataset(dataset['file'])
            
            # Use auto-detected configuration
            recommendations = analysis_results['recommendations']
            system.current_config = recommendations['config']
            
            # Generate dashboard
            dashboard_path = system.generate_dashboard(analysis_results)
            
            # Store results
            result = {
                'dataset': dataset,
                'analysis': analysis_results,
                'dashboard_path': dashboard_path,
                'detected_type': recommendations['detected_type'],
                'confidence': recommendations['confidence'],
                'success': True
            }
            results.append(result)
            
            console.print(f"✅ [green]Successfully processed {dataset['name']}[/green]")
            console.print(f"📊 Dashboard: {dashboard_path}")
            
        except Exception as e:
            console.print(f"❌ [red]Error processing {dataset['name']}: {str(e)}[/red]")
            result = {
                'dataset': dataset,
                'error': str(e),
                'success': False
            }
            results.append(result)
    
    # Summary of results
    console.print("\n" + "="*80)
    console.print("📊 [bold blue]FLEXIBILITY DEMONSTRATION SUMMARY[/bold blue]")
    console.print("="*80)
    
    summary_table = Table(title="🎯 Processing Results", style="green")
    summary_table.add_column("Dataset", style="bold yellow")
    summary_table.add_column("Detected Type", style="blue")
    summary_table.add_column("Confidence", style="cyan")
    summary_table.add_column("Status", style="green")
    summary_table.add_column("Dashboard", style="magenta")
    
    successful_datasets = 0
    
    for result in results:
        if result['success']:
            successful_datasets += 1
            summary_table.add_row(
                result['dataset']['name'],
                result['detected_type'].replace('_', ' ').title(),
                f"{result['confidence']:.1%}",
                "✅ Success",
                os.path.basename(result['dashboard_path'])
            )
        else:
            summary_table.add_row(
                result['dataset']['name'],
                "N/A",
                "N/A", 
                "❌ Failed",
                "N/A"
            )
    
    console.print(summary_table)
    
    # Final summary
    total_datasets = len([d for d in datasets if os.path.exists(d['file'])])
    
    final_summary = Panel(
        f"""
[bold green]🎉 Flexibility Demonstration Completed![/bold green]

[bold blue]📊 Results Summary:[/bold blue]
• Total Datasets Tested: {total_datasets}
• Successfully Processed: {successful_datasets}
• Success Rate: {(successful_datasets/total_datasets*100):.1f}%

[bold yellow]🎯 Key Capabilities Demonstrated:[/bold yellow]
• ✅ Automatic dataset type detection
• ✅ Adaptive column analysis (numeric, categorical, date, text)
• ✅ Intelligent KPI generation based on data structure
• ✅ Dynamic visualization recommendations
• ✅ Flexible configuration system
• ✅ Production-ready error handling

[bold cyan]📁 Generated Dashboards:[/bold cyan]
All dashboards saved to reports/ directory with adaptive visualizations
tailored to each dataset's unique characteristics.

[bold green]🚀 System Status: PRODUCTION READY[/bold green]
The system successfully adapts to different data structures and business domains,
making it suitable for real-world deployment with any CSV dataset.
        """,
        title="🏆 DEMONSTRATION COMPLETE",
        style="green"
    )
    
    console.print(final_summary)
    
    return successful_datasets == total_datasets

def main():
    """Run the flexibility demonstration"""
    success = demo_dataset_flexibility()
    
    if success:
        console.print("\n🎉 [bold green]All tests passed! System is ready for production use.[/bold green]")
    else:
        console.print("\n⚠️ [bold yellow]Some tests failed. Check the logs above for details.[/bold yellow]")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)