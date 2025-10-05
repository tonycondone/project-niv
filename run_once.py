#!/usr/bin/env python3
"""
PROJECT NIV - One-Time Run Script
Simple script to process any CSV file and generate visualizations
"""

import os
import sys
import json
import argparse
from pathlib import Path
from etl_processor import ETLProcessor
from web_server import app
import threading
import time
import webbrowser
from datetime import datetime

def print_banner():
    """Print project banner"""
    print("=" * 70)
    print("🚀 PROJECT NIV - One-Time Data Processing")
    print("📊 ETL + ApexCharts.js Integration")
    print("=" * 70)

def validate_csv_file(file_path):
    """Validate if CSV file exists and is readable"""
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found")
        return False
    
    if not file_path.lower().endswith('.csv'):
        print(f"❌ Error: File '{file_path}' is not a CSV file")
        return False
    
    try:
        import pandas as pd
        pd.read_csv(file_path, nrows=1)  # Test read first row
        return True
    except Exception as e:
        print(f"❌ Error: Cannot read CSV file '{file_path}': {str(e)}")
        return False

def process_csv_file(csv_file, filters=None, transformations=None, output_dir="reports"):
    """Process CSV file with ETL pipeline"""
    print(f"\n🔄 Processing CSV file: {csv_file}")
    print("-" * 50)
    
    # Initialize ETL processor
    etl = ETLProcessor(data_dir=".", output_dir=output_dir)
    
    try:
        # Run ETL process
        results = etl.run_full_etl(
            csv_file=csv_file,
            filters=filters,
            transformations=transformations
        )
        
        print("✅ ETL Process Completed Successfully!")
        print(f"📊 Original rows: {results['summary']['original_rows']}")
        print(f"📊 Processed rows: {results['summary']['processed_rows']}")
        print(f"📊 Columns: {results['summary']['columns']}")
        print(f"📁 Output files: {len(results['output_files'])}")
        print(f"📈 Charts generated: {len(results['chart_configs'])}")
        
        # Print output files
        print("\n📁 Generated Files:")
        for file_type, file_path in results['output_files'].items():
            print(f"   {file_type.upper()}: {file_path}")
        
        # Print chart types
        print("\n📈 Generated Charts:")
        for chart_type in results['chart_configs'].keys():
            print(f"   {chart_type.upper()}: Interactive chart ready")
        
        return etl, results
        
    except Exception as e:
        print(f"❌ ETL process failed: {str(e)}")
        return None, None

def start_web_server(port=5000, open_browser=True):
    """Start web server in background thread"""
    print(f"\n🌐 Starting web server on port {port}...")
    
    def run_server():
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    if open_browser:
        url = f"http://localhost:{port}"
        print(f"🌐 Web dashboard: {url}")
        print("🔄 Opening browser...")
        try:
            webbrowser.open(url)
        except:
            print("⚠️  Could not open browser automatically. Please visit the URL manually.")
    
    return server_thread

def create_sample_data():
    """Create sample data if none exists"""
    sample_data = """Date,Product,Category,Sales,Quantity,Region,Profit
2024-01-01,Widget A,Electronics,1500,10,North,300
2024-01-02,Widget B,Electronics,2200,15,South,440
2024-01-03,Gadget X,Electronics,1800,12,East,360
2024-01-04,Tool Y,Hardware,1200,8,West,240
2024-01-05,Widget A,Electronics,1600,11,North,320
2024-01-06,Gadget Z,Electronics,2500,18,South,500
2024-01-07,Tool X,Hardware,900,6,East,180
2024-01-08,Widget C,Electronics,1900,13,West,380
2024-01-09,Gadget Y,Electronics,2100,14,North,420
2024-01-10,Tool Z,Hardware,1100,7,South,220"""
    
    sample_file = "sample_data.csv"
    with open(sample_file, 'w') as f:
        f.write(sample_data)
    
    print(f"📁 Created sample data file: {sample_file}")
    return sample_file

def interactive_mode():
    """Interactive mode for user input"""
    print("\n🎯 Interactive Mode")
    print("-" * 30)
    
    # Get CSV file
    while True:
        csv_file = input("📁 Enter CSV file path (or press Enter for sample data): ").strip()
        
        if not csv_file:
            csv_file = create_sample_data()
            break
        
        if validate_csv_file(csv_file):
            break
        else:
            print("Please try again or press Enter for sample data.")
    
    # Get filters
    print("\n🔍 Filter Options (press Enter to skip):")
    print("Examples:")
    print("  Range filter: {\"Sales\": {\"min\": 1000, \"max\": 5000}}")
    print("  Value filter: {\"Category\": [\"Electronics\", \"Hardware\"]}")
    
    filters_input = input("Enter filters (JSON format): ").strip()
    filters = None
    if filters_input:
        try:
            filters = json.loads(filters_input)
            print(f"✅ Filters applied: {filters}")
        except json.JSONDecodeError:
            print("⚠️  Invalid JSON format. Skipping filters.")
    
    # Get transformations
    print("\n🔧 Transformation Options:")
    print("Available: normalize, standardize, log_transform")
    print("Example: normalize standardize")
    
    transformations_input = input("Enter transformations (space-separated): ").strip()
    transformations = None
    if transformations_input:
        transformations = transformations_input.split()
        print(f"✅ Transformations applied: {transformations}")
    
    return csv_file, filters, transformations

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='PROJECT NIV - One-Time Data Processing')
    parser.add_argument('--csv', help='CSV file to process')
    parser.add_argument('--filters', help='JSON string of filter conditions')
    parser.add_argument('--transformations', nargs='+', 
                       choices=['normalize', 'log_transform', 'standardize'],
                       help='Data transformations to apply')
    parser.add_argument('--web', action='store_true', 
                       help='Start web dashboard after processing')
    parser.add_argument('--port', type=int, default=5000, 
                       help='Web server port (default: 5000)')
    parser.add_argument('--no-browser', action='store_true', 
                       help='Do not open browser automatically')
    parser.add_argument('--interactive', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Interactive mode
    if args.interactive:
        csv_file, filters, transformations = interactive_mode()
    else:
        # Command line mode
        if not args.csv:
            print("📁 No CSV file provided. Creating sample data...")
            csv_file = create_sample_data()
        else:
            csv_file = args.csv
            if not validate_csv_file(csv_file):
                print("❌ Exiting due to invalid CSV file.")
                return
        
        filters = None
        if args.filters:
            try:
                filters = json.loads(args.filters)
            except json.JSONDecodeError:
                print("⚠️  Invalid JSON format for filters. Skipping.")
        
        transformations = args.transformations
    
    # Process CSV file
    etl, results = process_csv_file(csv_file, filters, transformations)
    
    if etl is None:
        print("❌ Processing failed. Exiting.")
        return
    
    # Start web server if requested
    if args.web:
        server_thread = start_web_server(args.port, not args.no_browser)
        
        print("\n" + "=" * 70)
        print("🎉 PROCESSING COMPLETE!")
        print("=" * 70)
        print("📊 Your data has been processed and visualizations are ready!")
        print(f"🌐 Web dashboard: http://localhost:{args.port}")
        print("🔄 Press Ctrl+C to stop the web server")
        print("=" * 70)
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down web server...")
            print("✅ Goodbye!")
    else:
        print("\n" + "=" * 70)
        print("🎉 PROCESSING COMPLETE!")
        print("=" * 70)
        print("📊 Your data has been processed successfully!")
        print("🌐 To view interactive charts, run:")
        print("   python3 run_once.py --csv your_file.csv --web")
        print("=" * 70)

if __name__ == "__main__":
    main()