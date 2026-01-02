# Performance Benchmarks and Monitoring Guide

## Overview

Comprehensive performance monitoring and benchmarking system for HEDIS Portfolio Optimizer with real-time metrics tracking and optimization targets.

## Target Metrics

### Desktop Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| Initial Load | < 3 seconds | Time from navigation to first content |
| Time to Interactive | < 5 seconds | Time until page is fully interactive |
| Chart Render | < 1 second | Time to render Plotly charts |
| Filter Apply | < 500ms | Time to apply filters and update data |
| Export Generation | < 2 seconds | Time to generate CSV/Excel exports |

### Mobile Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| Initial Load | < 2 seconds | 4G network conditions |
| Time to Interactive | < 3 seconds | Time until page is fully interactive |
| Chart Render | < 1 second | Time to render charts on mobile |
| Scroll Performance | 60 FPS | Smooth scrolling without jank |
| Touch Response | < 100ms | Time from touch to visual feedback |

### Optimization Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cache Hit Rate | > 90% | Percentage of cache hits vs misses |
| Bundle Size | < 5 MB | Total app bundle size |
| Data Fetch Time | < 1 second | Time to fetch data from database |
| Re-render Time | < 300ms | Time to re-render components |

## Monitoring Setup

### Automatic Tracking

The performance monitor automatically tracks:

1. **Function Execution Times**: Functions decorated with `@track_performance`
2. **Cache Performance**: Cache hits and misses
3. **Memory Usage**: Current and peak memory consumption
4. **Session State Size**: Size of Streamlit session state
5. **Data Processing**: Fetch, render, filter, and export times

### Using Performance Decorators

```python
from utils.performance_monitor import track_performance
from utils.performance_helpers import (
    cached_with_tracking,
    track_render_time,
    track_filter_time,
    track_export_time
)

# Track function execution
@track_performance("chart_render")
def render_chart():
    st.plotly_chart(fig)

# Cache with tracking
@cached_with_tracking(ttl=3600)
def fetch_data():
    return execute_query(query)

# Track render time
@track_render_time("chart")
def update_chart():
    st.plotly_chart(fig)

# Track filter time
@track_filter_time()
def apply_filters(data, filters):
    return data[data['measure'].isin(filters)]

# Track export time
@track_export_time()
def export_to_csv(data):
    return data.to_csv()
```

### Streamlit Fragments

Use fragments for granular updates to reduce re-rendering:

```python
from utils.performance_helpers import use_fragment

@use_fragment
def update_chart():
    st.plotly_chart(fig)
```

### Manual Tracking

```python
from utils.performance_helpers import log_performance_metric

# Log custom metric
log_performance_metric("custom_operation", 0.5, "seconds")
```

## Performance Dashboard

Access the Performance Dashboard from the sidebar:
**⚡ Performance Dashboard**

The dashboard shows:

1. **Performance Overview**: Cache hit rate, memory usage, session state size
2. **Desktop Benchmarks**: Real-time comparison against targets
3. **Mobile Benchmarks**: Mobile-specific targets
4. **Optimization Targets**: Cache, data fetch, re-render metrics
5. **Detailed Metrics**: Function timings, cache performance, memory trends
6. **Benchmark Status**: Pass/fail summary

## Tools

### Chrome DevTools Performance Tab

1. Open Chrome DevTools (F12)
2. Go to Performance tab
3. Click Record
4. Interact with dashboard
5. Stop recording
6. Analyze performance timeline

**Key Metrics to Check**:
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- Total Blocking Time (TBT)
- Cumulative Layout Shift (CLS)

### Streamlit Built-in Profiler

Streamlit includes built-in performance profiling:

```python
# Enable profiling
streamlit run app.py --server.profiler true
```

### Custom Performance Decorators

Use the provided decorators for automatic tracking:

- `@track_performance`: Track function execution time
- `@cached_with_tracking`: Cache with performance tracking
- `@track_render_time`: Track component render time
- `@track_filter_time`: Track filter application time
- `@track_export_time`: Track export generation time

