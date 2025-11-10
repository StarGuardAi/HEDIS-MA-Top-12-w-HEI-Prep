"""
Validate data quality for fraud detection dataset.

This script performs comprehensive data quality checks including:
- Missing values
- Duplicates
- Value ranges
- Data types
- Class distribution
- Feature distributions
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Tuple
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataQualityValidator:
    """Validate data quality for fraud detection dataset."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize validator with dataframe."""
        self.df = df.copy()
        self.issues = []
        self.warnings = []
        self.stats = {}
    
    def check_missing_values(self, max_missing_pct: float = 10.0) -> List[str]:
        """Check for missing values."""
        issues = []
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        for col, pct in missing_pct.items():
            if pct > 0:
                if pct > max_missing_pct:
                    issues.append(f"High missing values in '{col}': {pct:.2f}% (>{max_missing_pct}%)")
                else:
                    self.warnings.append(f"Missing values in '{col}': {pct:.2f}%")
        
        self.stats['missing_values'] = {
            'total_missing': int(missing.sum()),
            'columns_with_missing': int((missing > 0).sum()),
            'missing_percentage': float(missing_pct.max())
        }
        
        return issues
    
    def check_duplicates(self, max_duplicates: int = 100) -> List[str]:
        """Check for duplicate rows."""
        issues = []
        dup_count = self.df.duplicated().sum()
        
        if dup_count > max_duplicates:
            issues.append(f"Too many duplicate rows: {dup_count} (>{max_duplicates})")
        
        self.stats['duplicates'] = {
            'count': int(dup_count),
            'percentage': float((dup_count / len(self.df)) * 100)
        }
        
        return issues
    
    def check_value_ranges(self, expected_ranges: Dict[str, Tuple[float, float]]) -> List[str]:
        """Check that values are within expected ranges."""
        issues = []
        
        for col, (min_val, max_val) in expected_ranges.items():
            if col not in self.df.columns:
                self.warnings.append(f"Expected column '{col}' not found")
                continue
            
            actual_min = self.df[col].min()
            actual_max = self.df[col].max()
            
            if actual_min < min_val or actual_max > max_val:
                issues.append(
                    f"'{col}' outside expected range [{min_val}, {max_val}]: "
                    f"actual [{actual_min:.2f}, {actual_max:.2f}]"
                )
        
        return issues
    
    def check_data_types(self, expected_types: Dict[str, type]) -> List[str]:
        """Check that columns have expected data types."""
        issues = []
        
        for col, expected_type in expected_types.items():
            if col not in self.df.columns:
                continue
            
            actual_type = self.df[col].dtype
            if not pd.api.types.is_dtype_equal(actual_type, expected_type):
                # Allow some flexibility (e.g., int64 vs int32)
                if not (pd.api.types.is_integer_dtype(actual_type) and 
                       pd.api.types.is_integer_dtype(expected_type)):
                    issues.append(
                        f"'{col}' has wrong type: expected {expected_type}, "
                        f"got {actual_type}"
                    )
        
        return issues
    
    def check_class_distribution(self, target_col: str = 'is_fraud') -> List[str]:
        """Check class distribution for target variable."""
        issues = []
        
        if target_col not in self.df.columns:
            self.warnings.append(f"Target column '{target_col}' not found")
            return issues
        
        class_counts = self.df[target_col].value_counts()
        class_pct = self.df[target_col].value_counts(normalize=True) * 100
        
        self.stats['class_distribution'] = {
            'class_counts': class_counts.to_dict(),
            'class_percentages': class_pct.to_dict(),
            'total_samples': int(len(self.df))
        }
        
        # Check for extreme imbalance (if fraud rate < 0.1% or > 50%)
        if 1 in class_pct.index:
            fraud_rate = class_pct[1]
            if fraud_rate < 0.1:
                issues.append(f"Very low fraud rate: {fraud_rate:.2f}% (<0.1%)")
            elif fraud_rate > 50:
                issues.append(f"Very high fraud rate: {fraud_rate:.2f}% (>50%)")
        
        # Check for missing classes
        if len(class_counts) < 2:
            issues.append(f"Missing classes in '{target_col}': only found {list(class_counts.index)}")
        
        return issues
    
    def check_feature_distributions(self) -> List[str]:
        """Check for suspicious feature distributions."""
        issues = []
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col == 'is_fraud':  # Skip target variable
                continue
            
            # Check for constant columns
            if self.df[col].nunique() == 1:
                issues.append(f"Constant column '{col}': all values are {self.df[col].iloc[0]}")
            
            # Check for columns with very few unique values
            unique_ratio = self.df[col].nunique() / len(self.df)
            if unique_ratio < 0.01 and len(self.df) > 1000:
                self.warnings.append(
                    f"Low cardinality in '{col}': {self.df[col].nunique()} unique values "
                    f"({unique_ratio*100:.1f}% of total)"
                )
            
            # Check for infinite values
            if np.isinf(self.df[col]).any():
                issues.append(f"Infinite values found in '{col}'")
            
            # Check for extreme outliers (beyond 5 standard deviations)
            if self.df[col].dtype in [np.float64, np.float32, np.int64, np.int32]:
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                extreme_outliers = (z_scores > 5).sum()
                if extreme_outliers > len(self.df) * 0.01:  # More than 1% extreme outliers
                    self.warnings.append(
                        f"Many extreme outliers in '{col}': {extreme_outliers} values "
                        f"({extreme_outliers/len(self.df)*100:.1f}%)"
                    )
        
        return issues
    
    def check_basic_stats(self) -> Dict:
        """Calculate basic statistics."""
        stats = {
            'shape': {
                'rows': int(len(self.df)),
                'columns': int(len(self.df.columns))
            },
            'columns': list(self.df.columns),
            'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            'memory_usage_mb': float(self.df.memory_usage(deep=True).sum() / 1024**2)
        }
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats['numeric_summary'] = self.df[numeric_cols].describe().to_dict()
        
        return stats
    
    def validate_all(
        self,
        max_missing_pct: float = 10.0,
        max_duplicates: int = 100,
        expected_ranges: Dict = None,
        expected_types: Dict = None,
        target_col: str = 'is_fraud'
    ) -> Tuple[bool, Dict]:
        """
        Run all validation checks.
        
        Returns:
            (is_valid, validation_report)
        """
        if expected_ranges is None:
            expected_ranges = {}
        if expected_types is None:
            expected_types = {}
        
        logger.info("Running data quality checks...")
        logger.info("=" * 60)
        
        # Run all checks
        self.issues.extend(self.check_missing_values(max_missing_pct))
        self.issues.extend(self.check_duplicates(max_duplicates))
        self.issues.extend(self.check_value_ranges(expected_ranges))
        self.issues.extend(self.check_data_types(expected_types))
        self.issues.extend(self.check_class_distribution(target_col))
        self.issues.extend(self.check_feature_distributions())
        
        # Get basic stats
        basic_stats = self.check_basic_stats()
        self.stats.update(basic_stats)
        
        # Compile report
        is_valid = len(self.issues) == 0
        
        report = {
            'is_valid': is_valid,
            'issues_count': len(self.issues),
            'warnings_count': len(self.warnings),
            'issues': self.issues,
            'warnings': self.warnings,
            'statistics': self.stats
        }
        
        return is_valid, report


