#!/usr/bin/env python3
"""
LinkedIn Publishing Automation for HEDIS GSD Milestones

Automatically posts milestone completions to LinkedIn using LinkedIn API.
Requires LinkedIn Developer credentials.

Setup:
1. Create LinkedIn App: https://www.linkedin.com/developers/apps
2. Get Client ID and Client Secret
3. Set environment variables:
   - LINKEDIN_CLIENT_ID
   - LINKEDIN_CLIENT_SECRET
   - LINKEDIN_ACCESS_TOKEN (or use OAuth flow)

Usage:
    python scripts/publish_to_linkedin.py --milestone 1
    python scripts/publish_to_linkedin.py --milestone 2 --post-type technical
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import logging

# Optional: LinkedIn API (requires linkedin-api or requests)
try:
    import requests
except ImportError:
    requests = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInPublisher:
    """Automates posting milestones to LinkedIn"""
    
    # Contact Information
    EMAIL = "reichert.starguardai@gmail.com"
    LINKEDIN_URL = "https://www.linkedin.com/in/rreichert-hedis-data-science-ai/"
    GITHUB_URL = "https://github.com/StarGuardAi"
    GITHUB_REPO = "https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep"
    PORTFOLIO_URL = "https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit"
    
    # Hashtag Strategy (Following LinkedIn Best Practices)
    CORE_HASHTAGS = "#HealthcareAnalytics #HEDIS #MachineLearning #ValueBasedCare"
    TECHNICAL_HASHTAGS = "#Python #MLOps #DataScience #HealthTech #ExplainableAI #HIPAA"
    BUSINESS_HASHTAGS = "#ACO #MedicareAdvantage #StarRatings #PopulationHealth #QualityMeasures #HealthTech"
    COMPLIANCE_HASHTAGS = "#HIPAA #DataPrivacy #HealthcareCompliance #EthicalAI #DataGovernance #HealthTech"
    
    def __init__(self, milestone_id: int = None):
        self.milestone_id = milestone_id
        self.project_root = Path(__file__).parent.parent
        
        # LinkedIn API credentials (from environment)
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        
        # Load milestone data
        self.milestones = self._load_milestones()
        
    def _load_milestones(self) -> dict:
        """Load milestone data from milestones.json"""
        milestone_file = self.project_root / 'milestones.json'
        
        if not milestone_file.exists():
            logger.error(f"Milestones file not found: {milestone_file}")
            return {}
        
        with open(milestone_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    def _get_milestone_data(self, milestone_id: int) -> dict:
        """Get specific milestone data"""
        for milestone in self.milestones.get('milestones', []):
            if milestone['id'] == milestone_id:
                return milestone
        return None
    
    def generate_post_content(self, post_type: str = 'technical') -> str:
        """
        Generate LinkedIn post content for milestone
        
        Args:
            post_type: 'technical', 'impact', or 'storytelling'
        """
        milestone = self._get_milestone_data(self.milestone_id)
        
        if not milestone:
            logger.error(f"Milestone {self.milestone_id} not found")
            return ""
        
        # Check if milestone is completed
        if milestone['status'] != 'completed':
            logger.warning(f"Milestone {self.milestone_id} is not completed yet")
        
        if post_type == 'technical':
            return self._generate_technical_post(milestone)
        elif post_type == 'impact':
            return self._generate_impact_post(milestone)
        elif post_type == 'storytelling':
            return self._generate_storytelling_post(milestone)
        else:
            return self._generate_technical_post(milestone)
    
    def _generate_technical_post(self, milestone: dict) -> str:
        """Generate technical deep-dive post"""
        
        # Get specific content based on milestone
        if milestone['id'] == 1:
            post = f"""🎯 **Milestone {milestone['id']} Complete: {milestone['title']}**

Built a production-ready healthcare ML pipeline using cutting-edge AI-assisted development!

**The Achievement:**
• Built with Cursor AI + Claude Sonnet 3.5 + ChatGPT-4
• {milestone['description']}
• 91% AUC-ROC model performance
• 100% HIPAA compliance
• 60% faster development with AI tools

**Key Deliverables:**
"""
            for deliverable in milestone.get('deliverables', []):
                post += f"✅ {deliverable}\n"
            
            post += f"""
**Success Criteria Met:**
"""
            for criterion in milestone.get('success_criteria', []):
                post += f"✅ {criterion}\n"
            
            post += f"""
**AI-Assisted Development:**
🤖 Cursor AI: Intelligent code generation and completion
🧠 Claude Sonnet: Healthcare compliance code reviews
💬 ChatGPT-4: HEDIS specification interpretation

