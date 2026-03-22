# Cron-Job.org Setup — Keep HF Spaces Awake

Free pings every 30 minutes keep your HuggingFace Spaces from sleeping (48-hour sleep timer resets on each visit).

## Space URLs to Ping

| Space | URL |
|-------|-----|
| AuditShield Live | https://rreichert-auditshield-live.hf.space |
| StarGuard Desktop | https://rreichert-starguard-desktop.hf.space |
| StarGuard Mobile | https://rreichert-starguardai.hf.space |
| SovereignShield Desktop | https://rreichert-sovereignshield.hf.space |
| SovereignShield Mobile | https://rreichert-sovereignshield-mobile.hf.space |

> If any URL differs, check your Space settings → "Embed this Space" for the exact URL.

## Steps (≈10 minutes, free)

1. Go to [cron-job.org](https://cron-job.org) → create a free account
2. Click **Create cronjob**
3. For each Space URL:
   - **URL:** paste the Space URL
   - **Execution schedule:** Every 30 minutes
   - **Request method:** GET
   - **Title:** e.g. `ping-auditshield`, `ping-starguard-desktop`, etc.
   - **Save** → repeat for all 5
4. Under **Notifications**, set email alert if a job fails 3× — alerts you if a Space goes down

**Total cost:** $0. HuggingFace treats each ping as a visit and resets the 48-hour sleep timer.
