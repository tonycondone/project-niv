'use client';

import { BarChart3, Database, Columns, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface SummaryCardsProps {
  summary: {
    original_rows: number;
    processed_rows: number;
    columns: number;
  };
}

const cards = [
  {
    title: 'Original Data',
    value: 'original_rows',
    icon: Database,
    color: 'text-primary-500',
    bgColor: 'bg-primary-500/10',
  },
  {
    title: 'Processed',
    value: 'processed_rows',
    icon: TrendingUp,
    color: 'text-accent',
    bgColor: 'bg-accent/10',
  },
  {
    title: 'Columns',
    value: 'columns',
    icon: Columns,
    color: 'text-warning',
    bgColor: 'bg-warning/10',
  },
  {
    title: 'Charts',
    value: 'charts',
    icon: BarChart3,
    color: 'text-secondary-600',
    bgColor: 'bg-secondary-600/10',
  },
];

export function SummaryCards({ summary }: SummaryCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card) => {
        const Icon = card.icon;
        const value = card.value === 'charts' ? 4 : summary[card.value as keyof typeof summary];
        
        return (
          <Card key={card.title} className="card-hover">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {card.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${card.bgColor}`}>
                <Icon className={`h-4 w-4 ${card.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{value?.toLocaleString() || 0}</div>
              <p className="text-xs text-muted-foreground">
                {card.value === 'charts' ? 'visualizations' : 'records'}
              </p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}