## Optimization Strategies

### 1. Caching

**Goal**: Achieve >90% cache hit rate

```python
# Use Streamlit caching
@st.cache_data(ttl=3600)
def fetch_data():
    return execute_query(query)

# Use cached_with_tracking for monitoring
@cached_with_tracking(ttl=3600)
def expensive_computation(param):
    return compute(param)
```

**Best Practices**:
- Cache database queries
- Cache expensive computations
- Set appropriate TTL values
- Use `max_entries` to limit cache size

### 2. Data Optimization

**Goal**: Reduce data fetch time to <1s

```python
from utils.performance_helpers import optimize_dataframe

# Optimize DataFrame
df = optimize_dataframe(df, optimize_types=True, optimize_memory=True)
```

**Best Practices**:
- Use database indexes
- Limit query result sets
- Optimize DataFrame dtypes
- Use pagination for large datasets

### 3. Render Optimization

**Goal**: Reduce re-render time to <300ms

```python
# Use fragments for granular updates
@use_fragment
def update_chart():
    st.plotly_chart(fig)

# Track render time
@track_render_time("chart")
def render_chart():
    st.plotly_chart(fig)
```

**Best Practices**:
- Use `st.experimental_fragment` for isolated updates
- Minimize full page re-renders
- Cache chart configurations
- Use lazy loading for heavy components

### 4. Memory Management

**Goal**: Keep memory usage reasonable

```python
# Clear session state when not needed
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.session_state.clear()
```

**Best Practices**:
- Clear unused session state
- Limit cache size with `max_entries`
- Use generators for large datasets
- Monitor memory usage in dashboard

## Performance Testing

### Load Time Testing

1. Open Chrome DevTools
2. Go to Network tab
3. Enable throttling (4G for mobile)
4. Reload page
5. Check load time

### Chart Render Testing

```python
@track_performance("chart_render")
def test_chart_render():
    start = time.perf_counter()
    st.plotly_chart(fig)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Chart render took {elapsed:.2f}s"
```

### Filter Performance Testing

```python
@track_filter_time()
def test_filter_performance():
    filtered = apply_filters(data, filters)
    # Should complete in <500ms
```

## Benchmarking Workflow

1. **Baseline Measurement**: Measure current performance
2. **Set Targets**: Define benchmark targets
3. **Optimize**: Apply optimization strategies
4. **Re-measure**: Check improvement
5. **Iterate**: Continue optimizing

## Performance Dashboard Usage

### Viewing Metrics

1. Navigate to **⚡ Performance Dashboard**
2. View real-time metrics
3. Check benchmark status
4. Review detailed metrics

### Exporting Data

1. Click "Export Performance Data"
2. Download JSON file
3. Analyze in external tools

### Resetting Metrics

1. Click "Reset Metrics" in sidebar
2. Start fresh measurement
3. Continue monitoring

## Troubleshooting

### High Memory Usage

- Check session state size
- Clear unused caches
- Optimize DataFrame memory
- Limit data size

### Slow Chart Rendering

- Reduce data points
- Simplify chart configuration
- Use chart caching
- Check Plotly version

### Low Cache Hit Rate

- Increase cache TTL
- Review cache keys
- Check cache invalidation
- Optimize cache strategy

### Slow Data Fetching

- Optimize database queries
- Add indexes
- Use connection pooling
- Consider data pre-aggregation

## Best Practices

1. **Monitor Regularly**: Check performance dashboard frequently
2. **Set Alerts**: Monitor for performance degradation
3. **Profile Before Optimizing**: Identify actual bottlenecks
4. **Test on Real Devices**: Use BrowserStack for mobile testing
5. **Document Changes**: Track performance impact of changes

## Next Steps

1. **Enable Monitoring**: Start using performance decorators
2. **Set Baselines**: Measure current performance
3. **Optimize**: Apply optimization strategies
4. **Monitor**: Track improvements in dashboard
5. **Iterate**: Continue optimizing

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Performance Benchmarks** | Real-time monitoring | Optimization targets

