# Performance Monitoring - Quick Start

## 🚀 Quick Setup

### 1. Access Performance Dashboard
Navigate to **⚡ Performance Dashboard** in the sidebar

### 2. Enable Monitoring
Add decorators to your functions:

```python
from utils.performance_monitor import track_performance
from utils.performance_helpers import cached_with_tracking

@track_performance("my_function")
def my_function():
    # Your code
    pass

@cached_with_tracking(ttl=3600)
def fetch_data():
    return execute_query(query)
```

### 3. View Metrics
Check the Performance Dashboard for:
- Real-time metrics
- Benchmark comparisons
- Cache performance
- Memory usage

## 📊 Target Metrics

### Desktop
- Initial Load: < 3s
- Chart Render: < 1s
- Filter Apply: < 500ms
- Export: < 2s

### Mobile
- Initial Load: < 2s
- Chart Render: < 1s
- Touch Response: < 100ms

### Optimization
- Cache Hit Rate: > 90%
- Data Fetch: < 1s
- Re-render: < 300ms

## 🛠️ Common Decorators

```python
# Track execution time
@track_performance("function_name")

# Cache with tracking
@cached_with_tracking(ttl=3600)

# Track render time
@track_render_time("component")

# Track filter time
@track_filter_time()

# Track export time
@track_export_time()

# Use fragments
@use_fragment
```

## 📈 View Dashboard

1. Open sidebar
2. Click "⚡ Performance Dashboard"
3. View metrics and benchmarks
4. Export data if needed

## 🎯 Optimization Tips

1. **Cache Everything**: Use `@st.cache_data` for queries
2. **Optimize DataFrames**: Use `optimize_dataframe()`
3. **Use Fragments**: Reduce full page re-renders
4. **Monitor Regularly**: Check dashboard frequently

## 📚 More Information

See `PERFORMANCE_BENCHMARKS.md` for:
- Detailed benchmarks
- Optimization strategies
- Troubleshooting guide
- Best practices

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Ready to monitor?** Open the Performance Dashboard!

