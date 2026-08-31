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

  // The basemap is drawn into a custom pane, so its tiles are not under
  // .leaflet-tile-pane — match the tile images directly.
  const tileSelector = 'img.leaflet-tile';

  test('basemap tiles are requested from a keyless provider', async ({ page }) => {
    const tiles = page.locator(tileSelector);
    await expect(tiles.first()).toBeAttached();
    const sources = await tiles.evaluateAll(imgs => imgs.map(img => img.src));
    expect(sources.length).toBeGreaterThan(0);
    // CARTO now watermarks its keyless tiles with "API KEY REQUIRED".
    expect(sources.some(src => src.includes('cartocdn.com'))).toBe(false);
  });

  test('basemap tiles load successfully', async ({ page }) => {
    const tiles = page.locator(tileSelector);
    await expect(tiles.first()).toBeAttached();
    // A tile that 404s or is blocked decodes to a zero-width image.
    await expect.poll(async () =>
      tiles.evaluateAll(imgs =>
        imgs.filter(img => img.complete && img.naturalWidth > 0).length
      )
    ).toBeGreaterThan(0);
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
