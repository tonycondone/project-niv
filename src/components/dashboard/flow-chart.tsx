'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface FlowChartProps {
  flowData: {
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
  onClose?: () => void;
}

export function FlowChart({ flowData, onClose }: FlowChartProps) {
  return (
    <Card className="card-hover">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-primary-500" />
          ETL Process Flow
        </CardTitle>
        {onClose && (
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {flowData.nodes.map((node) => {
            const statusIcon = node.status === 'completed' ? '✅' : 
                             node.status === 'error' ? '❌' : '⏳';
            const statusColor = node.status === 'completed' ? 'text-accent' : 
                              node.status === 'error' ? 'text-error' : 'text-warning';
            
            return (
              <div key={node.id} className="flex items-center gap-3 p-3 bg-surface-light rounded-lg">
                <span className="text-lg">{statusIcon}</span>
                <span className={`font-medium ${statusColor}`}>{node.label}</span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}