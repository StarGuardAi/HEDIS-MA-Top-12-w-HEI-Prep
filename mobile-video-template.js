const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false,
    args: ['--start-maximized']
  });
  
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
  });
  
  const page = await context.newPage();
  
  console.log('🎬 Starting Mobile Video #1: Healthcare Analytics in Your Pocket');
  
  try {
    // SCENE 1: Landing (2s)
    console.log('Scene 1: Landing page...');
    await page.goto('https://rreichert-starguardai.hf.space');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // SCENE 2: Dashboard Home (6s)
    console.log('Scene 2: Dashboard...');
    // Look for main navigation or dashboard link
    // Adjust this selector based on your actual app
    const dashboardLink = await page.locator('text=/dashboard|home/i').first();
    if ((await dashboardLink.count()) > 0) {
      await dashboardLink.click();
      await page.waitForTimeout(2000);
    }
    await page.evaluate(() => window.scrollBy({ top: 150, behavior: 'smooth' }));
    await page.waitForTimeout(4000);
    
    // SCENE 3: Star Rating Widget (6s)
    console.log('Scene 3: Star Ratings...');
    const starRating = await page.locator('text=/star.rating|stars/i').first();
    if ((await starRating.count()) > 0) {
      await starRating.click();
      await page.waitForTimeout(3000);
    }
    await page.evaluate(() => window.scrollBy({ top: 100, behavior: 'smooth' }));
    await page.waitForTimeout(3000);
    
    // SCENE 4: Member Alerts (6s)
    console.log('Scene 4: Member alerts...');
    const alerts = await page.locator('text=/alert|notification/i').first();
    if ((await alerts.count()) > 0) {
      await alerts.click();
      await page.waitForTimeout(6000);
    }
    
    // SCENE 5: Measure Performance (6s)
    console.log('Scene 5: Measures...');
    const measures = await page.locator('text=/measure|hedis/i').first();
    if ((await measures.count()) > 0) {
      await measures.click();
      await page.waitForTimeout(6000);
    }
    
    // SCENE 6: Predictive Insights (6s)
    console.log('Scene 6: Predictions...');
    const predictions = await page.locator('text=/predict|forecast|ai/i').first();
    if ((await predictions.count()) > 0) {
      await predictions.click();
      await page.waitForTimeout(6000);
    }
    
    // SCENE 7: QR Code/CTA (10s)
    console.log('Scene 7: CTA screen...');
    await page.goto('about:blank');
    await page.setContent(`
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; font-family: 'Segoe UI', Arial, sans-serif;">
        <h1 style="font-size: 42px; margin-bottom: 25px; font-weight: 600; text-align: center; padding: 0 20px;">Schedule Your Demo</h1>
        <div style="background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
          <img src="YOUR_QR_CODE_URL_HERE" alt="QR Code" style="width: 250px; height: 250px;" />
        </div>
        <p style="font-size: 28px; font-weight: 500; margin-bottom: 10px;">tinyurl.com/bdevpdz5</p>
        <p style="font-size: 20px; opacity: 0.9;">Robert Reichert</p>
        <p style="font-size: 18px; opacity: 0.8; margin-top: 5px;">Healthcare AI Architect</p>
      </div>
    `);
    await page.waitForTimeout(10000);
    
    // SCENE 8: Fade out (3s)
    console.log('Scene 8: Fade out...');
    await page.evaluate(() => {
      document.body.style.transition = 'opacity 3s';
      document.body.style.opacity = '0';
    });
    await page.waitForTimeout(3000);
    
    console.log('✅ Recording complete - 45 seconds!');
    console.log('📹 Use screen recording software to capture this playback');
    
  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await browser.close();
  }
})();
