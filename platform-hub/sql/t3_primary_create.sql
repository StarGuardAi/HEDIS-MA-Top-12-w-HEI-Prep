-- ============================================================
-- T3 Branch A - CREATE cross_app_findings on Primary (helper-aligned)
-- Project: wiwmphjkupcnntawpafg
-- Date:    2026-05-14 (reconciled with live insert helpers)
-- Owner:   RSI (rreichert@...)
-- Model:   D2 - add sub_surface; all other columns match
--           Artifacts/shared/supabase_findings.py + supabase_platform.py
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS public.cross_app_findings (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_app      text NOT NULL
                    CHECK (source_app IN ('auditshield','starguard','sovereignshield')),
    finding_type    text NOT NULL,
    title           text,
    description     text,
    severity        text NOT NULL DEFAULT 'info'
                    CHECK (severity IN ('info','low','medium','high','critical')),
    status          text NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open','remediated','resolved','dismissed')),
    metadata        jsonb NOT NULL DEFAULT '{}'::jsonb,
    session_id      text,
    payload         jsonb,
    measure_id      text,
    policy_id       text,
    sub_surface     text
                    CHECK (sub_surface IS NULL OR sub_surface IN ('desktop','mobile')),
    created_at      timestamptz NOT NULL DEFAULT now(),
    updated_at      timestamptz NOT NULL DEFAULT now(),
    resolved_at     timestamptz NULL
);

CREATE INDEX IF NOT EXISTS idx_caf_source_surface
    ON public.cross_app_findings (source_app, sub_surface);
CREATE INDEX IF NOT EXISTS idx_caf_status_created
    ON public.cross_app_findings (status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_caf_finding_type
    ON public.cross_app_findings (finding_type);
CREATE INDEX IF NOT EXISTS idx_caf_session_id
    ON public.cross_app_findings (session_id)
    WHERE session_id IS NOT NULL;

-- Keep updated_at fresh on UPDATE (REST path often omits updated_at)
CREATE OR REPLACE FUNCTION public.caf_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_caf_updated_at ON public.cross_app_findings;
CREATE TRIGGER trg_caf_updated_at
    BEFORE UPDATE ON public.cross_app_findings
    FOR EACH ROW
    EXECUTE FUNCTION public.caf_set_updated_at();

ALTER TABLE public.cross_app_findings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS caf_read_authed ON public.cross_app_findings;
CREATE POLICY caf_read_authed ON public.cross_app_findings
    FOR SELECT TO authenticated, service_role USING (true);

DROP POLICY IF EXISTS caf_insert_service ON public.cross_app_findings;
CREATE POLICY caf_insert_service ON public.cross_app_findings
    FOR INSERT TO service_role WITH CHECK (true);

DROP POLICY IF EXISTS caf_update_service ON public.cross_app_findings;
CREATE POLICY caf_update_service ON public.cross_app_findings
    FOR UPDATE TO service_role USING (true) WITH CHECK (true);

DROP VIEW IF EXISTS public.platform_hub_kpis;
CREATE VIEW public.platform_hub_kpis
    WITH (security_invoker = false)
    AS
SELECT
    source_app,
    sub_surface,
    finding_type,
    status,
    count(*)        AS finding_count,
    max(created_at) AS latest_created_at
FROM public.cross_app_findings
GROUP BY source_app, sub_surface, finding_type, status;

-- Aggregated KPIs only: anon can read the view, not raw findings rows (RLS on base table).
GRANT SELECT ON public.platform_hub_kpis TO anon, authenticated, service_role;

REVOKE ALL ON TABLE public.cross_app_findings FROM anon;

-- Sanity probe (manual run)
-- SELECT * FROM public.platform_hub_kpis ORDER BY source_app, sub_surface;
