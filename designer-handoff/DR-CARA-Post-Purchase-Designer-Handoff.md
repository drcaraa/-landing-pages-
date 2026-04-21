# DR. CARA | Post-Purchase Experience
## Website Designer Handoff Document

**Prepared for:** Website Designer
**Prepared by:** Dr. Cara Alexander
**Date:** April 2026
**Project:** Post-Purchase Client Experience — Squarespace Build

---

# PART 1: HIGH-LEVEL OVERVIEW

---

## 1. Project Summary

We need to build the post-purchase client experience on our existing Squarespace Business site (drcara.net). When a client purchases one of our two products, they are redirected to a confirmation page (hosted on Vercel) and receive an automated email sequence (handled by Google Apps Script). Their ongoing content access — session recordings, course materials, and premium resources — lives on Squarespace.

**Your job is to build the Squarespace pages. Everything else is already built or automated.**

---

## 2. What the Designer IS and IS NOT Responsible For

### YOU ARE BUILDING (Squarespace):
- Replay Vault course page (session recordings)
- GroundID Leader course page (12-week cohort content)
- Member Area (premium gated content)
- Prompt Guide page (downloadable PDFs)

### ALREADY BUILT (Do NOT touch):
- Landing pages and quiz (Vercel — separate hosting)
- Confirmation pages after purchase (Vercel)
- Payment processing (Stripe)
- Automated email sequences (Google Apps Script)
- Virtual Mind AI platform (Delphi.ai — external tool)

---

## 3. How Everything Connects

```
CLIENT JOURNEY:

  Quiz (Vercel)
    |
    v
  Results + Landing Page (Vercel)
    |
    v
  Payment (Stripe via drcara.net)
    |
    +---> Confirmation Page (Vercel)
    |
    +---> Google Sheet (CRM — automatic)
    |
    +---> Welcome Email (Gmail — automatic)
    |
    +---> Squarespace Access (WHAT YOU ARE BUILDING)
            |
            +---> /replay-vault        [Squarespace Course]
            +---> /groundid-leader     [Squarespace Course]
            +---> /member-area         [Squarespace Member Site]
            +---> /prompt-guide        [Squarespace Page]
```

---

## 4. What to Build in Squarespace — Summary

| # | Page | URL Slug | Type | Access |
|---|------|----------|------|--------|
| 1 | Replay Vault | `/replay-vault` | Squarespace Course | Members only (VM subscribers + GroundID enrollees) |
| 2 | GroundID Leader | `/groundid-leader` | Squarespace Course | GroundID Leader enrollees only |
| 3 | Member Area | `/member-area` | Squarespace Member Site | All paying members |
| 4 | Prompt Guide | `/prompt-guide` | Member Page or Digital Product | All paying members |

---

## 5. Brand Reference

### Colors

**Primary Brand Colors:**

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Orange | `#E8600A` | CTAs, buttons, highlights, accent borders |
| Orange Dark | `#C44D00` | Button hover states |
| Orange Light | `#FFF0E5` | Callout backgrounds |
| Gold | `#C9A850` | Footer borders, premium accent |

**Profile-Specific Accent Colors:**

| Profile | Hex | Usage |
|---------|-----|-------|
| The Architect | `#c84200` | Deep burnt orange |
| The Carrier | `#c89000` | Golden amber |
| The Performer | `#d81360` | Deep magenta |
| The Sentinel | `#df4f0f` | Orange-red |

**Text & Background Colors:**

| Color | Hex | Usage |
|-------|-----|-------|
| Dark (headings) | `#2A2320` | Primary headings |
| Body Text | `#4A3F38` | Paragraph text |
| Muted | `#A09080` | Captions, footer text |
| Cream Background | `#FFFAF5` | Content boxes, summaries |
| Subtle Border | `#E8E0D8` | Dividers, box borders |
| Success Green | `#2E7D4F` | Confirmation states, guarantees |

### Fonts

| Type | Font | Fallback |
|------|------|----------|
| Headlines / Serif | EB Garamond (400, 500, 600, 700) | Georgia, Times New Roman |
| Body / Sans-serif | System stack | -apple-system, Segoe UI, Arial |

### Tone & Voice
- Clinical but warm. Direct but not cold.
- Speaks to leaders as equals, not students.
- Uses "you" and "the work" frequently.
- Avoids hype, urgency, or exclamation points.
- Framework language: RPR (Receive-Perceive-Respond), Leadership Origin Profile, GroundID, Virtual Mind.

