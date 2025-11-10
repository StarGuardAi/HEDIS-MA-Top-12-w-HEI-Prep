# GitHub Organizations Setup Plan

**Date:** 2025-10-30  
**Status:** Planning  
**Purpose:** Set up 2 GitHub orgs with organized repos

---

## Overview

Set up two GitHub organizations:
1. **StarGuardAi** - Keep original healthcare content (1 repo)
2. **reichert-sentinel-ai** - Host migrated law enforcement content (3 repos)

---

## Phase 1: StarGuardAi Org Setup

### Objectives
- Verify existing repo transfer
- Ensure org shows only `HEDIS-MA-Top-12-w-HEI-Prep` repo
- Update org profile if needed

### Tasks

**1.1 Verify Repo Transfer**
```powershell
# Check current remote
git remote -v

# Verify repo exists in org
gh repo view StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep --web

# Confirm org membership
gh api user/orgs --jq '.[].login'
```

**1.2 Update Org Profile (Optional)**
- Access: https://github.com/orgs/StarGuardAi/settings/profile
- Update org description, website, location as needed
- Set privacy settings

---

## Phase 2: reichert-sentinel-ai Org Setup

### Repositories to Create

1. **guardian-fraud-analytics**
   - Description: "Guardian: AI-Powered Fraud Detection System"
   - Focus: Procurement fraud, financial fraud detection

2. **foresight-crime-prediction**
   - Description: "Foresight: Predictive Crime Intelligence Platform"
   - Focus: Big data fusion, criminal network mapping, predictive analytics

3. **cipher-threat-tracker**
   - Description: "Cipher: Cyber Threat Attribution & Analysis"
   - Focus: Homeland security intelligence, cyber threats

---

## Phase 3: Content Organization

### Source Directory
`.\sentinel-migrated`

### Categorization Rules

**Guardian (fraud-analytics):**
- Files/content related to:
  - Procurement fraud detection
  - Financial fraud detection
  - Fraud prediction models
  - AML (Anti-Money Laundering) analytics
  - Bid rigging, phantom vendors, kickback schemes

**Foresight (crime-prediction):**
- Files/content related to:
  - Big data fusion (CAD, RMS, NIBRS, OSINT)
  - Criminal network mapping
  - Crime prediction models
  - Graph analytics
  - Time-series forecasting
  - Geospatial analysis & hotspot detection

**Cipher (threat-tracker):**
- Files/content related to:
  - Homeland security intelligence
  - Cyber threat intelligence
  - Threat attribution
  - Security analytics
  - Critical infrastructure protection

**Shared/Common Files:**
- Core infrastructure (src/, tests/, scripts/)
- Documentation (docs/architecture.md, docs/WRITING_STYLE_GUIDE.md)
- Configuration files (requirements.txt, Dockerfile, etc.)
- Each repo gets a copy of shared infrastructure

---

## Phase 4: Repository Creation & Setup

### Step-by-Step Process

**4.1 Create Repos via GitHub CLI**

```powershell
# Create Guardian repo
gh repo create reichert-sentinel-ai/guardian-fraud-analytics \
  --private \
  --description "Guardian: AI-Powered Fraud Detection System - Procurement and financial fraud detection using ML/AI" \
  --homepage "https://github.com/reichert-sentinel-ai/guardian-fraud-analytics"

# Create Foresight repo
gh repo create reichert-sentinel-ai/foresight-crime-prediction \
  --private \
  --description "Foresight: Predictive Crime Intelligence Platform - Big data fusion and criminal network mapping" \
  --homepage "https://github.com/reichert-sentinel-ai/foresight-crime-prediction"

# Create Cipher repo
gh repo create reichert-sentinel-ai/cipher-threat-tracker \
  --private \
  --description "Cipher: Cyber Threat Attribution & Analysis - Homeland security and cyber threat intelligence" \
  --homepage "https://github.com/reichert-sentinel-ai/cipher-threat-tracker"
```

**4.2 Create Project Directories**

```powershell
# Create staging directories
New-Item -ItemType Directory -Path ".\repo-guardian" -Force
New-Item -ItemType Directory -Path ".\repo-foresight" -Force
New-Item -ItemType Directory -Path ".\repo-cipher" -Force
```

**4.3 Organize Content**

Create a PowerShell script `organize-content.ps1` to:
- Copy shared infrastructure to all 3 repos
- Copy project-specific content based on categorization rules
- Create project-specific README.md files
- Generate initial commit structure

---

## Phase 5: Project README Creation

### Guardian README Template

```markdown
# Guardian: AI-Powered Fraud Detection System

**Organization:** [reichert-sentinel-ai](https://github.com/reichert-sentinel-ai)  
**Focus:** Procurement and Financial Fraud Detection

---

## Overview

Guardian is an AI-powered fraud detection system designed to identify fraudulent activities in government procurement contracts and financial transactions.

### Key Capabilities
- Procurement Fraud Detection (bid rigging, phantom vendors, kickback schemes)
- Financial Fraud Detection (money laundering, suspicious transactions)
- Real-time Monitoring & Alerting
- Predictive Fraud Analytics

### Technology Stack
- **ML/AI:** scikit-learn, XGBoost, PyTorch
- **Databases:** PostgreSQL, Neo4j
- **Analytics:** Fraud detection models, graph analytics
- **Languages:** Python, SQL

---

## Quick Start

[Installation and setup instructions]

---

## Project Structure

[Directory structure]

---

*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
```

Similar templates for Foresight and Cipher with their respective focus areas.

---

## Phase 6: Git Initialization & Push

**6.1 Initialize Each Repo**

```powershell
# For each project directory
cd repo-guardian
git init
git add .
git commit -m "Initial commit: Guardian fraud detection system"
git branch -M main
git remote add origin https://github.com/reichert-sentinel-ai/guardian-fraud-analytics.git
git push -u origin main

# Repeat for repo-foresight and repo-cipher
```

**6.2 Verify Pushes**

```powershell
# Verify repos exist and have content
gh repo view reichert-sentinel-ai/guardian-fraud-analytics
gh repo view reichert-sentinel-ai/foresight-crime-prediction
gh repo view reichert-sentinel-ai/cipher-threat-tracker
```

---

## Phase 7: Verification

### Checklist

- [ ] StarGuardAi org shows only HEDIS-MA-Top-12-w-HEI-Prep repo
- [ ] reichert-sentinel-ai org has 3 repos visible
- [ ] All 3 repos have README.md with project descriptions
- [ ] Content is organized correctly by focus area
- [ ] Shared infrastructure present in all repos
- [ ] Git remotes configured correctly
- [ ] All repos are pushed to GitHub

---

## Implementation Scripts Needed

1. **organize-content.ps1** - Categorize and copy files to project directories
2. **create-project-readmes.ps1** - Generate README.md for each repo
3. **setup-repos.ps1** - Initialize git, configure remotes, push

---

## Content Categorization Details

Since most files in `sentinel-migrated` are general documentation, the categorization will be:

1. **Core Infrastructure** → All repos (src/, tests/, scripts/, config files)
2. **General Documentation** → Distribute based on keywords:
   - Fraud-related docs → Guardian
   - Crime/prediction docs → Foresight
   - Threat/security docs → Cipher
3. **Project-Specific Docs** → Create new for each repo

---

*Last Updated: 2025-10-30*

