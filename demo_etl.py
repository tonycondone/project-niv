#!/usr/bin/env python3
"""
ETL Demo Script for PROJECT NIV
Demonstrates the ETL process with ApexCharts.js integration
"""

import json
import os
import sys
from etl_processor import ETLProcessor

def print_banner():
    """Print demo banner"""
    print("=" * 60)
    print("🚀 PROJECT NIV - ETL PROCESS DEMO")
    print("📊 ApexCharts.js Integration")
    print("=" * 60)

def demo_basic_etl():
    """Demo basic ETL process"""
    print("\n🔄 DEMO 1: Basic ETL Process")
    print("-" * 40)
    
    etl = ETLProcessor()
    
    try:
        # Run ETL with sample data
        results = etl.run_full_etl('sample.csv')
        
        print("✅ ETL Process Completed!")
        print(f"📊 Original rows: {results['summary']['original_rows']}")
        print(f"📊 Processed rows: {results['summary']['processed_rows']}")
        print(f"📊 Columns: {results['summary']['columns']}")
        print(f"📁 Output files: {len(results['output_files'])}")
        print(f"📈 Charts generated: {len(results['chart_configs'])}")
        
        return etl
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def demo_filtered_etl():
    """Demo ETL with filters"""
    print("\n🔄 DEMO 2: ETL with Filters")
    print("-" * 40)
    
    etl = ETLProcessor()
    
    # Define filters
    filters = {
        'Sales': {'min': 2000, 'max': 3000}
    }
    
    try:
        results = etl.run_full_etl('sample_detailed.csv', filters=filters)
        
        print("✅ Filtered ETL Process Completed!")
        print(f"📊 Original rows: {results['summary']['original_rows']}")
        print(f"📊 Processed rows: {results['summary']['processed_rows']}")
        print(f"🔍 Filter applied: Sales between 2000-3000")
        
        return etl
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def demo_transformations():
    """Demo ETL with transformations"""
    print("\n🔄 DEMO 3: ETL with Transformations")
    print("-" * 40)
    
    etl = ETLProcessor()
    
    # Define transformations
    transformations = ['normalize', 'standardize']
    
    try:
        results = etl.run_full_etl('sample_detailed.csv', transformations=transformations)
        
        print("✅ Transformation ETL Process Completed!")
        print(f"📊 Original rows: {results['summary']['original_rows']}")
        print(f"📊 Processed rows: {results['summary']['processed_rows']}")
        print(f"🔄 Transformations: {', '.join(transformations)}")
        
        return etl
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def demo_apexcharts_configs(etl):
    """Demo ApexCharts configurations"""
    print("\n📊 DEMO 4: ApexCharts Configurations")
    print("-" * 40)
    
    if etl is None or etl.filtered_data is None:
        print("❌ No ETL data available")
        return
    
    chart_types = ['line', 'bar', 'area', 'pie', 'scatter']
    
    for chart_type in chart_types:
        try:
            config = etl.generate_apexcharts_config(chart_type)
            print(f"✅ {chart_type.upper()} chart config generated")
            print(f"   - Series: {len(config.get('series', []))}")
            print(f"   - Chart type: {config.get('chart', {}).get('type', 'unknown')}")
        except Exception as e:
            print(f"❌ {chart_type.upper()} chart failed: {str(e)}")

def demo_flow_chart(etl):
    """Demo flow chart generation"""
    print("\n🔄 DEMO 5: ETL Flow Chart")
    print("-" * 40)
    
    if etl is None:
        print("❌ No ETL processor available")
        return
    
    try:
        flow_data = etl.create_flow_chart_data()
        
        print("✅ Flow chart data generated!")
        print(f"📊 Nodes: {len(flow_data['nodes'])}")
        print(f"🔗 Edges: {len(flow_data['edges'])}")
        
        print("\n📋 Process Flow:")
        for node in flow_data['nodes']:
            status = "✅" if node['status'] == 'completed' else "⏳"
            print(f"   {status} {node['label']}: {node['description']}")
        
    except Exception as e:
        print(f"❌ Error generating flow chart: {str(e)}")

def save_demo_results(etl):
    """Save demo results for web interface"""
    print("\n💾 DEMO 6: Saving Results for Web Interface")
    print("-" * 40)
    
    if etl is None or etl.filtered_data is None:
        print("❌ No ETL data available")
        return
    
    try:
        # Generate all chart configurations
        chart_configs = {}
        for chart_type in ['line', 'bar', 'area', 'pie']:
            try:
                chart_configs[chart_type] = etl.generate_apexcharts_config(chart_type)
            except Exception as e:
                print(f"⚠️  Could not generate {chart_type} chart: {str(e)}")
        
        # Create flow chart data
        flow_data = etl.create_flow_chart_data()
        
        # Prepare complete results
        results = {
            'chart_configs': chart_configs,
            'flow_data': flow_data,
            'summary': {
                'original_rows': len(etl.raw_data) if etl.raw_data is not None else 0,
                'processed_rows': len(etl.filtered_data) if etl.filtered_data is not None else 0,
                'columns': len(etl.filtered_data.columns) if etl.filtered_data is not None else 0
            },
            'metadata': etl.etl_metadata
        }
        
        # Save to file
        output_file = 'reports/demo_results.json'
        os.makedirs('reports', exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Demo results saved to: {output_file}")
        print(f"📊 Charts: {len(chart_configs)}")
        print(f"🔄 Flow nodes: {len(flow_data['nodes'])}")
        
    except Exception as e:
        print(f"❌ Error saving demo results: {str(e)}")

def main():
    """Main demo function"""
    print_banner()
    
    # Check if data files exist
    if not os.path.exists('data/sample.csv'):
        print("❌ Error: data/sample.csv not found")
        return
    
    if not os.path.exists('data/sample_detailed.csv'):
        print("❌ Error: data/sample_detailed.csv not found")
        return
    
    # Run demos
    etl1 = demo_basic_etl()
    etl2 = demo_filtered_etl()
    etl3 = demo_transformations()
    
    # Use the last successful ETL for demonstrations
    demo_etl = etl3 or etl2 or etl1
    
    if demo_etl:
        demo_apexcharts_configs(demo_etl)
        demo_flow_chart(demo_etl)
        save_demo_results(demo_etl)
    
    print("\n" + "=" * 60)
    print("🎉 ETL DEMO COMPLETED!")
    print("🌐 To view interactive charts, run: python main.py --mode web")
    print("📊 Then visit: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    main()