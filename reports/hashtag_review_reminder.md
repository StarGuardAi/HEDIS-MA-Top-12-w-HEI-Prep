# Quarterly Hashtag Review Reminder

**Current Review Date:** October 22, 2025  
**Next Review Due:** January 22, 2026 (3 months)

---

## 📊 Why Quarterly Reviews Matter

LinkedIn hashtag trends change rapidly, especially in:
- **AI/Healthcare** - New technologies emerge monthly
- **Medicare Advantage** - CMS policy changes affect terminology
- **Star Ratings** - Annual updates create new trending topics

**Goal:** Maximize post engagement by staying current with trending hashtags

---

## 🔄 Review Process (Every 3 Months)

### Step 1: Generate Engagement Report
```bash
python scripts/update_profile.py --engagement-report
```

**Review:**
- Which post types got most engagement?
- Which hashtag combinations performed best?
- Are there patterns in high-performing posts?

### Step 2: Research Current Trends

**LinkedIn Hashtag Analytics:**
1. Search each hashtag on LinkedIn
2. Check "# followers" count
3. Note trending topics in feed

**Industry Publications:**
- HIMSS Newsletter
- NCQA Updates
- CMS Star Ratings announcements
- Healthcare IT News

**Competitor Analysis:**
- Check posts from Jeff Schoenborn, Michael Ford
- Note which hashtags MA analytics leaders use
- Track emerging terminology

### Step 3: Update Hashtag Sets

**Edit `scripts/update_profile.py`:**

```python
HASHTAG_SETS = {
    'technical': "#NewHashtag1 #NewHashtag2 ...",
    'business': "#NewHashtag3 #NewHashtag4 ...",
    # etc.
}
```

**Document changes in this file:**
```markdown
## Hashtag Changes - [Date]

### Added:
- #NewHashtag1 - Reason: Trending in MA analytics
- #NewHashtag2 - Reason: CMS policy change

### Removed:
- #OldHashtag1 - Reason: Low engagement
- #OldHashtag2 - Reason: Replaced by more specific term

### Performance Notes:
- Business posts outperformed technical 2:1
- Diabetes-focused hashtags had 30% more engagement
```

### Step 4: Test New Hashtags

```bash
python scripts/update_profile.py --test-hashtags
```

**Verify:**
- All hashtag sets updated
- No duplicate hashtags
- Total = 10 per post (4 core + 6 context)

### Step 5: Update .cursorrules

Update the hashtag strategy section in `.cursorrules` with new hashtags.

### Step 6: Set Next Review Date

Update "Next Review Due" at top of this file (add 3 months).

---

## 📈 Current Hashtag Performance (Update After Each Review)

### Review: October 22, 2025

**Top Performing Hashtags:**
- (Update after first engagement report)

**Emerging Trends:**
- #HealthEquityIndex - New CMS focus for 2027
- #HEI2027 - Trending in MA circles
- #HEDIS2025 - Annual update discussions

**Recommended Focus:**
- Diabetes portfolio hashtags (#DiabetesCareManagement)
- Medicare Advantage specific (#MedicareStars, #CMSStarRatings)
- Technical credibility (#CursorAI, #AIinHealthcare)

**Next Steps:**
- Post Milestone 1 and track engagement
- Wait 48 hours for data
- Update linkedin_engagement_tracker.json
- Run engagement report before next review

---

## 📅 Review Schedule

| Review Date | Status | Key Changes | Engagement Impact |
|-------------|--------|-------------|-------------------|
| Oct 22, 2025 | ✅ Initial Setup | Created hashtag strategy | Baseline established |
| Jan 22, 2026 | ⏰ Due | TBD | TBD |
| Apr 22, 2026 | Pending | TBD | TBD |
| Jul 22, 2026 | Pending | TBD | TBD |
| Oct 22, 2026 | Pending | Annual review | TBD |

---

## 💡 Quick Tips

**Before Each Review:**
1. Update engagement data in `reports/linkedin_engagement_tracker.json`
2. Run engagement report: `python scripts/update_profile.py --engagement-report`
3. Read latest MA industry news

**During Review:**
1. Spend 30 minutes researching LinkedIn trends
2. Check 5-10 competitor posts
3. Update hashtags based on data + trends
4. Document all changes

**After Review:**
1. Test hashtag selection
2. Update documentation
3. Set calendar reminder for next review (3 months)
4. Post new content with updated hashtags

---

## 🎯 Success Metrics

Track these quarterly:

| Metric | Oct 2025 | Jan 2026 | Apr 2026 | Jul 2026 |
|--------|----------|----------|----------|----------|
| Avg Likes per Post | TBD | TBD | TBD | TBD |
| Avg Comments | TBD | TBD | TBD | TBD |
| Profile Views | TBD | TBD | TBD | TBD |
| Connection Requests | TBD | TBD | TBD | TBD |
| Inbound Messages | TBD | TBD | TBD | TBD |

**Goal:** 20% increase in engagement each quarter

---

## 📞 Resources

- **Engagement Tracker:** `reports/linkedin_engagement_tracker.json`
- **Update Script:** `scripts/update_profile.py`
- **Cursor Rules:** `.cursorrules` (hashtag strategy section)
- **Industry Leaders:** See `linkedin_outreach_strategy.md`

---

**Set Calendar Reminder:**
- **Date:** January 22, 2026
- **Task:** LinkedIn Hashtag Quarterly Review
- **Time:** 1 hour
- **Location:** This file + engagement report
