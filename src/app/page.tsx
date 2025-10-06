import { Dashboard } from '@/components/dashboard/dashboard';
import { Header } from '@/components/layout/header';
import { Sidebar } from '@/components/layout/sidebar';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <Dashboard />
        </main>
      </div>
    </div>
  );
}