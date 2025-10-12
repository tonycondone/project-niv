import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Dashboard } from '@/components/dashboard/dashboard';

describe('Dashboard', () => {
  beforeEach(() => {
    // Mock fetch without using any
    (global as unknown as { fetch: unknown }).fetch = jest.fn((url: string) => {
      if (url.includes('/api/backend/etl-data')) {
        return Promise.resolve({
          ok: true,
          json: async () => ({
            summary: { original_rows: 100, processed_rows: 80, columns: 5 },
            chart_configs: {},
            flow_data: { nodes: [], edges: [] },
          }),
        }) as unknown as Promise<Response>;
      }
      return Promise.reject(new Error('Unknown URL: ' + url));
    });
  });

  it('shows loading then renders dashboard title', async () => {
    render(<Dashboard />);
    expect(screen.getByText(/Loading Dashboard/i)).toBeInTheDocument();
    await waitFor(() =>
      expect(screen.getByText(/Data Analysis Dashboard/i)).toBeInTheDocument()
    );
  });

  it('handles fetch failure gracefully', async () => {
    // @ts-expect-error override
    global.fetch = jest.fn(() => Promise.resolve({ ok: false, status: 500, statusText: 'Server Error' }));
    render(<Dashboard />);
    await waitFor(() =>
      expect(screen.getByText(/Error Loading Data/i)).toBeInTheDocument()
    );
  });
});
