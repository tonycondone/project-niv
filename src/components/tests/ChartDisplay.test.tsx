import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ChartsGrid } from '@/components/dashboard/charts-grid';

it('renders with empty chart configs without crashing', () => {
  const { container } = render(<ChartsGrid chartConfigs={{}} />);
  expect(container).toBeInTheDocument();
});
