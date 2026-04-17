# GroundID Coffee — Website Section Designer Brief

**Client:** Dr. Cara Alexander — Connected Leadership
**Destination page:** https://www.drcara.net/drcarahome-1
**Product launch:** Mid-June 2026
**Deliverables included in this handoff:**

1. `drcarahome-coffee-section.html` — full mid-page section (the primary section)
2. `drcarahome-coffee-teaser.html` — compact above-the-fold card (can live higher on the page, in a sidebar, or near the hero)
3. This brief (voice, visuals, placement guidance, implementation notes)

---

## 1. What we are adding

Two modular, self-contained HTML blocks that introduce the new **GroundID Coffee** product line on the homepage and drive waitlist signups ahead of the mid-June 2026 launch.

Both blocks are self-contained (styles scoped, no external dependencies) and are designed to be pasted into **Squarespace Code Blocks** on `drcarahome-1`.

### The full section (primary)
`drcarahome-coffee-section.html`

- Launch tag: "New · Launching Mid-June 2026"
- Eyebrow: "GroundID Coffee"
- Headline: "Coffee is not the ritual. Returning to yourself is."
- Subhead: positions the product + the weekly live community session
- 3-pillar grid: The Principle / The Practice / The Framework
- Subscription "What's included" box (5 bullets)
- Primary CTA button: **Join the GroundID Coffee Waitlist** → `mailto:drcara@drcaraa.com` with a pre-filled subject + body
- Fine print: waitlist perks (launch pricing, priority onboarding, first roast)

### The teaser (smaller, optional)
`drcarahome-coffee-teaser.html`

- A compact horizontal card (copy on the left, button on the right)
- Can live above the fold, in a sidebar, or repeated near the bottom of the page
- Same waitlist mailto CTA
- Collapses to a stacked layout on mobile automatically

---

## 2. Where each block should live

Recommended placement:

| Block | Placement | Purpose |
|---|---|---|
| **Teaser card** | Near the top of `drcarahome-1`, below the hero / above the first major section | Catches returning visitors and new traffic right away. Signals "something new is here." |
| **Full section** | Mid-page, ideally after the main "what I do" or "leadership work" section | Deeper dive for visitors who scroll. Carries the ritual, the pillars, and the subscription details. |

The two pieces are intentionally redundant in CTA (both point to the same waitlist mailto) — visitors should only have one action to take no matter where they land.

---

## 3. Voice & tone (must preserve)

The copy is in Dr. Cara's established voice: **grounded, confident, unhurried, intentional.** Do not soften or "marketize" it.

- Not stimulation → intentionality
- Not product features → ritual and philosophy
- Not slogans → cues for a mindset
- Not "wake up energized" copy → "return to yourself before the day runs you"

When in doubt, keep sentences short and declarative. No exclamation marks. No emoji. No "elevate / unleash / unlock your best self" language.

**The three packaging lines are permanent and should appear verbatim on the bag and in this section:**

1. "Connect to yourself so you can connect to others." *(The Principle)*
2. "Choose intentionality with each cup of GroundID." *(The Practice)*
3. "You can only control how you Receive, Perceive, and Respond." *(The Framework)*

---

## 4. Visual system (matches the rest of the funnel)

| Token | Value | Use |
|---|---|---|
| Primary orange | `#c84200` | Headlines of interest, CTA buttons, left borders on callouts |
| Orange light (hover) | `#e05a1a` | CTA hover |
| Orange pale (tint) | `#fff9f4` | Callout backgrounds, pillar 1 background |
| Gold | `#C9A850` | Pillar 2 accent, secondary dividers |
| Gold pale | `#FDF9EF` | Pillar 2 background |
| Pink | `#E8B4B8` | Pillar 3 accent |
| Pink pale | `#FBF1F1` | Pillar 3 background |
| Dark text | `#2A2320` | Headlines |
| Body text | `#4A3F38` | Paragraphs |
| Muted | `#A09080` | Fine print |

**Typography**
- Serif: `EB Garamond` (via Google Fonts — already used elsewhere on the funnel; if not loaded on `drcarahome-1`, it falls back gracefully to Georgia)
- Sans: system UI stack (`-apple-system, BlinkMacSystemFont, Segoe UI, Arial, Helvetica, sans-serif`)

**Design philosophy** (direct from Dr. Cara)

> "Orange as the primary color conveys warmth, confidence, and energy without feeling aggressive. Pink and gold are used as light accents — supporting, not overpowering. This balance matters."
>
> "The design feels confident and intentional, not busy or decorative. It signals presence and leadership rather than trend or novelty."

If you add imagery, keep it minimal. A single product photo of a bag of GroundID Coffee (to be provided when available) can sit at the top of the full section. No lifestyle collages. No grid of 8 bean icons.

---

## 5. Implementation notes for the designer

### How to paste into Squarespace
1. Open `drcara.net/drcarahome-1` in edit mode
2. Add a **Code Block** where each section should live
3. Paste the entire contents of the `.html` file
4. Leave "Display Source" unchecked
5. Save

### Scoping
All styles live inside either `.gid-coffee-section` or `.gid-coffee-teaser`. They will not bleed into the rest of the Squarespace theme, and the Squarespace theme should not bleed into them (with one caveat — see below).

### Known Squarespace gotchas
- Squarespace link styles may try to override the button color. The CSS already uses `!important` on the CTA's `color` and `text-decoration`, which is the correct fix here.
- If Squarespace's base `<h2>` style is aggressive, you may need to slightly increase specificity (e.g., `.gid-coffee-section .gid-headline`) — currently it uses a class, so conflicts should be rare.
- EB Garamond: if the homepage doesn't already include the Google Fonts link for EB Garamond, add this inside Site Header Code Injection once:
  ```html
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  ```

### Mobile
Both files include responsive breakpoints at 560px / 640px. The 3-pillar grid collapses to a single column, and the teaser card stacks with a full-width button.

---

## 6. CTA and lead capture

The CTA button opens the user's email client with:
- **To:** `drcara@drcaraa.com`
- **Subject:** `GroundID Coffee Waitlist`
- **Body (pre-filled):**
  ```
  Please add me to the GroundID Coffee waitlist.

  Name:
  City / Shipping country:

  I'd like to be notified when subscriptions open in mid-June 2026.
  ```

This is intentional for launch. When a proper form + backend is ready, we'll swap the `href` in one place (the `<a class="gid-cta">` or `.gid-teaser-cta` in each file). No other changes required.

---

## 7. Quality bar

- The coffee section should look and feel **of a piece with the existing funnel** (quiz, profile landing pages, confirmation pages). Not a separate brand expression.
- It must not feel Canva-generated. Restraint is the point.
- The design should earn the attention it's asking for: calm, confident, grounded, and purposeful.

---

## 8. Files in this handoff folder

```
/designer-handoff
├── GroundID-Coffee-Section-Designer-Brief.md    ← you are here
├── drcarahome-coffee-section.html               ← full mid-page section
└── drcarahome-coffee-teaser.html                ← compact above-the-fold card
```

Both `.html` files are drop-in ready. Open them in a browser first to QA before pasting into Squarespace.

---

## 9. Contact

**Dr. Cara Alexander**
drcara@drcaraa.com
drcara.net
@drcaraa

Any questions on voice, visual system, or placement — direct to Dr. Cara.
