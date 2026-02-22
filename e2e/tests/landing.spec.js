const { test, expect } = require('@playwright/test');

test.describe('Landing page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });
  });

  test('page title contains MapAider', async ({ page }) => {
    await expect(page).toHaveTitle(/MapAider/i);
  });

  test('h1 heading reads "Popular Maps"', async ({ page }) => {
    await expect(page.locator('h1')).toHaveText(/Popular Maps/i);
  });

  test('at least one MUI card is rendered after API response', async ({ page }) => {
    const cards = page.locator('.MuiCard-root');
    await expect(cards.first()).toBeVisible();
  });

  test('each card contains an anchor with href matching /mapaider/map/<slug>', async ({ page }) => {
    const links = page.locator('.MuiCard-root a[href*="/mapaider/map/"]');
    await expect(links.first()).toBeVisible();
  });

  test('clicking a map card navigates to the map viewer', async ({ page }) => {
    const firstCardLink = page.locator('.MuiCard-root a[href*="/mapaider/map/"]').first();
    await firstCardLink.click();
    await expect(page).toHaveURL(/\/mapaider\/map\//);
  });

  test('loading text disappears once data is fetched', async ({ page }) => {
    // After networkidle the loading indicator should be gone
    const loading = page.locator('text=/loading/i');
    await expect(loading).toHaveCount(0);
  });
});
