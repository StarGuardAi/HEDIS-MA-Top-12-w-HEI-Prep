#!/usr/bin/env python3
"""
Phase 2 Chats 1 & 2: Comprehensive Test Suite
Tests member engagement tracking and provider network analytics.

Author: Robert Reichert
Created: 2025-11-18
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


class Phase2TestSuite:
    """Comprehensive test suite for Phase 2 Chats 1 and 2."""
    
    def __init__(self, db_config: Dict[str, str]):
        """Initialize test suite with database configuration."""
        self.db_config = db_config
        self.conn = None
        self.test_results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            return True
        except psycopg2.Error as e:
            print(f"[FAIL] Database connection failed: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def log_test(self, test_name: str, passed: bool, message: str = "", warning: bool = False):
        """Log test result."""
        status = "[PASS]" if passed else ("[WARN]" if warning else "[FAIL]")
        self.test_results.append((test_name, passed, message, warning))
        if passed:
            self.passed += 1
        elif warning:
            self.warnings += 1
        else:
            self.failed += 1
        print(f"  {status} {test_name}")
        if message:
            print(f"      {message}")
    
    def test_table_exists(self, table_name: str) -> bool:
        """Test if a table exists."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (table_name,))
                return cur.fetchone()[0]
        except psycopg2.Error:
            return False
    
    def test_view_exists(self, view_name: str) -> bool:
        """Test if a view exists."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.views 
                        WHERE table_name = %s
                    );
                """, (view_name,))
                return cur.fetchone()[0]
        except psycopg2.Error:
            return False
    
    def test_row_count(self, table_name: str, min_count: int = 1, max_count: int = None) -> Tuple[bool, int]:
        """Test row count in a table."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cur.fetchone()[0]
                passed = count >= min_count and (max_count is None or count <= max_count)
                return passed, count
        except psycopg2.Error as e:
            return False, 0
    
    def run_phase2_chat1_tests(self):
        """Run tests for Phase 2 Chat 1 (Member Engagement)."""
        print("\n" + "=" * 80)
        print("PHASE 2 CHAT 1 TESTS: Member Engagement & Outreach Effectiveness")
        print("=" * 80)
        
        # Test 1: Required tables exist
        print("\n[TEST GROUP] Table Existence Checks")
        required_tables = [
            'member_engagement_scores',
            'member_contact_preferences',
            'outreach_campaigns',
            'member_outreach_contacts',
            'barrier_resolutions'
        ]
        
        for table in required_tables:
            exists = self.test_table_exists(table)
            self.log_test(
                f"Table exists: {table}",
                exists,
                "" if exists else f"Table {table} not found"
            )
        
        # Test 2: Data volume checks
        print("\n[TEST GROUP] Data Volume Validation")
        
        passed, count = self.test_row_count('member_engagement_scores', 9000, 11000)
        self.log_test(
            "Member engagement scores: 9K-11K records",
            passed,
            f"Found {count:,} records" if passed else f"Expected 9K-11K, found {count:,}"
        )
        
        passed, count = self.test_row_count('member_contact_preferences', 7000, 9000)
        self.log_test(
            "Contact preferences: 7K-9K records (80% coverage)",
            passed,
            f"Found {count:,} records ({count/10000*100:.1f}% coverage)" if passed else f"Expected 7K-9K, found {count:,}"
        )
        
        passed, count = self.test_row_count('outreach_campaigns', 10, 15)
        self.log_test(
            "Outreach campaigns: 10-15 campaigns",
            passed,
            f"Found {count} campaigns" if passed else f"Expected 10-15, found {count}"
        )
        
        passed, count = self.test_row_count('member_outreach_contacts', 5000, 15000)
        self.log_test(
            "Outreach contacts: 5K-15K records",
            passed,
            f"Found {count:,} contact records" if passed else f"Expected 5K-15K, found {count:,}"
        )
        
        # Test 3: Data integrity checks
        print("\n[TEST GROUP] Data Integrity Validation")
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check engagement score ranges
            cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN overall_engagement_score < 0 OR overall_engagement_score > 100 THEN 1 END) as invalid_scores
                FROM member_engagement_scores;
            """)
            result = cur.fetchone()
            passed = result['invalid_scores'] == 0
            self.log_test(
                "Engagement scores in valid range (0-100)",
                passed,
                f"{result['invalid_scores']} invalid scores found" if not passed else "All scores valid"
            )
            
            # Check engagement tier distribution
            cur.execute("""
                SELECT 
                    engagement_tier,
                    COUNT(*) as count
                FROM member_engagement_scores
                GROUP BY engagement_tier
                ORDER BY 
                    CASE engagement_tier
                        WHEN 'High' THEN 1
                        WHEN 'Medium' THEN 2
                        WHEN 'Low' THEN 3
                        ELSE 4
                    END;
            """)
            tiers = cur.fetchall()
            tier_names = [t['engagement_tier'] for t in tiers]
            tier_counts = {t['engagement_tier']: t['count'] for t in tiers}
            expected_tiers = ['High', 'Medium', 'Low', 'Very Low']
            all_present = all(tier in tier_names for tier in expected_tiers)
            # This is a warning, not a failure - random generation may not produce all tiers
            has_required = 'High' in tier_names and 'Medium' in tier_names and 'Low' in tier_names
            passed = has_required
            warning = not all_present and has_required
            tier_summary = ', '.join([f"{t}: {tier_counts.get(t, 0)}" for t in tier_names])
            self.log_test(
                "Engagement tiers properly distributed",
                passed,
                f"Found tiers: {tier_summary}",
                warning=warning
            )
            
            # Check contact method distribution
            cur.execute("""
                SELECT 
                    contact_method,
                    COUNT(*) as count
                FROM member_outreach_contacts
                GROUP BY contact_method
                ORDER BY count DESC;
            """)
            methods = cur.fetchall()
            passed = len(methods) >= 3
            self.log_test(
                "Multiple contact methods used",
                passed,
                f"Found {len(methods)} methods: {', '.join([m['contact_method'] for m in methods])}"
            )
        
        # Test 4: View functionality
        print("\n[TEST GROUP] View Functionality Tests")
        
        required_views = [
            'vw_member_engagement_summary',
            'vw_campaign_performance',
            'vw_contact_method_effectiveness',
            'vw_barrier_analysis'
        ]
        
        for view in required_views:
            exists = self.test_view_exists(view)
            if exists:
                # Try to query the view
                try:
                    with self.conn.cursor() as cur:
                        cur.execute(f"SELECT COUNT(*) FROM {view};")
                        count = cur.fetchone()[0]
                    self.log_test(
                        f"View accessible: {view}",
                        True,
                        f"Returns {count:,} rows"
                    )
                except psycopg2.Error as e:
                    self.log_test(
                        f"View accessible: {view}",
                        False,
                        f"Query failed: {str(e)[:100]}"
                    )
            else:
                self.log_test(
                    f"View exists: {view}",
                    False,
                    f"View {view} not found"
                )
        
        # Test 5: Key relationships
        print("\n[TEST GROUP] Relationship Integrity")
        
        with self.conn.cursor() as cur:
            # Check member engagement scores reference valid members
            cur.execute("""
                SELECT COUNT(*) as orphaned
                FROM member_engagement_scores mes
                LEFT JOIN plan_members pm ON mes.member_id = pm.member_id
                WHERE pm.member_id IS NULL;
            """)
            orphaned = cur.fetchone()[0]
            self.log_test(
                "Engagement scores reference valid members",
                orphaned == 0,
                f"{orphaned} orphaned records" if orphaned > 0 else "All references valid"
            )
            
            # Check outreach contacts reference valid campaigns
            cur.execute("""
                SELECT COUNT(*) as orphaned
                FROM member_outreach_contacts moc
                LEFT JOIN outreach_campaigns oc ON moc.campaign_id = oc.campaign_id
                WHERE moc.campaign_id IS NOT NULL AND oc.campaign_id IS NULL;
            """)
            orphaned = cur.fetchone()[0]
            self.log_test(
                "Outreach contacts reference valid campaigns",
                orphaned == 0,
                f"{orphaned} orphaned records" if orphaned > 0 else "All references valid"
            )
    
    def run_phase2_chat2_tests(self):
        """Run tests for Phase 2 Chat 2 (Provider Network)."""
        print("\n" + "=" * 80)
        print("PHASE 2 CHAT 2 TESTS: Provider Network Performance & Attribution")
        print("=" * 80)
        
        # Test 1: Required tables exist
        print("\n[TEST GROUP] Table Existence Checks")
        required_tables = [
            'provider_directory',
            'provider_performance',
            'member_provider_attribution',
            'provider_referrals',
            'provider_collaboration_scores',
            'network_adequacy_metrics'
        ]
        
        for table in required_tables:
            exists = self.test_table_exists(table)
            self.log_test(
                f"Table exists: {table}",
                exists,
                "" if exists else f"Table {table} not found"
            )
        
        # Test 2: Data volume checks
        print("\n[TEST GROUP] Data Volume Validation")
        
        passed, count = self.test_row_count('provider_directory', 450, 550)
        self.log_test(
            "Provider directory: 450-550 providers",
            passed,
            f"Found {count} providers" if passed else f"Expected 450-550, found {count}"
        )
        
        passed, count = self.test_row_count('member_provider_attribution', 12000, 15000)
        self.log_test(
            "Member-provider attributions: 12K-15K records",
            passed,
            f"Found {count:,} attributions" if passed else f"Expected 12K-15K, found {count:,}"
        )
        
        passed, count = self.test_row_count('provider_performance', 2000, 5000)
        self.log_test(
            "Provider performance records: 2K-5K records",
            passed,
            f"Found {count:,} performance records" if passed else f"Expected 2K-5K, found {count:,}"
        )
        
        passed, count = self.test_row_count('provider_collaboration_scores', 450, 550)
        self.log_test(
            "Collaboration scores: 450-550 records",
            passed,
            f"Found {count} scores" if passed else f"Expected 450-550, found {count}"
        )
        
        # Test 3: Attribution coverage
        print("\n[TEST GROUP] Attribution Coverage Validation")
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check PCP attribution coverage
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT pm.member_id) as total_members,
                    COUNT(DISTINCT mpa.member_id) as members_with_pcp
                FROM plan_members pm
                LEFT JOIN member_provider_attribution mpa 
                    ON pm.member_id = mpa.member_id 
                    AND mpa.attribution_type = 'PCP'
                    AND mpa.is_current = TRUE
                WHERE pm.member_id LIKE 'M%';
            """)
            result = cur.fetchone()
            pcp_coverage = (result['members_with_pcp'] / result['total_members'] * 100) if result['total_members'] > 0 else 0
            passed = pcp_coverage >= 95
            self.log_test(
                "PCP attribution coverage >= 95%",
                passed,
                f"{pcp_coverage:.1f}% coverage ({result['members_with_pcp']:,}/{result['total_members']:,})"
            )
            
            # Check specialist attribution
            cur.execute("""
                SELECT COUNT(DISTINCT member_id) as members_with_specialist
                FROM member_provider_attribution
                WHERE attribution_type = 'Specialist'
                  AND is_current = TRUE;
            """)
            specialist_count = cur.fetchone()['members_with_specialist']
            specialist_pct = (specialist_count / result['total_members'] * 100) if result['total_members'] > 0 else 0
            passed = 15 <= specialist_pct <= 40
            self.log_test(
                "Specialist attribution: 15-40% of members",
                passed,
                f"{specialist_pct:.1f}% coverage ({specialist_count:,} members)"
            )
        
        # Test 4: Provider type distribution
        print("\n[TEST GROUP] Provider Distribution Validation")
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    provider_type,
                    COUNT(*) as count
                FROM provider_directory
                WHERE network_status = 'Active'
                GROUP BY provider_type;
            """)
            types = cur.fetchall()
            pcp_count = next((t['count'] for t in types if t['provider_type'] == 'PCP'), 0)
            spec_count = next((t['count'] for t in types if t['provider_type'] == 'Specialist'), 0)
            
            passed = 200 <= pcp_count <= 300
            self.log_test(
                "PCP count: 200-300 providers",
                passed,
                f"Found {pcp_count} PCPs"
            )
            
            passed = 200 <= spec_count <= 300
            self.log_test(
                "Specialist count: 200-300 providers",
                passed,
                f"Found {spec_count} specialists"
            )
        
        # Test 5: Performance metrics integrity
        print("\n[TEST GROUP] Performance Metrics Validation")
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check performance rate ranges
            cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN performance_rate < 0 OR performance_rate > 100 THEN 1 END) as invalid_rates
                FROM provider_performance;
            """)
            result = cur.fetchone()
            passed = result['invalid_rates'] == 0
            self.log_test(
                "Performance rates in valid range (0-100)",
                passed,
                f"{result['invalid_rates']} invalid rates found" if not passed else "All rates valid"
            )
            
            # Check percentile ranks
            cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN percentile_rank < 0 OR percentile_rank > 100 THEN 1 END) as invalid_percentiles
                FROM provider_performance
                WHERE percentile_rank IS NOT NULL;
            """)
            result = cur.fetchone()
            passed = result['invalid_percentiles'] == 0 if result['total'] > 0 else True
            self.log_test(
                "Percentile ranks in valid range (0-100)",
                passed,
                f"{result['invalid_percentiles']} invalid percentiles" if not passed else "All percentiles valid"
            )
        
        # Test 6: View functionality
        print("\n[TEST GROUP] View Functionality Tests")
        
        required_views = [
            'vw_provider_performance_summary',
            'vw_provider_measure_performance',
            'vw_network_adequacy_dashboard',
            'vw_referral_network_analysis',
            'vw_provider_performance_rankings'
        ]
        
        for view in required_views:
            exists = self.test_view_exists(view)
            if exists:
                try:
                    with self.conn.cursor() as cur:
                        cur.execute(f"SELECT COUNT(*) FROM {view};")
                        count = cur.fetchone()[0]
                    self.log_test(
                        f"View accessible: {view}",
                        True,
                        f"Returns {count:,} rows"
                    )
                except psycopg2.Error as e:
                    self.log_test(
                        f"View accessible: {view}",
                        False,
                        f"Query failed: {str(e)[:100]}"
                    )
            else:
                self.log_test(
                    f"View exists: {view}",
                    False,
                    f"View {view} not found"
                )
        
        # Test 7: Relationship integrity
        print("\n[TEST GROUP] Relationship Integrity")
        
        with self.conn.cursor() as cur:
            # Check attributions reference valid providers
            cur.execute("""
                SELECT COUNT(*) as orphaned
                FROM member_provider_attribution mpa
                LEFT JOIN provider_directory pd ON mpa.provider_id = pd.provider_id
                WHERE pd.provider_id IS NULL;
            """)
            orphaned = cur.fetchone()[0]
            self.log_test(
                "Attributions reference valid providers",
                orphaned == 0,
                f"{orphaned} orphaned records" if orphaned > 0 else "All references valid"
            )
            
            # Check performance records reference valid providers
            cur.execute("""
                SELECT COUNT(*) as orphaned
                FROM provider_performance pp
                LEFT JOIN provider_directory pd ON pp.provider_id = pd.provider_id
                WHERE pd.provider_id IS NULL;
            """)
            orphaned = cur.fetchone()[0]
            self.log_test(
                "Performance records reference valid providers",
                orphaned == 0,
                f"{orphaned} orphaned records" if orphaned > 0 else "All references valid"
            )
    
    def run_integration_tests(self):
        """Run integration tests between Phase 2 Chat 1 and Chat 2."""
        print("\n" + "=" * 80)
        print("INTEGRATION TESTS: Phase 2 Chat 1 & Chat 2")
        print("=" * 80)
        
        print("\n[TEST GROUP] Cross-Phase Data Relationships")
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check members have both engagement scores and provider attribution
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT pm.member_id) as total_members,
                    COUNT(DISTINCT mes.member_id) as members_with_engagement,
                    COUNT(DISTINCT mpa.member_id) as members_with_attribution
                FROM plan_members pm
                LEFT JOIN member_engagement_scores mes ON pm.member_id = mes.member_id
                LEFT JOIN member_provider_attribution mpa ON pm.member_id = mpa.member_id AND mpa.is_current = TRUE
                WHERE pm.member_id LIKE 'M%';
            """)
            result = cur.fetchone()
            engagement_pct = (result['members_with_engagement'] / result['total_members'] * 100) if result['total_members'] > 0 else 0
            attribution_pct = (result['members_with_attribution'] / result['total_members'] * 100) if result['total_members'] > 0 else 0
            
            passed = engagement_pct >= 95 and attribution_pct >= 95
            self.log_test(
                "Members have both engagement scores and provider attribution",
                passed,
                f"Engagement: {engagement_pct:.1f}%, Attribution: {attribution_pct:.1f}%"
            )
            
            # Check provider performance aligns with member gaps
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT pp.provider_id) as providers_with_performance,
                    SUM(pp.open_gaps) as total_open_gaps_provider,
                    (SELECT COUNT(*) FROM member_gaps WHERE gap_status = 'Open') as total_open_gaps_member
                FROM provider_performance pp
                WHERE pp.measurement_year = 2024;
            """)
            result = cur.fetchone()
            # This is a sanity check - provider gaps should be a subset of member gaps
            passed = result['total_open_gaps_provider'] <= result['total_open_gaps_member'] * 1.5
            self.log_test(
                "Provider gap counts align with member gap counts",
                passed,
                f"Provider gaps: {result['total_open_gaps_provider']:,}, Member gaps: {result['total_open_gaps_member']:,}"
            )
    
    def generate_summary(self):
        """Generate test summary report."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total_tests = self.passed + self.failed + self.warnings
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"  [PASS] {self.passed} ({self.passed/total_tests*100:.1f}%)")
        print(f"  [WARN] {self.warnings} ({self.warnings/total_tests*100:.1f}%)")
        print(f"  [FAIL] {self.failed} ({self.failed/total_tests*100:.1f}%)")
        
        if self.failed > 0:
            print("\n[FAILED TESTS]")
            for test_name, passed, message, warning in self.test_results:
                if not passed and not warning:
                    print(f"  - {test_name}")
                    if message:
                        print(f"    {message}")
        
        if self.warnings > 0:
            print("\n[WARNINGS]")
            for test_name, passed, message, warning in self.test_results:
                if warning:
                    print(f"  - {test_name}")
                    if message:
                        print(f"    {message}")
        
        print("\n" + "=" * 80)
        
        if self.failed == 0:
            print("[SUCCESS] All critical tests passed!")
            if self.warnings > 0:
                print(f"[NOTE] {self.warnings} warnings found - review recommended")
            return True
        else:
            print(f"[FAILURE] {self.failed} critical test(s) failed")
            return False
    
    def run_all_tests(self):
        """Run all test suites."""
        print("=" * 80)
        print("PHASE 2 COMPREHENSIVE TEST SUITE")
        print("Testing Chats 1 & 2: Member Engagement & Provider Network")
        print("=" * 80)
        
        if not self.connect():
            return False
        
        try:
            self.run_phase2_chat1_tests()
            self.run_phase2_chat2_tests()
            self.run_integration_tests()
            return self.generate_summary()
        finally:
            self.close()


def get_db_config() -> Dict[str, str]:
    """Get database configuration from environment or defaults."""
    import os
    
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": os.getenv("DB_PORT", "5432")
    }


def main():
    """Main entry point."""
    db_config = get_db_config()
    
    # Allow override via command line arguments
    if len(sys.argv) > 1:
        db_config["host"] = sys.argv[1] if len(sys.argv) > 1 else db_config["host"]
        db_config["database"] = sys.argv[2] if len(sys.argv) > 2 else db_config["database"]
        db_config["user"] = sys.argv[3] if len(sys.argv) > 3 else db_config["user"]
        db_config["password"] = sys.argv[4] if len(sys.argv) > 4 else db_config["password"]
    
    suite = Phase2TestSuite(db_config)
    success = suite.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

