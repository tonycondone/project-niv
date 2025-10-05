"""
Web Server for ETL Data Visualization
Serves ApexCharts.js visualizations and provides API endpoints
"""

from flask import Flask, render_template, jsonify, request, send_file, send_from_directory
import json
import os
from etl_processor import ETLProcessor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# Global ETL processor instance
etl_processor = ETLProcessor(data_dir='.')

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('chart_template.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/etl-data')
def get_etl_data():
    """API endpoint to get ETL data"""
    try:
        # Check if we have processed data, if not try to load sample data
        if etl_processor.filtered_data is None:
            # Try to load sample data automatically
            try:
                sample_files = ['data/sample_detailed.csv', 'data/sample.csv', 'sample_detailed.csv', 'sample.csv']
                for sample_file in sample_files:
                    if os.path.exists(sample_file):
                        logger.info(f"Auto-loading sample data from {sample_file}")
                        etl_processor.run_full_etl(sample_file)
                        break
                else:
                    return jsonify({'error': 'No ETL data available and no sample data found. Please run ETL process first.'}), 400
            except Exception as e:
                logger.error(f"Error auto-loading sample data: {str(e)}")
                return jsonify({'error': 'No ETL data available. Please run ETL process first.'}), 400
        
        # Generate chart configurations
        chart_configs = {}
        for chart_type in ['line', 'bar', 'area', 'pie']:
            try:
                chart_configs[chart_type] = etl_processor.generate_apexcharts_config(chart_type)
            except Exception as e:
                logger.warning(f"Could not generate {chart_type} chart: {str(e)}")
        
        # Create flow chart data
        flow_data = etl_processor.create_flow_chart_data()
        
        # Prepare response
        response = {
            'chart_configs': chart_configs,
            'flow_data': flow_data,
            'summary': {
                'original_rows': len(etl_processor.raw_data) if etl_processor.raw_data is not None else 0,
                'processed_rows': len(etl_processor.filtered_data) if etl_processor.filtered_data is not None else 0,
                'columns': len(etl_processor.filtered_data.columns) if etl_processor.filtered_data is not None else 0
            },
            'metadata': etl_processor.etl_metadata
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error getting ETL data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/run-etl', methods=['POST'])
def run_etl():
    """API endpoint to run ETL process"""
    try:
        data = request.get_json()
        csv_file = data.get('csv_file', 'sample.csv')
        filters = data.get('filters', None)
        transformations = data.get('transformations', None)
        
        # Run ETL process
        results = etl_processor.run_full_etl(csv_file, filters, transformations)
        
        return jsonify({
            'success': True,
            'message': 'ETL process completed successfully',
            'results': results
        })
    
    except Exception as e:
        logger.error(f"Error running ETL: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart/<chart_type>')
def get_chart_config(chart_type):
    """API endpoint to get specific chart configuration"""
    try:
        if etl_processor.filtered_data is None:
            return jsonify({'error': 'No data available'}), 400
        
        config = etl_processor.generate_apexcharts_config(chart_type)
        return jsonify(config)
    
    except Exception as e:
        logger.error(f"Error getting chart config: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/flow-chart')
def get_flow_chart():
    """API endpoint to get flow chart data"""
    try:
        flow_data = etl_processor.create_flow_chart_data()
        return jsonify(flow_data)
    
    except Exception as e:
        logger.error(f"Error getting flow chart: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/export')
def export_data():
    """API endpoint to export processed data"""
    try:
        if etl_processor.filtered_data is None:
            return jsonify({'error': 'No data available'}), 400
        
        # Save data to temporary file
        output_file = 'reports/exported_data.csv'
        etl_processor.filtered_data.to_csv(output_file, index=False)
        
        return send_file(output_file, as_attachment=True, download_name='etl_export.csv')
    
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'etl_processor': 'ready' if etl_processor else 'not_initialized',
        'data_available': etl_processor.filtered_data is not None
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the web server
    print("🚀 Starting ETL Visualization Server...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔧 API Docs: http://localhost:5000/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)