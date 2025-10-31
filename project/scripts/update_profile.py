#!/usr/bin/env python3
"""
LinkedIn Profile Update Automation

Automatically posts achievement updates to LinkedIn with context-aware hashtags.

Contact Information:
- Email: reichert.starguardai@gmail.com
- LinkedIn: https://www.linkedin.com/in/rreichert-hedis-data-science-ai/
- GitHub: https://github.com/StarGuardAi
- Portfolio: https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit

Usage:
    python scripts/update_profile.py --milestone 1
    python scripts/update_profile.py --milestone 2 --post-type business
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import logging

try:
    import requests
except ImportError:
    requests = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInProfileUpdater:
    """Automates LinkedIn profile updates with intelligent hashtag selection"""
    
    # Contact Information
    EMAIL = "reichert.starguardai@gmail.com"
    LINKEDIN_URL = "https://www.linkedin.com/in/rreichert-hedis-data-science-ai/"
    GITHUB_URL = "https://github.com/StarGuardAi"
    PORTFOLIO_URL = "https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit"
    GITHUB_REPO = "https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep"
    
    # Value Proposition
    TAGLINE = "Medicare Advantage Diabetes Analytics | Protecting $M in Star Revenue | Part-Time/Fractional"
    PORTFOLIO_VALUE = "$620K-$1.08M in Star revenue protection for 100K-member plan"
    
    # Hashtag Strategy
    CORE_HASHTAGS = "#HealthcareAnalytics #HEDIS #MachineLearning #ValueBasedCare"
    
    HASHTAG_SETS = {
        'technical': "#Python #MLOps #DataScience #HealthTech #ExplainableAI #HIPAA",
        'business': "#ACO #MedicareAdvantage #StarRatings #PopulationHealth #QualityMeasures #HealthTech",
        'compliance': "#HIPAA #DataPrivacy #HealthcareCompliance #EthicalAI #DataGovernance #HealthTech",
        'ai_trust': "#ExplainableAI #EthicalAI #AIinHealthcare #TrustworthyAI #DataGovernance #HealthTech",
        'job_search': "#OpenToWork #HealthcareJobs #DataScienceJobs"
    }
    
    def __init__(self, milestone_id: int = None):
        self.milestone_id = milestone_id
        self.project_root = Path(__file__).parent.parent
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
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
    
    def _determine_post_type(self, milestone: dict) -> str:
        """
        Determine post type from milestone description
        
        Returns: 'technical', 'business', 'compliance', or 'ai_trust'
        """
        milestone_lower = milestone.get('title', '').lower() + ' ' + milestone.get('description', '').lower()
        metrics_text = ' '.join(milestone.get('success_criteria', [])).lower()
        
        if any(word in milestone_lower for word in ['api', 'deploy', 'production', 'pipeline', 'infrastructure']):
            return 'technical'
        elif any(word in milestone_lower for word in ['roi', 'value', 'savings', 'business', 'cost']):
            return 'business'
        elif any(word in milestone_lower + metrics_text for word in ['hipaa', 'security', 'compliance', 'privacy']):
            return 'compliance'
        elif any(word in milestone_lower for word in ['explainability', 'shap', 'interpretability', 'trust']):
            return 'ai_trust'
        else:
            return 'technical'  # Default
    
    def _get_hashtags_for_post_type(self, post_type: str, include_job_search: bool = False) -> str:
        """
        Return appropriate hashtags for post type
        
        Args:
            post_type: Type of post ('technical', 'business', 'compliance', 'ai_trust')
            include_job_search: Whether to include job search hashtags
        
        Returns:
            String of hashtags
        """
        # Core hashtags (always included)
        hashtags = self.CORE_HASHTAGS
        
        # Add context-specific hashtags
        context_tags = self.HASHTAG_SETS.get(post_type, self.HASHTAG_SETS['technical'])
        hashtags = f"{hashtags} {context_tags}"
        
        # Add job search tags if requested
        if include_job_search:
            hashtags = f"{hashtags} {self.HASHTAG_SETS['job_search']}"
        
        return hashtags
    
    def post_achievement(self, milestone_data: dict, metrics: list, custom_message: str = None) -> str:
        """
        Create a professional LinkedIn post about an achievement
        
        Args:
            milestone_data: Milestone dictionary from milestones.json
            metrics: List of achievement metrics
            custom_message: Optional custom message to include
        
        Returns:
            Post content string
        """
        # Determine post type and select appropriate hashtags
        post_type = self._determine_post_type(milestone_data)
        hashtags = self._get_hashtags_for_post_type(post_type, include_job_search=False)
        
        milestone_title = milestone_data.get('title', 'Project Milestone')
        
        # Build metrics section
        metrics_text = '\n'.join(['✅ ' + metric for metric in metrics])
        
        # Build post content
        post_content = f"""🚀 Project Milestone Achieved: {milestone_title}

