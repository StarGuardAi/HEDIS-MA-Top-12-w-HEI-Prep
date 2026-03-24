-- Step 0: platform_hub_kpis view (run in Supabase SQL Editor)
-- Uses cross_app_findings.status (open/remediated), not resolved_at

DROP VIEW IF EXISTS platform_hub_kpis;

CREATE OR REPLACE VIEW platform_hub_kpis AS
SELECT
    COUNT(*) FILTER (WHERE status = 'open')                                  AS open_findings_total,
    COUNT(*) FILTER (WHERE source_app = 'auditshield'     AND status = 'open') AS open_audit_flags,
    COUNT(*) FILTER (WHERE source_app = 'starguard'       AND status = 'open') AS open_star_gaps,
    COUNT(*) FILTER (WHERE source_app = 'sovereignshield' AND status = 'open') AS open_policy_violations,
    COUNT(*) FILTER (WHERE severity = 'critical'          AND status = 'open') AS critical_open,
    COUNT(*) FILTER (WHERE status = 'remediated')                              AS remediated_total
FROM cross_app_findings;
