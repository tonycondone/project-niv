import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('reports', exist_ok=True)

def generate_report():
    print("📊 [PROJECT NIV] Starting data processing...")
    
    # Read data
    print("📁 Reading data from data/sample.csv...")
    df = pd.read_csv('data/sample.csv')
    print(f"✅ Data loaded successfully! Shape: {df.shape}")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Generate summary
    print("📈 Generating statistical summary...")
    summary = df.describe().to_string()
    print("✅ Summary generated!")

    # Generate chart
    print("📊 Creating visualization...")
    df.plot(kind='bar', x=df.columns[0], y=df.columns[1])
    plt.tight_layout()
    chart_path = 'reports/chart.png'
    plt.savefig(chart_path)
    print(f"✅ Chart saved to {chart_path}")

    # Save Excel report
    print("📄 Saving Excel report...")
    output_file = 'reports/report.xlsx'
    df.to_excel(output_file, index=False)
    print(f"✅ Excel report saved to {output_file}")
    
    print("🎉 Data processing completed successfully!")
    return output_file, summary