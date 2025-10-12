#!/usr/bin/env python3
"""
Data Analysis Script for PROJECT NIV
Analyzes processed data and visualizations
"""

import json
import glob
import os
from datetime import datetime

def analyze_processed_data():
    """Analyze the latest processed data file"""

    # Find the latest data file
    data_files = glob.glob('reports/data_*.json')
    if not data_files:
        print("❌ No processed data files found")
        return

    # Get the most recent file
    latest_file = max(data_files, key=os.path.getctime)

    print(f'📊 ANALYZING PROCESSED DATA: {os.path.basename(latest_file)}')
    print('=' * 60)

    with open(latest_file, 'r') as f:
        processed_data = json.load(f)

    print(f'📋 Total records: {len(processed_data)}')
    if processed_data:
        print(f'📈 Columns: {list(processed_data[0].keys())}')

        # Calculate summary statistics
        sales_values = [item['Sales'] for item in processed_data]
        quantity_values = [item['Quantity'] for item in processed_data]
        profit_values = [item['Profit'] for item in processed_data]

        print(f'\n💰 Sales Summary:')
        print(f'   Total: ${sum(sales_values):,}')
        print(f'   Average: ${sum(sales_values)/len(sales_values):.0f}')
        print(f'   Range: ${min(sales_values)} - ${max(sales_values)}')

        print(f'\n📦 Quantity Summary:')
        print(f'   Total: {sum(quantity_values)} units')
        print(f'   Average: {sum(quantity_values)/len(quantity_values):.1f} units')
        print(f'   Range: {min(quantity_values)} - {max(quantity_values)} units')

        print(f'\n💵 Profit Summary:')
        print(f'   Total: ${sum(profit_values):,}')
        print(f'   Average: ${sum(profit_values)/len(profit_values):.0f}')
        print(f'   Range: ${min(profit_values)} - ${max(profit_values)}')

        # Category breakdown
        categories = {}
        for item in processed_data:
            cat = item['Category']
            categories[cat] = categories.get(cat, 0) + item['Sales']

        print(f'\n🏷️ Sales by Category:')
        for cat, total in categories.items():
            print(f'   {cat}: ${total:,}')

        # Region breakdown
        regions = {}
        for item in processed_data:
            reg = item['Region']
            regions[reg] = regions.get(reg, 0) + item['Sales']

        print(f'\n🌍 Sales by Region:')
        for reg, total in regions.items():
            print(f'   {reg}: ${total:,}')

    # Show visualization files
    print(f'\n🎨 VISUALIZATION FILES:')
    chart_configs = glob.glob('reports/data_*.json')
    excel_files = glob.glob('reports/processed_data_*.xlsx')

    print(f'📊 Chart configurations: {len(chart_configs)}')
    print(f'📋 Excel reports: {len(excel_files)}')

    # Show recent files
    all_files = chart_configs + excel_files
    print(f'\n📁 Recent output files:')
    for file in sorted(all_files, key=os.path.getctime)[-5:]:
        size = os.path.getsize(file)
        file_type = "Chart Config" if file.endswith('.json') else "Excel Report"
        print(f'   {os.path.basename(file)} ({file_type}, {size:,} bytes)')

def show_chart_configurations():
    """Show available chart configurations"""

    print(f'\n📊 CHART CONFIGURATIONS')
    print('=' * 40)

    # Load demo results which contains chart configs
    demo_file = 'reports/demo_results.json'
    if os.path.exists(demo_file):
        with open(demo_file, 'r') as f:
            demo_data = json.load(f)

        chart_configs = demo_data.get('chart_configs', {})

        for chart_type, config in chart_configs.items():
            print(f'\n📈 {chart_type.upper()} CHART:')
            print(f'   Type: {config.get("chart", {}).get("type", "unknown")}')

            # Handle different chart config structures
            if chart_type == 'pie':
                # Pie chart has different structure
                series = config.get('series', [])
                labels = config.get('labels', [])
                print(f'   Data points: {len(series)}')
                print(f'   Labels: {len(labels)}')
                if series:
                    print(f'   Sample values: {series[:3]}')
            else:
                # Line, bar, area charts
                series = config.get('series', [])
                print(f'   Series count: {len(series)}')
                if series and isinstance(series[0], dict):
                    print(f'   Series names: {[s.get("name", "unnamed") for s in series[:3]]}')
                    if len(series) > 3:
                        print(f'   ... and {len(series) - 3} more series')

                # Show sample data points
                if series and len(series) > 0:
                    first_series = series[0]
                    if isinstance(first_series, dict) and 'data' in first_series:
                        sample_data = first_series['data'][:5]  # First 5 data points
                        print(f'   Sample data: {sample_data}')
                    elif isinstance(first_series, (int, float)):
                        print(f'   Sample values: {series[:5]}')

def main():
    """Main analysis function"""
    print(f'🚀 PROJECT NIV - DATA ANALYSIS REPORT')
    print(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 60)

    analyze_processed_data()
    show_chart_configurations()

    print(f'\n✅ ANALYSIS COMPLETE')
    print(f'💡 To view interactive visualizations, run: python3 web_server.py')
    print(f'   Then visit: http://localhost:5000')

if __name__ == "__main__":
    main()