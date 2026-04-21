# Dr. Cara Landing Pages — Revision Chart

**Client:** Dr. Cara Alexander — Connected Leadership
**Prepared:** April 17, 2026
**Scope:** Audit of 6 landing pages on drcara.net + GroundID Coffee launch integration
**Total audit items:** 25 + Coffee section add

---

## Pages Audited

1. `/drcarahome-1` (Home)
2. `/drcara-framework` (Framework)
3. `/drcara-work-together` (Work Together)
4. `/drcara-about` (About)
5. `/drcara-lead-free-now` (Lead Free Now)
6. `/drcara-contact-new` (Contact)

---

## Priority 1 — Broken Links & Wrong Destinations

| # | Page | Element | Current State | Required Fix |
|---|------|---------|---------------|--------------|
| 1 | Work Together | Logo / Home link | Points to `/drcarahome` — an OLDER page with outdated framework ("Recognizing Value, Embodying Grace, Conquering Control") | Change to `/drcarahome-1` |
| 2 | Lead Free Now | "Try the Virtual Mind Free" button | Links to `https://groundid.net` (assessment) | Link to `https://www.delphi.ai/drcara` |
| 3 | Lead Free Now | "Explore Ways to Work Together" button | Links to `https://groundid.net` | Link to `/drcara-work-together` |
| 4 | Work Together | "Enroll Now" / "Enroll in GroundID Leader" button (orange section, GroundID Leader Program) | Incorrect destination (links to `groundid.net` assessment) | Link to actual enrollment / Stripe checkout / `/drcara-contact-new` |
| 5 | Work Together | "Contact Dr. Cara" button | Links to `https://groundid.net` | Link to `/drcara-contact-new` |
| 6 | Home | "See the Framework →" button | Links to `http://delphi.ai/drcara/talk` — Virtual Mind, insecure HTTP, label mismatch | Relabel to "Try the Virtual Mind" OR relink to `/drcara-framework`; upgrade to HTTPS |
| 20 | Work Together | Virtual Mind mention in orange section | **No link at all** — the paragraph describes Virtual Mind but doesn't link to it | Add link to `https://www.delphi.ai/drcara` |
| 21 | Lead Free Now | Virtual Mind reference link | Incorrect destination | Point to `https://www.delphi.ai/drcara` |
| 22 | Lead Free Now | "Go Deeper" link | Incorrect destination | Confirm intended target — likely `/drcara-work-together` or `/drcara-framework` |
| 23 | Contact | LinkedIn link | Wrong URL | Correct to `https://www.linkedin.com/in/drcaraa/` |

---

## Priority 2 — Design & Visual Fixes

| # | Page | Issue | Required Fix |
|---|------|-------|--------------|
| 24 | Framework | Only the **last box** in the framework section is highlighted — all others appear un-highlighted | Highlight all 4 framework boxes consistently (The Architect, The Carrier, The Performer, The Sentinel) |
| 25 | About | AI-generated photo at bottom of page looks low quality / uncanny | Replace with real photo of Dr. Cara or remove entirely |

---

## Priority 3 — Data Inconsistencies