**Tech Stack:**
Python, scikit-learn, pandas, NumPy, SHAP, pytest, HEDIS, HIPAA

**What's Next:**
Moving to Milestone {milestone['id'] + 1}: API Development & Testing

{self.CORE_HASHTAGS} {self.TECHNICAL_HASHTAGS}

📧 Contact: {self.EMAIL}
💻 GitHub: {self.GITHUB_REPO}
🔗 Portfolio: {self.PORTFOLIO_URL}
"""
        
        elif milestone['id'] == 2:
            post = f"""🚀 **Milestone {milestone['id']} Complete: {milestone['title']}**

Achieved 91% AUC-ROC for predicting diabetic patient risk using AI-assisted development!

**The Innovation:**
• Developed with Cursor AI + Claude Sonnet + ChatGPT-4
• {milestone['description']}
• SHAP interpretability for clinical validation
• Comprehensive bias analysis
• Production-ready ML pipeline

**Model Performance:**
✅ AUC-ROC: 91%
✅ Sensitivity: 87%
✅ Specificity: 81%
✅ 100% test coverage
✅ Temporal validation (no data leakage)

**Key Features:**
"""
            for deliverable in milestone.get('deliverables', []):
                post += f"• {deliverable}\n"
            
            post += f"""
**AI Tools Accelerated Development:**
• Cursor AI generated boilerplate and test fixtures
• Claude Sonnet performed 6 compliance code reviews
• ChatGPT helped interpret HEDIS clinical specifications

**Business Impact:**
• 6,200+ high-risk members identified
• 1,870-2,493 potential interventions
• Improved HEDIS quality measure performance

**What's Next:**
Building production REST API (< 100ms response time)

{self.CORE_HASHTAGS} {self.BUSINESS_HASHTAGS}

📧 Contact: {self.EMAIL}
💻 GitHub: {self.GITHUB_REPO}
🔗 Portfolio: {self.PORTFOLIO_URL}
"""
        
        else:
            # Generic template for other milestones
            post = f"""✅ **Milestone {milestone['id']} Complete: {milestone['title']}**

{milestone['description']}

**Deliverables:**
"""
            for deliverable in milestone.get('deliverables', []):
                post += f"✅ {deliverable}\n"
            
            post += f"""
**Success Criteria:**
"""
            for criterion in milestone.get('success_criteria', []):
                post += f"✅ {criterion}\n"
            
            post += f"""
**Completion Date:** {milestone.get('completion_date', 'TBD')}

{self.CORE_HASHTAGS} {self.TECHNICAL_HASHTAGS}

📧 Contact: {self.EMAIL}
💻 GitHub: {self.GITHUB_REPO}
"""
        
        return post
    
    def _generate_impact_post(self, milestone: dict) -> str:
        """Generate impact-focused post"""
        post = f"""🏥 **Healthcare AI Milestone: {milestone['title']}**

Just completed a major step in building AI that helps prevent diabetic complications.

**The Impact:**
{milestone['description']}

For a health plan with 25,000 diabetic members:
📊 Identifies ~6,200 high-risk patients
🎯 Enables proactive intervention
💰 Prevents costly complications
📈 Improves quality scores

**What This Means:**
Early identification → Timely intervention → Better outcomes

**Key Achievements:**
"""
        for deliverable in milestone.get('deliverables', []):
            post += f"✅ {deliverable}\n"
        
        post += f"""
**Built with Modern AI Tools:**
Cursor AI + Claude Sonnet + ChatGPT accelerated development 60%

What's your experience with AI in healthcare?

{self.CORE_HASHTAGS} {self.BUSINESS_HASHTAGS}

📧 Contact: {self.EMAIL}
💻 GitHub: {self.GITHUB_REPO}
"""
        return post
    
    def _generate_storytelling_post(self, milestone: dict) -> str:
        """Generate storytelling format post"""
        post = f"""💡 **The Question That Started It All**

"Why didn't we catch this earlier?"

A care manager asked after a diabetic patient was hospitalized with preventable complications.

That question led to Milestone {milestone['id']}: {milestone['title']}

**What We Built:**
{milestone['description']}

**The Results:**
"""
        for criterion in milestone.get('success_criteria', []):
            post += f"• {criterion}\n"
        
        post += f"""
**The Innovation:**
Used Cursor AI + Claude Sonnet + ChatGPT to build this 60% faster while maintaining full HIPAA compliance.