### Design References
Review these existing pages for visual tone and layout patterns:
- Landing pages: hosted on Vercel (will provide URLs)
- Confirmation pages: `virtual-mind-confirmation.html` and `groundid-leader-confirmation.html`

---

## 6. Two Products — What Each Client Gets

### Product 1: Virtual Mind ($49/month subscription)

| Detail | Value |
|--------|-------|
| Price | $49/month, cancel anytime |
| Access | 24/7 unlimited AI coaching conversations |
| Platform | Delphi.ai (external — not on Squarespace) |
| Squarespace access | Replay Vault + Member Area + Prompt Guide |
| Live component | Weekly GroundID Live sessions (Zoom) |

### Product 2: GroundID Leader ($9,000 / $3,000 x 3 months)

| Detail | Value |
|--------|-------|
| Price | $9,000 total ($3,000/month x 3) |
| Format | 12 live 90-minute sessions with Dr. Cara |
| Cohort size | Maximum 10 leaders |
| Enrollment | Quarterly cohorts |
| Squarespace access | GroundID Leader course + Replay Vault + Member Area + Prompt Guide |
| Physical product | RPR Practice Deck shipped before Week 1 |
| Bonus | 30-day Virtual Mind pre-access |
| Post-program | 90-day community access |
| Guarantee | 2 sessions, full Month 1 refund |

---
---

# PART 2: DETAILED BUILD SPECS (APPENDIX)

---

## Appendix A: Replay Vault — Squarespace Course

**URL:** `drcara.net/replay-vault`
**Type:** Squarespace Course
**Access:** Members only (all paying members — VM subscribers + GroundID enrollees)

### Purpose
Houses recorded GroundID Live sessions so members can watch/rewatch at any time.

### Course Structure

```
REPLAY VAULT
  |
  +-- Section: [Month Year] (e.g., "April 2026")
  |     +-- Lesson: "GroundID Live — [Date] — [Topic]"
  |     +-- Lesson: "GroundID Live — [Date] — [Topic]"
  |
  +-- Section: [Month Year] (e.g., "March 2026")
  |     +-- Lesson: "GroundID Live — [Date] — [Topic]"
  |     +-- ...
```

### Content Per Lesson
- Video: Zoom recording (uploaded weekly after each session)
- Description: 2-3 sentences about what was covered
- No quizzes, no completion tracking needed

### Workflow
1. Dr. Cara records GroundID Live on Zoom (weekly)
2. Downloads recording from Zoom
3. Uploads to Squarespace as a new lesson under the current month's section
4. Members receive access immediately

### Design Notes
- Clean, minimal layout
- Organized reverse-chronologically (newest first)
- Each section = one month
- No progress tracking needed — this is a library, not a course to complete

---

## Appendix B: GroundID Leader Course — Squarespace Course

**URL:** `drcara.net/groundid-leader`
**Type:** Squarespace Course
**Access:** GroundID Leader enrollees only (separate access from general members)

### Purpose
Central hub for the 12-week GroundID Leader experience. Houses pre-work, session recordings, and cohort resources.

### Course Structure

```
GROUNDID LEADER
  |
  +-- Module 1: PRE-WORK (Available immediately after enrollment)
  |     +-- Lesson: "Welcome to GroundID Leader" (text + video welcome)
  |     +-- Lesson: "Leadership Identity Brief" (intake form — link to Google Form)
  |     +-- Lesson: "Shipping Address Form" (for RPR Practice Deck — link to Google Form)
  |     +-- Lesson: "Your Virtual Mind Pre-Access" (instructions + link to delphi.ai/drcara)
  |     +-- Lesson: "Session Schedule & Zoom Links" (all 12 session dates + calendar links)
  |
  +-- Module 2: SESSIONS (Added weekly as sessions occur)
  |     +-- Lesson: "Session 1 — [Topic]" (recording + notes)
  |     +-- Lesson: "Session 2 — [Topic]"
  |     +-- ... through Session 12
  |
  +-- Module 3: RESOURCES
        +-- Lesson: "RPR Practice Deck — Digital Companion" (PDF download)
        +-- Lesson: "Your Leadership Origin Profile" (link to grounid.com)
        +-- Lesson: "Premium Prompt Guide" (PDF download, profile-specific)
        +-- Lesson: "Post-Program Community" (access info for 90-day post-program)
```

