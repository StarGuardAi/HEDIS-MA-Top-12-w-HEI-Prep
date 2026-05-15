-- ============================================================
-- T3 Branch B - ALTER existing cross_app_findings on Primary (helper-aligned)
-- Project: wiwmphjkupcnntawpafg
-- Date:    2026-05-14 (reconciled with live insert helpers)
-- Idempotent: ADD IF NOT EXISTS, DROP/ADD constraints & policies, no DROP COLUMN
-- ============================================================

-- 1. Ensure every column the helpers expect exists (legacy-safe)
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS source_app text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS finding_type text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS title text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS description text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS severity text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS status text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS metadata jsonb;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS session_id text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS payload jsonb;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS measure_id text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS policy_id text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS sub_surface text;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS created_at timestamptz;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS updated_at timestamptz;
ALTER TABLE public.cross_app_findings ADD COLUMN IF NOT EXISTS resolved_at timestamptz;

-- Defaults where safe (do not overwrite populated rows)
ALTER TABLE public.cross_app_findings
    ALTER COLUMN metadata SET DEFAULT '{}'::jsonb;
ALTER TABLE public.cross_app_findings
    ALTER COLUMN severity SET DEFAULT 'info';
ALTER TABLE public.cross_app_findings
    ALTER COLUMN status SET DEFAULT 'open';
ALTER TABLE public.cross_app_findings
    ALTER COLUMN created_at SET DEFAULT now();
ALTER TABLE public.cross_app_findings
    ALTER COLUMN updated_at SET DEFAULT now();

-- 2. CHECK constraints (idempotent drop/add)
ALTER TABLE public.cross_app_findings
    DROP CONSTRAINT IF EXISTS cross_app_findings_source_app_check;
ALTER TABLE public.cross_app_findings
    ADD CONSTRAINT cross_app_findings_source_app_check
    CHECK (source_app IS NULL OR source_app IN ('auditshield','starguard','sovereignshield'));

ALTER TABLE public.cross_app_findings
    DROP CONSTRAINT IF EXISTS cross_app_findings_sub_surface_check;
ALTER TABLE public.cross_app_findings
    ADD CONSTRAINT cross_app_findings_sub_surface_check
    CHECK (sub_surface IS NULL OR sub_surface IN ('desktop','mobile'));

ALTER TABLE public.cross_app_findings
    DROP CONSTRAINT IF EXISTS cross_app_findings_severity_check;
ALTER TABLE public.cross_app_findings
    ADD CONSTRAINT cross_app_findings_severity_check
    CHECK (
        severity IS NULL
        OR severity IN ('info','low','medium','high','critical')
    );

ALTER TABLE public.cross_app_findings
    DROP CONSTRAINT IF EXISTS cross_app_findings_status_check;
ALTER TABLE public.cross_app_findings
    ADD CONSTRAINT cross_app_findings_status_check
    CHECK (
        status IS NULL
        OR status IN ('open','remediated','resolved','dismissed')
    );

-- 3. Backfill sub_surface from JSON metadata / legacy payload (best-effort)
UPDATE public.cross_app_findings
SET sub_surface = m.sub
FROM (
    SELECT
        id,
        CASE
            WHEN lower(COALESCE(metadata->>'sub_surface', '')) IN ('desktop', 'mobile')
                THEN lower(metadata->>'sub_surface')
            WHEN lower(COALESCE(payload->>'sub_surface', '')) IN ('desktop', 'mobile')
                THEN lower(payload->>'sub_surface')
            WHEN lower(COALESCE(metadata->>'platform', '')) IN ('desktop', 'mobile')
                THEN lower(metadata->>'platform')
            ELSE NULL
        END AS sub
    FROM public.cross_app_findings
) AS m
WHERE public.cross_app_findings.id = m.id
  AND public.cross_app_findings.sub_surface IS NULL
  AND m.sub IS NOT NULL;

-- 4. Indexes
CREATE INDEX IF NOT EXISTS idx_caf_source_surface
    ON public.cross_app_findings (source_app, sub_surface);
CREATE INDEX IF NOT EXISTS idx_caf_status_created
    ON public.cross_app_findings (status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_caf_finding_type
    ON public.cross_app_findings (finding_type);
CREATE INDEX IF NOT EXISTS idx_caf_session_id
    ON public.cross_app_findings (session_id)
    WHERE session_id IS NOT NULL;

-- 5. updated_at trigger
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

-- 6. View (security_invoker = false: definer-style so anon SELECT on view is not blocked by base-table RLS)
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

GRANT SELECT ON public.platform_hub_kpis TO anon, authenticated, service_role;

REVOKE ALL ON TABLE public.cross_app_findings FROM anon;

-- 7. RLS + policies (idempotent)
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
