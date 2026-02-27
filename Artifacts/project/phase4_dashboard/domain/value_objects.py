"""
Value Objects

Immutable value objects representing domain concepts.
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class DateRange:
    """Date range value object"""
    start_date: date
    end_date: date
    
    def __post_init__(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before end date")
    
    def days(self) -> int:
        """Get number of days in range"""
        return (self.end_date - self.start_date).days
    
    def contains(self, check_date: date) -> bool:
        """Check if date is within range"""
        return self.start_date <= check_date <= self.end_date
    
    def overlaps(self, other: 'DateRange') -> bool:
        """Check if date ranges overlap"""
        return self.start_date <= other.end_date and other.start_date <= self.end_date


@dataclass(frozen=True)
class MeasureRate:
    """Measure rate value object"""
    numerator: int
    denominator: int
    rate: float
    
    def __post_init__(self):
        if self.denominator == 0:
            raise ValueError("Denominator cannot be zero")
        if self.numerator < 0 or self.denominator < 0:
            raise ValueError("Numerator and denominator must be non-negative")
        if not 0 <= self.rate <= 100:
            raise ValueError("Rate must be between 0 and 100")
    
    @classmethod
    def calculate(cls, numerator: int, denominator: int) -> 'MeasureRate':
        """Calculate measure rate from numerator and denominator"""
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        rate = (numerator / denominator) * 100
        return cls(numerator=numerator, denominator=denominator, rate=rate)
    
    def percentage_points(self) -> float:
        """Get rate as percentage points"""
        return self.rate
    
    def is_above_threshold(self, threshold: float) -> bool:
        """Check if rate is above threshold"""
        return self.rate >= threshold


@dataclass(frozen=True)
class StarRating:
    """Star rating value object"""
    overall_rating: float
    process_domain: float
    outcome_domain: float
    patient_experience_domain: float
    access_domain: float
    
    def __post_init__(self):
        if not all(1 <= domain <= 5 for domain in [
            self.overall_rating,
            self.process_domain,
            self.outcome_domain,
            self.patient_experience_domain,
            self.access_domain
        ]):
            raise ValueError("All ratings must be between 1 and 5")
    
    def rounded_rating(self) -> float:
        """Get rounded overall rating"""
        return round(self.overall_rating * 2) / 2  # Round to nearest 0.5
    
    def is_above_threshold(self, threshold: float) -> bool:
        """Check if rating is above threshold"""
        return self.overall_rating >= threshold
    
    def distance_to_next_tier(self) -> float:
        """Calculate distance to next 0.5 star tier"""
        current_tier = int(self.overall_rating * 2) / 2
        next_tier = current_tier + 0.5
        return next_tier - self.overall_rating


@dataclass(frozen=True)
class ROI:
    """ROI value object"""
    investment: Decimal
    return_value: Decimal
    roi_percentage: float
    net_benefit: Decimal
    
    def __post_init__(self):
        if self.investment < 0:
            raise ValueError("Investment cannot be negative")
    
    @classmethod
    def calculate(cls, investment: Decimal, return_value: Decimal) -> 'ROI':
        """Calculate ROI from investment and return"""
        if investment == 0:
            raise ValueError("Investment cannot be zero")
        roi_percentage = float((return_value - investment) / investment * 100)
        net_benefit = return_value - investment
        return cls(
            investment=investment,
            return_value=return_value,
            roi_percentage=roi_percentage,
            net_benefit=net_benefit
        )
    
    def is_positive(self) -> bool:
        """Check if ROI is positive"""
        return self.net_benefit > 0
    
    def payback_period_months(self, monthly_benefit: Decimal) -> Optional[float]:
        """Calculate payback period in months"""
        if monthly_benefit <= 0:
            return None
        return float(self.investment / monthly_benefit)