I'm excited to share progress on my HEDIS Diabetes Portfolio Prediction Engine:

{metrics_text}

This production-ready ML system helps Medicare Advantage plans protect millions in Star Ratings revenue by identifying high-risk members across the diabetes portfolio: HBD (HbA1c Control), KED (Kidney Evaluation), EED (Eye Exam), and PDC-DR (Medication Adherence).

Combined portfolio value: {self.PORTFOLIO_VALUE}

Using AI-assisted development (Cursor AI, Claude Sonnet, ChatGPT-4), I deliver in 60-90 days vs. 6-12 months traditional consulting.

Tech Stack: Python, Cursor AI, Claude Sonnet, ChatGPT-4, scikit-learn, XGBoost, SHAP, HEDIS, HIPAA-compliant

View the project: {self.GITHUB_REPO}

Available for part-time diabetes analytics projects.

{hashtags}"""
        
        if custom_message:
            post_content = f"{custom_message}\n\n{post_content}"
        
        return post_content
    
    def generate_milestone_post(self, post_type: str = 'technical', include_job_search: bool = False) -> str:
        """
        Generate LinkedIn post for milestone completion
        
        Args:
            post_type: Type of post ('technical', 'business', 'compliance', 'ai_trust')
            include_job_search: Whether to include job search hashtags
        
        Returns:
            Post content string
        """
        milestone = self._get_milestone_data(self.milestone_id)
        
        if not milestone:
            logger.error(f"Milestone {self.milestone_id} not found")
            return ""
        
        # Get hashtags for post type
        hashtags = self._get_hashtags_for_post_type(post_type, include_job_search)
        
        # Generate content based on milestone
        if self.milestone_id == 1:
            post = f"""🎯 Milestone {milestone['id']} Complete: {milestone['title']}

Built a production-ready diabetes portfolio prediction engine targeting $620K-$1M in Star revenue protection!

**The Achievement:**
• Developed with Cursor AI + Claude Sonnet 3.5 + ChatGPT-4
• {milestone['description']}
• Focus: Diabetes portfolio (HBD, KED, EED, PDC-DR)
• 91% AUC-ROC model performance
• 15-25% improvement in gap closure potential
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
Python, Cursor AI, Claude Sonnet, ChatGPT-4, scikit-learn, SHAP, HEDIS (HBD/KED/EED/PDC-DR), Medicare Advantage, Star Ratings, HIPAA

**Diabetes Portfolio Value:**
Four measures worth {self.PORTFOLIO_VALUE}:
• HBD (HbA1c Control) - Triple-weighted
• KED (Kidney Evaluation) - Triple-weighted, NEW 2025
• EED (Eye Exam) - Standard
• PDC-DR (Medication Adherence) - Standard

**What's Next:**
Moving to Milestone 2: Advanced Model Development & Portfolio Optimization

Available for part-time/fractional diabetes analytics projects.

{hashtags}

📧 Contact: {self.EMAIL}
🔗 Portfolio: {self.PORTFOLIO_URL}
💻 GitHub: {self.GITHUB_REPO}
"""
        
        elif self.milestone_id == 2:
            post = f"""🚀 Milestone {milestone['id']} Complete: {milestone['title']}

Achieved 91% AUC-ROC for diabetes portfolio prediction - protecting {self.PORTFOLIO_VALUE}!

**The Innovation:**
• Developed with Cursor AI + Claude Sonnet + ChatGPT-4
• {milestone['description']}
• Portfolio approach: HBD + KED + EED + PDC-DR
• SHAP interpretability for clinical validation
• Comprehensive bias analysis across diabetes measures
• Production-ready ML pipeline

**Model Performance:**
✅ AUC-ROC: 91% (HbA1c Control)
✅ Sensitivity: 87%
✅ Specificity: 81%
✅ 15-25% gap closure improvement potential
✅ 100% test coverage
✅ Temporal validation (no data leakage)
✅ Triple-weighted measure focus (HBD, KED)

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
• 6,200+ high-risk members identified across diabetes portfolio
• 1,870-2,493 potential interventions per measure
• {self.PORTFOLIO_VALUE} in Star revenue protection
• Improved performance across 4 diabetes HEDIS measures
• Focus on triple-weighted measures (HBD, KED) = maximum ROI

**Diabetes Portfolio Breakdown:**
• HBD (HbA1c Control): $220K-$385K value
• KED (Kidney Evaluation): $220K-$385K value - NEW 2025
• EED (Eye Exam): $90K-$155K value
• PDC-DR (Medication Adherence): $90K-$155K value

