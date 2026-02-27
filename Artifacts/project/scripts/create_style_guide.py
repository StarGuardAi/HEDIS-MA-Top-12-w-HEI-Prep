#!/usr/bin/env python3
"""
Writing Style Guide Generator for Sentinel Analytics

Generates comprehensive writing style guide content for law enforcement
and intelligence domain documentation.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict


class StyleGuideCreator:
    """Creates comprehensive writing style guide content."""
    
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.style_guide_path = self.target_dir / 'WRITING_STYLE_GUIDE.md'
        self.temp_path = self.target_dir / 'WRITING_STYLE_GUIDE.draft.md'
    
    def generate_style_guide_content(self) -> str:
        """
        Generate comprehensive style guide content.
        
        Returns:
            Complete style guide markdown content
        """
        sections = [
            self._generate_header(),
            self._generate_toc(),
            self._generate_purpose(),
            self._generate_voice_tone(),
            self._generate_domain_terminology(),
            self._generate_glossary(),
            self._generate_hashtag_standards(),
            self._generate_writing_guidelines(),
            self._generate_documentation_standards(),
            self._generate_examples(),
            self._generate_footer()
        ]
        
        return '\n\n'.join(sections)
    
    def _generate_header(self) -> str:
        """Generate header section."""
        return """# 📝 Sentinel Analytics Writing Style Guide

**Complete reference for writing style, tone, and formatting across all project documentation, content, and communications.**

**Version:** 1.0  
**Last Updated:** {date}  
**Domain:** Law Enforcement & Intelligence Analytics

---

*This guide ensures consistency, professionalism, and clarity across all Sentinel Analytics communications, documentation, and content.*
""".format(date=datetime.now().strftime('%Y-%m-%d'))
    
    def _generate_toc(self) -> str:
        """Generate table of contents."""
        return """## 📑 Table of Contents