### Content Per Session Lesson
- Video: Zoom recording of the session
- Description: Session topic, key takeaways
- Optional: Any handouts or worksheets from that session

### Design Notes
- Feels premium and cohort-specific
- Module 1 (Pre-Work) should feel urgent/action-oriented — these are tasks to complete before the program starts
- Module 2 (Sessions) grows over 12 weeks — starts empty, fills up
- Module 3 (Resources) is the evergreen reference library

---

## Appendix C: Member Area — Squarespace Member Site

**URL:** `drcara.net/member-area`
**Type:** Squarespace Member Site
**Access:** All paying members

### Purpose
Premium content hub for all members. Houses downloadable resources and member-exclusive content.

### Pages to Create

```
MEMBER AREA
  |
  +-- Page: "Premium Prompt Guides"
  |     +-- The Architect Prompt Guide (PDF download)
  |     +-- The Carrier Prompt Guide (PDF download)
  |     +-- The Performer Prompt Guide (PDF download)
  |     +-- The Sentinel Prompt Guide (PDF download)
  |
  +-- Page: "Resources"
  |     +-- RPR Framework Overview (PDF)
  |     +-- Leadership Origin Profile Guide (link to grounid.com)
  |     +-- Virtual Mind Quick Start (text + link to delphi.ai/drcara)
  |
  +-- Page: "Member Insights" (Optional — for future use)
        +-- Member-only blog posts or articles from Dr. Cara
        +-- Can be added over time
```

### Design Notes
- Clean, library-style layout
- PDFs should be easy to find and download
- Each Prompt Guide should be visually distinguished (use profile colors)
- This area should feel exclusive but not complicated

---

## Appendix D: Post-Purchase Email Flow (For Context)

The designer does NOT build this. It is automated via Google Apps Script + Gmail. But the designer needs to understand what clients receive so the Squarespace experience is consistent.

### Virtual Mind Email Sequence

| Day | Email Subject | Key Content | Links In Email |
|-----|--------------|-------------|----------------|
| 0 (instant) | "Welcome to Virtual Mind — Your access is live" | Access links, profile info, GroundID Live schedule | delphi.ai/drcara, drcara.net/replay-vault, drcara.net/prompt-guide |
| 3 | "Three prompts for The [Profile]" | 3 profile-specific conversation starters for Virtual Mind | delphi.ai/drcara |
| 7 | "This week's GroundID Live is yours" | GroundID Live details, what to bring, Replay Vault link | delphi.ai/drcara, drcara.net/replay-vault |

### GroundID Leader Email Sequence

| Day | Email Subject | Key Content | Links In Email |
|-----|--------------|-------------|----------------|
| 0 (instant) | "Welcome to GroundID Leader — You are in" | 5 action items, enrollment summary, guarantee | drcara.net/groundid-leader, delphi.ai/drcara |
| 2 | "Your Leadership Identity Brief — complete before we begin" | Reminder to complete intake form | drcara.net/groundid-leader, delphi.ai/drcara |
| 5 | "Your Virtual Mind pre-access — use it before Session 1" | Pattern-noticing guidance, VM access | delphi.ai/drcara |

### Why This Matters For The Designer
- Clients arrive at Squarespace pages via links in these emails
- The landing experience on `/replay-vault`, `/groundid-leader`, `/member-area`, and `/prompt-guide` must match the tone and visual quality of the emails
- Clients will land on these pages within their first week — first impressions matter

---

## Appendix E: Client Journey Maps

### Journey 1: Virtual Mind Subscriber

```
DAY 0: Purchase ($49/month)
  |
  +---> Sees: Confirmation page (Vercel)
  +---> Receives: Welcome email with all access links
  +---> Action: Opens Virtual Mind (delphi.ai/drcara)
  +---> Action: Visits Member Area for Prompt Guide (drcara.net/member-area)
  |
DAY 3: Follow-up email
  +---> Receives: 3 profile-specific prompts
  +---> Action: Returns to Virtual Mind
  |
DAY 7: GroundID Live reminder
  +---> Receives: Session details
  +---> Action: Attends GroundID Live (Zoom)
  +---> Action: Visits Replay Vault if missed (drcara.net/replay-vault)
  |
ONGOING (Weekly):
  +---> Attends GroundID Live (Zoom)
  +---> Uses Virtual Mind (delphi.ai/drcara)
  +---> Reviews Replay Vault recordings (drcara.net/replay-vault)
```