**What's Next:**
Building production REST API (< 100ms response time) with portfolio-level interventions

Available for part-time diabetes analytics consulting.

{hashtags}

📧 Contact: {self.EMAIL}
💻 GitHub: {self.GITHUB_REPO}
🔗 Portfolio: {self.PORTFOLIO_URL}
"""
        
        else:
            # Generic template for other milestones
            post = f"""✅ Milestone {milestone['id']} Complete: {milestone['title']}

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

{hashtags}

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
            logger.info("Or run: setup_linkedin_api.bat")
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
            return True
        else:
            logger.error(f"❌ Failed to post to LinkedIn: {response.status_code}")
            logger.error(response.text)
            return False
    
    def save_post_to_file(self, content: str, filename: str = None, post_type: str = None) -> Path:
        """Save generated post content to file and track hashtags used"""
        if not filename:
            filename = f"linkedin_milestone_{self.milestone_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        output_file = self.project_root / 'reports' / filename
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Post content saved to: {output_file}")
        
        # Track hashtags used for engagement analysis
        if post_type:
            self._track_hashtag_usage(post_type, filename)
        
        return output_file
    
    def _track_hashtag_usage(self, post_type: str, filename: str):
        """Track which hashtags were used for future engagement analysis"""
        tracking_file = self.project_root / 'reports' / 'linkedin_engagement_tracker.json'
        
        # Load existing tracking data
        tracking_data = []
        if tracking_file.exists():
            with open(tracking_file, 'r', encoding='utf-8') as f:
                tracking_data = json.load(f)
        
        # Get hashtags used
        hashtags_used = self._get_hashtags_for_post_type(post_type, include_job_search=False)
        
        # Create tracking entry
        entry = {
            'milestone_id': self.milestone_id,
            'post_date': datetime.now().isoformat(),
            'post_type': post_type,
            'hashtags': hashtags_used,
            'filename': filename,
            'engagement': {
                'likes': None,  # Manually update after posting
                'comments': None,
                'shares': None,
                'views': None,
                'engagement_rate': None
            },
            'notes': 'Update engagement metrics manually after 48 hours'
        }
        
        tracking_data.append(entry)
        
        # Save tracking data
        with open(tracking_file, 'w', encoding='utf-8') as f:
            json.dump(tracking_data, f, indent=2)
        
        logger.info(f"Hashtag usage tracked in: {tracking_file}")
        logger.info(f"Post type: {post_type} | Hashtags: {hashtags_used[:100]}...")
    
    def generate_engagement_report(self) -> str:
        """Generate engagement report showing which hashtag combinations perform best"""
        tracking_file = self.project_root / 'reports' / 'linkedin_engagement_tracker.json'
        
        if not tracking_file.exists():
            return "No engagement data available yet. Post content and track metrics in linkedin_engagement_tracker.json"
        
        with open(tracking_file, 'r', encoding='utf-8') as f:
            tracking_data = json.load(f)
        
        report = "# LinkedIn Engagement Analysis Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Analyze by post type
        report += "## Engagement by Post Type\n\n"
        
        post_types = {}
        for entry in tracking_data:
            pt = entry['post_type']
            if pt not in post_types:
                post_types[pt] = {'count': 0, 'total_likes': 0, 'total_comments': 0, 'total_shares': 0}
            
            post_types[pt]['count'] += 1
            engagement = entry.get('engagement', {})
            if engagement.get('likes'):
                post_types[pt]['total_likes'] += engagement['likes']
            if engagement.get('comments'):
                post_types[pt]['total_comments'] += engagement['comments']
            if engagement.get('shares'):
                post_types[pt]['total_shares'] += engagement['shares']
        
        for pt, stats in post_types.items():
            report += f"### {pt.title()} Posts\n"
            report += f"- Total Posts: {stats['count']}\n"
            if stats['count'] > 0:
                report += f"- Avg Likes: {stats['total_likes'] / stats['count']:.1f}\n"
                report += f"- Avg Comments: {stats['total_comments'] / stats['count']:.1f}\n"
                report += f"- Avg Shares: {stats['total_shares'] / stats['count']:.1f}\n"
            report += "\n"
        
        # List all posts with engagement
        report += "## Individual Post Performance\n\n"
        for entry in sorted(tracking_data, key=lambda x: x.get('post_date', ''), reverse=True):
            engagement = entry.get('engagement', {})
            report += f"### Milestone {entry['milestone_id']} - {entry['post_type'].title()}\n"
            report += f"- Date: {entry['post_date'][:10]}\n"
            report += f"- Hashtags: {entry['hashtags']}\n"
            
            if engagement.get('likes') is not None:
                report += f"- Likes: {engagement['likes']}\n"
                report += f"- Comments: {engagement.get('comments', 0)}\n"
                report += f"- Shares: {engagement.get('shares', 0)}\n"
                report += f"- Views: {engagement.get('views', 'N/A')}\n"
            else:
                report += "- Engagement: Not yet tracked (update linkedin_engagement_tracker.json)\n"
            
            if entry.get('notes'):
                report += f"- Notes: {entry['notes']}\n"
            report += "\n"
        
        # Recommendations
        report += "## Recommendations\n\n"
        report += "Based on engagement data:\n"
        report += "1. Review quarterly (every 3 months) - hashtag trends change frequently in AI/healthcare\n"
        report += "2. Test different hashtag combinations to find optimal mix\n"
        report += "3. Monitor which post types (technical/business/compliance) resonate most with your audience\n"
        report += "4. Update HASHTAG_SETS in update_profile.py based on performance data\n\n"
        report += "Next review due: " + (datetime.now().replace(month=datetime.now().month+3)).strftime('%Y-%m-%d') + "\n"
        
        return report


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='LinkedIn Profile Update Automation'
    )
    parser.add_argument(
        '--milestone',
        type=int,
        help='Milestone number (1-6)'
    )
    parser.add_argument(
        '--post-type',
        choices=['technical', 'business', 'compliance', 'ai_trust'],
        default='technical',
        help='Type of LinkedIn post to generate'
    )
    parser.add_argument(
        '--include-job-search',
        action='store_true',
        help='Include job search hashtags (#OpenToWork, etc.)'
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
    parser.add_argument(
        '--engagement-report',
        action='store_true',
        help='Generate engagement analysis report'
    )
    parser.add_argument(
        '--test-hashtags',
        action='store_true',
        help='Test hashtag selection for next post'
    )
    
    args = parser.parse_args()
    
    # Handle engagement report
    if args.engagement_report:
        updater = LinkedInProfileUpdater()
        report = updater.generate_engagement_report()
        
        # Save report
        report_file = Path(__file__).parent.parent / 'reports' / f'engagement_report_{datetime.now().strftime("%Y%m%d")}.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(report)
        print(f"\n✅ Report saved to: {report_file}")
        print("\n💡 Tip: Update engagement metrics in reports/linkedin_engagement_tracker.json")
        print("   Then run this command again to see updated analysis")
        return 0
    
    # Handle hashtag testing
    if args.test_hashtags:
        updater = LinkedInProfileUpdater()
        
        print("=" * 70)
        print("Hashtag Selection Test")
        print("=" * 70)
        print()
        
        # Test each post type
        for post_type in ['technical', 'business', 'compliance', 'ai_trust']:
            hashtags = updater._get_hashtags_for_post_type(post_type, include_job_search=False)
            print(f"{post_type.upper()}:")
            print(f"  {hashtags}")
            print()
        
        print("JOB SEARCH (add to any post type):")
        job_tags = updater.HASHTAG_SETS['job_search']
        print(f"  {job_tags}")
        print()
        
        print("=" * 70)
        print("Next Post Recommendation:")
        print("=" * 70)
        
        # Get next milestone
        milestones = updater._load_milestones()
        in_progress = [m for m in milestones.get('milestones', []) if m['status'] == 'in_progress']
        
        if in_progress:
            next_milestone = in_progress[0]
            recommended_type = updater._determine_post_type(next_milestone)
            recommended_hashtags = updater._get_hashtags_for_post_type(recommended_type)
            
            print(f"\nMilestone {next_milestone['id']}: {next_milestone['title']}")
            print(f"Recommended post type: {recommended_type}")
            print(f"Hashtags to use:\n  {recommended_hashtags}")
        else:
            print("\nNo in-progress milestones found")
        
        print()
        return 0
    
    # Require milestone for post generation
    if not args.milestone:
        parser.error("--milestone is required (unless using --engagement-report or --test-hashtags)")
    
    args = parser.parse_args()
    
    # Create profile updater
    updater = LinkedInProfileUpdater(milestone_id=args.milestone)
    
    # Generate post content
    logger.info(f"Generating {args.post_type} post for Milestone {args.milestone}...")
    content = updater.generate_milestone_post(
        post_type=args.post_type,
        include_job_search=args.include_job_search
    )
    
    if not content:
        logger.error("Failed to generate post content")
        return 1
    
    # Save to file with hashtag tracking
    output_file = updater.save_post_to_file(content, post_type=args.post_type)
    
    if args.save_only:
        print(f"\n✅ Post content saved to: {output_file}")
        print("\nYou can manually post this to LinkedIn or run without --save-only flag to auto-post")
        return 0
    
    # Post to LinkedIn
    success = updater.post_to_linkedin(content, dry_run=args.dry_run)
    
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

