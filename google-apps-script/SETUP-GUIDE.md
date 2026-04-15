# DR. CARA — Post-Purchase Automation Setup Guide

## What This Does

When a client pays via Stripe, this system automatically:
1. Logs them in your Google Sheet (your CRM)
2. Sends a personalized welcome email from your Gmail
3. Schedules follow-up emails (Day 3, Day 7 for VM; Day 2, Day 5 for GroundID)
4. Sends those follow-ups automatically each morning

All content delivery happens through your existing **Squarespace Business** site at drcara.net (Courses + Member Sites). No additional platforms needed.

---

## Your Complete Stack (No New Tools)

| Tool | Role | Cost |
|------|------|------|
| **Squarespace Business** | Website, Courses (Replay Vault + GroundID Leader), Member Sites, Email Campaigns | Already have |
| **Google Business** | Gmail (welcome emails), Sheets (CRM), Calendar (session invites), Apps Script (automation) | Already have |
| **Stripe** | Payment processing | Already have |
| **Delphi.ai** | Virtual Mind AI coaching | Already have |
| **Vercel** | Landing pages + confirmation pages | Already have |
| **Zoom** | GroundID Live sessions | Already have |

**Additional cost: $0/month**

---

## Step-by-Step Setup

### 1. Set Up Squarespace Courses & Member Areas

**Replay Vault (Squarespace Course)**
1. In Squarespace → Pages → + → Course
2. Name: "Replay Vault"
3. URL slug: `/replay-vault`
4. Add sections by month/date for each GroundID Live recording
5. Set access: Members only (requires login)
6. After each weekly GroundID Live, upload the Zoom recording as a new lesson

**GroundID Leader Course (Squarespace Course)**
1. Pages → + → Course
2. Name: "GroundID Leader"
3. URL slug: `/groundid-leader`
4. Create modules:
   - Module 1: "Pre-Work" — Leadership Identity Brief intake form, RPR Practice Deck shipping form
   - Module 2: "Sessions" — Add session recordings weekly after each live session
   - Module 3: "Resources" — Prompt guides, cohort info, Zoom links
5. Set access: Members only

**Member Area (Squarespace Member Site)**
1. Pages → + → Member Area
2. Name: "Member Area"
3. URL slug: `/member-area`
4. Add pages for:
   - Premium Prompt Guides (4 profile versions as downloadable PDFs)
   - Resource library
   - Member-only content/insights

**Connecting Stripe to Squarespace**
- Squarespace integrates natively with Stripe
- Your existing Stripe account connects directly in Squarespace → Commerce → Payments
- Squarespace can auto-grant course/member access when payment is received

### 2. Create the Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com) → Create new spreadsheet
2. Name it: **"DR. CARA Client Database"**
3. Rename the first tab to: **"Quiz Leads"** (this is where your Google Form quiz data goes)
4. Create additional tabs:
   - **VM Subscribers** — Virtual Mind clients
   - **GroundID Cohort** — GroundID Leader enrollees
   - **Email Log** — tracks all sent emails
   - **Scheduled Emails** — pending follow-up emails
5. Copy the Sheet ID from the URL:
   `https://docs.google.com/spreadsheets/d/`**THIS_PART**`/edit`

### 3. Set Up the Apps Script

1. In your Google Sheet → **Extensions** → **Apps Script**
2. Delete the default `Code.gs` content
3. Paste the entire contents of `stripe-webhook.gs`
4. Update the CONFIG section at the top:
   - `SHEET_ID` → your Google Sheet ID from step 2
   - `VM_PRICE_ID` → your Stripe price ID for Virtual Mind
   - `GROUNDID_PRICE_ID` → your Stripe price ID for GroundID Leader
   - `REPLAY_VAULT_URL` → your Squarespace Replay Vault URL
   - `MEMBER_AREA_URL` → your Squarespace Member Area URL
   - `GROUNDID_COURSE_URL` → your Squarespace GroundID Leader course URL
   - `PROMPT_GUIDE_URL` → your Squarespace Prompt Guide page URL
   - `CURRENT_COHORT` → e.g., `'Q2-2026'`
