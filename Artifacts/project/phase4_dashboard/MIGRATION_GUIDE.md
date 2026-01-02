# Migration Guide: Production-Grade Architecture

## Overview

This guide explains how to migrate existing code to the new production-grade architecture. The migration is designed to be incremental - you can migrate components one at a time.

## Architecture Benefits

### Before (Current State)
- Mixed concerns in single files
- Business logic in UI layer
- Hard to test
- Tight coupling
- No clear separation

### After (Target State)
- Clear layer separation
- Testable components
- Loose coupling
- Dependency injection
- Type safety

## Migration Strategy

### Phase 1: Foundation ✅ (Complete)

**What was done:**
- Created core layer (config, logging, exceptions)
- Created domain layer (entities, value objects)
- Created infrastructure layer (database, cache)

**How to use:**
```python
# Instead of direct imports
from utils.database import get_db_connection

# Use new infrastructure
from infrastructure.database import get_db_manager
db_manager = get_db_manager()
```

### Phase 2: Services (Next Steps)

**What to do:**
1. Create application services
2. Extract business logic from pages
3. Create repository interfaces

**Example migration:**

**Before:**
```python
# In a page file
def calculate_roi(investment, return_value):
    roi = (return_value - investment) / investment * 100
    return roi
```

**After:**
```python
# In application/services/roi_service.py
from domain.value_objects import ROI

class ROIService:
    def calculate_roi(self, investment: Decimal, return_value: Decimal) -> ROI:
        return ROI.calculate(investment, return_value)

# In page
from application.services import ROIService
roi_service = ROIService()
roi = roi_service.calculate_roi(investment, return_value)
```

### Phase 3: Refactoring Pages

**What to do:**
1. Extract business logic to services
2. Use domain entities instead of dicts
3. Use value objects for calculations

**Example:**

**Before:**
```python
# In page
df = execute_query("SELECT * FROM members")
members = df.to_dict('records')
for member in members:
    age = calculate_age(member['date_of_birth'])
```

**After:**
```python
# In page
from application.services import MemberService
from domain.entities import Member

member_service = MemberService()
members = member_service.get_all_members()
for member in members:  # member is a Member entity
    age = member.age()  # Rich domain method
```

## Step-by-Step Migration

### Step 1: Update Configuration

**Old way:**
```python
import os
db_host = os.getenv('DB_HOST', 'localhost')
```

**New way:**
```python
from core.config import get_settings
settings = get_settings()
db_host = settings.database.host
```

### Step 2: Update Logging

**Old way:**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Message")
```

**New way:**
```python
from core.logging import get_logger
logger = get_logger(__name__)
logger.info("Message")
```

### Step 3: Update Error Handling

**Old way:**
```python
try:
    result = execute_query(query)
except Exception as e:
    st.error(f"Error: {e}")
```

**New way:**
```python
from core.exceptions import DatabaseError

try:
    result = db_manager.execute_query(query)
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    st.error(f"Database error: {e.message}")
```

### Step 4: Use Domain Entities

**Old way:**
```python
member_data = {
    'member_id': '123',
    'name': 'John Doe',
    'age': 65
}
```

**New way:**
```python
from domain.entities import Member
from datetime import datetime

member = Member(
    member_id='123',
    first_name='John',
    last_name='Doe',
    date_of_birth=datetime(1959, 1, 1),
    gender='M',
    risk_score=0.75,
    state='CA',
    zip_code='90210'
)
age = member.age()  # Rich domain method
```

### Step 5: Use Value Objects

**Old way:**
```python
numerator = 100
denominator = 200
rate = numerator / denominator * 100
```

**New way:**
```python
from domain.value_objects import MeasureRate

measure_rate = MeasureRate.calculate(numerator=100, denominator=200)
rate = measure_rate.percentage_points()
is_above = measure_rate.is_above_threshold(50.0)
```

## Migration Checklist

### Core Layer
- [x] Configuration management
- [x] Logging setup
- [x] Exception hierarchy

### Domain Layer
- [x] Entity definitions
- [x] Value object definitions

### Infrastructure Layer
- [x] Database manager
- [x] Cache manager
- [ ] Repository implementations

### Application Layer
- [ ] Service definitions
- [ ] DTO definitions
- [ ] Use case implementations

### Presentation Layer
- [ ] Refactor pages to use services
- [ ] Extract business logic
- [ ] Use domain entities

## Testing Migration

### Before Migration
```python
# Hard to test - depends on database
def get_members():
    return execute_query("SELECT * FROM members")
```

### After Migration
```python
# Easy to test - can mock repository
class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository
    
    def get_members(self):
        return self.repository.find_all()

# In tests
mock_repo = Mock(MemberRepository)
service = MemberService(mock_repo)
members = service.get_members()
```

## Common Patterns

### Pattern 1: Service Layer

**Create service:**
```python
# application/services/member_service.py
from domain.entities import Member
from infrastructure.repositories import MemberRepository

class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository
    
    def get_member(self, member_id: str) -> Member:
        return self.repository.find_by_id(member_id)
    
    def get_high_risk_members(self) -> List[Member]:
        return self.repository.find_by_risk_score(min_score=0.7)
```

**Use in page:**
```python
# In page file
from infrastructure.database import get_db_manager
from infrastructure.repositories import MemberRepository
from application.services import MemberService

db_manager = get_db_manager()
repository = MemberRepository(db_manager)
service = MemberService(repository)

members = service.get_high_risk_members()
```

### Pattern 2: Caching

**Before:**
```python
@st.cache_data
def expensive_calculation():
    # ...
```

**After:**
```python
from infrastructure.cache import cached

@cached(prefix="calculation", ttl=3600)
def expensive_calculation():
    # ...
```

### Pattern 3: Error Handling

**Before:**
```python
try:
    result = do_something()
except Exception as e:
    st.error(str(e))
```

**After:**
```python
from core.exceptions import BusinessLogicError
from core.logging import get_logger

logger = get_logger(__name__)

try:
    result = do_something()
except BusinessLogicError as e:
    logger.error(f"Business logic error: {e}", extra=e.details)
    st.error(e.message)
except Exception as e:
    logger.exception("Unexpected error")
    st.error("An unexpected error occurred")
```

## Backward Compatibility

The new architecture is designed to work alongside existing code:

1. **Gradual Migration**: Migrate one component at a time
2. **Adapter Pattern**: Create adapters for legacy code
3. **Dual Support**: Support both old and new patterns during transition

## Getting Help

- See `ARCHITECTURE.md` for detailed architecture documentation
- Check examples in `application/services/` (when created)
- Review domain models in `domain/entities.py`

## Next Steps

1. **Start Small**: Migrate one page or utility at a time
2. **Test Thoroughly**: Write tests for migrated code
3. **Document Changes**: Update documentation as you migrate
4. **Get Feedback**: Review with team before full migration

