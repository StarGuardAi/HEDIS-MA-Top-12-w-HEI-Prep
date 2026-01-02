# Care Gap Closure Workflow Guide

## Overview

End-to-end care gap closure workflow system that manages the complete lifecycle from gap identification to closure verification.

## Workflow Stages

### 1. Gap Identification

**Auto-Detection**:
- Automatically detect gaps from claims data
- Classify by urgency and value
- Assign priority scores (P1-P4)
- Route to appropriate coordinator

**Priority Scoring**:
- **P1**: Highest value + highest urgency
- **P2**: High value or high urgency
- **P3**: Medium value and urgency
- **P4**: Low value or low urgency

**Urgency Levels**:
- **Critical**: < 30 days to deadline
- **High**: 30-60 days
- **Medium**: 60-90 days
- **Low**: > 90 days

**Auto-Assignment**:
- Assigns gaps to coordinators based on:
  - Priority level
  - Coordinator capacity
  - Expertise match
  - Geographic proximity

### 2. Outreach Planning

**Optimal Contact Time**:
- Predicts best time to contact member
- Considers time zone
- Historical contact patterns
- Member preferences

**Preferred Channel**:
- Phone
- SMS
- Email
- Mail
- In-Person

**Language Preference**:
- Detects member language preference
- Provides script templates in appropriate language

**Prior Contact History**:
- Reviews previous contact attempts
- Identifies successful channels
- Notes member preferences

**Barrier Identification**:
- Transportation issues
- Language barriers
- Financial concerns
- Health literacy
- Other barriers

**Script Templates**:
- Measure-specific scripts
- Gap reason-specific scripts
- Customizable templates

### 3. Intervention Tracking

**Contact Logging**:
- Log all contact attempts
- Document conversation notes
- Track contact outcomes:
  - Reached
  - Voicemail
  - No Answer
  - Busy
  - Wrong Number

**Follow-up Scheduling**:
- Automatic follow-up recommendations
- Based on contact outcome
- Deadline proximity
- Member response

**Barrier Tracking**:
- Document barriers identified
- Track barrier resolution
- Escalation triggers

**Escalation**:
- Automatic escalation for:
  - Critical gaps with failed attempts
  - Multiple barriers
  - Supervisor approval needed

### 4. Closure Verification

**Verification Methods**:
- **Claims**: Auto-verify from claims data
- **Lab Results**: Auto-verify from lab interfaces
- **Manual**: Supervisor-approved closure
- **Other**: Custom verification

**Auto-Closure**:
- Automatically closes when evidence received
- Links to claims/lab results
- Requires no manual intervention

**Supervisor Approval**:
- Required for exceptions
- Manual closures
- Exclusion applications

**Exclusion Documentation**:
- Document exclusion reasons
- Track excluded gaps
- Maintain audit trail

### 5. Reporting & Analytics

**Coordinator Performance**:
- Total gaps assigned
- Closure rate
- Average time to close
- Cost per closure
- In-progress gaps
- Pending verifications

**Closure Rates**:
- By measure
- By coordinator
- By geography
- By intervention type

**Time-to-Close Metrics**:
- Average
- Median
- Percentiles (25th, 75th)
- Min/Max

**ROI Analysis**:
- ROI by intervention type
- Cost per closure
- Revenue per closure
- Total ROI

**Geographic Performance**:
- Closure rates by region
- Geographic trends
- Regional comparisons

### 6. Alerts & Reminders

**Upcoming Deadlines**:
- Alerts for gaps with deadlines approaching
- Configurable days ahead (default: 30 days)
- Priority-based alerts

**Missed Appointments**:
- Alerts for missed appointments
- Automatic re-scheduling
- Follow-up reminders

**Lab Results Pending**:
- Alerts for lab results pending > threshold
- Default threshold: 14 days
- Follow-up reminders

**Lost to Follow-up**:
- Alerts for members with no contact
- Default threshold: 30 days
- Escalation triggers

**Escalation Alerts**:
- Alerts for gaps requiring escalation
- Supervisor notifications
- Priority escalation

## Integrations

### CRM System (Salesforce, etc.)
- Sync member data
- Track interactions
- Update contact history
- Export workflows

### EHR System (Epic, Cerner)
- Link to medical records
- Verify interventions
- Document outcomes
- Track appointments

