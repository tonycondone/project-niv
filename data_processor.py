import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('reports', exist_ok=True)

def generate_report():
    # Read data
    df = pd.read_csv('data/sample.csv')
    summary = df.describe().to_string()

    # Generate chart
    df.plot(kind='bar', x=df.columns[0], y=df.columns[1])
    plt.tight_layout()
    chart_path = 'reports/chart.png'
    plt.savefig(chart_path)

    # Save Excel report
    output_file = 'reports/report.xlsx'
    df.to_excel(output_file, index=False)

    return output_file, summary