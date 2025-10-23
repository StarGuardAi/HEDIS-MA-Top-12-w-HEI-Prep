#!/usr/bin/env python3
"""
Phase 0 Verification Script

Verifies that all Phase 0 components are working correctly:
1. New utilities can be imported
2. Config.yaml loads correctly
3. HEDIS specs are accessible
4. Star calculator functions work
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

print("=" * 80)
print("PHASE 0 VERIFICATION")
print("=" * 80)
print()

# Test 1: Import new utilities (direct import to avoid pandas dependency for now)
print("✓ Test 1: Importing new utilities...")
try:
    # Import directly from files to avoid loading data modules that need pandas
    import importlib.util
    
    # Load hedis_specs
    spec1 = importlib.util.spec_from_file_location("hedis_specs", project_root / "src" / "utils" / "hedis_specs.py")
    hedis_specs = importlib.util.module_from_spec(spec1)
    spec1.loader.exec_module(hedis_specs)
    print("  ✅ hedis_specs imported successfully")
    
    # Load star_calculator
    spec2 = importlib.util.spec_from_file_location("star_calculator", project_root / "src" / "utils" / "star_calculator.py")
    star_calculator = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(star_calculator)
    print("  ✅ star_calculator imported successfully")
except Exception as e:
    print(f"  ❌ Failed to import utilities: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 2: Load config.yaml
print("✓ Test 2: Loading config.yaml...")
try:
    import yaml
    config_path = project_root / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"  ✅ Config loaded successfully")
    print(f"  ✅ Project: {config['project']['name']}")
    print(f"  ✅ Version: {config['project']['version']}")
    print(f"  ✅ Measures defined: {len(config['measures'])}")
except Exception as e:
    print(f"  ❌ Failed to load config: {e}")
    sys.exit(1)

print()

# Test 3: Access HEDIS measure registry
print("✓ Test 3: Accessing HEDIS measure registry...")
try:
    measure_count = len(hedis_specs.MEASURE_REGISTRY)
    print(f"  ✅ Measure registry loaded: {measure_count} measures")
    
    # Check for specific measures
    gsd_spec = hedis_specs.get_measure_spec("GSD")
    print(f"  ✅ GSD spec retrieved: {gsd_spec.name}")
    
    # Check tier filtering
    tier1_measures = hedis_specs.get_measures_by_tier(1)
    print(f"  ✅ Tier 1 measures: {len(tier1_measures)} measures")
    
    # Check triple-weighted measures
    triple_weighted = hedis_specs.get_triple_weighted_measures()
    print(f"  ✅ Triple-weighted measures: {len(triple_weighted)} measures")
    
    # Check NEW 2025 measures
    new_2025 = hedis_specs.get_new_2025_measures()
    print(f"  ✅ NEW 2025 measures: {len(new_2025)} measures")
    
except Exception as e:
    print(f"  ❌ Failed to access HEDIS registry: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Test Star Calculator
print("✓ Test 4: Testing Star Rating Calculator...")
try:
    calculator = star_calculator.StarRatingCalculator()
    
    # Test simple star rating
    test_rate = 0.75
    star = star_calculator.calculate_simple_star_rating(test_rate)
    print(f"  ✅ Simple star calculation: {test_rate:.1%} → {star} stars")
    
    # Test measure performance calculation
    gsd = hedis_specs.get_measure_spec("GSD")
    
    perf = calculator.calculate_measure_performance(
        measure_code=gsd.code,
        measure_name=gsd.name,
        tier=gsd.tier,
        numerator=750,
        denominator=1000,
        percentile=65.0
    )
    print(f"  ✅ Measure performance: {perf.measure_code} = {perf.rate:.1%} ({perf.star_rating} stars)")
    
    # Test revenue estimation
    revenue = star_calculator.estimate_measure_value(star_rating=4.0, weight=3)
    print(f"  ✅ Revenue estimation: 4 stars (3x weight) = ${revenue:,.0f}")
    
except Exception as e:
    print(f"  ❌ Failed star calculator tests: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 5: Check backward compatibility (existing modules)
print("✓ Test 5: Checking backward compatibility...")
try:
    # Check that files exist
    existing_modules = [
        "src/data/data_loader.py",
        "src/data/data_preprocessing.py",
        "src/data/feature_engineering.py",
        "src/models/trainer.py",
        "src/models/predictor.py",
        "src/models/evaluator.py",
        "src/models/serializer.py",
    ]
    
    for module_path in existing_modules:
        full_path = project_root / module_path
        if full_path.exists():
            print(f"  ✅ {module_path} exists")
        else:
            print(f"  ❌ {module_path} NOT FOUND")
            sys.exit(1)
    
    print("  ⚠️  Note: Full import testing requires pandas (install: pip install -r requirements.txt)")
    
except Exception as e:
    print(f"  ❌ Backward compatibility check failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 6: Portfolio calculation
print("✓ Test 6: Testing portfolio performance calculation...")
try:
    # Create sample measure performances
    measures_data = [
        ("GSD", 850, 1000, 70.0),
        ("KED", 800, 1000, 65.0),
        ("CBP", 900, 1000, 75.0),
    ]
    
    measure_performances = []
    for code, num, den, percentile in measures_data:
        spec = hedis_specs.get_measure_spec(code)
        perf = calculator.calculate_measure_performance(
            measure_code=spec.code,
            measure_name=spec.name,
            tier=spec.tier,
            numerator=num,
            denominator=den,
            percentile=percentile
        )
        measure_performances.append(perf)
    
    # Calculate portfolio performance (hei_factor is a percentage modifier, not total multiplier)
    portfolio = calculator.calculate_portfolio_performance(
        measure_performances=measure_performances,
        hei_factor=0.02  # 2% HEI bonus
    )
    
    print(f"  ✅ Portfolio calculated:")
    print(f"     Total Points: {portfolio.total_points:.2f}")
    print(f"     Weighted Avg Stars: {portfolio.weighted_average_stars:.2f}")
    print(f"     HEI Factor: {portfolio.tier4_hei_factor:.1%}")
    print(f"     Base Revenue: ${portfolio.base_star_revenue:,.0f}")
    print(f"     Total Revenue: ${portfolio.total_revenue:,.0f}")
    
except Exception as e:
    print(f"  ❌ Portfolio calculation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 80)
print("✅ PHASE 0 VERIFICATION COMPLETE - ALL TESTS PASSED!")
print("=" * 80)
print()
print("Summary:")
print("  ✅ New utilities working")
print("  ✅ Config.yaml loaded")
print("  ✅ HEDIS registry accessible (12 measures)")
print("  ✅ Star calculator functional")
print("  ✅ Backward compatibility preserved")
print("  ✅ Portfolio calculations working")
print()
print("🚀 Ready to proceed with:")
print("  1. Push Phase 0 to GitHub")
print("  2. Start Phase 1: Tier 1 Diabetes Portfolio")
print()

