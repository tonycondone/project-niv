'use client';

import { RefreshCw, Download, Workflow, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ControlsProps {
  onRefresh: () => void;
  onExport: () => void;
  onToggleFlowChart: () => void;
  loading: boolean;
}

export function Controls({ onRefresh, onExport, onToggleFlowChart, loading }: ControlsProps) {
  return (
    <div className="flex flex-wrap items-center gap-4 p-4 bg-surface rounded-lg border border-border">
      <div className="flex items-center gap-2">
        <Button 
          onClick={onRefresh}
          disabled={loading}
          className="bg-primary-500 hover:bg-primary-600"
          data-testid="refresh-button"
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh Data
        </Button>
        
        <Button 
          onClick={onExport}
          variant="outline"
          disabled={loading}
          data-testid="export-button"
        >
          <Download className="h-4 w-4 mr-2" />
          Export Data
        </Button>
        
        <Button 
          onClick={onToggleFlowChart}
          variant="outline"
          disabled={loading}
          data-testid="flow-button"
        >
          <Workflow className="h-4 w-4 mr-2" />
          Process Flow
        </Button>
        
        <Button 
          variant="outline"
          disabled={loading}
          data-testid="upload-button"
        >
          <Upload className="h-4 w-4 mr-2" />
          Upload Data
        </Button>
      </div>
    </div>
  );
}