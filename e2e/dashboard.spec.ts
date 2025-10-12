import { test, expect } from '@playwright/test';

// Minimal smoke e2e to ensure page renders
// Full flows (upload/export/filter) would need UI elements wired

test('User can load dashboard', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('PROJECT NIV')).toBeVisible();
  await expect(page.getByText('Data Analysis Dashboard')).toBeVisible({ timeout: 15000 });
});
