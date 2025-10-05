#!/usr/bin/env python3
"""
PROJECT NIV - Quick Start Example
Simple example showing how to use the one-time run script
"""

import subprocess
import sys
import os

def print_banner():
    print("=" * 60)
    print("🚀 PROJECT NIV - Quick Start Example")
    print("=" * 60)

def run_command(cmd, description):
    """Run a command and display results"""
    print(f"\n🔄 {description}")
    print("-" * 40)
    print(f"Command: {cmd}")
    print()
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("❌ Error!")
            if result.stderr:
                print("Error:")
                print(result.stderr)
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def main():
    print_banner()
    
    print("""
This example demonstrates how to use PROJECT NIV with different options.

Available examples:
1. Basic processing with sample data
2. Processing with filters
3. Processing with transformations
4. Interactive mode
5. Web dashboard mode
""")
    
    # Check if we have sample data
    if not os.path.exists("data/sample_detailed.csv"):
        print("❌ Sample data not found. Please ensure data/sample_detailed.csv exists.")
        return
    
    examples = [
        {
            "cmd": "python3 run_once.py --csv data/sample_detailed.csv",
            "desc": "Basic ETL processing with sample data"
        },
        {
            "cmd": 'python3 run_once.py --csv data/sample_detailed.csv --filters \'{"Sales": {"min": 1500, "max": 2500}}\'',
            "desc": "ETL processing with sales range filter (1500-2500)"
        },
        {
            "cmd": "python3 run_once.py --csv data/sample_detailed.csv --transformations normalize",
            "desc": "ETL processing with data normalization"
        },
        {
            "cmd": "python3 run_once.py --csv data/sample_detailed.csv --transformations normalize standardize",
            "desc": "ETL processing with multiple transformations"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*60}")
        print(f"Example {i}: {example['desc']}")
        print('='*60)
        
        run_command(example['cmd'], example['desc'])
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print(f"\n{'='*60}")
    print("🎉 All examples completed!")
    print('='*60)
    
    print("""
Next steps:
1. Try the interactive mode: python3 run_once.py --interactive
2. Start web dashboard: python3 run_once.py --csv data/sample_detailed.csv --web
3. Read the full guide: STEP_BY_STEP_GUIDE.md
4. Explore advanced features in main.py
""")

if __name__ == "__main__":
    main()