"""
Hierarchical Context Builder for HEDIS Analytics
Implements 3-layer context architecture with intelligent caching
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import hashlib

@dataclass
class ContextLayer:
    """Represents a single layer in hierarchical context"""
    name: str
    data: Dict[str, Any]
    size_bytes: int
    last_updated: datetime
    ttl_seconds: int
    relevance_score: float

class HierarchicalContextBuilder:
    """
    Build context in 3 hierarchical layers:
    Layer 1: Domain Knowledge (HEDIS specs, cached 1 hour)
    Layer 2: Measure-Specific (measure specs, cached 5 min)
    Layer 3: Query-Specific (fresh data, cached 30 sec)
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "size_bytes": 0
        }
    
    def build_context(
        self, 
        query: str, 
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        Build hierarchical context for query.
        
        Returns:
            {
                "layer_1_domain": {...},
                "layer_2_measure": {...},
                "layer_3_query": {...},
                "metadata": {
                    "total_size": int,
                    "cache_hits": int,
                    "efficiency_score": float
                }
            }
        """
        context = {}
        
        # Layer 1: Domain Knowledge (check cache first)
        layer_1 = self._get_or_build_layer_1()
        context["layer_1_domain"] = layer_1.data
        
        # Layer 2: Measure-Specific (check cache, filter by query)
        measures = self._extract_measures_from_query(query)
        layer_2 = self._get_or_build_layer_2(measures)
        context["layer_2_measure"] = layer_2.data
        
        # Layer 3: Query-Specific (always fresh)
        layer_3 = self._build_layer_3(query)
        context["layer_3_query"] = layer_3.data
        
        # Calculate metadata
        context["metadata"] = {
            "total_size": layer_1.size_bytes + layer_2.size_bytes + layer_3.size_bytes,
            "cache_hits": sum(1 for l in [layer_1, layer_2] if self._is_cached(l)),
            "efficiency_score": self._calculate_efficiency(layer_1, layer_2, layer_3),
            "layers_cached": [l.name for l in [layer_1, layer_2] if self._is_cached(l)]
        }
        
        return context
    
    def _get_or_build_layer_1(self) -> ContextLayer:
        """Layer 1: Domain Knowledge - HEDIS specs, guidelines"""
        cache_key = "layer_1_domain"
        
        if self._is_cache_valid(cache_key, ttl_seconds=3600):  # 1 hour TTL
            self.cache_stats["hits"] += 1
            return self.cache[cache_key]
        
        self.cache_stats["misses"] += 1
        
        # Build layer 1 data
        data = {
            "hedis_overview": self._load_hedis_overview(),
            "clinical_guidelines": self._load_clinical_guidelines(),
            "terminology": self._load_terminology(),
            "regulatory_requirements": self._load_regulatory_requirements()
        }
        
        layer = ContextLayer(
            name="Domain Knowledge",
            data=data,
            size_bytes=len(json.dumps(data)),
            last_updated=datetime.now(),
            ttl_seconds=3600,
            relevance_score=1.0
        )
        
        self.cache[cache_key] = layer
        return layer
    
    def _get_or_build_layer_2(self, measures: List[str]) -> ContextLayer:
        """Layer 2: Measure-Specific Context"""
        cache_key = f"layer_2_measures_{'_'.join(sorted(measures))}"
        
        if self._is_cache_valid(cache_key, ttl_seconds=300):  # 5 min TTL
            self.cache_stats["hits"] += 1
            return self.cache[cache_key]
        
        self.cache_stats["misses"] += 1
        
        # Build layer 2 data
        data = {}
        for measure_id in measures:
            data[measure_id] = {
                "spec": self._load_measure_spec(measure_id),
                "performance": self._load_measure_performance(measure_id),
                "roi_data": self._load_measure_roi(measure_id)
            }
        
        layer = ContextLayer(
            name="Measure-Specific",
            data=data,
            size_bytes=len(json.dumps(data)),
            last_updated=datetime.now(),
            ttl_seconds=300,
            relevance_score=0.9
        )
        
        self.cache[cache_key] = layer
        return layer
    
    def _build_layer_3(self, query: str) -> ContextLayer:
        """Layer 3: Query-Specific (always fresh)"""
        # This is always built fresh, never cached
        data = {
            "query_intent": self._parse_query_intent(query),
            "relevant_data": {},  # Populated by tools
            "calculations": {}    # Populated by calculations
        }
        
        layer = ContextLayer(
            name="Query-Specific",
            data=data,
            size_bytes=len(json.dumps(data)),
            last_updated=datetime.now(),
            ttl_seconds=30,
            relevance_score=1.0
        )
        
        return layer
    
    def _is_cache_valid(self, key: str, ttl_seconds: int) -> bool:
        """Check if cache entry exists and is still valid"""
        if key not in self.cache:
            return False
        
        layer = self.cache[key]
        age_seconds = (datetime.now() - layer.last_updated).total_seconds()
        
        return age_seconds < ttl_seconds
    
    def _is_cached(self, layer: ContextLayer) -> bool:
        """Check if layer came from cache"""
        for cached_layer in self.cache.values():
            if cached_layer.name == layer.name and cached_layer.last_updated == layer.last_updated:
                # Check if it's not too fresh (was actually cached)
                age_seconds = (datetime.now() - layer.last_updated).total_seconds()
                return age_seconds > 1  # More than 1 second old = was cached
        return False
    
    def _calculate_efficiency(self, l1: ContextLayer, l2: ContextLayer, l3: ContextLayer) -> float:
        """Calculate context efficiency score (0-100)"""
        # Higher score = more cache hits, less fresh data needed
        cache_hit_weight = 0.6
        size_efficiency_weight = 0.4
        
        # Cache hit score
        layers = [l1, l2]
        cache_hits = sum(1 for l in layers if self._is_cached(l))
        cache_hit_score = (cache_hits / len(layers)) * 100
        
        # Size efficiency (smaller = better)
        total_size = l1.size_bytes + l2.size_bytes + l3.size_bytes
        max_expected_size = 500000  # 500KB
        size_score = max(0, (1 - total_size / max_expected_size)) * 100
        
        efficiency = (cache_hit_weight * cache_hit_score) + (size_efficiency_weight * size_score)
        return round(efficiency, 1)
    
    def _extract_measures_from_query(self, query: str) -> List[str]:
        """Extract HEDIS measure IDs from query"""
        measures = []
        query_upper = query.upper()
        
        # Common HEDIS measures
        measure_patterns = ["CDC", "EED", "GSD", "HBD", "KED", "CBP", "BPD", "COL", "SPC"]
        
        for measure in measure_patterns:
            if measure in query_upper:
                measures.append(measure)
        
        # Default to CDC if no measures found
        if not measures:
            measures = ["CDC"]
        
        return list(set(measures))
    
    def _parse_query_intent(self, query: str) -> Dict[str, Any]:
        """Parse query to understand intent"""
        query_lower = query.lower()
        
        return {
            "needs_calculation": any(kw in query_lower for kw in ["roi", "calculate", "compute"]),
            "needs_data": any(kw in query_lower for kw in ["member", "gap", "performance"]),
            "needs_validation": any(kw in query_lower for kw in ["validate", "compliance", "hedis"]),
            "measure_specific": len(self._extract_measures_from_query(query)) > 0
        }
    
    # Placeholder methods - integrate with your actual data sources
    def _load_hedis_overview(self) -> str:
        return "HEDIS (Healthcare Effectiveness Data and Information Set) measures..."
    
    def _load_clinical_guidelines(self) -> str:
        return "Clinical guidelines for diabetes care..."
    
    def _load_terminology(self) -> Dict[str, str]:
        return {
            "HEDIS": "Healthcare Effectiveness Data and Information Set",
            "Star Rating": "CMS quality rating system (1-5 stars)",
            "Gap-in-Care": "Member missing required preventive service"
        }
    
    def _load_regulatory_requirements(self) -> str:
        return "HIPAA compliance requirements..."
    
    def _load_measure_spec(self, measure_id: str) -> Dict[str, Any]:
        return {"measure_id": measure_id, "spec": "Placeholder spec"}
    
    def _load_measure_performance(self, measure_id: str) -> Dict[str, Any]:
        return {"current_rate": 0.75, "target_rate": 0.82}
    
    def _load_measure_roi(self, measure_id: str) -> Dict[str, Any]:
        return {"roi_ratio": 2.8, "confidence": 0.94}

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_hits": self.cache_stats["hits"],
            "cache_misses": self.cache_stats["misses"],
            "hit_rate": round(hit_rate, 1),
            "total_size_bytes": sum(layer.size_bytes for layer in self.cache.values()),
            "cached_layers": len(self.cache)
        }



