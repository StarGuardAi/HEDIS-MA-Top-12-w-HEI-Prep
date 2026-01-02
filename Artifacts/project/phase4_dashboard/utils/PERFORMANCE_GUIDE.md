# Performance Optimization Guide

## Overview

Comprehensive performance optimization system for HEDIS Portfolio Optimizer with caching, monitoring, and lazy loading strategies.

## Quick Start

```python
from utils.performance import (
    load_member_data,
    calculate_member_priorities,
    filter_data,
    performance_monitor,
    lazy_load_section,
    Benchmark
)

# Load data (cached for 1 hour)
df = load_member_data()

# Calculate priorities (cached)
df = calculate_member_priorities(df)

# Filter (cached)
filtered = filter_data(df, {'measures': ['HbA1c Testing']})
```

## Caching Strategies

### 1. Data Caching

**Use `@st.cache_data` for:**
- DataFrames
- Lists
- Dictionaries
- Any serializable data

**TTL (Time To Live) Guidelines:**
- Frequently changing: 300-900 seconds (5-15 minutes)
- Moderately changing: 1800-3600 seconds (30-60 minutes)
- Rarely changing: 7200+ seconds (2+ hours)

**Example:**
```python
@st.cache_data(ttl=3600)  # 1 hour
def load_member_data():
    # Expensive data loading
    return df
```

### 2. Resource Caching

**Use `@st.cache_resource` for:**
- ML models
- Database connections
- File handles
- Non-serializable objects

**Example:**
```python
@st.cache_resource
def load_ml_model():
    import joblib
    return joblib.load('model.pkl')
```

### 3. Function Result Caching

**Cache expensive calculations:**
```python
@st.cache_data
def calculate_priorities(df, weights):
    # Complex calculation
    return result
```

## Performance Monitoring

### Using the Decorator

```python
from utils.performance import performance_monitor

@performance_monitor
def my_expensive_function():
    # Your code
    pass
```

### Viewing Performance Metrics

```python
from utils.performance import render_performance_dashboard

render_performance_dashboard()
```

### Manual Benchmarking

```python
from utils.performance import Benchmark, benchmark_function

# Context manager
with Benchmark("data_loading"):
    df = load_member_data()

# Function wrapper
result, duration = benchmark_function(load_member_data)
st.write(f"Took {duration:.3f}s")
```

## Lazy Loading

### Lazy Load Sections

```python
from utils.performance import lazy_load_section

def load_heavy_chart():
    # Expensive chart generation
    return fig

fig = lazy_load_section('chart', load_heavy_chart, "Loading chart...")
st.plotly_chart(fig)
```

### Conditional Rendering

```python
from utils.performance import conditional_render

if st.checkbox("Show detailed analysis"):
    conditional_render(
        True,
        lambda: render_expensive_analysis(),
        "Check box to load analysis"
    )
```

## Query Optimization

### Filter Caching

```python
from utils.performance import filter_data

filters = {
    'measures': ['HbA1c Testing'],
    'min_value': 1000,
    'status': ['Open', 'Pending']
}

filtered_df = filter_data(df, filters)  # Cached
```

### Aggregation Caching

```python
from utils.performance import aggregate_by_measure

summary = aggregate_by_measure(df)  # Cached
```

## Mobile Optimizations

### Lightweight Summary

```python
from utils.performance import get_mobile_summary_data

summary = get_mobile_summary_data()  # Cached, lightweight
```

### Top N Caching

```python
from utils.performance import get_top_opportunities

top_5 = get_top_opportunities(df, top_n=5)  # Cached
```

## Cache Management

### Clear All Caches

```python
from utils.performance import clear_all_caches

if st.button("Clear Cache"):
    clear_all_caches()
```

### Clear Specific Caches

```python
from utils.performance import clear_data_cache, clear_resource_cache

clear_data_cache()  # Clear data only
clear_resource_cache()  # Clear resources only
```

### Cache Information

```python
from utils.performance import get_cache_info

info = get_cache_info()
st.json(info)
```

## Best Practices

### 1. Use Appropriate TTL

```python
# ✅ Good: Appropriate TTL
@st.cache_data(ttl=3600)  # 1 hour for member data
def load_member_data():
    pass

# ❌ Bad: Too short or too long
@st.cache_data(ttl=60)  # Too short - cache invalidates too often
@st.cache_data(ttl=86400)  # Too long - stale data
```

### 2. Cache at Right Level

```python
# ✅ Good: Cache at data loading level
@st.cache_data
def load_data():
    return expensive_operation()

# ❌ Bad: Cache at UI level
@st.cache_data
def render_chart():  # Don't cache UI rendering
    return fig
```

### 3. Use Lazy Loading for Heavy Sections

```python
# ✅ Good: Lazy load expensive sections
if st.checkbox("Show analysis"):
    analysis = lazy_load_section('analysis', load_analysis)

# ❌ Bad: Load everything upfront
analysis = load_analysis()  # Always loads, even if not needed
```

### 4. Monitor Performance

```python
# ✅ Good: Monitor expensive operations
@performance_monitor
def expensive_calculation():
    pass

# ❌ Bad: No monitoring
def expensive_calculation():  # Can't track performance
    pass
```

### 5. Optimize DataFrames

```python
# ✅ Good: Optimize memory
df = optimize_dataframe(df)

# ❌ Bad: Keep large DataFrames
df = load_data()  # May use more memory than needed
```

## Performance Targets

### Desktop

- Initial load: < 2 seconds
- Navigation: < 0.5 seconds
- Chart render: < 1 second
- Filter apply: < 0.5 seconds

### Mobile

- Initial load: < 3 seconds
- Navigation: < 0.3 seconds
- Chart render: < 0.5 seconds
- Filter apply: < 0.3 seconds

## Troubleshooting

### Cache Not Working

- Check function parameters are hashable
- Verify TTL hasn't expired
- Ensure no uncacheable objects in parameters

### Slow Performance

- Check performance log for bottlenecks
- Use lazy loading for heavy sections
- Optimize DataFrame memory usage
- Consider reducing data size

### Memory Issues

- Use `optimize_dataframe()` to reduce memory
- Clear caches periodically
- Limit data loaded at once
- Use pagination for large datasets

## Examples

See `performance.py` for complete examples and integration patterns.

---

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Performance System** | Caching | Monitoring | Optimization ⚡

