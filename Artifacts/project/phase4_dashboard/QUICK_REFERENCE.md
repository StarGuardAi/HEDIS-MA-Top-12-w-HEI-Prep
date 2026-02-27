# Architecture Quick Reference

## 🚀 Quick Start

### 1. Configuration

```python
from core.config import get_settings

settings = get_settings()
# Access any setting
db_host = settings.database.host
log_level = settings.logging.level
api_key = settings.api.openai_api_key
```

### 2. Logging

```python
from core.logging import get_logger

logger = get_logger(__name__)
logger.info("Info message")
logger.error("Error message", exc_info=True)
logger.debug("Debug message")
```

### 3. Error Handling

```python
from core.exceptions import DatabaseError, ValidationError

try:
    result = operation()
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    st.error(e.message)
except ValidationError as e:
    logger.warning(f"Validation error: {e}")
    st.warning(e.message)
```

### 4. Domain Entities

```python
from domain.entities import Member, Gap, Measure
from datetime import datetime

# Create member
member = Member(
    member_id="123",
    first_name="John",
    last_name="Doe",
    date_of_birth=datetime(1959, 1, 1),
    gender="M",
    risk_score=0.75,
    state="CA",
    zip_code="90210"
)

# Use rich domain methods
age = member.age()
full_name = member.full_name()
```

### 5. Value Objects

```python
from domain.value_objects import MeasureRate, DateRange, StarRating, ROI
from datetime import date
from decimal import Decimal

# Measure rate
rate = MeasureRate.calculate(numerator=100, denominator=200)
is_above = rate.is_above_threshold(50.0)

# Date range
date_range = DateRange(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)
days = date_range.days()

# Star rating
rating = StarRating(
    overall_rating=4.2,
    process_domain=4.0,
    outcome_domain=4.5,
    patient_experience_domain=4.3,
    access_domain=4.1
)
rounded = rating.rounded_rating()

# ROI
roi = ROI.calculate(
    investment=Decimal("100000"),
    return_value=Decimal("150000")
)
is_positive = roi.is_positive()
```

### 6. Database Access

```python
from infrastructure.database import get_db_manager

db_manager = get_db_manager()

# Execute query
df = db_manager.execute_query("SELECT * FROM members")

# With parameters
df = db_manager.execute_query(
    "SELECT * FROM members WHERE state = :state",
    params={"state": "CA"}
)

# Health check
is_healthy = db_manager.health_check()
```

### 7. Caching

```python
from infrastructure.cache import get_cache_manager, cached

# Direct usage
cache = get_cache_manager()
cache.set("key", "value", ttl=3600)
value = cache.get("key")
cache.delete("key")

# Decorator
@cached(prefix="members", ttl=3600)
def get_all_members():
    return expensive_operation()
```

## 📁 File Organization

```
core/              - Foundation (config, logging, exceptions)
domain/            - Business logic (entities, value objects)
infrastructure/     - Technical (database, cache)
application/       - Services (to be created)
presentation/      - UI (existing pages)
utils/             - Legacy utilities
```

## 🔄 Common Patterns

### Pattern: Service with Caching

```python
from infrastructure.cache import cached
from infrastructure.database import get_db_manager

class MemberService:
    def __init__(self):
        self.db = get_db_manager()
    
    @cached(prefix="members", ttl=3600)
    def get_all_members(self):
        df = self.db.execute_query("SELECT * FROM members")
        return [Member.from_dict(row) for row in df.to_dict('records')]
```

### Pattern: Error Handling with Logging

```python
from core.logging import get_logger
from core.exceptions import DatabaseError

logger = get_logger(__name__)

def get_member_data(member_id: str):
    try:
        result = db_manager.execute_query(
            "SELECT * FROM members WHERE member_id = :id",
            params={"id": member_id}
        )
        if result.empty:
            raise NotFoundError(f"Member {member_id} not found")
        return result
    except DatabaseError as e:
        logger.error(f"Database error getting member {member_id}: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise
```

### Pattern: Configuration-Based Feature Flags

```python
from core.config import get_settings

settings = get_settings()

if settings.enable_ai_insights:
    # Use AI insights
    pass

if settings.enable_ml_predictions:
    # Use ML predictions
    pass
```

## 🎯 Best Practices

1. **Always use type hints**
2. **Use domain entities instead of dicts**
3. **Use value objects for calculations**
4. **Log errors with context**
5. **Use configuration for all settings**
6. **Handle errors explicitly**
7. **Cache expensive operations**

## 📚 More Information

- See `ARCHITECTURE.md` for detailed documentation
- See `MIGRATION_GUIDE.md` for migration steps
- See `ARCHITECTURE_SUMMARY.md` for status

