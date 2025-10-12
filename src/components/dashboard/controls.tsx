'use client';

import { useRef } from 'react';
import { RefreshCw, Download, Workflow, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ControlsProps {
  onRefresh: () => void;
  onExport: () => void;
  onToggleFlowChart: () => void;
  onUpload: (file: File) => void | Promise<void>;
  loading: boolean;
}

export function Controls({ onRefresh, onExport, onToggleFlowChart, onUpload, loading }: ControlsProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const openFileDialog = () => fileInputRef.current?.click();

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
          onClick={openFileDialog}
        >
          <Upload className="h-4 w-4 mr-2" />
          Upload Data
        </Button>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv,text/csv"
        className="hidden"
        data-testid="upload-input"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) {
            void onUpload(file);
            // Reset so selecting the same file again triggers change
            e.currentTarget.value = '';
          }
        }}
      />
    </div>
  );
}