**What It Means:**
No more "Why didn't we catch this earlier?"

Now we identify risk BEFORE complications occur.

That's the power of healthcare AI. 🚀

{self.CORE_HASHTAGS} {self.COMPLIANCE_HASHTAGS}

📧 Contact: {self.EMAIL}
💻 GitHub: {self.GITHUB_REPO}
"""
        return post
    
    def post_to_linkedin(self, content: str, dry_run: bool = False) -> bool:
        """
        Post content to LinkedIn using API
        
        Args:
            content: Post content
            dry_run: If True, only print content without posting
        
        Returns:
            True if successful, False otherwise
        """
        if dry_run:
            logger.info("=== DRY RUN - Post Content ===")
            print(content)
            logger.info("=" * 50)
            return True
        
        if not requests:
            logger.error("requests library not installed. Run: pip install requests")
            return False
        
        if not self.access_token:
            logger.error("LinkedIn access token not found in environment")
            logger.info("Set LINKEDIN_ACCESS_TOKEN environment variable")
            return False
        
        # LinkedIn API endpoint
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Get user profile (for author URN)
        profile_url = "https://api.linkedin.com/v2/me"
        profile_response = requests.get(profile_url, headers=headers)
        
        if profile_response.status_code != 200:
            logger.error(f"Failed to get LinkedIn profile: {profile_response.status_code}")
            logger.error(profile_response.text)
            return False
        
        profile_data = profile_response.json()
        author_urn = f"urn:li:person:{profile_data['id']}"
        
        # Prepare post data
        post_data = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        # Post to LinkedIn
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            logger.info("✅ Successfully posted to LinkedIn!")
            
            # Update milestone publishing status
            self._update_publishing_status('linkedin', 'published')
            return True
        else:
            logger.error(f"❌ Failed to post to LinkedIn: {response.status_code}")
            logger.error(response.text)
            return False
    
    def _update_publishing_status(self, platform: str, status: str):
        """Update publishing status in milestones.json"""
        milestone_file = self.project_root / 'milestones.json'
        
        with open(milestone_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for milestone in data.get('milestones', []):
            if milestone['id'] == self.milestone_id:
                milestone['publishing_status'][platform] = status
                break
        
        # Update last_updated timestamp
        data['last_updated'] = datetime.now().isoformat()
        
        with open(milestone_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Updated {platform} status to '{status}' for Milestone {self.milestone_id}")
    
    def save_post_to_file(self, content: str, filename: str = None):
        """Save generated post content to file"""
        if not filename:
            filename = f"linkedin_milestone_{self.milestone_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        output_file = self.project_root / 'reports' / filename
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Post content saved to: {output_file}")
        return output_file


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Publish HEDIS GSD milestones to LinkedIn'
    )
    parser.add_argument(
        '--milestone',
        type=int,
        required=True,
        help='Milestone number (1-6)'
    )
    parser.add_argument(
        '--post-type',
        choices=['technical', 'impact', 'storytelling'],
        default='technical',
        help='Type of LinkedIn post to generate'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Generate content but do not post'
    )
    parser.add_argument(
        '--save-only',
        action='store_true',
        help='Save content to file without posting'
    )
    
    args = parser.parse_args()
    
    # Create publisher
    publisher = LinkedInPublisher(milestone_id=args.milestone)
    
    # Generate post content
    logger.info(f"Generating {args.post_type} post for Milestone {args.milestone}...")
    content = publisher.generate_post_content(post_type=args.post_type)
    
    if not content:
        logger.error("Failed to generate post content")
        return 1
    
    # Save to file
    output_file = publisher.save_post_to_file(content)
    
    if args.save_only:
        print(f"\n✅ Post content saved to: {output_file}")
        print("\nYou can manually post this to LinkedIn or run without --save-only flag to auto-post")
        return 0
    
    # Post to LinkedIn
    success = publisher.post_to_linkedin(content, dry_run=args.dry_run)
    
    if success:
        if args.dry_run:
            print("\n✅ DRY RUN complete. Content generated above.")
            print(f"📄 Content also saved to: {output_file}")
            print("\nTo actually post, run without --dry-run flag")
        else:
            print("\n✅ Successfully posted to LinkedIn!")
            print(f"📄 Content saved to: {output_file}")
        return 0
    else:
        print("\n❌ Failed to post to LinkedIn")
        print(f"📄 Content saved to: {output_file}")
        print("\nYou can manually copy and post this content")
        return 1


if __name__ == "__main__":
    sys.exit(main())