### Journey 2: GroundID Leader Enrollee

```
DAY 0: Enrollment ($9,000 / $3,000 x 3)
  |
  +---> Sees: Confirmation page (Vercel)
  +---> Receives: Welcome email with 5 action items
  +---> Action: Logs into course portal (drcara.net/groundid-leader)
  |
DAY 1-2: Onboarding
  +---> Action: Completes Leadership Identity Brief (Google Form via course portal)
  +---> Action: Submits shipping address for RPR Practice Deck
  +---> Action: Opens Virtual Mind pre-access (delphi.ai/drcara)
  +---> Receives: Day 2 reminder email if brief not completed
  |
DAY 5: Pre-access reminder
  +---> Receives: Virtual Mind pre-access email
  +---> Action: Uses Virtual Mind to start noticing patterns
  |
PRE-WEEK 1:
  +---> Receives: RPR Practice Deck (shipped to home)
  +---> Action: Adds all 12 sessions to calendar
  |
WEEKS 1-12: Active Program
  +---> Attends: Weekly 90-minute sessions (Zoom)
  +---> Reviews: Session recordings in course portal (drcara.net/groundid-leader)
  +---> Uses: Virtual Mind between sessions
  +---> Accesses: Resources in course portal
  |
POST-PROGRAM (90 days):
  +---> Retains: Community access
  +---> Retains: Replay Vault access
  +---> Retains: Virtual Mind (if subscribed separately)
```

---

## Appendix F: URL Structure & Navigation

### Complete URL Map for drcara.net

| URL | Type | Purpose | Who Sees It |
|-----|------|---------|-------------|
| `drcara.net` | Main site | Homepage, about, services | Everyone |
| `drcara.net/replay-vault` | Squarespace Course | GroundID Live recordings | All paying members |
| `drcara.net/groundid-leader` | Squarespace Course | 12-week cohort content | GroundID Leader enrollees |
| `drcara.net/member-area` | Squarespace Member Site | Premium resources hub | All paying members |
| `drcara.net/prompt-guide` | Member Page | Profile-specific prompt guide PDFs | All paying members |
| `drcara.net/pay-link/[id]` | Stripe Checkout | Payment page | Pre-purchase |

### External URLs (Not on Squarespace)

| URL | Platform | Purpose |
|-----|----------|---------|
| `delphi.ai/drcara` | Delphi.ai | Virtual Mind AI coaching |
| `grounid.com` | GrounID | Leadership Origin Profile sharing |
| Landing pages + quiz | Vercel | Lead generation, pre-purchase |
| Confirmation pages | Vercel | Post-purchase immediate experience |

### Navigation Recommendation

Add to Squarespace main navigation (logged-in members only):
- "Member Area" → `/member-area`
- "Replay Vault" → `/replay-vault`
- "Virtual Mind" → `delphi.ai/drcara` (external link)

GroundID Leader enrollees also see:
- "My Program" → `/groundid-leader` (or accessible from Member Area)

---

## Designer Checklist

Use this to track your progress:

- [ ] Set up Squarespace Course: Replay Vault (`/replay-vault`)
- [ ] Configure member-only access for Replay Vault
- [ ] Create first month section with placeholder lessons
- [ ] Set up Squarespace Course: GroundID Leader (`/groundid-leader`)
- [ ] Create Module 1: Pre-Work (5 lessons)
- [ ] Create Module 2: Sessions (empty, to be filled weekly)
- [ ] Create Module 3: Resources (4 lessons)
- [ ] Configure enrollee-only access for GroundID Leader
- [ ] Set up Squarespace Member Site: Member Area (`/member-area`)
- [ ] Create Prompt Guides page with 4 PDF downloads
- [ ] Create Resources page
- [ ] Set up member-only access
- [ ] Connect Stripe to Squarespace (Commerce → Payments)
- [ ] Test member login flow
- [ ] Test course access for both member tiers
- [ ] Add member navigation links (logged-in users only)
- [ ] Review mobile responsiveness for all new pages
- [ ] Brand check: colors, fonts, and tone match existing site

---

**Questions?** Reply directly in this document or email Dr. Cara.
