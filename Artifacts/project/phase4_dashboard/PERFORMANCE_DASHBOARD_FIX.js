// Robust JavaScript fix for Performance Dashboard sidebar label
// Uses MutationObserver to catch dynamically loaded content

(function() {
    'use strict';
    
    function fixPerformanceDashboardLabel() {
        // Try multiple selectors for sidebar navigation
        const selectors = [
            '[data-testid="stSidebarNav"]',
            '[data-testid="stSidebar"] [role="navigation"]',
            '[data-testid="stSidebar"] nav',
            '.css-1d391kg [role="navigation"]'
        ];
        
        let sidebarNav = null;
        for (const selector of selectors) {
            sidebarNav = document.querySelector(selector);
            if (sidebarNav) break;
        }
        
        if (!sidebarNav) {
            return false; // Sidebar not found yet
        }
        
        // Find all links in sidebar
        const links = sidebarNav.querySelectorAll('a, [role="link"]');
        let found = false;
        
        links.forEach(link => {
            // Get text from link and all child elements
            const fullText = link.textContent || link.innerText || '';
            const trimmedText = fullText.trim();
            
            // Check various patterns
            const patterns = [
                /^z\s+Performance\s+Dashboard/i,
                /^z_Performance_Dashboard/i,
                /Performance\s+Dashboard.*starts.*with.*z/i,
                /z.*Performance.*Dashboard/i
            ];
            
            let shouldReplace = false;
            for (const pattern of patterns) {
                if (pattern.test(trimmedText)) {
                    shouldReplace = true;
                    break;
                }
            }
            
            // Also check if it starts with 'z' and contains 'Performance Dashboard'
            if (!shouldReplace && trimmedText.toLowerCase().includes('performance dashboard')) {
                const firstChar = trimmedText.charAt(0).toLowerCase();
                if (firstChar === 'z' || trimmedText.startsWith('z ')) {
                    shouldReplace = true;
                }
            }
            
            if (shouldReplace) {
                // Replace the text content
                link.textContent = '⚡ Performance Dashboard';
                link.innerText = '⚡ Performance Dashboard';
                
                // Update any child spans or divs
                const children = link.querySelectorAll('span, div, p');
                children.forEach(child => {
                    const childText = (child.textContent || child.innerText || '').trim();
                    if (childText.toLowerCase().includes('performance dashboard') && 
                        (childText.startsWith('z') || childText.startsWith('z '))) {
                        child.textContent = '⚡ Performance Dashboard';
                        child.innerText = '⚡ Performance Dashboard';
                    }
                });
                
                found = true;
            }
        });
        
        return found;
    }
    
    // Run immediately
    fixPerformanceDashboardLabel();
    
    // Run after delays
    setTimeout(fixPerformanceDashboardLabel, 100);
    setTimeout(fixPerformanceDashboardLabel, 500);
    setTimeout(fixPerformanceDashboardLabel, 1000);
    setTimeout(fixPerformanceDashboardLabel, 2000);
    setTimeout(fixPerformanceDashboardLabel, 3000);
    
    // Use MutationObserver to watch for DOM changes
    const observer = new MutationObserver(function(mutations) {
        let shouldCheck = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0 || mutation.type === 'childList') {
                shouldCheck = true;
            }
        });
        if (shouldCheck) {
            setTimeout(fixPerformanceDashboardLabel, 100);
        }
    });
    
    // Observe the sidebar and document body
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        observer.observe(sidebar, {
            childList: true,
            subtree: true,
            characterData: true
        });
    }
    
    // Also observe the entire document for navigation changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Periodic check as backup
    setInterval(fixPerformanceDashboardLabel, 2000);
})();

