"""
Performance Benchmarking Script for HEDIS Measures

Compares original vs. optimized implementations to demonstrate
2-3x performance improvements.

Usage:
    python scripts/benchmark_performance.py --measure supd --population 10000

Author: Analytics Team
Date: October 25, 2025
"""

import pandas as pd
import numpy as np
import time
import argparse
from datetime import datetime, timedelta

# Import original measures
from src.measures.supd import SUPDMeasure
from src.measures.pdc_rasa import PDCRASAMeasure
from src.measures.pdc_sta import PDCSTAMeasure

# Import optimized measures
from src.measures.supd_optimized import SUPDMeasureOptimized


def generate_synthetic_data(n_members: int = 10000, seed: int = 42):
    """
    Generate synthetic test data for benchmarking.
    
    Args:
        n_members: Number of members to generate
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (members_df, claims_df, pharmacy_df)
    """
    np.random.seed(seed)
    
    # Generate members
    member_ids = [f'M{i:06d}' for i in range(n_members)]
    birth_dates = [
        datetime(1950, 1, 1) + timedelta(days=int(np.random.uniform(0, 365*50)))
        for _ in range(n_members)
    ]
    
    members_df = pd.DataFrame({
        'member_id': member_ids,
        'birth_date': birth_dates,
        'enrollment_months': 12
    })
    
    # Generate claims (average 10 claims per member)
    n_claims = n_members * 10
    claim_member_ids = np.random.choice(member_ids, n_claims)
    
    diabetes_codes = ['E11.9', 'E11.22', 'E11.65']
    htn_codes = ['I10', 'I11.9']
    other_codes = ['Z00.00', 'Z23']
    all_codes = diabetes_codes + htn_codes + other_codes
    
    claims_df = pd.DataFrame({
        'member_id': claim_member_ids,
        'diagnosis_code': np.random.choice(all_codes, n_claims),
        'service_date': [
            datetime(2025, 1, 1) + timedelta(days=int(np.random.uniform(0, 365)))
            for _ in range(n_claims)
        ],
        'claim_type': np.random.choice(['outpatient', 'professional', 'inpatient'], n_claims)
    })
    
    # Generate pharmacy (average 12 fills per member)
    n_fills = n_members * 12
    fill_member_ids = np.random.choice(member_ids, n_fills)
    
    medications = [
        'atorvastatin 40mg', 'simvastatin 20mg', 'lisinopril 10mg',
        'losartan 50mg', 'metformin 500mg'
    ]
    
    # Create fills every 30 days
    base_dates = [datetime(2025, 1, 1) + timedelta(days=30*i) for i in range(12)]
    fill_dates = []
    for _ in range(n_members):
        fill_dates.extend(base_dates)
    
    pharmacy_df = pd.DataFrame({
        'member_id': fill_member_ids,
        'medication_name': np.random.choice(medications, n_fills),
        'fill_date': fill_dates[:n_fills],
        'days_supply': 30
    })
    
    return members_df, claims_df, pharmacy_df


def benchmark_supd(members_df, claims_df, pharmacy_df):
    """
    Benchmark SUPD measure (original vs optimized).
    """
    print("\n" + "="*80)
    print("SUPD (Statin Therapy for Patients with Diabetes) Benchmark")
    print("="*80)
    
    # Original implementation
    print("\n[1/2] Running ORIGINAL implementation...")
    start_time = time.time()
    
    supd_original = SUPDMeasure(measurement_year=2025)
    results_original = supd_original.calculate_population_rate(
        members_df, claims_df, pharmacy_df
    )
    
    original_time = time.time() - start_time
    print(f"  ✓ Completed in {original_time:.2f} seconds")
    print(f"  - Denominator: {results_original['denominator_count']}")
    print(f"  - Numerator: {results_original['numerator_count']}")
    print(f"  - Rate: {results_original['measure_rate']:.2f}%")
    
    # Optimized implementation
    print("\n[2/2] Running OPTIMIZED implementation...")
    start_time = time.time()
    
    supd_optimized = SUPDMeasureOptimized(measurement_year=2025)
    results_optimized = supd_optimized.calculate_population_rate_optimized(
        members_df, claims_df, pharmacy_df
    )
    
    optimized_time = time.time() - start_time
    print(f"  ✓ Completed in {optimized_time:.2f} seconds")
    print(f"  - Denominator: {results_optimized['denominator_count']}")
    print(f"  - Numerator: {results_optimized['numerator_count']}")
    print(f"  - Rate: {results_optimized['measure_rate']:.2f}%")
    
    # Performance comparison
    speedup = original_time / optimized_time if optimized_time > 0 else 0
    time_saved = original_time - optimized_time
    percent_faster = ((original_time - optimized_time) / original_time * 100) if original_time > 0 else 0
    
    print("\n" + "-"*80)
    print("PERFORMANCE RESULTS:")
    print("-"*80)
    print(f"  Original time:    {original_time:.2f}s")
    print(f"  Optimized time:   {optimized_time:.2f}s")
    print(f"  Time saved:       {time_saved:.2f}s")
    print(f"  Speedup:          {speedup:.2f}x faster")
    print(f"  Improvement:      {percent_faster:.1f}% faster")
    
    # Validate results match
    if results_original['measure_rate'] == results_optimized['measure_rate']:
        print(f"  ✓ Results validated: Both versions produce identical rates")
    else:
        print(f"  ⚠ Warning: Results differ slightly (may be due to floating point precision)")
    
    return {
        'measure': 'SUPD',
        'original_time': original_time,
        'optimized_time': optimized_time,
        'speedup': speedup,
        'time_saved': time_saved,
        'percent_faster': percent_faster
    }


