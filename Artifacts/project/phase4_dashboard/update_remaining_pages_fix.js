// Enhanced JavaScript fix for remaining pages
// This catches corrupted emoji characters and ensures "⚡ Performance Dashboard" is always shown

const ENHANCED_JS_PATTERN = `            // Check if it's Performance Dashboard - catch ANY variation including corrupted emojis
            const isPerformanceDashboard = (
                lowerText.includes('performance dashboard') ||
                lowerText.includes('performance_dashboard') ||
                /performance\\s*dashboard/i.test(fullText)
            );
            
            // Check if it needs fixing (missing emoji, has wrong prefix, or corrupted characters)
            const needsFix = (
                isPerformanceDashboard && (
                    fullText.startsWith('z') ||
                    fullText.startsWith('â') ||
                    fullText.startsWith('š') ||
                    fullText.startsWith('¡') ||
                    !fullText.includes('⚡')
                )
            );
            
            if (needsFix || (isPerformanceDashboard && fullText !== '⚡ Performance Dashboard')) {
                // Force set to correct text
                link.textContent = '⚡ Performance Dashboard';
                link.innerText = '⚡ Performance Dashboard';
                
                // Fix all child elements
                link.querySelectorAll('span, div, p, *').forEach(child => {
                    const childText = (child.textContent || child.innerText || '').trim();
                    if (childText.toLowerCase().includes('performance dashboard') && 
                        childText !== '⚡ Performance Dashboard') {
                        child.textContent = '⚡ Performance Dashboard';
                        child.innerText = '⚡ Performance Dashboard';
                    }
                });
                found = true;
            }`;