### Claims Data Warehouse
- Auto-detect gaps
- Verify closures
- Track completion
- Monitor trends

### Lab Interfaces
- Receive lab results
- Auto-close gaps
- Track pending labs
- Alert on delays

### SMS/Email Platforms
- Send outreach messages
- Track delivery
- Monitor responses
- Schedule follow-ups

## Mobile Coordinator App

### Features

**Member List**:
- Assigned gaps list
- Prioritized by priority/urgency
- Quick call buttons
- Status indicators

**Quick Actions**:
- One-tap call
- Quick note entry
- Status updates
- Task completion

**Quick Stats**:
- Personal performance metrics
- Closure rate
- Total gaps

**Today's Alerts**:
- Urgent deadlines
- Missed appointments
- Lab results pending
- Lost to follow-up

### Usage

1. **View Tasks**: See assigned gaps
2. **Call Member**: One-tap calling
3. **Add Note**: Quick note entry
4. **Update Status**: Mark progress
5. **Close Gap**: Verify closure

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    GAP IDENTIFICATION                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Auto-Detect  │→ │ Classify     │→ │ Assign       │     │
│  │ from Claims  │  │ Urgency/Value│  │ Coordinator  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    OUTREACH PLANNING                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Predict      │→ │ Determine    │→ │ Generate     │     │
│  │ Contact Time │  │ Channel      │  │ Script       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  INTERVENTION TRACKING                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Log Contact  │→ │ Document     │→ │ Schedule     │     │
│  │ Attempt      │  │ Notes/Barriers│  │ Follow-up    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  CLOSURE VERIFICATION                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Link Claims │→ │ Auto-Close   │→ │ Supervisor   │     │
│  │ /Lab Results│  │ or Manual    │  │ Approval     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    REPORTING & ALERTS                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Performance │→ │ Analytics    │→ │ Alerts &     │     │
│  │ Dashboards  │  │ & ROI        │  │ Reminders    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Complete Workflow Cycle

### Example: HbA1c Gap Closure

1. **Identification** (Day 0):
   - Gap detected: Member missing HbA1c test
   - Classified: High urgency (45 days to deadline)
   - Priority: P2 (High value measure)
   - Assigned: COORD001

2. **Outreach Planning** (Day 0):
   - Optimal time: 10:00 AM (member timezone)
   - Channel: Phone (member preference)
   - Language: English
   - Script: HbA1c testing script
   - Barriers: None identified

3. **Intervention** (Day 1):
   - Contact: Phone call at 10:15 AM
   - Outcome: Reached
   - Notes: Member agrees to schedule test
   - Follow-up: Schedule lab appointment

4. **Tracking** (Day 2-14):
   - Lab appointment scheduled
   - Reminder sent
   - Lab completed
   - Results pending

5. **Verification** (Day 15):
   - Lab results received
   - Auto-closed via lab interface
   - Verified: Claims system
   - Status: CLOSED

6. **Reporting**:
   - Time to close: 15 days
   - Cost: $375 (15 days × $25/day)
   - ROI: Positive (quality bonus impact)

## Best Practices

1. **Prioritize High-Value Gaps**: Focus on P1 and P2 gaps first
2. **Use Optimal Channels**: Respect member preferences
3. **Document Everything**: Complete notes and barriers
4. **Follow Up Promptly**: Don't let gaps go stale
5. **Monitor Alerts**: Respond to urgent deadlines
6. **Track Performance**: Review coordinator metrics regularly

## Troubleshooting

### Gap Not Auto-Assigned
- Check coordinator capacity
- Verify priority scoring
- Review assignment rules

### Outreach Plan Not Generated
- Verify member data available
- Check contact history
- Review barriers

### Closure Not Verified
- Check claims/lab integration
- Verify evidence received
- Review supervisor approval

### Alerts Not Showing
- Check alert thresholds
- Verify gap status
- Review alert configuration

## Next Steps

1. **Configure Integrations**: Set up CRM, EHR, claims, lab interfaces
2. **Train Coordinators**: On workflow stages and mobile app
3. **Set Up Alerts**: Configure thresholds and notifications
4. **Monitor Performance**: Review dashboards regularly
5. **Optimize Workflow**: Adjust based on performance data

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Gap Closure Workflow** | End-to-end management | From identification to closure