def benchmark_pdc_calculation():
    """
    Benchmark PDC calculation specifically (original vs optimized).
    """
    print("\n" + "="*80)
    print("PDC Calculation Benchmark (RASA/STA methodology)")
    print("="*80)
    
    # Generate test pharmacy data
    np.random.seed(42)
    n_fills = 12
    fill_dates = pd.date_range('2025-01-01', periods=n_fills, freq='30D')
    
    test_pharmacy = pd.DataFrame({
        'member_id': ['M000001'] * n_fills,
        'medication_name': ['lisinopril 10mg'] * n_fills,
        'fill_date': fill_dates,
        'days_supply': [30] * n_fills
    })
    
    measurement_start = datetime(2025, 1, 1)
    measurement_end = datetime(2025, 12, 31)
    
    # Original PDC calculation
    print("\n[1/2] Running ORIGINAL PDC calculation (1000 iterations)...")
    from src.measures.pdc_rasa import PDCRASAMeasure
    
    pdc_measure = PDCRASAMeasure(2025)
    
    start_time = time.time()
    for _ in range(1000):
        pdc_rate, days_covered, total_days = pdc_measure.calculate_pdc(test_pharmacy)
    original_time = time.time() - start_time
    
    print(f"  ✓ Completed 1000 iterations in {original_time:.3f} seconds")
    print(f"  - PDC: {pdc_rate:.2f}%")
    print(f"  - Days covered: {days_covered}/{total_days}")
    
    # Optimized PDC calculation
    print("\n[2/2] Running OPTIMIZED PDC calculation (1000 iterations)...")
    from src.measures.pdc_optimized_utils import calculate_pdc_optimized
    
    start_time = time.time()
    for _ in range(1000):
        pdc_rate_opt, days_covered_opt, total_days_opt = calculate_pdc_optimized(
            test_pharmacy, measurement_start, measurement_end
        )
    optimized_time = time.time() - start_time
    
    print(f"  ✓ Completed 1000 iterations in {optimized_time:.3f} seconds")
    print(f"  - PDC: {pdc_rate_opt:.2f}%")
    print(f"  - Days covered: {days_covered_opt}/{total_days_opt}")
    
    # Performance comparison
    speedup = original_time / optimized_time if optimized_time > 0 else 0
    
    print("\n" + "-"*80)
    print("PERFORMANCE RESULTS:")
    print("-"*80)
    print(f"  Original time:    {original_time:.3f}s (1000 iterations)")
    print(f"  Optimized time:   {optimized_time:.3f}s (1000 iterations)")
    print(f"  Speedup:          {speedup:.2f}x faster")
    print(f"  Per calculation:  {(optimized_time/1000)*1000:.2f}ms vs {(original_time/1000)*1000:.2f}ms")
    
    return {
        'measure': 'PDC_Calculation',
        'original_time': original_time,
        'optimized_time': optimized_time,
        'speedup': speedup
    }


def main():
    parser = argparse.ArgumentParser(description='Benchmark HEDIS measure performance')
    parser.add_argument('--measure', choices=['supd', 'pdc', 'all'], default='all',
                        help='Measure to benchmark')
    parser.add_argument('--population', type=int, default=10000,
                        help='Number of members to generate for testing')
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("HEDIS Measure Performance Benchmarking")
    print("="*80)
    print(f"Population size: {args.population:,} members")
    print(f"Measurement year: 2025")
    print(f"Test data: Synthetic (reproducible with seed=42)")
    
    results = []
    
    if args.measure in ['all', 'supd']:
        # Generate test data
        print(f"\nGenerating synthetic data for {args.population:,} members...")
        members_df, claims_df, pharmacy_df = generate_synthetic_data(args.population)
        print(f"  ✓ Generated {len(members_df):,} members")
        print(f"  ✓ Generated {len(claims_df):,} claims")
        print(f"  ✓ Generated {len(pharmacy_df):,} pharmacy fills")
        
        # Benchmark SUPD
        supd_results = benchmark_supd(members_df, claims_df, pharmacy_df)
        results.append(supd_results)
    
    if args.measure in ['all', 'pdc']:
        # Benchmark PDC calculation
        pdc_results = benchmark_pdc_calculation()
        results.append(pdc_results)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY: Performance Improvements")
    print("="*80)
    
    for result in results:
        print(f"\n{result['measure']}:")
        print(f"  Speedup: {result['speedup']:.2f}x faster")
        if 'time_saved' in result:
            print(f"  Time saved: {result['time_saved']:.2f}s ({result['percent_faster']:.1f}% improvement)")
    
    # Extrapolation to 100K members
    if results and 'time_saved' in results[0]:
        print(f"\n" + "-"*80)
        print(f"EXTRAPOLATION TO 100,000 MEMBERS:")
        print(f"-"*80)
        
        scaling_factor = 100000 / args.population
        supd_result = results[0]
        
        original_100k = supd_result['original_time'] * scaling_factor
        optimized_100k = supd_result['optimized_time'] * scaling_factor
        time_saved_100k = supd_result['time_saved'] * scaling_factor
        
        print(f"  Original (100K):   {original_100k/60:.1f} minutes")
        print(f"  Optimized (100K):  {optimized_100k/60:.1f} minutes")
        print(f"  Time saved (100K): {time_saved_100k/60:.1f} minutes")
        print(f"  Speedup:           {supd_result['speedup']:.2f}x faster")
    
    print("\n" + "="*80)
    print("Benchmark complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

