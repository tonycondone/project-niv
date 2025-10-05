from data_processor import generate_report
from email_utils import send_email
from etl_processor import ETLProcessor
import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description='PROJECT NIV - ETL Data Analysis Tool')
    parser.add_argument('--mode', choices=['legacy', 'etl', 'web'], default='etl',
                       help='Run mode: legacy (original), etl (new ETL process), web (start web server)')
    parser.add_argument('--csv', default='sample.csv', help='CSV file to process')
    parser.add_argument('--filters', help='JSON string of filter conditions')
    parser.add_argument('--transformations', nargs='+', 
                       choices=['normalize', 'log_transform', 'standardize'],
                       help='Data transformations to apply')
    parser.add_argument('--chart-types', nargs='+', 
                       choices=['line', 'bar', 'area', 'pie', 'scatter'],
                       default=['line', 'bar', 'area', 'pie'],
                       help='Types of charts to generate')
    parser.add_argument('--output-format', choices=['excel', 'csv', 'json'], 
                       default='excel', help='Output format for processed data')
    
    args = parser.parse_args()
    
    if args.mode == 'legacy':
        # Original functionality
        print("🔄 Running legacy mode...")
        report_file, summary = generate_report()
        send_email(report_file, summary)
        print("✅ Legacy report generated and sent")
    
    elif args.mode == 'etl':
        # New ETL functionality
        print("🔄 Running ETL mode...")
        
        # Parse filters if provided
        filters = None
        if args.filters:
            try:
                filters = json.loads(args.filters)
            except json.JSONDecodeError:
                print("❌ Error: Invalid JSON format for filters")
                return
        
        # Initialize ETL processor
        etl = ETLProcessor()
        
        try:
            # Run ETL process
            results = etl.run_full_etl(
                csv_file=args.csv,
                filters=filters,
                transformations=args.transformations
            )
            
            print("✅ ETL Process Completed Successfully!")
            print(f"📊 Original rows: {results['summary']['original_rows']}")
            print(f"📊 Processed rows: {results['summary']['processed_rows']}")
            print(f"📊 Columns: {results['summary']['columns']}")
            print(f"📁 Output files: {list(results['output_files'].values())}")
            print(f"📈 Charts generated: {len(results['chart_configs'])}")
            
            # Save chart configurations for web interface
            charts_file = 'reports/chart_configs.json'
            with open(charts_file, 'w') as f:
                json.dump(results['chart_configs'], f, indent=2)
            print(f"💾 Chart configurations saved to: {charts_file}")
            
        except Exception as e:
            print(f"❌ ETL process failed: {str(e)}")
    
    elif args.mode == 'web':
        # Start web server
        print("🌐 Starting web server...")
        from web_server import app
        app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()