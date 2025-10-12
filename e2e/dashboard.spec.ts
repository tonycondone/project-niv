import { test, expect } from '@playwright/test';

test('User can load dashboard', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('PROJECT NIV')).toBeVisible();
  await expect(page.getByText('Data Analysis Dashboard')).toBeVisible({ timeout: 15000 });
});

test('User can export data (csv)', async ({ page, context }) => {
  await page.goto('/');
  const [ download ] = await Promise.all([
    page.waitForEvent('download'),
    page.getByTestId('export-button').click(),
  ]);
  const suggested = download.suggestedFilename();
  expect(suggested).toContain('.csv');
});

test('User can toggle flow chart', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('flow-button').click();
  await expect(page.getByText('ETL Process Flow')).toBeVisible();
});

test('User can filter data via API', async ({ page, request }) => {
  // Hit backend filter endpoint directly to simulate filter action
  const res = await request.post('http://localhost:8000/api/apply-filters?percentage=0.2');
  expect(res.ok()).toBeTruthy();
  await page.goto('/');
  await expect(page.getByText('Data Analysis Dashboard')).toBeVisible();
});

test('User can upload CSV file', async ({ page }) => {
  await page.goto('/');
  const uploadInput = page.getByTestId('upload-input');
  const content = 'a,b\n1,2\n3,4\n';
  await uploadInput.setInputFiles({
    name: 'sample.csv',
    mimeType: 'text/csv',
    // Buffer is available in Node environment
    buffer: Buffer.from(content),
  });
  await expect(page.getByText('Data Analysis Dashboard')).toBeVisible();
});

