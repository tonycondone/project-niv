'use client';

import { 
  BarChart3, 
  Database, 
  FileText, 
  Settings, 
  Upload,
  Download,
  RefreshCw
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', href: '#', icon: BarChart3, current: true },
  { name: 'Data Sources', href: '#', icon: Database, current: false },
  { name: 'Reports', href: '#', icon: FileText, current: false },
  { name: 'Settings', href: '#', icon: Settings, current: false },
];

const actions = [
  { name: 'Upload Data', icon: Upload },
  { name: 'Export Data', icon: Download },
  { name: 'Refresh', icon: RefreshCw },
];

export function Sidebar() {
  return (
    <div className="w-64 bg-surface border-r border-border">
      <div className="flex flex-col h-full">
        <nav className="flex-1 px-4 py-6 space-y-2">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Button
                key={item.name}
                variant={item.current ? 'secondary' : 'ghost'}
                className={cn(
                  'w-full justify-start',
                  item.current && 'bg-primary/20 text-primary-500'
                )}
              >
                <Icon className="mr-3 h-5 w-5" />
                {item.name}
              </Button>
            );
          })}
        </nav>
        
        <div className="px-4 py-4 border-t border-border">
          <div className="space-y-2">
            {actions.map((action) => {
              const Icon = action.icon;
              return (
                <Button
                  key={action.name}
                  variant="outline"
                  size="sm"
                  className="w-full justify-start"
                >
                  <Icon className="mr-2 h-4 w-4" />
                  {action.name}
                </Button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}