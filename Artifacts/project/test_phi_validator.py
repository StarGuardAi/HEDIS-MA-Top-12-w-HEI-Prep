"""
Test script for PHI Validator
Tests Rule 1.1 implementation
"""
import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.security.phi_validator import PHIValidator, validate_no_phi, PHIValidationResult

# Set up logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_ssn_detection():
    """Test SSN pattern detection."""
    print("=" * 80)
    print("Test 1: SSN Pattern Detection")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Test valid SSN pattern
    content = "Member SSN: 123-45-6789"
    result = validator.validate_no_phi(content, context="test")
    
    assert not result.is_valid, "Should detect SSN pattern"
    assert 'SSN' in result.violation_types, "Should identify SSN violation type"
    assert len(result.errors) > 0, "Should have errors"
    
    print(f"[SUCCESS] SSN detected: {result.violation_types}")
    print(f"   Errors: {len(result.errors)}")
    
    # Test SSN without separators
    content = "SSN: 123456789"
    result = validator.validate_no_phi(content, context="test")
    assert not result.is_valid, "Should detect SSN pattern (no separators)"
    
    # Test clean content
    content = "No PHI here, just regular text"
    result = validator.validate_no_phi(content, context="test")
    assert result.is_valid, "Should pass clean content"
    
    print("\n[SUCCESS] SSN detection test passed!\n")


def test_name_detection():
    """Test name pattern detection."""
    print("=" * 80)
    print("Test 2: Name Pattern Detection")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Test name pattern
    content = "Patient: John Doe"
    result = validator.validate_no_phi(content, context="test")
    
    assert not result.is_valid, "Should detect name pattern"
    assert 'NAME' in result.violation_types, "Should identify NAME violation type"
    
    print(f"[SUCCESS] Name detected: {result.violation_types}")
    
    # Test false positives (should be filtered)
    content = "Total Cost: $1000, Total Revenue: $2000"
    result = validator.validate_no_phi(content, context="test")
    assert result.is_valid, "Should filter false positives (Total Cost, Total Revenue)"
    
    print("\n[SUCCESS] Name detection test passed!\n")


def test_dob_detection():
    """Test date of birth pattern detection."""
    print("=" * 80)
    print("Test 3: DOB Pattern Detection")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Test DOB pattern
    content = "Date of Birth: 01/15/1980"
    result = validator.validate_no_phi(content, context="test")
    
    assert not result.is_valid, "Should detect DOB pattern"
    assert 'DOB' in result.violation_types, "Should identify DOB violation type"
    
    print(f"[SUCCESS] DOB detected: {result.violation_types}")
    
    # Test different format
    content = "DOB: 1/5/1990"
    result = validator.validate_no_phi(content, context="test")
    assert not result.is_valid, "Should detect DOB pattern (single digit)"
    
    print("\n[SUCCESS] DOB detection test passed!\n")


def test_member_id_detection():
    """Test member ID pattern detection."""
    print("=" * 80)
    print("Test 4: Member ID Pattern Detection")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Test member ID pattern
    content = "Member ID: MBR123456"
    result = validator.validate_no_phi(content, context="test")
    
    assert not result.is_valid, "Should detect member ID pattern"
    assert 'MEMBER_ID' in result.violation_types, "Should identify MEMBER_ID violation type"
    
    print(f"[SUCCESS] Member ID detected: {result.violation_types}")
    
    # Test longer member ID
    content = "Member: MBR123456789"
    result = validator.validate_no_phi(content, context="test")
    assert not result.is_valid, "Should detect member ID pattern (longer)"
    
    print("\n[SUCCESS] Member ID detection test passed!\n")


def test_context_assembly_validation():
    """Test validation before context assembly."""
    print("=" * 80)
    print("Test 5: Context Assembly Validation")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Test clean context
    context_data = {
        "measure_spec": "HbA1c Testing",
        "aggregate_stats": {"avg_roi": 1.35, "members_count": 1500}
    }
    result = validator.validate_before_context_assembly(context_data)
    assert result.is_valid, "Should pass clean context"
    
    # Test context with PHI
    context_data = {
        "member_id": "MBR123456",
        "member_name": "John Doe"
    }
    result = validator.validate_before_context_assembly(context_data)
    assert not result.is_valid, "Should reject context with PHI"
    assert len(result.violation_types) >= 2, "Should detect multiple PHI types"
    
    print(f"[SUCCESS] Context validation: {result.violation_types}")
    print("\n[SUCCESS] Context assembly validation test passed!\n")


def test_tool_call_validation():
    """Test validation before tool call."""
    print("=" * 80)
    print("Test 6: Tool Call Validation")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Test clean tool params
    tool_params = {
        "measure_id": "GSD",
        "intervention_count": 1000,
        "cost_per_intervention": 25.0
    }
    result = validator.validate_before_tool_call(tool_params, "calculate_roi")
    assert result.is_valid, "Should pass clean tool parameters"
    
    # Test tool params with PHI
    tool_params = {
        "member_id": "MBR123456",
        "ssn": "123-45-6789"
    }
    result = validator.validate_before_tool_call(tool_params, "query_database")
    assert not result.is_valid, "Should reject tool parameters with PHI"
    
    print(f"[SUCCESS] Tool call validation: {result.violation_types}")
    print("\n[SUCCESS] Tool call validation test passed!\n")


def test_result_validation():
    """Test validation before result return."""
    print("=" * 80)
    print("Test 7: Result Validation")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Test clean result
    result_data = {
        "roi_ratio": 2.5,
        "net_benefit": 10000,
        "summary": "ROI analysis complete"
    }
    validation_result = validator.validate_before_result_return(result_data)
    assert validation_result.is_valid, "Should pass clean result"
    
    # Test result with PHI
    result_data = {
        "member_name": "Jane Smith",
        "dob": "01/15/1980"
    }
    validation_result = validator.validate_before_result_return(result_data)
    assert not validation_result.is_valid, "Should reject result with PHI"
    
    print(f"[SUCCESS] Result validation: {validation_result.violation_types}")
    print("\n[SUCCESS] Result validation test passed!\n")


def test_validation_stats():
    """Test validation statistics."""
    print("=" * 80)
    print("Test 8: Validation Statistics")
    print("=" * 80)
    
    validator = PHIValidator()
    
    # Run multiple validations
    validator.validate_no_phi("Clean content")
    validator.validate_no_phi("John Doe")  # Should trigger violation
    validator.validate_no_phi("Another clean content")
    
    stats = validator.get_validation_stats()
    
    print(f"Total Validations: {stats['total_validations']}")
    print(f"Violations Detected: {stats['violations_detected']}")
    print(f"Violation Rate: {stats['violation_rate']:.1f}%")
    
    assert stats['total_validations'] == 3
    assert stats['violations_detected'] >= 1
    
    print("\n[SUCCESS] Validation statistics test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("PHI Validator Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_ssn_detection()
        test_name_detection()
        test_dob_detection()
        test_member_id_detection()
        test_context_assembly_validation()
        test_tool_call_validation()
        test_result_validation()
        test_validation_stats()
        
        print("=" * 80)
        print("[SUCCESS] All tests passed!")
        print("=" * 80)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n[FAILED] Test assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

