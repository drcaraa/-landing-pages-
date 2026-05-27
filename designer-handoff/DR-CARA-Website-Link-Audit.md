# Dr. Cara Website — Link Audit & Fix List

**Client:** Dr. Cara Alexander — Connected Leadership
**Prepared:** May 26, 2026
**Scope:** drcara.net (Squarespace), plus linked properties (groundid.net, grounid.com, delphi.ai/drcara)
**Pages crawled:** 9 on drcara.net · **Unique URLs checked:** 31
**Total items:** 16 (4 critical · 6 important · 6 housekeeping)

---

## How to use this document

This is a **designer worklist**, not a content review. Each row is one concrete fix with the exact "from → to" change. Work top-down — Critical first, then Important, then Housekeeping. The "Where to find it" column tells you which Squarespace page to open and where on the page to look.

When a fix is done, check it off. When all four Critical fixes are live, the site's broken-link bleed stops.

---

## Critical — broken or wrong destination

These are confirmed broken (HTTP 404) or sending traffic to the wrong place. Fix first.

### C1. Site nav "Lead Free Now" link is broken on every page

| Field | Detail |
|---|---|
| **Where to find it** | Squarespace → Design → Site Header → Main Navigation |
| **Element** | Nav item labeled "Lead Free Now" |
| **Current behavior** | Links to `/drcara-lead-free-now` → returns **HTTP 404** |
| **Correct destination** | `/lead-free-now` (the real page; returns HTTP 200) |
| **Why it matters** | This is in the global nav, so every page on the site has a broken link in its header. Highest-impact fix. |
| **Done when** | Clicking "Lead Free Now" in the nav from any page loads the real Lead Free Now page. |

### C2. "Explore Ways to Work Together" button on /contact is broken

| Field | Detail |
|---|---|
| **Where to find it** | Squarespace → Pages → `/contact` → scroll to the "Explore Ways to Work Together" button |
| **Element** | Button labeled "Explore Ways to Work Together" |
| **Current behavior** | Links to `/drcara-work-together` → returns **HTTP 404** |
| **Correct destination** | `/work-together` (the real page; returns HTTP 200) |
| **Done when** | Clicking the button on /contact loads the Work Together page. |

### C3. Homepage "Take the Free Assessment" CTAs point to wrong tool

| Field | Detail |
|---|---|
| **Where to find it** | Squarespace → Pages → Home → two places: (a) the "Five Tensions" section, (b) the "Profile assessment" section |
| **Element** | Two buttons both labeled "Take the Free Assessment →" |
| **Current behavior** | Both link to `https://www.delphi.ai/drcara/talk?q=…` — that's the Virtual Mind **chat tool**, not the assessment |
| **Correct destination** | `https://groundid.net` (the Leadership Origin Profile quiz) |
| **Why it matters** | The label says "Assessment" but the link goes to a chat. Visitors land on the wrong tool. Also: `/lead-free-now` and `/framework` already do this correctly — only the homepage is wrong, which means visibility is highest for the broken behavior. |
| **Done when** | Both homepage "Take the Free Assessment" buttons land on https://groundid.net. |

### C4. Homepage Virtual Mind CTA uses an outdated Delphi URL

| Field | Detail |
|---|---|
| **Where to find it** | Squarespace → Pages → Home → hero section → "Virtual Mind — Try It Free, No Email" CTA |
| **Element** | "Virtual Mind — Try It Free" button |
| **Current behavior** | Links to `https://www.delphi.ai/drcara/talk?q=What+should+I+do+next` — Delphi renamed `/talk` to `/chat` and currently 301-redirects the old URL |
| **Correct destination** | `https://www.delphi.ai/drcara/chat?q=What+should+I+do+next` (note `/chat` not `/talk`) |
| **Why it matters** | Works today because of Delphi's redirect, but redirects can be removed any time. Update now to remove the dependency. |
| **Done when** | The CTA URL contains `/chat` directly, no redirect involved. |

---

## Important — works, but needs cleanup

These don't 404, but they're confusing, inconsistent, or unverified.

### I1. RPR Coffee launch date contradicts itself

| Field | Detail |
|---|---|
| **Where to find it** | Two locations: (a) Homepage RPR Coffee section, (b) groundid.net/coffee landing page |
| **Issue** | Homepage says "Coming **July 2026**". The dedicated /coffee page says "**June 2026**" for the same product. |
| **Action** | Decide which month is correct, then update whichever page is wrong. Both must agree. |
| **Done when** | Both pages show the same launch month for RPR Coffee. |

### I2. Footer has two distinct labels pointing to the same URL

| Field | Detail |
|---|---|
| **Where to find it** | Footer (visible on every page) — "Coaching Disclaimer" and "Professional Services Disclaimer" stacked on top of each other |
| **Issue** | Both links go to `/coaching-disclaimer`. Two different labels, one destination — confusing for visitors and search engines. |
| **Action** | Either (a) create a real `/professional-services-disclaimer` page with separate content, or (b) remove the duplicate footer link. |
| **Done when** | Each visible footer link goes to its own unique page. |

### I3. "Login Account" nav item is a dead link

| Field | Detail |
|---|---|
| **Where to find it** | Site nav (visible on every page) |
| **Issue** | Nav item "Login Account" has `href="#"` — clicking it does nothing |
| **Action** | Either (a) wire it to the Squarespace member-area login URL if member accounts are intended, or (b) remove the nav item entirely. As-is, it's a dead UI element on every page. |
| **Done when** | Clicking "Login Account" either logs the user in (or opens login) — or the item is gone. |

