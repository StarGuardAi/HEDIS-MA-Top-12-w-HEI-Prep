# Services Copy Replacement — Full Block Patch

Apply across all four apps. Use the version that matches how the block is stored in each file.

---

## Version A: HTML (plain text)

**Files:** `Artifacts/www/starguard_services.html`, `Artifacts/www/auditshield_services.html`

**Find this block (Contract Pricing section):**
```html
        <!-- Contract Pricing -->
        <div class="content-section">
            <h2 class="section-title">Contract Pay Ranges</h2>
            <p class="section-subtitle">US Market - Full Stack AI Generative Specialist</p>

            <p class="section-text">
                For a <strong>Full Stack AI Generative specialist</strong>, rates are significantly higher than standard full-stack development because you are charging for <strong>domain expertise + security + AI proficiency</strong>.
            </p>

            <div class="pricing-grid">
                <div class="pricing-card">
                    <div class="pricing-tier">Mid-Level</div>
                    <div class="pricing-title">Contractor</div>
                    <div class="pricing-range">Consulting Rate</div>
                    ...
                </div>
                <div class="pricing-card featured">
                    <div class="pricing-tier">Senior / Lead</div>
                    ...
                </div>
            </div>

            <div class="project-pricing">
                <h3>Project-Based Pricing</h3>
                ...
            </div>
        </div>
```

**Replace with:**
```html
        <!-- Engagement Model -->
        <div class="content-section">
            <h2 class="section-title">Strategic Advisory & Implementation Leadership</h2>
            <p class="section-subtitle">Premium Healthcare AI Consulting — Engagement Terms Scoped to Complexity and Strategic Value</p>

            <p class="section-text">
                Engagement terms are scoped to complexity and strategic value—letting the conversation set the rate, which is standard practice at the senior champion level.
            </p>

            <div class="market-shift">
                <h3>What You Can Expect</h3>
                <p>
                    Strategic advisory for PoC through production implementation. Scope and investment are discussed directly—no published rate anchors. This approach allows us to tailor engagement terms to your specific needs.
                </p>
            </div>

            <p class="section-text">
                <strong>Contact:</strong> <a href="mailto:reichert.starguardai@gmail.com" style="color: var(--accent-teal); font-weight: 600;">reichert.starguardai@gmail.com</a>
            </p>
        </div>
```

**Footer addition** — Add before the Important Notice paragraph:
```html
            <p class="footer-text" style="margin-bottom: 10px;">
                <a href="mailto:reichert.starguardai@gmail.com" style="color: var(--accent-teal); text-decoration: underline;">reichert.starguardai@gmail.com</a>
            </p>
```

---

## Version B: SovereignShield (Shiny ui)

**File:** `Artifacts/project/sovereignshield/app.py`

**Find:** `services_panel()` with card headers like "Senior Consultant Rate", "Consulting Rate", and button `reichert.starguardai@email.com` (typo).

**Replace the entire `services_panel()` return block with:**

```python
    @render.ui
    def services_panel() -> Any:
        return ui.div(
            ui.row(
                ui.column(
                    12,
                    ui.card(
                        ui.card_header("Strategic Advisory & Implementation Leadership"),
                        ui.card_body(
                            ui.p(
                                "Engagement terms are scoped to complexity and strategic value—"
                                "letting the conversation set the rate, standard practice at the senior champion level."
                            ),
                            ui.p(
                                "Strategic advisory for PoC through production implementation. "
                                "Scope and investment discussed directly—no published rate anchors."
                            ),
                        ),
                        class_="services-card mb-3",
                    ),
                ),
            ),
            ui.div(
                ui.p("Available March 2026 | Contract | Remote", class_="mb-2"),
                ui.a(
                    "reichert.starguardai@gmail.com",
                    href="mailto:reichert.starguardai@gmail.com",
                    class_="btn",
                    style=f"background-color:{_BRAND_GREEN}; color:#fff; padding: 10px 20px; display: inline-block; border-radius: 8px; text-decoration: none;",
                ),
                class_="text-center mt-4 p-3",
            ),
            class_="container py-3",
        )
```

**Color note:** SovereignShield uses `_BRAND_GREEN` (#10B981) for the contact button. StarGuard/AuditShield HTML stays with `--accent-teal` / purple gradient.

---

## Version C: Color swap (SovereignShield only)

Where the services UI uses `#4A3E8F` (purple), replace with `#10B981` (green) in SovereignShield's CSS/vars for the services block.
