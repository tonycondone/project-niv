#!/usr/bin/env python3
"""
Example Usage Script for PROJECT NIV ETL Process
Demonstrates different ways to use the ETL functionality
"""

import json
from etl_processor import ETLProcessor

def example_basic_etl():
    """Example: Basic ETL process"""
    print("🔄 Example 1: Basic ETL Process")
    print("-" * 40)
    
    etl = ETLProcessor()
    
    # Run basic ETL
    results = etl.run_full_etl('sample.csv')
    
    print(f"✅ Processed {results['summary']['processed_rows']} rows")
    print(f"📁 Output files: {list(results['output_files'].keys())}")
    print(f"📈 Charts: {len(results['chart_configs'])}")
    
    return etl

def example_filtered_etl():
    """Example: ETL with filters"""
    print("\n🔄 Example 2: ETL with Filters")
    print("-" * 40)
    
    etl = ETLProcessor()
    
    # Define filters
    filters = {
        'Sales': {'min': 1500, 'max': 2500},
        'Category': ['Electronics']
    }
    
    results = etl.run_full_etl('sample_detailed.csv', filters=filters)
    
    print(f"✅ Filtered to {results['summary']['processed_rows']} rows")
    print(f"🔍 Filters: Sales 1500-2500, Category=Electronics")
    
    return etl

def example_transformations():
    """Example: ETL with transformations"""
    print("\n🔄 Example 3: ETL with Transformations")
    print("-" * 40)
    
    etl = ETLProcessor()
    
    # Define transformations
    transformations = ['normalize', 'standardize']
    
    results = etl.run_full_etl('sample_detailed.csv', transformations=transformations)
    
    print(f"✅ Applied transformations: {', '.join(transformations)}")
    print(f"📊 Processed {results['summary']['processed_rows']} rows")
    
    return etl

def example_chart_generation(etl):
    """Example: Generate specific charts"""
    print("\n📊 Example 4: Chart Generation")
    print("-" * 40)
    
    if etl is None or etl.filtered_data is None:
        print("❌ No ETL data available")
        return
    
    # Generate different chart types
    chart_types = ['line', 'bar', 'pie', 'scatter']
    
    for chart_type in chart_types:
        try:
            config = etl.generate_apexcharts_config(chart_type)
            print(f"✅ {chart_type.upper()} chart config generated")
            
            # Save individual chart config
            with open(f'reports/{chart_type}_chart.json', 'w') as f:
                json.dump(config, f, indent=2)
            print(f"   💾 Saved to: reports/{chart_type}_chart.json")
            
        except Exception as e:
            print(f"❌ {chart_type.upper()} chart failed: {str(e)}")

def example_flow_chart(etl):
    """Example: Generate flow chart"""
    print("\n🔄 Example 5: Flow Chart Generation")
    print("-" * 40)
    
    if etl is None:
        print("❌ No ETL processor available")
        return
    
    flow_data = etl.create_flow_chart_data()
    
    print("✅ Flow chart data generated:")
    for node in flow_data['nodes']:
        status = "✅" if node['status'] == 'completed' else "⏳"
        print(f"   {status} {node['label']}")
    
    # Save flow chart data
    with open('reports/flow_chart.json', 'w') as f:
        json.dump(flow_data, f, indent=2)
    print("💾 Flow chart saved to: reports/flow_chart.json")

def main():
    """Main example function"""
    print("=" * 60)
    print("📚 PROJECT NIV - ETL USAGE EXAMPLES")
    print("=" * 60)
    
    # Run examples
    etl1 = example_basic_etl()
    etl2 = example_filtered_etl()
    etl3 = example_transformations()
    
    # Use the last ETL for chart examples
    demo_etl = etl3 or etl2 or etl1
    
    if demo_etl:
        example_chart_generation(demo_etl)
        example_flow_chart(demo_etl)
    
    print("\n" + "=" * 60)
    print("🎉 EXAMPLES COMPLETED!")
    print("🌐 To view interactive charts:")
    print("   python3 main.py --mode web")
    print("   Then visit: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    main()