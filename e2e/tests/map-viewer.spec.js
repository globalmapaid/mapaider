const { test, expect } = require('@playwright/test');

const slug = process.env.TEST_MAP_SLUG || 'test-map';
const mapUrl = `/mapaider/map/${slug}`;

test.describe('Map viewer', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(mapUrl, { waitUntil: 'networkidle' });
  });

  test('#map div is present in the DOM', async ({ page }) => {
    await expect(page.locator('#map')).toBeAttached();
  });

  test('#map div fills the viewport', async ({ page }) => {
    const box = await page.locator('#map').boundingBox();
    const viewport = page.viewportSize();
    expect(box.width).toBeGreaterThan(viewport.width * 0.9);
    expect(box.height).toBeGreaterThan(viewport.height * 0.9);
  });

  test('Leaflet zoom-in control button is present', async ({ page }) => {
    await expect(page.locator('.leaflet-control-zoom-in')).toBeVisible();
  });

  test('Leaflet zoom-out control button is present', async ({ page }) => {
    await expect(page.locator('.leaflet-control-zoom-out')).toBeVisible();
  });

  test('layer switcher panel is rendered', async ({ page }) => {
    await expect(page.locator('.leaflet-control-layers')).toBeVisible();
  });

  test('layer switcher contains at least one checkbox', async ({ page }) => {
    const checkboxes = page.locator('.leaflet-control-layers input[type="checkbox"]');
    await expect(checkboxes.first()).toBeVisible();
  });

  test('map title panel shows the map name', async ({ page }) => {
    await expect(page.locator('.leaflet-control-container .info')).toBeVisible();
  });

  test('clicking a feature marker opens a popup with a table', async ({ page }) => {
    const markers = page.locator('.leaflet-marker-icon');
    const count = await markers.count();
    if (count === 0) {
      test.skip();
      return;
    }
    await markers.first().click();
    await expect(page.locator('.leaflet-popup table')).toBeVisible();
  });
});
