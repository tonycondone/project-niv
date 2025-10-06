'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, BarChart, PieChart, AreaChart } from 'recharts';

interface ChartsGridProps {
  chartConfigs: Record<string, any>;
}

const chartComponents = {
  line: LineChart,
  bar: BarChart,
  pie: PieChart,
  area: AreaChart,
};

export function ChartsGrid({ chartConfigs }: ChartsGridProps) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {Object.entries(chartConfigs).map(([chartType, config]) => {
        const ChartComponent = chartComponents[chartType as keyof typeof chartComponents];
        
        if (!ChartComponent) return null;

        return (
          <Card key={chartType} className="card-hover">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-primary-500" />
                {config.title?.text || `${chartType.charAt(0).toUpperCase()}${chartType.slice(1)} Chart`}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80 w-full">
                <ChartComponent
                  data={config.series?.[0]?.data || []}
                  width={400}
                  height={300}
                >
                  {/* Add chart elements based on chart type */}
                </ChartComponent>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}