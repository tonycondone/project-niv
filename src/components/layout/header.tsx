'use client';

import { BarChart3, Settings, Bell, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

export function Header() {
  return (
    <header className="border-b border-border bg-surface">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-8 w-8 text-primary-500" />
            <div>
              <h1 className="text-xl font-bold gradient-text">PROJECT NIV</h1>
              <p className="text-sm text-muted-foreground">Data Analysis Platform</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <Badge variant="secondary" className="bg-accent/20 text-accent">
            <div className="h-2 w-2 rounded-full bg-accent mr-2 animate-pulse" />
            System Ready
          </Badge>
          
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
          </Button>
          
          <Button variant="ghost" size="icon">
            <Settings className="h-5 w-5" />
          </Button>
          
          <Button variant="ghost" size="icon">
            <User className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}