1. [Purpose & Audience](#purpose--audience)
2. [Voice & Tone](#voice--tone)
3. [Domain Terminology](#domain-terminology)
4. [Glossary](#glossary)
5. [Hashtag Standards](#hashtag-standards)
6. [Writing Guidelines](#writing-guidelines)
7. [Documentation Standards](#documentation-standards)
8. [Examples](#examples)

---"""
    
    def _generate_purpose(self) -> str:
        """Generate purpose and audience section."""
        return """## 🎯 Purpose & Audience

### Purpose

This style guide standardizes writing across all Sentinel Analytics materials to ensure:
- **Consistency** in terminology and presentation
- **Clarity** in technical and business communications
- **Professionalism** in all external-facing content
- **Accuracy** in domain-specific language
- **Accessibility** for diverse audiences

### Primary Audiences

1. **Law Enforcement Professionals**
   - Detectives, analysts, supervisors
   - Operations and intelligence units
   - Command staff and leadership

2. **Government & Public Sector**
   - Federal, state, local agencies
   - Procurement officers
   - Compliance and oversight officials

3. **Technical Stakeholders**
   - Data scientists and engineers
   - Intelligence analysts
   - System administrators

4. **Business Stakeholders**
   - Procurement decision-makers
   - Contract administrators
   - Executive leadership

### Document Types Covered

- Technical documentation
- Business proposals and presentations
- Case studies and success stories
- Training materials
- Social media content
- Blog posts and articles
- Code documentation
- API documentation"""
    
    def _generate_voice_tone(self) -> str:
        """Generate voice and tone section."""
        return """## 🗣️ Voice & Tone

### Core Writing Principles

**BE:**
- ✅ **Confident** (grounded in evidence and results)
- ✅ **Factual** (let data and outcomes speak)
- ✅ **Strategic** (frame as operational advantage)
- ✅ **Authoritative** (demonstrate expertise)
- ✅ **Clear** (avoid unnecessary jargon)
- ✅ **Professional** (law enforcement standards)
- ✅ **Quantitative** (focus on measurable impact)
- ✅ **Respectful** (honor the mission and community)

**AVOID:**
- ❌ Speculative language ("might", "could potentially")
- ❌ Over-technical jargon without context
- ❌ Defensive positioning
- ❌ Generic buzzwords without substance
- ❌ Law enforcement slang or colloquialisms
- ❌ Over-promising capabilities
- ❌ Minimizing threats or risks

### Tone by Context

#### Technical Documentation
- **Tone:** Precise, instructive, thorough
- **Voice:** Educational and supportive
- **Example:** "The network analysis module identifies connections between subjects using graph algorithms. Configure the threshold parameter to balance sensitivity and specificity."

#### Business Communications
- **Tone:** Results-oriented, strategic, professional
- **Voice:** Consultant and trusted advisor
- **Example:** "Our procurement fraud detection system identified $2.3M in suspicious activity within the first quarter, enabling early intervention and recovery."

#### Case Studies
- **Tone:** Narrative, results-focused, credible
- **Voice:** Storyteller and partner
- **Example:** "The XYZ Police Department implemented our criminal network mapping tool, resulting in a 35% increase in case closure rates for organized crime investigations."

#### Social Media
- **Tone:** Engaging, informative, respectful
- **Voice:** Industry thought leader
- **Example:** "Today's law enforcement agencies face unprecedented data challenges. Our big data fusion platform integrates CAD, RMS, and NIBRS for unified intelligence analysis. #LawEnforcementAnalytics #DataFusion"

---
"""
    
    def _generate_domain_terminology(self) -> str:
        """Generate domain terminology section."""
        return """## 🎯 Domain Terminology

### Five Focus Areas

#### 1. Procurement Fraud Detection

**Key Terms:**
- **Bid Rigging:** Collusive agreement among vendors to manipulate bidding processes
- **Phantom Vendors:** Fictitious suppliers created for fraudulent invoicing
- **Kickback Scheme:** Payment or favors exchanged for favorable contract awards
- **Conflict of Interest:** Situation where personal or financial interests may compromise objectivity

**Usage Example:**
> "Our procurement fraud detection system identifies bid rigging patterns by analyzing bidding behavior, vendor relationships, and contract award anomalies across multiple agencies."

#### 2. Big Data Fusion for Law Enforcement

**Key Terms:**
- **CAD:** Computer-Aided Dispatch (emergency call and response system)
- **RMS:** Records Management System (criminal records database)
- **NIBRS:** National Incident-Based Reporting System (FBI crime data standard)
- **OSINT:** Open Source Intelligence (publicly available information)
- **Data Fusion:** Integration of multiple data sources for comprehensive analysis

**Usage Example:**
> "Our platform fuses CAD dispatch data, RMS incident reports, and NIBRS statistics with OSINT feeds to create a unified intelligence picture for operational planning."

#### 3. Criminal Network Mapping

**Key Terms:**
- **Social Network Analysis (SNA):** Mathematical analysis of relationships and connections
- **Criminal Network:** Group structure of individuals connected through criminal activities
- **Centrality Metrics:** Measures identifying key individuals in networks
- **Link Analysis:** Investigation of connections between subjects, locations, and events
- **Association Mapping:** Visualization of relationships and affiliations

**Usage Example:**
> "Using social network analysis and centrality metrics, our criminal network mapping tool identifies key actors and communication pathways within organized crime structures."

#### 4. Financial Fraud Detection

**Key Terms:**
- **AML:** Anti-Money Laundering (regulatory compliance framework)
- **Transaction Monitoring:** Real-time analysis of financial transactions for suspicious patterns
- **Pattern Recognition:** Automated detection of unusual activity patterns
- **Suspicious Activity Report (SAR):** Formal documentation of potentially illegal transactions
- **Risk Profiling:** Assessment of individual or entity risk levels

**Usage Example:**
> "Our transaction monitoring system employs pattern recognition algorithms to identify suspicious activity patterns that trigger SAR filings for AML compliance."

#### 5. Homeland Security Intelligence

**Key Terms:**
- **Threat Assessment:** Evaluation of potential risks to security
- **Attribution:** Identification of responsible parties for security incidents
- **Indicators of Compromise (IOC):** Evidence suggesting a security breach
- **Threat Intelligence:** Information about potential security threats
- **Critical Infrastructure:** Essential systems and assets requiring protection

**Usage Example:**
> "Our threat intelligence platform aggregates indicators of compromise from multiple sources to provide comprehensive threat assessments for critical infrastructure protection."

---
"""
    
    def _generate_glossary(self) -> str:
        """Generate comprehensive glossary section."""
        glossary_terms = {
            "Intelligence Fusion": "Integration of multiple intelligence sources and data types to create comprehensive situational awareness",
            "Subject": "Individual under investigation or analysis (replaces 'patient' from healthcare domain)",
            "Case File": "Collection of documents and evidence related to an investigation",
            "Threat Assessment": "Systematic evaluation of potential risks and their likelihood",
            "Investigation Strategy": "Plan for conducting an inquiry or analysis (replaces 'treatment plan')",
            "Inter-Agency Coordination": "Collaboration between multiple law enforcement or government agencies",
            "Community Safety": "Protection and well-being of public (replaces 'population health')",
            "Risk Profiling": "Assessment of individual or entity risk levels based on behavioral patterns",
            "Incident Data": "Information about events, crimes, or security occurrences",
            "Agency Network": "Connected group of law enforcement organizations (replaces 'provider network')",
            "Criminal Intelligence Database": "Systematic collection of information about criminal activities and actors",
            "Performance Metrics": "Measurable indicators of system or operational effectiveness",
            "Network Mapping": "Visualization and analysis of relationships between entities",
            "Data Fusion": "Integration of disparate data sources for unified analysis",
            "Link Analysis": "Investigation of connections between subjects, events, and locations",
            "Pattern Recognition": "Automated identification of recurring patterns in data",
            "Anomaly Detection": "Identification of unusual or suspicious patterns that deviate from normal behavior",
            "Predictive Modeling": "Statistical techniques for forecasting future events or outcomes",
            "Threat Intelligence": "Information about potential security threats and adversaries",
            "Social Network Analysis": "Mathematical analysis of relationships and connections in networks",
            "Open Source Intelligence (OSINT)": "Information gathered from publicly available sources",
            "Human Intelligence (HUMINT)": "Information obtained from human sources",
            "Signals Intelligence (SIGINT)": "Information gathered from electronic communications",
            "Geospatial Intelligence (GEOINT)": "Information derived from geographic and spatial data",
            "All-Source Intelligence": "Integrated analysis combining multiple intelligence disciplines",
            "Intelligence Cycle": "Process of planning, collection, processing, analysis, and dissemination",
            "Operational Security (OPSEC)": "Protection of sensitive operational information",
            "Source Protection": "Safeguarding identities and methods of intelligence sources",
            "Compartmentalization": "Restricting access to information on a need-to-know basis",
            "Chain of Custody": "Documented trail of evidence handling and transfer",
            "Attribution": "Identification of responsible parties for security incidents or crimes",
            "Indicators of Compromise (IOC)": "Evidence suggesting a security breach or threat",
            "Threat Actor": "Individual or group posing a security threat",
            "Attack Surface": "Total vulnerabilities and entry points that could be exploited",
            "Risk Assessment": "Evaluation of potential threats and their impact",
            "Vulnerability Analysis": "Identification and assessment of security weaknesses",
            "Counterintelligence": "Activities to prevent espionage and protect intelligence",
            "Surveillance": "Monitoring of activities, communications, or behavior",
            "Reconnaissance": "Gathering of information about targets or environments",
            "Criminal Profiling": "Analysis of behavioral patterns to understand motivations and predict actions",
            "Forensic Analysis": "Scientific examination of evidence for legal purposes",
            "Digital Forensics": "Recovery and analysis of information from digital devices",
            "Metadata Analysis": "Examination of data about data (timestamps, locations, relationships)",
            "Behavioral Analysis": "Study of patterns in actions and decision-making",
            "Temporal Analysis": "Examination of time-based patterns and sequences",
            "Geospatial Analysis": "Analysis of location-based data and patterns",
            "Correlation Analysis": "Identification of relationships between different data points",
            "Alerting": "Automatic notification of detected events or anomalies",
            "Dashboards": "Visual interfaces displaying key metrics and information",
            "Reporting": "Generation of structured summaries and analyses"
        }
        
        glossary_lines = ["## 📚 Glossary\n"]
        glossary_lines.append("**Comprehensive terminology reference for law enforcement and intelligence analytics.**\n")
        glossary_lines.append("| Term | Definition |")
        glossary_lines.append("|------|------------|")
        
        for term, definition in sorted(glossary_terms.items()):
            # Escape pipe characters in definitions
            definition_escaped = definition.replace('|', '\\|')
            glossary_lines.append(f"| **{term}** | {definition_escaped} |")
        
        return '\n'.join(glossary_lines)
    
    def _generate_hashtag_standards(self) -> str:
        """Generate hashtag standards section."""
        return """## #️⃣ Hashtag Standards

### Core Hashtags (Always Include - Pick 4)

**Primary Set:**
- `#LawEnforcementAnalytics`
- `#CriminalIntelligence`
- `#DataFusion`
- `#PredictiveAnalytics`

**Alternative Core:**
- `#IntelligenceAnalytics`
- `#PublicSafety`
- `#CrimePrevention`
- `#ThreatIntelligence`

### Context-Specific Hashtags (Choose 6 Based on Content)

#### Procurement Fraud Focus
- `#ProcurementFraud`
- `#ContractFraud`
- `#BidRigging`
- `#GovernmentAccountability`
- `#FraudDetection`
- `#PublicSectorAnalytics`

#### Big Data Fusion Focus
- `#BigDataFusion`
- `#LawEnforcementAnalytics`
- `#IntelligenceFusion`
- `#DataIntegration`
- `#CADRMS`
- `#OSINT`

#### Criminal Networks Focus
- `#CriminalNetworks`
- `#NetworkMapping`
- `#OrganizedCrime`
- `#SocialNetworkAnalysis`
- `#LinkAnalysis`
- `#CrimeIntelligence`

#### Financial Fraud Focus
- `#FinancialFraud`
- `#FraudDetection`
- `#AML`
- `#TransactionMonitoring`
- `#AntiMoneyLaundering`
- `#FinancialCrimes`

#### Homeland Security Focus
- `#HomelandSecurity`
- `#NationalSecurity`
- `#ThreatIntelligence`
- `#CounterTerrorism`
- `#CriticalInfrastructure`
- `#SecurityAnalytics`

#### Technical Implementation Focus
- `#Python`
- `#MachineLearning`
- `#DataScience`
- `#Analytics`
- `#AI`
- `#BigData`

### Hashtag Guidelines

1. **Use 10 hashtags total** (4 core + 6 context-specific)
2. **Place at end of post** (after main content)
3. **Mix general and specific** (broad reach + targeted engagement)
4. **Review quarterly** (hashtag trends change)
5. **Avoid overuse** (max 10 per post)
6. **Research before using** (ensure appropriate audience)

### Avoid These Hashtags

- Generic tags: `#AI`, `#Technology`, `#Business` (too broad)
- Healthcare tags: `#Healthcare`, `#HEDIS`, `#HealthcareAnalytics` (wrong domain)
- Overly promotional: `#BestEver`, `#Amazing`, `#Revolutionary`
- Slang or informal: `#CopStuff`, `#PoliceLife` (unprofessional)

---
"""
    
    def _generate_writing_guidelines(self) -> str:
        """Generate writing guidelines section."""
        return """## ✍️ Writing Guidelines

### Sentence Structure

**DO:**
- Use active voice: "The system identifies threats" (not "Threats are identified by the system")
- Keep sentences clear and concise (15-25 words average)
- Vary sentence length for readability
- Lead with the most important information

**DON'T:**
- Use passive voice unnecessarily
- Create run-on sentences (over 35 words)
- Start multiple consecutive sentences the same way
- Bury key points in complex sentence structures

### Paragraph Structure

**Structure:**
1. **Topic sentence** - States main point
2. **Supporting sentences** - Provide evidence or detail
3. **Concluding sentence** - Reinforces or transitions

**Length:** 3-5 sentences per paragraph (50-100 words)

**Example:**
> Our procurement fraud detection system analyzes bidding patterns across multiple contracts. By examining vendor relationships, timing correlations, and price anomalies, the system identifies collusive behavior. This automated analysis enables early intervention before significant losses occur.

### Punctuation & Formatting

#### Commas
- Use after introductory phrases: "During the investigation, we discovered..."
- Separate items in lists: "The system tracks vendors, contracts, and payments"
- Before conjunctions in compound sentences: "The alert was triggered, and the analyst reviewed the data"

#### Dashes
- Use em dashes (—) for emphasis: "The key finding—identified through pattern analysis—was the timing correlation"
- Use en dashes (–) for ranges: "Coverage spans 2019–2023"

#### Quotation Marks
- Use double quotes for direct quotes: "The system identified $2.3M in suspicious activity"
- Use single quotes for terms or emphasis: "The 'phantom vendor' pattern was detected"

#### Numbers
- Spell out one through nine; use numerals for 10+
- Use numerals for percentages, dates, measurements: "3 percent", "December 15, 2023", "5 meters"
- Format large numbers: "$2.3M" or "$2,300,000" (be consistent)

### Technical Writing

#### Code Examples
- Always include language specification: ```python
- Provide context before code blocks
- Explain what the code does
- Include expected outputs when helpful

#### API Documentation
- Use consistent formatting: `endpoint_name(param_type)` 
- Document all parameters
- Include request/response examples
- Note error conditions

#### Terminology
- Define acronyms on first use: "Computer-Aided Dispatch (CAD)"
- Use consistent terms throughout document
- Reference glossary for definitions

---
"""
    
    def _generate_documentation_standards(self) -> str:
        """Generate documentation standards section."""
        return """## 📄 Documentation Standards

### Code Documentation

#### Function Docstrings
```python
def analyze_network_connections(subject_id: str, threshold: float) -> Dict[str, Any]:
    \"\"\"
    Analyze criminal network connections for a subject.
    
    This function identifies all direct and indirect connections
    to a subject using social network analysis algorithms. It
    calculates centrality metrics and identifies key actors in
    the network structure.
    
    Args:
        subject_id: Unique identifier for the subject under analysis
        threshold: Minimum connection strength to include (0.0-1.0)
    
    Returns:
        Dictionary containing:
        - connections: List of connected subject IDs
        - centrality_score: Centrality metric for the subject
        - key_actors: List of high-centrality actors in network
    
    Raises:
        ValueError: If subject_id is empty or threshold is out of range
        DatabaseError: If database connection fails
    
    Example:
        >>> results = analyze_network_connections('SUB-12345', 0.5)
        >>> print(results['centrality_score'])
        0.823
    \"\"\"
```

#### Class Documentation
```python
class ThreatIntelligencePlatform:
    \"\"\"
    Platform for aggregating and analyzing threat intelligence.
    
    This class provides methods for collecting threat intelligence
    from multiple sources, correlating indicators of compromise,
    and generating threat assessments for security operations.
    
    Attributes:
        source_count: Number of intelligence sources configured
        last_update: Timestamp of most recent data refresh
    
    Example:
        >>> platform = ThreatIntelligencePlatform()
        >>> platform.add_source('OSINT Feed', url='https://example.com/feeds')
        >>> threat_assessment = platform.assess_threat_level('suspect-123')
    \"\"\"
```

### README Structure

Every project README should include:

```markdown
# Project Name

Brief one-sentence description.

## Overview

2-3 paragraphs explaining what the project does, why it exists,
and who it's for.

## Features

- Key capability 1
- Key capability 2
- Key capability 3

## Installation

Step-by-step installation instructions.

## Usage

Basic usage examples with code snippets.

## Configuration

How to configure the system (if applicable).

## API Reference

Link to detailed API documentation or inline summary.

## Contributing

Guidelines for contributors (if applicable).

## License

License information.
```

### Technical Report Structure

1. **Executive Summary** (1 page)
   - Key findings
   - Recommendations
   - Impact assessment

2. **Introduction** (1-2 pages)
   - Background
   - Objectives
   - Scope

3. **Methodology** (2-3 pages)
   - Approach
   - Data sources
   - Analysis techniques

4. **Findings** (3-5 pages)
   - Results with visualizations
   - Statistical analysis
   - Key insights

5. **Discussion** (2-3 pages)
   - Interpretation of findings
   - Implications
   - Limitations

6. **Recommendations** (1-2 pages)
   - Action items
   - Implementation considerations
   - Risk assessment

7. **Appendices**
   - Additional data
   - Technical details
   - References

---
"""
    
    def _generate_examples(self) -> str:
        """Generate examples section."""
        return """## 💡 Examples

### Good vs. Bad Examples

#### Example 1: Technical Description

**❌ BAD:**
> "Our thing does stuff with data and finds things that are bad. It's really good and uses AI."

**✅ GOOD:**
> "Our anomaly detection system analyzes transaction patterns in real-time using machine learning algorithms. The system identifies suspicious activities by comparing current behavior against established baselines, flagging transactions that exceed statistical thresholds for manual review."

#### Example 2: Business Communication

**❌ BAD:**
> "We can help you catch fraud maybe. Our system is awesome and has a lot of features."

**✅ GOOD:**
> "Our procurement fraud detection platform identified $2.3M in suspicious contract activity for the XYZ Agency within the first quarter, enabling early intervention and recovery. The system analyzes bidding patterns, vendor relationships, and payment anomalies across multiple procurement cycles."

#### Example 3: Social Media Post

**❌ BAD:**
> "Check out our new fraud thing! It's really cool and does AI stuff. #AI #Tech #Cool"

**✅ GOOD:**
> "Law enforcement agencies face unprecedented challenges in detecting procurement fraud across multiple contracts and vendors. Our platform uses network analysis to identify collusive patterns that humans might miss. Early detection saves taxpayer dollars and maintains public trust.

#LawEnforcementAnalytics #FraudDetection #ProcurementFraud #PublicSectorAnalytics #CriminalIntelligence #DataFusion #PredictiveAnalytics #NetworkAnalysis #GovernmentAccountability #PublicSafety"

#### Example 4: Code Documentation

**❌ BAD:**
```python
def check_fraud(x):
    # Does fraud checking
    return y
```

**✅ GOOD:**
```python
def detect_bid_rigging_pattern(vendor_ids: List[str], 
                              contract_data: pd.DataFrame) -> bool:
    \"\"\"
    Detect potential bid rigging patterns in contract awards.
    
    Analyzes bidding behavior and contract awards to identify
    collusive patterns indicating potential bid rigging schemes.
    
    Args:
        vendor_ids: List of vendor identifiers to analyze
        contract_data: DataFrame containing contract bidding and award information
        
    Returns:
        True if bid rigging pattern detected, False otherwise
        
    Example:
        >>> vendors = ['V-001', 'V-002', 'V-003']
        >>> contracts = load_contract_data('2023')
        >>> is_rigged = detect_bid_rigging_pattern(vendors, contracts)
    \"\"\"
```

### Email Communication Template

**Subject:** Procurement Fraud Detection - Q1 2023 Results

**Body:**
> Dear [Name],
> 
> I wanted to share the Q1 2023 results from our procurement fraud detection implementation:
> 
> **Key Findings:**
> - Identified $2.3M in suspicious contract activity
> - 12 contracts flagged for review
> - 3 patterns detected across multiple vendors
> 
> **Recommended Actions:**
> 1. Review flagged contracts (list attached)
> 2. Investigate identified patterns (report attached)
> 3. Schedule follow-up meeting to discuss findings
> 
> Please let me know if you'd like to discuss these findings further.
> 
> Best regards,  
> [Your Name]

---
"""
    
    def _generate_footer(self) -> str:
        """Generate footer section."""
        return """---

## 📖 Additional Resources

- [Sentinel Analytics Documentation](https://github.com/sentinel-analytics)
- [Domain Terminology Reference](./docs/domain-terminology.md)
- [Code Review Guidelines](./docs/code-review-guidelines.md)

---

**Questions or suggestions?** Contact: reichert.sentinel.ai@gmail.com

*This style guide is a living document and will be updated based on feedback and evolving requirements.*
"""
    
    def create_draft(self) -> None:
        """
        Create draft version of style guide.
        
        Generates content and saves to temporary draft file for manual review.
        """
        print("\n" + "="*60)
        print("WRITING STYLE GUIDE GENERATOR")
        print("="*60 + "\n")
        
        print("[INFO] Generating draft style guide...")
        content = self.generate_style_guide_content()
        
        # Ensure target directory exists
        self.temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Draft created: {self.temp_path}\n")
    
    def open_for_editing(self) -> None:
        """
        Open draft in appropriate editor.
        
        Attempts to open in VS Code, falls back to system default.
        Waits for editor to close before returning.
        """
        import platform
        import subprocess
        import os
        
        print("[INFO] Opening draft for manual editing...")
        print("   Review, edit, then save and close.\n")
        
        system = platform.system()
        
        try:
            if system == "Windows":
                # Try VS Code first, fall back to default
                try:
                    subprocess.run(['code', '--wait', str(self.temp_path)], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fall back to default Windows editor
                    os.startfile(str(self.temp_path))
                    input("   Press Enter after you've finished editing and closed the file...")
            
            elif system == "Darwin":  # macOS
                # Try VS Code first, fall back to default
                try:
                    subprocess.run(['code', '--wait', str(self.temp_path)], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Use default macOS editor
                    subprocess.run(['open', '-W', str(self.temp_path)], check=True)
            
            else:  # Linux
                # Try multiple editors
                editors = ['code', 'gedit', 'nano', 'vim']
                editor_found = False
                for editor in editors:
                    try:
                        if editor == 'code':
                            subprocess.run([editor, '--wait', str(self.temp_path)], check=True)
                        else:
                            subprocess.run([editor, str(self.temp_path)], check=True)
                            if editor in ['nano', 'vim']:
                                input("   Press Enter after closing the editor...")
                        editor_found = True
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                
                if not editor_found:
                    raise FileNotFoundError("No suitable editor found")
            
            print("\n[OK] Editor closed. Changes saved.")
        
        except Exception as e:
            print(f"[WARN] Could not open editor automatically: {e}")
            print(f"   Please manually edit: {self.temp_path}")
            input("\n   Press Enter when finished editing...")
    
    def request_approval(self) -> bool:
        """
        Interactive approval process.
        
        Returns:
            True if approved, False if cancelled
        """
        if not self.temp_path.exists():
            print("[ERROR] Draft file not found. Please create draft first.")
            return False
        
        print("\n" + "-"*60)
        print("APPROVAL REQUIRED")
        print("-"*60)
        print(f"\nDraft location: {self.temp_path}")
        
        # Show preview
        print("\n--- PREVIEW (first 20 lines) ---")
        with open(self.temp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:20]
            print(''.join(lines))
        print("--- (preview ends) ---\n")
        
        while True:
            print("Options:")
            print("  [v] View full content")
            print("  [e] Edit again")
            print("  [a] Approve and continue")
            print("  [c] Cancel")
            
            response = input("\nYour choice: ").strip().lower()
            
            if response == 'v':
                print("\n" + "="*60)
                print("FULL CONTENT")
                print("="*60 + "\n")
                with open(self.temp_path, 'r', encoding='utf-8') as f:
                    # Handle Unicode encoding for Windows console
                    import sys
                    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
                        try:
                            sys.stdout.reconfigure(encoding='utf-8')
                        except AttributeError:
                            pass
                    content = f.read()
                    print(content)
                print("\n" + "="*60 + "\n")
            
            elif response == 'e':
                self.open_for_editing()
                print("\n" + "-"*60)
                print("Returning to approval menu...")
                print("-"*60)
            
            elif response == 'a':
                print("\n[OK] Draft approved!")
                return True
            
            elif response == 'c':
                print("\n[INFO] Approval cancelled.")
                return False
            
            else:
                print("[WARN] Invalid choice. Please enter v, e, a, or c.")
    
    def finalize(self) -> None:
        """
        Move draft to final location.
        
        Handles overwrite confirmation and creates backup if needed.
        """
        import shutil
        
        if not self.temp_path.exists():
            print("[ERROR] Draft file not found. Please create draft first.")
            return
        
        # Check if final file exists
        if self.style_guide_path.exists():
            print(f"\n[WARN] {self.style_guide_path} already exists.")
            response = input("Overwrite? (yes/no): ").strip().lower()
            
            if response not in ['yes', 'y']:
                print("[INFO] Keeping existing file. Draft preserved.")
                return
            
            # Backup existing
            backup_path = self.style_guide_path.with_suffix('.md.backup')
            shutil.copy(self.style_guide_path, backup_path)
            print(f"[INFO] Backed up to: {backup_path}")
        
        # Move draft to final location
        shutil.move(str(self.temp_path), str(self.style_guide_path))
        print(f"[OK] Finalized: {self.style_guide_path}")
    
    def commit_to_git(self, custom_message: str = None) -> bool:
        """
        Commit style guide to git repository.
        
        Args:
            custom_message: Optional custom commit message
            
        Returns:
            True if commit succeeded, False otherwise
        """
        import subprocess
        
        print("\n" + "-"*60)
        print("GIT COMMIT")
        print("-"*60)
        
        # Check if in git repo
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--is-inside-work-tree'],
                cwd=self.target_dir,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("[WARN] Not a git repository. Skipping commit.")
                return False
        except FileNotFoundError:
            print("[WARN] Git not found. Skipping commit.")
            return False
        
        # Check for uncommitted changes
        result = subprocess.run(
            ['git', 'status', '--porcelain', 'WRITING_STYLE_GUIDE.md'],
            cwd=self.target_dir,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            print("[WARN] Style guide not in git changes. Nothing to commit.")
            return False
        
        try:
            # Add file
            subprocess.run(
                ['git', 'add', 'WRITING_STYLE_GUIDE.md'],
                cwd=self.target_dir,
                check=True
            )
            print("[OK] Added to staging")
            
            # Prepare commit message
            if custom_message:
                commit_msg = custom_message
            else:
                commit_msg = """Add Sentinel Analytics Writing Style Guide

- Domain-specific terminology for law enforcement and intelligence
- Comprehensive glossary (50+ terms)
- Hashtag standards for 5 focus areas
- Writing guidelines with examples
- Documentation best practices
- README templates and standards"""
            
            # Commit
            subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.target_dir,
                check=True
            )
            print("[OK] Committed to git")
            
            # Check if remote exists
            result = subprocess.run(
                ['git', 'remote'],
                cwd=self.target_dir,
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                push = input("\nPush to remote? (yes/no): ").strip().lower()
                if push in ['yes', 'y']:
                    branch_result = subprocess.run(
                        ['git', 'branch', '--show-current'],
                        cwd=self.target_dir,
                        capture_output=True,
                        text=True
                    )
                    branch = branch_result.stdout.strip()
                    
                    if branch:
                        subprocess.run(
                            ['git', 'push', 'origin', branch],
                            cwd=self.target_dir,
                            check=True
                        )
                        print(f"[OK] Pushed to origin/{branch}")
                    else:
                        print("[WARN] Could not determine current branch")
                else:
                    print("[INFO] Remember to push when ready:")
                    print("   git push origin <branch>")
            
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Git commit failed: {e}")
            print("\n[INFO] Commit manually:")
            print("   git add WRITING_STYLE_GUIDE.md")
            print("   git commit -m 'Add Writing Style Guide'")
            return False
    
    def execute(self) -> None:
        """
        Execute complete workflow: create → edit → approve → finalize → commit.
        
        Orchestrates the entire style guide creation process interactively.
        """
        print("\n" + "="*60)
        print("WRITING STYLE GUIDE CREATION WORKFLOW")
        print("="*60)
        
        # Step 1: Create draft
        self.create_draft()
        
        # Step 2: Open for editing
        edit = input("\nOpen for editing? (yes/no): ").strip().lower()
        if edit in ['yes', 'y']:
            self.open_for_editing()
        
        # Step 3: Request approval
        approved = self.request_approval()
        
        if not approved:
            print("\n[INFO] Style guide creation cancelled.")
            
            # Clean up draft
            cleanup = input("Delete draft? (yes/no): ").strip().lower()
            if cleanup in ['yes', 'y']:
                if self.temp_path.exists():
                    self.temp_path.unlink()
                    print("[OK] Draft deleted.")
            else:
                print(f"[INFO] Draft preserved: {self.temp_path}")
            
            return
        
        # Step 4: Finalize
        self.finalize()
        
        # Step 5: Git commit
        commit = input("\nCommit to git? (yes/no): ").strip().lower()
        if commit in ['yes', 'y']:
            self.commit_to_git()
        else:
            print("\n[INFO] Style guide created but not committed.")
            print("   Commit manually when ready:")
            print(f"   cd {self.target_dir}")
            print("   git add WRITING_STYLE_GUIDE.md")
            print("   git commit -m 'Add Writing Style Guide'")
        
        print("\n" + "="*60)
        print("[OK] STYLE GUIDE CREATION COMPLETE")
        print("="*60)
        print(f"\nFile location: {self.style_guide_path}")
    
    def write_style_guide(self, output_path: str = None, overwrite: bool = False) -> Path:
        """
        Write style guide to file.
        
        Args:
            output_path: Optional custom output path
            overwrite: If True, overwrite existing file
            
        Returns:
            Path to written file
        """
        if output_path:
            file_path = Path(output_path)
        else:
            file_path = self.style_guide_path
        
        # Check if file exists
        if file_path.exists() and not overwrite:
            raise FileExistsError(
                f"Style guide already exists: {file_path}\n"
                "Use overwrite=True to replace it."
            )
        
        # Generate content
        content = self.generate_style_guide_content()
        
        # Write to file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Style guide written to: {file_path}")
        return file_path


def main():
    """Main function for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate writing style guide for Sentinel Analytics'
    )
    parser.add_argument(
        '--target-dir',
        default='.',
        help='Directory where style guide should be written (default: current directory)'
    )
    parser.add_argument(
        '--output',
        help='Custom output file path'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing file if it exists'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Print content to console instead of writing file'
    )
    parser.add_argument(
        '--create-draft',
        action='store_true',
        help='Create draft file for manual editing'
    )
    parser.add_argument(
        '--edit-draft',
        action='store_true',
        help='Open draft file in editor'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive workflow: create draft, edit, and approve'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Complete workflow: create → edit → approve → finalize → commit'
    )
    parser.add_argument(
        '--commit-message',
        help='Custom git commit message'
    )
    
    args = parser.parse_args()
    
    creator = StyleGuideCreator(args.target_dir)
    
    # Handle complete execution workflow
    if args.execute:
        creator.execute()
        return 0
    
    # Handle interactive workflow (without finalization)
    elif args.interactive:
        # Create draft
        creator.create_draft()
        
        # Open for editing
        creator.open_for_editing()
        
        # Request approval
        if creator.request_approval():
            # Finalize draft
            creator.finalize()
            
            # Optionally commit to git
            commit = input("\nCommit to git? (yes/no): ").strip().lower()
            if commit in ['yes', 'y']:
                creator.commit_to_git(custom_message=args.commit_message)
            else:
                print("\n[INFO] Style guide created but not committed.")
                print("   Commit manually when ready:")
                print(f"   cd {creator.target_dir}")
                print("   git add WRITING_STYLE_GUIDE.md")
                print("   git commit -m 'Add Writing Style Guide'")
        else:
            print("\n[INFO] Workflow cancelled. Draft saved at:")
            print(f"    {creator.temp_path}")
            return 1
    
    elif args.create_draft:
        creator.create_draft()
        print(f"\n[OK] Draft created. Use --edit-draft to edit or --interactive for full workflow.")
    
    elif args.edit_draft:
        if not creator.temp_path.exists():
            print("[ERROR] Draft file not found. Please create draft first with --create-draft")
            return 1
        creator.open_for_editing()
        print(f"\n[OK] Editing complete. Draft saved at: {creator.temp_path}")
    
    elif args.preview:
        content = creator.generate_style_guide_content()
        # Handle Unicode encoding for Windows console
        import sys
        if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except AttributeError:
                # Python < 3.7 fallback
                import io
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        print(content)
    else:
        creator.write_style_guide(
            output_path=args.output,
            overwrite=args.overwrite
        )
        print("\n[OK] Style guide generation complete!")
        print(f"    File: {creator.style_guide_path if not args.output else args.output}")


if __name__ == '__main__':
    main()

