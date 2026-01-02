"""
Performance Monitoring and Benchmarking
Tracks performance metrics, cache hit rates, and optimization targets
"""
import time
import functools
import sys
import tracemalloc
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from collections import defaultdict
import streamlit as st


class PerformanceMonitor:
    """
    Performance monitoring system for HEDIS Portfolio Optimizer.
    Tracks timing, cache performance, memory usage, and optimization metrics.
    """
    
    def __init__(self):
        self.metrics = {
            "timings": defaultdict(list),
            "cache_hits": 0,
            "cache_misses": 0,
            "memory_snapshots": [],
            "session_state_size": 0,
            "data_fetch_times": [],
            "render_times": [],
            "filter_times": [],
            "export_times": []
        }
        self.benchmarks = {
            "desktop": {
                "initial_load": 3.0,  # seconds
                "time_to_interactive": 5.0,
                "chart_render": 1.0,
                "filter_apply": 0.5,
                "export_generation": 2.0
            },
            "mobile": {
                "initial_load": 2.0,
                "time_to_interactive": 3.0,
                "chart_render": 1.0,
                "scroll_fps": 60.0,
                "touch_response": 0.1
            },
            "optimization": {
                "cache_hit_rate": 0.90,  # 90%
                "bundle_size_mb": 5.0,
                "data_fetch_time": 1.0,
                "rerender_time": 0.3
            }
        }
        self.tracemalloc_started = False
    
    def start_tracing(self):
        """Start memory tracing."""
        if not self.tracemalloc_started:
            tracemalloc.start()
            self.tracemalloc_started = True
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage in MB."""
        if not self.tracemalloc_started:
            # Try to use psutil if available, otherwise return baseline
            try:
                import psutil
                import os
                process = psutil.Process(os.getpid())
                mem_info = process.memory_info()
                return {
                    "current_mb": mem_info.rss / 1024 / 1024,
                    "peak_mb": mem_info.rss / 1024 / 1024
                }
            except ImportError:
                # psutil not available, return baseline estimate
                return {"current_mb": 50.0, "peak_mb": 50.0}
            except:
                # Other error, return baseline
                return {"current_mb": 50.0, "peak_mb": 50.0}
        
        current, peak = tracemalloc.get_traced_memory()
        return {
            "current_mb": current / 1024 / 1024,
            "peak_mb": peak / 1024 / 1024
        }
    
    def time_function(self, func_name: str = None):
        """
        Decorator to time function execution.
        
        Usage:
            @monitor.time_function("my_function")
            def my_function():
                ...
        """
        def decorator(func: Callable) -> Callable:
            name = func_name or func.__name__
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed = time.perf_counter() - start_time
                    self.metrics["timings"][name].append(elapsed)
                    # Log if exceeds benchmark
                    if name in ["chart_render", "filter_apply", "export_generation"]:
                        benchmark = self.benchmarks["desktop"].get(name, float('inf'))
                        if elapsed > benchmark:
                            self._log_performance_issue(name, elapsed, benchmark)
            return wrapper
        return decorator
    
    def track_cache(self, cache_key: str, hit: bool):
        """Track cache hit/miss."""
        if hit:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
    
    def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        if total == 0:
            return 0.0
        return self.metrics["cache_hits"] / total
    
    def track_data_fetch(self, duration: float):
        """Track data fetch time."""
        self.metrics["data_fetch_times"].append(duration)
    
    def track_render(self, duration: float):
        """Track render time."""
        self.metrics["render_times"].append(duration)
    
    def track_filter(self, duration: float):
        """Track filter application time."""
        self.metrics["filter_times"].append(duration)
    
    def track_export(self, duration: float):
        """Track export generation time."""
        self.metrics["export_times"].append(duration)
    
    def get_session_state_size(self) -> int:
        """Estimate session state size."""
        if hasattr(st, 'session_state'):
            # Rough estimate of session state size
            size = 0
            try:
                for key, value in st.session_state.items():
                    try:
                        # Get size of the value
                        if isinstance(value, (str, bytes)):
                            size += sys.getsizeof(value)
                        elif isinstance(value, (list, dict, tuple)):
                            size += sys.getsizeof(value)
                            # Try to get size of items
                            try:
                                size += sum(sys.getsizeof(str(item)) for item in (value if isinstance(value, list) else value.values() if isinstance(value, dict) else value))
                            except:
                                pass
                        else:
                            size += sys.getsizeof(str(value))
                    except:
                        # If we can't get size, estimate based on string representation
                        try:
                            size += len(str(value)) * 2  # Rough estimate: 2 bytes per char
                        except:
                            pass
            except:
                # Fallback estimate
                size = 10000  # ~10KB baseline
            self.metrics["session_state_size"] = size
            return size
        return 0
    
    def get_performance_summary(self) -> Dict:
        """Get comprehensive performance summary."""
        cache_hit_rate = self.get_cache_hit_rate()
        memory = self.get_memory_usage()
        session_size = self.get_session_state_size()
        
        # Calculate averages
        avg_timings = {}
        for func_name, times in self.metrics["timings"].items():
            if times:
                avg_timings[func_name] = {
                    "avg": sum(times) / len(times),
                    "min": min(times),
                    "max": max(times),
                    "count": len(times)
                }
        
        avg_data_fetch = sum(self.metrics["data_fetch_times"]) / len(self.metrics["data_fetch_times"]) if self.metrics["data_fetch_times"] else 0
        avg_render = sum(self.metrics["render_times"]) / len(self.metrics["render_times"]) if self.metrics["render_times"] else 0
        avg_filter = sum(self.metrics["filter_times"]) / len(self.metrics["filter_times"]) if self.metrics["filter_times"] else 0
        avg_export = sum(self.metrics["export_times"]) / len(self.metrics["export_times"]) if self.metrics["export_times"] else 0
        
        return {
            "cache_hit_rate": cache_hit_rate,
            "cache_hits": self.metrics["cache_hits"],
            "cache_misses": self.metrics["cache_misses"],
            "memory_current_mb": memory["current_mb"],
            "memory_peak_mb": memory["peak_mb"],
            "session_state_size_kb": session_size / 1024,
            "function_timings": avg_timings,
            "avg_data_fetch": avg_data_fetch,
            "avg_render": avg_render,
            "avg_filter": avg_filter,
            "avg_export": avg_export,
            "benchmarks": self.benchmarks
        }
    
    def check_benchmarks(self) -> Dict[str, Dict]:
        """Check current performance against benchmarks."""
        summary = self.get_performance_summary()
        results = {
            "desktop": {},
            "mobile": {},
            "optimization": {}
        }
        
        # Desktop benchmarks
        desktop_benchmarks = self.benchmarks["desktop"]
        if "chart_render" in summary["function_timings"]:
            actual = summary["function_timings"]["chart_render"]["avg"]
            target = desktop_benchmarks["chart_render"]
            results["desktop"]["chart_render"] = {
                "actual": actual,
                "target": target,
                "status": "pass" if actual <= target else "fail",
                "variance": actual - target
            }
        
        if summary["avg_filter"] > 0:
            results["desktop"]["filter_apply"] = {
                "actual": summary["avg_filter"],
                "target": desktop_benchmarks["filter_apply"],
                "status": "pass" if summary["avg_filter"] <= desktop_benchmarks["filter_apply"] else "fail",
                "variance": summary["avg_filter"] - desktop_benchmarks["filter_apply"]
            }
        
        if summary["avg_export"] > 0:
            results["desktop"]["export_generation"] = {
                "actual": summary["avg_export"],
                "target": desktop_benchmarks["export_generation"],
                "status": "pass" if summary["avg_export"] <= desktop_benchmarks["export_generation"] else "fail",
                "variance": summary["avg_export"] - desktop_benchmarks["export_generation"]
            }
        
        # Optimization benchmarks
        opt_benchmarks = self.benchmarks["optimization"]
        results["optimization"]["cache_hit_rate"] = {
            "actual": summary["cache_hit_rate"],
            "target": opt_benchmarks["cache_hit_rate"],
            "status": "pass" if summary["cache_hit_rate"] >= opt_benchmarks["cache_hit_rate"] else "fail",
            "variance": summary["cache_hit_rate"] - opt_benchmarks["cache_hit_rate"]
        }
        
        if summary["avg_data_fetch"] > 0:
            results["optimization"]["data_fetch_time"] = {
                "actual": summary["avg_data_fetch"],
                "target": opt_benchmarks["data_fetch_time"],
                "status": "pass" if summary["avg_data_fetch"] <= opt_benchmarks["data_fetch_time"] else "fail",
                "variance": summary["avg_data_fetch"] - opt_benchmarks["data_fetch_time"]
            }
        
        if summary["avg_render"] > 0:
            results["optimization"]["rerender_time"] = {
                "actual": summary["avg_render"],
                "target": opt_benchmarks["rerender_time"],
                "status": "pass" if summary["avg_render"] <= opt_benchmarks["rerender_time"] else "fail",
                "variance": summary["avg_render"] - opt_benchmarks["rerender_time"]
            }
        
        return results
    
    def _log_performance_issue(self, metric: str, actual: float, target: float):
        """Log performance issues (could be extended to send alerts)."""
        # In production, this could send to logging system or alerting
        pass
    
    def reset_metrics(self):
        """Reset all metrics (useful for testing)."""
        self.metrics = {
            "timings": defaultdict(list),
            "cache_hits": 0,
            "cache_misses": 0,
            "memory_snapshots": [],
            "session_state_size": 0,
            "data_fetch_times": [],
            "render_times": [],
            "filter_times": [],
            "export_times": []
        }
    
    def export_metrics(self) -> Dict:
        """Export all metrics for analysis."""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": dict(self.metrics),
            "summary": self.get_performance_summary(),
            "benchmarks": self.check_benchmarks()
        }


# Global performance monitor instance
_performance_monitor = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get or create global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
        _performance_monitor.start_tracing()
    return _performance_monitor


def track_performance(metric_name: str):
    """
    Decorator to track function performance.
    
    Usage:
        @track_performance("chart_render")
        def render_chart():
            ...
    """
    monitor = get_performance_monitor()
    return monitor.time_function(metric_name)

