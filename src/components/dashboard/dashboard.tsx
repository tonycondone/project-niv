'use client';

import { useState, useEffect } from 'react';
import { SummaryCards } from './summary-cards';
import { ChartsGrid } from './charts-grid';
import { Controls } from './controls';
import { FlowChart } from './flow-chart';
import { LoadingSpinner } from './loading-spinner';

interface ETLData {
  summary: {
    original_rows: number;
    processed_rows: number;
    columns: number;
  };
  chart_configs: Record<string, any>;
  flow_data: {
    nodes: Array<{
      id: string;
      label: string;
      status: 'completed' | 'pending' | 'error';
    }>;
    edges: Array<{
      from: string;
      to: string;
      label?: string;
    }>;
  };
}

export function Dashboard() {
  const [etlData, setEtlData] = useState<ETLData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [flowChartVisible, setFlowChartVisible] = useState(false);

  useEffect(() => {
    loadETLData();
  }, []);

  const loadETLData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/backend/etl-data');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setEtlData(data);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to load ETL data');
    } finally {
      setLoading(false);
    }
  };

  const refreshCharts = () => {
    loadETLData();
  };

  const exportData = async () => {
    try {
      const response = await fetch('/api/backend/data/export');
      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'etl_data_export.csv';
        link.click();
        URL.revokeObjectURL(url);
      } else {
        throw new Error('Export failed');
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to export data');
    }
  };

  const toggleFlowChart = () => {
    setFlowChartVisible(!flowChartVisible);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="text-error text-6xl mb-4">⚠️</div>
          <h3 className="text-xl font-semibold mb-2">Error Loading Data</h3>
          <p className="text-muted-foreground">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Data Analysis Dashboard</h1>
          <p className="text-muted-foreground">
            Transform your data into actionable insights
          </p>
        </div>
      </div>

      {etlData && (
        <>
          <SummaryCards summary={etlData.summary} />
          <Controls 
            onRefresh={refreshCharts}
            onExport={exportData}
            onToggleFlowChart={toggleFlowChart}
            loading={loading}
          />
          {flowChartVisible && <FlowChart flowData={etlData.flow_data} />}
          <ChartsGrid chartConfigs={etlData.chart_configs} />
        </>
      )}
    </div>
  );
}