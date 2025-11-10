# Testing False Positives

This document tests that words like "restart", "star", "guard" are not replaced incorrectly.

- restart: should remain "restart"
- star: should remain "star"  
- guard: should remain "guard"
- StarGuardAI: should be replaced with sentinel-analytics

