/**
 * Playwright demo video recording script for StarGuard AI Mobile
 * Targets: https://rreichert-starguardai.hf.space (or run locally)
 *
 * Setup:
 *   npm init -y
 *   npm install playwright
 *   node record-demo-video.js
 */

const { chromium } = require('playwright');

const BASE_URL = process.env.STARGUARD_URL || 'https://rreichert-starguardai.hf.space';

async function openMenu(page) {
  const sidebar = page.locator('#nav-sidebar');
  const isOpen = await sidebar.evaluate((el) => el?.classList?.contains('active'));
  if (!isOpen) {
    await page.click('#menu-toggle');
    await page.waitForTimeout(500);
  }
}

async function navigateTo(page, navId) {
  await openMenu(page);
  await page.click(`#nav-${navId}`);
  await page.waitForTimeout(800);
  await page.waitForLoadState('networkidle').catch(() => {});
}

(async () => {
  console.log('🎬 Starting Video: HEDIS Portfolio Optimizer (Mobile)...');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
  });

  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    recordVideo: {
      dir: './recordings/',
      size: { width: 390, height: 844 },
    },
  });

  const page = await context.newPage();

  try {
    // 1. Landing - Executive Dashboard (3 seconds)
    console.log('📱 Step 1: Loading landing page...');
    await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    // 2. HEDIS Gap Analyzer - Portfolio Overview (8 seconds)
    console.log('📊 Step 2: Opening HEDIS Gap Analyzer...');
    await navigateTo(page, 'hedis');
    await page.waitForTimeout(2000);
    await page.evaluate(() => window.scrollBy(0, 300));
    await page.waitForTimeout(3000);
    await page.evaluate(() => window.scrollBy(0, 300));
    await page.waitForTimeout(3000);

    // 3. BCS Measure Detail (8 seconds)
    console.log('🎯 Step 3: Drilling into BCS measure...');
    await page.selectOption('select[id*="hedis_measure"]', { value: 'BCS' });
    await page.waitForTimeout(1500);
    await page.getByRole('button', { name: /Analyze Gaps/ }).click();
    await page.waitForTimeout(3000);
    await page.evaluate(() => window.scrollBy(0, 200));
    await page.waitForTimeout(2000);
    await page.evaluate(() => window.scrollBy(0, 200));
    await page.waitForTimeout(3000);

    // 4. Care Gap Workflow - Member-level gaps (8 seconds)
    console.log('👥 Step 4: Showing member-level gaps...');
    await navigateTo(page, 'workflow');
    await page.waitForTimeout(3000);
    await page.evaluate(() => window.scrollBy(0, 250));
    await page.waitForTimeout(2500);
    await page.evaluate(() => window.scrollBy(0, 250));
    await page.waitForTimeout(2500);

    // 5. Star Rating Predictor - Predictive engine (8 seconds)
    console.log('🔮 Step 5: Showing predictive engine...');
    await navigateTo(page, 'star');
    await page.waitForTimeout(4000);
    const chartEl = page.locator('[class*="chart"], [class*="plot"], .card').first();
    if (await chartEl.count() > 0) await chartEl.hover();
    await page.waitForTimeout(4000);

    // 6. AI Validation Dashboard (8 seconds)
    console.log('✅ Step 6: Demonstrating validation...');
    await navigateTo(page, 'ai');
    await page.waitForTimeout(4000);
    await page.evaluate(() => window.scrollBy(0, 200));
    await page.waitForTimeout(4000);

    // 7. ROI Portfolio Optimizer (7 seconds)
    console.log('💰 Step 7: Showing ROI metrics...');
    await navigateTo(page, 'roi');
    await page.waitForTimeout(3500);
    const roiEl = page.locator('[class*="roi"], [class*="metric"], .card').first();
    if (await roiEl.count() > 0) await roiEl.hover();
    await page.waitForTimeout(3500);

    // 8. Return to Executive Dashboard (5 seconds)
    console.log('🏁 Step 8: Closing sequence...');
    await navigateTo(page, 'dashboard');
    await page.waitForTimeout(5000);

    console.log('✅ Recording complete! Closing browser...');
  } catch (error) {
    console.error('❌ Error during recording:', error.message);
  } finally {
    await context.close();
    await browser.close();
    console.log('💾 Video saved to ./recordings/');
    console.log('📹 Next step: Add voiceover and export final MP4');
  }
})();
