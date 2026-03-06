/**
 * StarGuard AI Shiny Python Navigation Discovery
 * Shiny-only (no Streamlit)
 *
 * Run: node discover-navigation.js
 */

const { chromium } = require('playwright');

const BASE_URL = process.env.STARGUARD_URL || 'https://rreichert-starguardai.hf.space';

(async () => {
  console.log('🔍 Discovering Shiny Python StarGuard AI navigation...\n');

  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  try {
    console.log('🖥️  Loading Shiny app...');
    await page.goto(BASE_URL, {
      waitUntil: 'networkidle',
      timeout: 60000,
    });
    await page.waitForTimeout(5000);

    console.log('\n📋 SHINY PYTHON NAVIGATION:');
    console.log('═══════════════════════════════════════\n');

    // 1. Shiny navbar tabs
    console.log('🔗 NAVIGATION TABS:');
    const navTabs = await page.locator('a.nav-link, ul.nav li a, [role="tab"]').all();
    for (let i = 0; i < navTabs.length; i++) {
      const text = await navTabs[i].textContent();
      const href = await navTabs[i].getAttribute('href');
      const dataValue = await navTabs[i].getAttribute('data-value');
      if (text && text.trim()) {
        console.log(`   ${i + 1}. "${text.trim()}" ${href || dataValue || ''}`);
      }
    }
    console.log('');

    // 2. Sidebar / hamburger menu (Shiny)
    console.log('📑 SIDEBAR / HAMBURGER MENU:');
    const sidebarItems = await page.locator('.sidebar-nav-item, [class*="sidebar"] a, aside a, nav a').all();
    const seen = new Set();
    for (let i = 0; i < sidebarItems.length; i++) {
      const text = (await sidebarItems[i].textContent())?.trim();
      if (text && !seen.has(text)) {
        seen.add(text);
        console.log(`   • "${text}"`);
      }
    }
    console.log('');

    // 3. Shiny selectInput (native select)
    console.log('📊 SELECT INPUTS:');
    const nativeSelects = await page.locator('select').all();
    for (let i = 0; i < nativeSelects.length; i++) {
      const id = await nativeSelects[i].getAttribute('id');
      let label = 'Unknown';
      try {
        if (id) {
          label = (await page.locator(`label[for="${id}"]`).textContent({ timeout: 1000 })) || 'No label';
        }
      } catch (e) {}
      console.log(`   Dropdown ${i + 1}: "${label?.trim()}" (id: ${id})`);
      const options = await nativeSelects[i].locator('option').allTextContents();
      options
        .filter((o) => o.trim())
        .slice(0, 12)
        .forEach((opt) => console.log(`      • "${opt.trim()}"`));
      if (options.length > 12) console.log(`      ... and ${options.length - 12} more`);
      console.log('');
    }
    console.log('');

    // 4. Buttons
    console.log('🔘 BUTTONS:');
    const buttons = await page.locator('button:visible').allTextContents();
    const uniqueButtons = [...new Set(buttons.map((b) => b.trim()).filter(Boolean))];
    uniqueButtons.slice(0, 15).forEach((text, i) => console.log(`   ${i + 1}. "${text}"`));
    console.log('');

    // 5. Value boxes / cards (Shiny)
    console.log('📈 VALUE BOXES / CARDS:');
    const cards = await page.locator('.card, .value-box, [class*="bslib-card"]').count();
    console.log(`   Found ${cards} card/value-box elements\n`);

    // 6. Plotly charts
    const plotlyCharts = await page.locator('.plotly, [class*="plotly"], .js-plotly-plot').count();
    console.log(`📊 PLOTLY CHARTS: ${plotlyCharts} found\n`);

    // 7. Tables
    const tables = await page.locator('table').count();
    console.log(`📋 TABLES: ${tables} found\n`);

    // 8. Page headings
    console.log('📝 PAGE HEADINGS:');
    const headings = await page.locator('h1, h2, h3').allTextContents();
    headings
      .filter((h) => h.trim())
      .slice(0, 10)
      .forEach((h, i) => console.log(`   ${i + 1}. "${h.trim()}"`));
    console.log('');

    // 9. Screenshots
    await page.screenshot({ path: 'shiny-desktop-full.png', fullPage: true });
    await page.screenshot({ path: 'shiny-desktop-viewport.png' });
    console.log('📸 Screenshots saved: shiny-desktop-full.png, shiny-desktop-viewport.png\n');

    const title = await page.title();
    console.log(`📄 Page Title: "${title}"\n`);

    console.log('═══════════════════════════════════════');
    console.log('\n✅ Discovery complete!');
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.log('\n💡 TROUBLESHOOTING: HuggingFace Space may be sleeping (30-60s).');
  } finally {
    await browser.close();
  }
})();
