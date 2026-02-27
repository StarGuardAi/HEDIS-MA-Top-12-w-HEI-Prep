// ============================================================================
// TAB CENTERING DIAGNOSTIC SCRIPT
// ============================================================================
// Copy and paste this entire script into Chrome DevTools Console (F12)
// on the Budget Variance page to diagnose tab centering issues
// ============================================================================

console.log("🔍 Starting Tab Centering Diagnostic...");
console.log("=".repeat(60));

// Step 1: Find all tab-related elements
console.log("\n📋 STEP 1: Finding all tab-related elements");
console.log("-".repeat(60));

const tabSelectors = [
    '[role="tablist"]',
    '[data-baseweb="tab-list"]',
    '.stTabs',
    '[data-testid="stTabs"]',
    '.stTabs > div',
    '.stTabs > div > div',
    '[class*="st-emotion-cache"]'
];

let foundElements = [];

tabSelectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    if (elements.length > 0) {
        console.log(`\n✅ Found ${elements.length} element(s) with selector: "${selector}"`);
        elements.forEach((el, i) => {
            if (!foundElements.includes(el)) {
                foundElements.push(el);
                console.log(`  Element ${i + 1}:`, el);
                console.log(`    Classes: ${el.className}`);
                console.log(`    Tag: ${el.tagName}`);
                console.log(`    Parent classes: ${el.parentElement?.className || 'none'}`);
                console.log(`    Computed display: ${window.getComputedStyle(el).display}`);
                console.log(`    Computed justify-content: ${window.getComputedStyle(el).justifyContent}`);
                
                // Highlight with red border
                el.style.border = "3px solid red";
                el.style.transition = "border 0.3s";
            }
        });
    } else {
        console.log(`❌ No elements found with selector: "${selector}"`);
    }
});

console.log(`\n📊 Total unique elements found: ${foundElements.length}`);

// Step 2: Test centering with different selectors
console.log("\n\n🎯 STEP 2: Testing centering with different selectors");
console.log("-".repeat(60));

// Test 1: role="tablist"
console.log("\n🧪 TEST 1: [role=\"tablist\"]");
const test1 = document.querySelector('[role="tablist"]');
if (test1) {
    const before = window.getComputedStyle(test1).justifyContent;
    test1.style.justifyContent = 'center';
    test1.style.display = 'flex';
    test1.style.width = '100%';
    const after = window.getComputedStyle(test1).justifyContent;
    console.log(`  Before: ${before}`);
    console.log(`  After: ${after}`);
    console.log(`  ✅ Applied centering - check if tabs moved`);
} else {
    console.log(`  ❌ Element not found`);
}

// Test 2: data-baseweb="tab-list"
console.log("\n🧪 TEST 2: [data-baseweb=\"tab-list\"]");
const test2 = document.querySelector('[data-baseweb="tab-list"]');
if (test2) {
    const before = window.getComputedStyle(test2).justifyContent;
    test2.style.justifyContent = 'center';
    test2.style.display = 'flex';
    const after = window.getComputedStyle(test2).justifyContent;
    console.log(`  Before: ${before}`);
    console.log(`  After: ${after}`);
    console.log(`  ✅ Applied centering - check if tabs moved`);
} else {
    console.log(`  ❌ Element not found`);
}

// Test 3: .stTabs > div > div
console.log("\n🧪 TEST 3: .stTabs > div > div");
const test3 = document.querySelector('.stTabs > div > div');
if (test3) {
    const before = window.getComputedStyle(test3).justifyContent;
    test3.style.justifyContent = 'center';
    test3.style.display = 'flex';
    const after = window.getComputedStyle(test3).justifyContent;
    console.log(`  Before: ${before}`);
    console.log(`  After: ${after}`);
    console.log(`  ✅ Applied centering - check if tabs moved`);
} else {
    console.log(`  ❌ Element not found`);
}

// Step 3: Force center all tab lists
console.log("\n\n🔧 STEP 3: Force centering all tab lists");
console.log("-".repeat(60));

document.querySelectorAll('[role="tablist"]').forEach((el, i) => {
    el.style.justifyContent = "center";
    el.style.display = "flex";
    el.style.width = "100%";
    el.style.marginLeft = "auto";
    el.style.marginRight = "auto";
    console.log(`✅ Centered tab list ${i + 1}:`, el);
    console.log(`   Classes: ${el.className}`);
});

document.querySelectorAll('[data-baseweb="tab-list"]').forEach((el, i) => {
    el.style.justifyContent = "center";
    el.style.display = "flex";
    el.style.width = "100%";
    el.style.marginLeft = "auto";
    el.style.marginRight = "auto";
    console.log(`✅ Centered baseweb tab list ${i + 1}:`, el);
    console.log(`   Classes: ${el.className}`);
});

// Step 4: Find emotion cache classes
console.log("\n\n🎨 STEP 4: Finding Streamlit emotion cache classes");
console.log("-".repeat(60));

const emotionCacheElements = document.querySelectorAll('[class*="st-emotion-cache"]');
const uniqueClasses = new Set();
emotionCacheElements.forEach(el => {
    el.className.split(' ').forEach(cls => {
        if (cls.includes('st-emotion-cache')) {
            uniqueClasses.add(cls);
        }
    });
});

console.log(`Found ${uniqueClasses.size} unique emotion cache classes:`);
uniqueClasses.forEach(cls => {
    console.log(`  - ${cls}`);
    
    // Check if this class is on a tab-related element
    const testEl = document.querySelector(`.${cls.split(' ')[0]}`);
    if (testEl && (
        testEl.getAttribute('role') === 'tablist' ||
        testEl.getAttribute('data-baseweb') === 'tab-list' ||
        testEl.closest('[role="tablist"]') ||
        testEl.closest('[data-baseweb="tab-list"]')
    )) {
        console.log(`    ⚠️  This class appears to be tab-related!`);
        testEl.style.justifyContent = 'center';
        testEl.style.display = 'flex';
    }
});

console.log("\n" + "=".repeat(60));
console.log("✅ Diagnostic complete!");
console.log("📝 Check the console output above and report:");
console.log("   1. Which test number (1, 2, or 3) centered the tabs");
console.log("   2. Any emotion cache class names that are tab-related");
console.log("   3. Whether tabs are now visually centered");