### I4. "Take the Free Assessment" label is split across two destinations site-wide

| Field | Detail |
|---|---|
| **Where to find it** | Every page that uses this anchor text |
| **Issue** | Sometimes "Take the Free Assessment" goes to groundid.net (correct), sometimes to Delphi (wrong — see C3) |
| **Action** | Standardize anchor text → destination mapping site-wide: <br>• "Take the Free Assessment" = always → groundid.net <br>• "Try the Virtual Mind" = always → delphi.ai/drcara/chat <br>Audit every page and unify. |
| **Done when** | The two labels each point to exactly one destination across the entire site. |

### I5. "Take the Assessment | Contact Dr. Cara" link is half-dead on /work-together

| Field | Detail |
|---|---|
| **Where to find it** | Squarespace → Pages → `/work-together` |
| **Element** | A single link reading "Take the Assessment \| Contact Dr. Cara" |
| **Issue** | The whole label is one link going only to `/contact`. The "Take the Assessment" half of the label points nowhere — it's just text. |
| **Action** | Split into two separate links: "Take the Assessment" → https://groundid.net, "Contact Dr. Cara" → /contact. Or drop the unused half. |
| **Done when** | Each labeled action is clickable and goes to its own destination. |

### I6. Checkout cart CTAs need manual verification

| Field | Detail |
|---|---|
| **Where to find it** | Homepage and `/work-together` — three CTAs: "Start Free →", "Claim a Founding Seat →", "Apply Now →" |
| **Issue** | All three URLs return HTTP 200, but Squarespace renders cart contents in the browser. The audit tool couldn't verify the right product loads with the right price. Squarespace cart tokens silently invalidate if a product is edited or deleted. |
| **Action** | Click each CTA in an incognito window. Confirm: (a) the cart opens, (b) the right product is in it, (c) the price is correct. Pay special attention to "Claim a Founding Seat" — limited-time pricing is most likely to drift. |
| **Done when** | All three carts open with the correct product and price. |

---

## Housekeeping — nice to clean up

Not bugs. Worth knowing or quietly fixing.

### H1. Add a redirect for `/drcarahome` (no `-1`)

The homepage's canonical URL is `/drcarahome-1`. Someone typing `/drcarahome` (without the `-1`) gets a 404. No active link points there today, but it's a typo trap. Add a Squarespace URL redirect: `/drcarahome` → `/`.

### H2. Mailto address uses double-a (drcaraa.com) — verified working

The "Email to Discuss" CTA on /contact and the RPR Coffee waitlist CTA both use `drcara@drcaraa.com`. The double-a is **intentional** (matches Instagram `dr.caraa`, LinkedIn `drcaraa`) and verified working via Google Workspace MX records. No action — just document this so a future editor doesn't "correct" it to a single-a address that doesn't exist.

### H3. The typo domain `grounid.com` is a working mirror — keep it renewed

`grounid.com` (single-d) is a byte-for-byte mirror of `groundid.net` on Vercel. It catches real typo traffic. No action needed, but make sure this domain stays renewed at the registrar — losing it would drop the typo safety net.

### H4. LinkedIn footer link blocks audit probes (not actually broken)

The LinkedIn icon in the footer returns HTTP 405 to automated checks. This is LinkedIn rate-limiting, not a broken link — the profile loads in a browser. No action needed.

### H5. Quiz-result archetype pages need a per-profile spot-check

The Leadership Origin Profile quiz on groundid.net routes the user to a profile-specific landing page (Architect / Carrier / Performer / Sentinel) after they submit. The link is generated in JavaScript at runtime, so it can't be checked from outside the live quiz. Recommend taking the quiz four times (or temporarily forcing each result in dev tools) to confirm all four archetype landing pages load correctly.

### H6. The `/cart` page is reachable but not in the main nav

`/cart` is reachable via the cart icon in the header. It's not orphaned — just worth noting that it doesn't show up in the main nav, which is correct Squarespace behavior.

---

## What we could NOT verify automatically

Three items needed a real browser session to verify and weren't testable from outside:

1. **Cart contents and prices** behind the three checkout CTAs (Squarespace renders these client-side)
2. **Each archetype's landing page** at the end of the GroundID quiz (JavaScript-routed)
3. **The "Login Account" intent** — whether it should be wired up or removed (a UX/strategy call, not a link-health call)

A human pass on these three would close out the audit.

---

## Quick reference — full URL map

| Anchor text | Should always point to |
|---|---|
| Take the Free Assessment | https://groundid.net |
| Try the Virtual Mind / Talk to the Virtual Mind | https://www.delphi.ai/drcara/chat |
| Lead Free Now | /lead-free-now |
| Work Together / Explore Ways to Work Together | /work-together |
| Contact Dr. Cara / Contact | /contact |
| The Framework | /framework |
| About | /about |
| Coffee / RPR Coffee | https://groundid.net/coffee |

When in doubt during a fix, cross-check against this table.

---

## Sign-off

When all Critical and Important items are done, please reply to Dr. Cara with:

- A list of the items completed (by ID — C1, C2, etc.)
- Any items you couldn't complete and why
- Date and time the changes went live

A re-audit will be run shortly after to confirm.