5. Click **Save** (Ctrl+S)

### 4. Deploy as Web App

1. Click **Deploy** → **New Deployment**
2. Click the gear icon → **Web App**
3. Settings:
   - Description: "Stripe Webhook"
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**
5. **Copy the Web App URL** — you'll need this for Stripe

### 5. Connect to Stripe

1. Go to [Stripe Dashboard](https://dashboard.stripe.com) → **Developers** → **Webhooks**
2. Click **Add Endpoint**
3. Paste your Web App URL
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
5. Click **Add Endpoint**
6. Copy the **Signing Secret** (starts with `whsec_`)
7. Go back to Apps Script and update `STRIPE_WEBHOOK_SECRET`

### 6. Set Up Daily Email Trigger

This sends the scheduled follow-up emails each morning:

1. In Apps Script → click the **clock icon** (Triggers) in the left sidebar
2. Click **+ Add Trigger**
3. Settings:
   - Function: `processScheduledEmails`
   - Event source: Time-driven
   - Type: Day timer
   - Time: 9am to 10am
4. Click **Save**

### 7. Test Everything

1. In Apps Script, update the test email in `testVMWelcomeEmail()`
2. Click the function dropdown → select `testVMWelcomeEmail` → click **Run**
3. Check your inbox for the welcome email
4. Repeat with `testGroundIDWelcomeEmail`

---

## Finding Your Stripe Price IDs

1. Stripe Dashboard → **Products**
2. Click on "Virtual Mind" (or whatever you named it)
3. Under Pricing, click the price
4. The Price ID starts with `price_` — copy it
5. Repeat for GroundID Leader

---

## Email Schedule Summary

### Virtual Mind ($49/month)
| When | Email | Subject |
|------|-------|---------|
| Instant | Welcome | "Welcome to Virtual Mind — Your access is live" |
| Day 3 | Prompts | "Three prompts for The [Profile]" |
| Day 7 | Live Reminder | "This week's GroundID Live is yours" |

### GroundID Leader ($9,000)
| When | Email | Subject |
|------|-------|---------|
| Instant | Welcome | "Welcome to GroundID Leader — You are in" |
| Day 2 | Brief Reminder | "Your Leadership Identity Brief — complete before we begin" |
| Day 5 | VM Pre-access | "Your Virtual Mind pre-access — use it before Session 1" |

---

## Weekly Workflow (After Setup)

| Day | Action | Tool |
|-----|--------|------|
| After GroundID Live | Download Zoom recording → Upload to Squarespace Replay Vault course | Zoom + Squarespace |
| After GroundID Leader session | Upload recording to GroundID Leader course in Squarespace | Squarespace |
| Weekly | Check Google Sheet for new enrollees, verify emails sent | Google Sheets |
| Quarterly | Update `CURRENT_COHORT` in Apps Script CONFIG | Apps Script |

---

## Updating for New Cohorts

Each quarter, update `CURRENT_COHORT` in the CONFIG:
1. Apps Script → update `CURRENT_COHORT: 'Q3-2026'`
2. Click **Save** (no redeployment needed for config changes)
3. In Squarespace, create a new section in the GroundID Leader course for the new cohort

---

## Connecting Quiz Leads

Your existing Google Forms quiz already sends data to Google Sheets. To connect it:
1. Open your quiz responses Google Sheet
2. Either use that same sheet (add the tabs above) or
3. Use `IMPORTRANGE` to pull quiz data into the new sheet

The webhook automatically looks up each buyer's profile by matching their email against the Quiz Leads tab.

---

## Quiz Lead Drip Campaign (Post-Quiz Nurture)

This sends a 3-email sequence to every person who takes the Leadership Origin Profile quiz, personalized by their profile (Architect, Carrier, Performer, Sentinel). The goal is to nurture quiz takers toward the Virtual Mind.

### Email Sequence

| Day | Subject | Purpose |
|-----|---------|---------|
| **Day 0** (instant) | "Your Leadership Origin Profile: The [Profile]" | Reinforce result, deliver value, build trust |
| **Day 2** | "What The [Profile] Misses — And How to See It" | Deeper RPR insight + growth edge |
| **Day 5** | "Your Next Step as The [Profile]" | CTA to Virtual Mind (free trial) |

### Setup Steps

1. **Open your Quiz Leads Google Sheet**
   - Sheet ID: `1-VekdkJ3CqXVXDUuB4NgaoUAT6MmhIS_IofXIGg3TOE`

2. **Add the Apps Script**
   - Extensions → Apps Script
   - Delete the default `Code.gs` content
   - Paste the entire contents of `quiz-drip.gs` from this folder
   - Update `CONFIG.VIRTUAL_MIND_CHECKOUT` with your Stripe checkout link
   - Click **Save**

3. **Deploy as Web App** (this creates the webhook endpoint)
   - Click **Deploy** → **New Deployment**
   - Click the gear icon → **Web App**
   - Description: "Quiz Lead Webhook"
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click **Deploy**
   - **Copy the Web App URL** — you need this for the quiz page

4. **Update the Quiz Landing Page**
   - Open `leadership-origin-quiz.html`
   - Find `YOUR_APPS_SCRIPT_WEB_APP_URL` near the bottom
   - Replace it with the Web App URL from step 3
   - Redeploy to Vercel

5. **Add Daily Email Trigger** (sends Day 2 + Day 5 emails)
   - In Apps Script → click the **clock icon** (Triggers)
   - Click **+ Add Trigger**
   - Function: `processScheduledQuizEmails`
   - Event source: **Time-driven**
   - Type: **Day timer**
   - Time: **9am to 10am**
   - Click **Save**

6. **Test It**
   - Visit the Web App URL in your browser — you should see: `{"status":"ok","message":"DR. CARA Quiz Drip webhook is live..."}`
   - In Apps Script, select `testDay0Email` from the function dropdown → click **Run**
   - Check your inbox for the test email
   - Run `testFullDrip` to test the complete flow (adds a test row + triggers all 3 emails)
   - Check the **Quiz Drip Schedule** tab — it auto-creates with pending emails

### How It Works

- When someone takes the quiz → the page POSTs directly to your Apps Script Web App
- The webhook writes the lead to the Quiz Leads sheet + sends Day 0 email immediately + schedules Day 2 and Day 5
- Each morning at 9am → `processScheduledQuizEmails` checks for emails due today and sends them
- All emails are tracked in the **Quiz Drip Schedule** tab (auto-created on first run)
- Duplicate emails are automatically skipped
- No Google Form needed — the quiz page talks directly to your sheet

### The Quiz Drip Schedule Tab

| Column | Purpose |
|--------|---------|
| Email | Lead's email address |
| Name | Lead's first name |
| Profile | Architect / Carrier / Performer / Sentinel |
| Day | 0, 2, or 5 |
| Send Date | When to send (YYYY-MM-DD) |
| Status | pending / sent / error |
| Sent At | Timestamp when actually sent |

---

## Squarespace Email Campaigns (Optional Enhancement)

If you want more visual branded emails beyond the automated Gmail drip:
1. Use **Squarespace Email Campaigns** (included with your Business plan) for:
   - Monthly newsletters to all members
   - Event announcements for GroundID Live
   - New content alerts (new Replay Vault sessions)
2. The automated Gmail drip handles the time-sensitive post-purchase sequence
3. Squarespace Email Campaigns handles ongoing engagement

This gives you two email channels:
- **Gmail via Apps Script** = automated, triggered by purchase, personalized
- **Squarespace Email Campaigns** = manual/scheduled, branded templates, ongoing engagement
