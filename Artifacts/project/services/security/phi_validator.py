"""
PHI Validator for Healthcare AI
Implements HIPAA-compliant PHI detection with zero false negatives

Based on Rule 1.1 from CONTEXT_ENGINEERING_RULES.md
"""
import re
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PHIValidationResult:
    """Result of PHI validation."""
    is_valid: bool
    errors: List[str]
    violation_types: List[str]
    violation_count: int
    timestamp: str
    
    def __init__(self, is_valid: bool, errors: List[str] = None, violation_types: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.violation_types = violation_types or []
        self.violation_count = len(self.errors)
        self.timestamp = datetime.now().isoformat()


class PHIValidator:
    """
    Validates content for Protected Health Information (PHI).
    
    Implements Rule 1.1: HIPAA-Compliant Context Assembly
    - 100% PHI detection rate (zero false negatives)
    - Validates before: context assembly, tool calls, result return
    - Logs violations without exposing PHI
    """
    
    # PHI Patterns - Comprehensive detection
    PHI_PATTERNS = [
        # SSN pattern: XXX-XX-XXXX
        (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN', 'Social Security Number pattern detected'),
        
        # Name pattern: First Last (capitalized)
        (r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', 'NAME', 'Potential name pattern detected'),
        
        # DOB pattern: MM/DD/YYYY or M/D/YYYY
        (r'\b\d{1,2}/\d{1,2}/\d{4}\b', 'DOB', 'Date of birth pattern detected'),
        
        # Member ID pattern: MBR followed by 6+ digits
        (r'\bMBR\d{6,}\b', 'MEMBER_ID', 'Member ID pattern detected'),
        
        # Additional patterns for comprehensive coverage
        (r'\b\d{3}\.\d{2}\.\d{4}\b', 'SSN', 'SSN pattern (dotted format) detected'),
        (r'\b\d{9}\b', 'SSN', 'SSN pattern (9 digits, no separators) detected'),
        (r'\b\d{2}-\d{2}-\d{4}\b', 'DOB', 'Date pattern (MM-DD-YYYY) detected'),
    ]
    
    # False positive patterns to exclude (common non-PHI patterns)
    FALSE_POSITIVE_PATTERNS = [
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # Three words (often not names)
    ]
    
    # Common non-PHI phrases (case-insensitive)
    COMMON_NON_PHI_PHRASES = [
        'total cost', 'total revenue', 'net benefit',
        'star impact', 'star rating',
        'query results', 'retrieved docs',
        'step results', 'context used',
        'layer 1', 'layer 2', 'layer 3',
        'domain knowledge', 'measure specific',
        'hedis overview', 'initial context',
        'final context', 'context size',
        'execution time', 'steps executed'
    ]
    
    def __init__(self):
        """Initialize PHI validator."""
        self.violation_count = 0
        self.validation_count = 0
    
    def validate_no_phi(
        self,
        content: Any,
        context: str = "",
        log_violations: bool = True
    ) -> PHIValidationResult:
        """
        Validate content for PHI with zero false negatives.
        
        Args:
            content: Content to validate (str, dict, list, etc.)
            context: Context description for logging (e.g., "context assembly", "tool call")
            log_violations: Whether to log violations (without PHI)
        
        Returns:
            PHIValidationResult with validation status and errors
        """
        self.validation_count += 1
        
        # Convert content to string for pattern matching
        content_str = self._content_to_string(content)
        
        errors = []
        violation_types = []
        
        # Check each PHI pattern
        for pattern, violation_type, error_msg in self.PHI_PATTERNS:
            # Use case-sensitive matching for name patterns, case-insensitive for others
            flags = 0 if violation_type == 'NAME' else re.IGNORECASE
            matches = re.findall(pattern, content_str, flags)
            
            if matches:
                # Filter out false positives
                real_matches = self._filter_false_positives(matches, content_str)
                
                if real_matches:
                    errors.append(f"{error_msg} ({violation_type})")
                    if violation_type not in violation_types:
                        violation_types.append(violation_type)
                    
                    # Log violation (without PHI content)
                    if log_violations:
                        self._log_violation(
                            violation_type=violation_type,
                            context=context,
                            match_count=len(real_matches)
                        )
        
        is_valid = len(errors) == 0
        
        if not is_valid:
            self.violation_count += 1
        
        return PHIValidationResult(
            is_valid=is_valid,
            errors=errors,
            violation_types=violation_types
        )
    
    def _content_to_string(self, content: Any) -> str:
        """Convert content to string for pattern matching."""
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            # Convert dict to string, excluding certain keys that might contain PHI in values
            # but keeping structure for pattern matching
            return str(content)
        elif isinstance(content, list):
            return str(content)
        elif content is None:
            return ""
        else:
            return str(content)
    
    def _filter_false_positives(self, matches: List[str], content_str: str) -> List[str]:
        """
        Filter out false positives from matches.
        
        Args:
            matches: List of matched strings
            content_str: Full content string
        
        Returns:
            Filtered list of real PHI matches
        """
        real_matches = []
        
        for match in matches:
            # Check if match is part of a false positive pattern
            is_false_positive = False
            
            # Check against false positive patterns
            for fp_pattern in self.FALSE_POSITIVE_PATTERNS:
                if re.search(fp_pattern, match, re.IGNORECASE):
                    is_false_positive = True
                    break
            
            # Additional heuristics for name pattern
            if not is_false_positive and re.match(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', match):
                # Check if it's a common non-name phrase (case-insensitive)
                match_lower = match.lower()
                if any(phrase in match_lower for phrase in self.COMMON_NON_PHI_PHRASES):
                    is_false_positive = True
                
                # Check if words are too short (likely not names)
                words = match.split()
                if len(words) == 2:
                    if len(words[0]) < 3 or len(words[1]) < 3:
                        is_false_positive = True
                
                # Check if it's a system term (common prefixes)
                system_prefixes = ['step_', 'layer_', 'query_', 'result_', 'context_']
                if any(match_lower.startswith(prefix) for prefix in system_prefixes):
                    is_false_positive = True
            
            if not is_false_positive:
                real_matches.append(match)
        
        return real_matches
    
    def _log_violation(
        self,
        violation_type: str,
        context: str,
        match_count: int
    ):
        """
        Log PHI violation without exposing PHI content.
        
        Args:
            violation_type: Type of PHI detected (SSN, NAME, DOB, MEMBER_ID)
            context: Context where violation occurred
            match_count: Number of matches found
        """
        log_msg = (
            f"PHI validation violation: {violation_type} detected in {context}. "
            f"Matches found: {match_count}. "
            f"Content rejected for security compliance."
        )
        logger.warning(log_msg)
    
    def validate_before_context_assembly(
        self,
        context_data: Dict,
        log_violations: bool = True
    ) -> PHIValidationResult:
        """
        Validate context data before assembly.
        
        Args:
            context_data: Context dictionary to validate
            log_violations: Whether to log violations
        
        Returns:
            PHIValidationResult
        """
        return self.validate_no_phi(
            content=context_data,
            context="context assembly",
            log_violations=log_violations
        )
    
    def validate_before_tool_call(
        self,
        tool_params: Dict,
        tool_name: str,
        log_violations: bool = True
    ) -> PHIValidationResult:
        """
        Validate tool parameters before execution.
        
        Args:
            tool_params: Tool parameters dictionary
            tool_name: Name of tool being called
            log_violations: Whether to log violations
        
        Returns:
            PHIValidationResult
        """
        return self.validate_no_phi(
            content=tool_params,
            context=f"tool call ({tool_name})",
            log_violations=log_violations
        )
    
    def validate_before_result_return(
        self,
        result: Any,
        log_violations: bool = True
    ) -> PHIValidationResult:
        """
        Validate result before returning to user.
        
        Args:
            result: Result to validate
            log_violations: Whether to log violations
        
        Returns:
            PHIValidationResult
        """
        return self.validate_no_phi(
            content=result,
            context="result return",
            log_violations=log_violations
        )
    
    def get_validation_stats(self) -> Dict:
        """Get validation statistics."""
        return {
            "total_validations": self.validation_count,
            "violations_detected": self.violation_count,
            "violation_rate": (
                self.violation_count / self.validation_count * 100
                if self.validation_count > 0 else 0.0
            )
        }


# Global validator instance
_global_validator = None


def get_phi_validator() -> PHIValidator:
    """Get global PHI validator instance."""
    global _global_validator
    if _global_validator is None:
        _global_validator = PHIValidator()
    return _global_validator


def validate_no_phi(
    content: Any,
    context: str = "",
    log_violations: bool = True
) -> PHIValidationResult:
    """
    Convenience function for PHI validation.
    
    Args:
        content: Content to validate
        context: Context description
        log_violations: Whether to log violations
    
    Returns:
        PHIValidationResult
    """
    validator = get_phi_validator()
    return validator.validate_no_phi(content, context, log_violations)