| # | Issue | Where It Appears | Required Fix |
|---|-------|------------------|--------------|
| 7 | Email address mismatch: `cara@drcaraa.com` vs `drcara@drcaraa.com` | Home / Framework / About use `cara@`; Contact uses `drcara@` | Confirm correct address, apply across all 6 pages |
| 8 | Domain mismatch: site is `drcara.net` but email domain is `drcaraa.com` (two a's) | Sitewide | Verify intentional; if typo, fix |
| 9 | Instagram handle: copy says `@drcaraa`, actual handle is `@dr.caraa` | Contact page body copy | Update copy to `@dr.caraa` |

---

## Priority 4 — Navigation & Structure

| # | Page | Issue | Required Fix |
|---|------|-------|--------------|
| 10 | Home | Top nav includes "Home" item; other pages do not | Remove "Home" from top nav (logo already handles it) |
| 11 | All pages | "Contact" only appears in footer, not primary nav | Add Contact to top nav across all pages |
| 12 | `/drcarahome` (old page) | Still live with outdated framework copy | Redirect to `/drcarahome-1` or delete entirely |

---

## Priority 5 — Copy & Brand Consistency

| # | Issue | Where | Required Fix |
|---|-------|-------|--------------|
| 13 | Brand name inconsistent: "Ground ID" vs "GroundID" vs "groundid" | Sitewide | Standardize to "GroundID" |
| 14 | Copyright reads: "Copyright @ 2026 \| Dr. Cara \| All Right Reserved" | Contact page footer | Change to "© 2026 \| Dr. Cara \| All Rights Reserved" |
| 15 | Framework naming varies: "Receive · Perceive · Respond" vs "RPR Framework" vs "Receive, Perceive, Respond" | Multiple pages | Pick one canonical format, apply sitewide |

---

## Priority 6 — Security, Link Hygiene & Legal

| # | Issue | Where | Required Fix |
|---|-------|-------|--------------|
| 16 | Pinterest link uses `http://` | Every page footer | Change to `https://` |
| 17 | YouTube URL has tracking param on some pages, clean on others | Footer varies by page | Standardize to clean `https://youtube.com/@drcaraa` |
| 18 | "See the Framework" button uses `http://delphi.ai/...` (insecure) | Home page | Change to `https://www.delphi.ai/drcara` |
| 19 | **Legal pages need to be updated** — Privacy Policy & Terms & Conditions links incomplete, unwired, or out of date | Footer, every page | Draft/refresh Privacy Policy + Terms, wire up footer links across all 6 pages |

---

## New Feature — GroundID Coffee Section (to be added)

A dedicated GroundID Coffee section must be integrated into the site for the mid-June 2026 product launch. The designer handoff has already been prepared and is located in this folder.

**Action required from designer:** Implement per the existing brief below.

| Item | Reference File | Purpose |
|------|----------------|---------|
| Full mid-page section | `drcarahome-coffee-section.html` | Primary section to drop into the Home page |
| Above-the-fold teaser card | `drcarahome-coffee-teaser.html` | Compact teaser to link into the section |
| Designer brief (full spec) | `GroundID-Coffee-Section-Designer-Brief.pdf` / `.md` | Voice, visuals, placement, implementation |
| Zipped handoff bundle | `GroundID-Coffee-Designer-Handoff.zip` | All above files packaged |

**Placement:** Mid-page on `/drcarahome-1` with the teaser card positioned above the fold. The destination page for all Coffee CTAs is `drcara.net/drcarahome-1` (the new home page — confirm it isn't wired to the old `/drcarahome`).

**Launch timing:** Mid-June 2026 — section can be built now and revealed at launch.

**Tone:** Connected Leadership voice; GroundID palette (orange `#c84200`, warm neutrals). Do not treat as a generic product card.

---

## Verified Working (No Action Needed)

| Element | Destination | Status |
|---------|-------------|--------|
| Main nav: Framework | `/drcara-framework` | Working |
| Main nav: Work Together | `/drcara-work-together` | Working |
| Main nav: About | `/drcara-about` | Working |
| Main nav: Lead Free Now | `/drcara-lead-free-now` | Working |
| Footer: Contact | `/drcara-contact-new` | Working |
| "Take the Free Assessment" buttons | `https://groundid.net` | Working — loads assessment |
| Virtual Mind (announcement bar) | `https://www.delphi.ai/drcara` | Working |
| Instagram | `https://www.instagram.com/dr.caraa` | Working |
| Phone: 301-852-9424 | Consistent sitewide | Working |
| Pricing: Virtual Mind $49/mo, GroundID Leader $9,000 ($3,000/mo) | Consistent sitewide | Working |

---

## Summary

- **10** broken or mislinked CTAs / missing links (Priority 1)
- **2** design & visual issues (Priority 2)
- **3** data inconsistencies (Priority 3)
- **3** navigation / structure issues (Priority 4)
- **3** copy / brand inconsistencies (Priority 5)
- **4** link hygiene, security & legal issues (Priority 6)
- **1** new feature — GroundID Coffee section to integrate

**Total: 25 audit items + 1 new feature add.**
Recommended attack order: Priority 1 → 2 → 3 → 4 → 5 → 6 → Coffee integration.