def print_report(report: Dict):
    """Print validation report in a readable format."""
    # Use logger for better Windows PowerShell compatibility
    logger.info("")
    logger.info("=" * 60)
    logger.info("DATA QUALITY VALIDATION REPORT")
    logger.info("=" * 60)
    
    # Overall status (using ASCII-safe characters)
    status = "[PASSED]" if report['is_valid'] else "[FAILED]"
    logger.info(f"\nStatus: {status}")
    logger.info(f"Issues found: {report['issues_count']}")
    logger.info(f"Warnings: {report['warnings_count']}")
    
    # Statistics
    stats = report['statistics']
    if 'shape' in stats:
        logger.info(f"\nDataset Shape: {stats['shape']['rows']:,} rows x {stats['shape']['columns']} columns")
        logger.info(f"Memory Usage: {stats['memory_usage_mb']:.2f} MB")
    
    # Class distribution
    if 'class_distribution' in stats:
        cd = stats['class_distribution']
        logger.info(f"\nClass Distribution:")
        for cls, count in cd['class_counts'].items():
            pct = cd['class_percentages'][cls]
            logger.info(f"  Class {cls}: {count:,} ({pct:.2f}%)")
    
    # Missing values
    if 'missing_values' in stats:
        mv = stats['missing_values']
        if mv['total_missing'] > 0:
            logger.info(f"\nMissing Values:")
            logger.info(f"  Total missing: {mv['total_missing']:,}")
            logger.info(f"  Columns with missing: {mv['columns_with_missing']}")
            logger.info(f"  Max missing %: {mv['missing_percentage']:.2f}%")
    
    # Issues
    if report['issues']:
        logger.info(f"\n[ISSUES] ({len(report['issues'])}):")
        for i, issue in enumerate(report['issues'], 1):
            logger.info(f"  {i}. {issue}")
    
    # Warnings
    if report['warnings']:
        logger.info(f"\n[WARNINGS] ({len(report['warnings'])}):")
        for i, warning in enumerate(report['warnings'], 1):
            logger.info(f"  {i}. {warning}")
    
    logger.info("\n" + "=" * 60)


def main():
    """Main function with command-line argument parsing."""
    import sys
    import io
    
    # Set UTF-8 encoding for Windows PowerShell compatibility
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except AttributeError:
            # Python < 3.7 compatibility
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(
        description='Validate data quality for fraud detection dataset',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_data_quality.py --input data/processed/train.csv
  python scripts/validate_data_quality.py -i data/processed/X_train.csv --output report.json
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Input CSV file to validate'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output JSON file for validation report (optional)'
    )
    
    parser.add_argument(
        '--max-missing-pct',
        type=float,
        default=10.0,
        help='Maximum allowed missing value percentage (default: 10.0)'
    )
    
    parser.add_argument(
        '--max-duplicates',
        type=int,
        default=100,
        help='Maximum allowed duplicate rows (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Load data
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return 1
    
    logger.info(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
        logger.info(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        return 1
    
    # Define expected ranges for common fraud detection features
    expected_ranges = {
        'amount': (0, 100000),
        'is_fraud': (0, 1),
        'hour': (0, 23),
    }
    
    # Define expected types
    expected_types = {
        'is_fraud': np.int64,
    }
    
    # Validate
    validator = DataQualityValidator(df)
    is_valid, report = validator.validate_all(
        max_missing_pct=args.max_missing_pct,
        max_duplicates=args.max_duplicates,
        expected_ranges=expected_ranges,
        expected_types=expected_types,
        target_col='is_fraud'
    )
    
    # Print report
    print_report(report)
    
    # Save report if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"Validation report saved to {output_path}")
    
    # Return exit code
    return 0 if is_valid else 1


if __name__ == "__main__":
    exit(main())

