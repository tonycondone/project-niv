#!/usr/bin/env python3
"""
PROJECT NIV - Demo Script
Shows all features of the automated email reporting system
"""

import os
import sys
from datetime import datetime

def print_header():
    print("🚀 PROJECT NIV - AUTOMATED EMAIL REPORTING SYSTEM")
    print("=" * 60)
    print(f"📅 Demo run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def show_project_structure():
    print("\n📁 PROJECT STRUCTURE:")
    print("-" * 30)
    
    structure = {
        "📄 main.py": "Main execution script",
        "📊 data_processor.py": "Data analysis and report generation",
        "📧 email_utils.py": "Email sending functionality",
        "⏰ scheduler.py": "Automated scheduling",
        "📋 config.json": "Email configuration",
        "📁 data/": "Input data directory",
        "   └── sample.csv": "Sample sales data",
        "📁 reports/": "Generated reports directory",
        "   ├── report.xlsx": "Excel report output",
        "   └── chart.png": "Data visualization"
    }
    
    for item, description in structure.items():
        print(f"{item:<20} - {description}")

def show_data_analysis():
    print("\n📊 DATA ANALYSIS DEMO:")
    print("-" * 30)
    
    try:
        import pandas as pd
        df = pd.read_csv('data/sample.csv')
        
        print(f"📋 Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"📊 Columns: {list(df.columns)}")
        print("\n📈 Statistical Summary:")
        print(df.describe())
        
        print("\n📋 Raw Data:")
        print(df.to_string(index=False))
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")

def show_features():
    print("\n✨ KEY FEATURES:")
    print("-" * 30)
    features = [
        "📊 Automated data processing from CSV files",
        "📈 Statistical analysis and visualization",
        "📄 Excel report generation",
        "📧 Email delivery with attachments",
        "⏰ Scheduled automation (weekly reports)",
        "🔧 Configurable email settings",
        "📱 Terminal-friendly output with progress indicators",
        "🛡️ Error handling and user feedback"
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_usage():
    print("\n🚀 USAGE EXAMPLES:")
    print("-" * 30)
    print("1. One-time report generation:")
    print("   python3 main.py")
    print()
    print("2. Start automated scheduler:")
    print("   python3 scheduler.py")
    print()
    print("3. Check generated files:")
    print("   ls -la reports/")
    print()
    print("4. View data summary:")
    print("   python3 -c \"import pandas as pd; print(pd.read_csv('data/sample.csv').describe())\"")

def main():
    print_header()
    show_project_structure()
    show_data_analysis()
    show_features()
    show_usage()
    
    print("\n" + "=" * 60)
    print("🎉 PROJECT NIV DEMO COMPLETED!")
    print("💡 This is a Python-based automated reporting system")
    print("📧 All work is visible on the terminal with detailed progress")
    print("=" * 60)

if __name__ == "__main__":
    main()