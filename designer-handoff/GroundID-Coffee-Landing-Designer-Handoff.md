# GroundID Coffee — Full Landing Page Designer Handoff

**Client:** Dr. Cara Alexander — Connected Leadership
**Product:** GroundID Coffee (Espresso + Drip, 12 oz)
**Launch:** Mid-June 2026
**Primary file:** `coffee-landing.html` (full, standalone landing page)
**Brand reference:** GroundID coffee bag label (hot-pink / orange / black, chevron peaks, heavy italic wordmark)

---

## 1. What this is

A full, self-contained, standalone landing page for the GroundID Coffee waitlist. Not a homepage section — a dedicated URL the designer should host at `drcara.net/coffee` (or similar) and link to from every CTA.

**One file. No dependencies except two Google Fonts (Anton + Inter) and one logo asset (`DrCara_Logo_LeadershipTag_Gold.png`, already in the repo).**

Everything else — colors, chevrons, product cards — is built with inline CSS + SVG so the designer can paste, tweak, or rebuild inside Squarespace, Webflow, Framer, or raw HTML without hunting assets.

---

## 2. Brand system (pulled directly from the bag)

### Colors

| Role | Hex | Usage |
|---|---|---|
| Black | `#000000` | Primary background |
| Off-black | `#0A0A0A` / `#111111` | Cards, panels |
| Hot pink | `#ED1E79` | Primary accent, CTA, eyebrow text |
| Hot pink (bright) | `#FF2D95` | Promise text, hover states |
| Pink deep | `#C01371` | Muted pink applications |
| Orange | `#F26B1F` | Wordmark, section headlines, "val" pills |
| Orange bright | `#FF7A2E` | Wordmark stroke/hover |
| Orange light | `#F9A55F` | Product type subtext |
| Peach | `#F4B896` | Tertiary accent, footer quote |
| Maroon | `#6B1D3F` | Chevron base layer, dividers |
| Maroon deep | `#4A1029` | Text shadow on wordmark |
| Gold | `#C9A850` | DR CARA logo only |
| Cream | `#F5F0EB` | Reserved (currently unused) |

Colors map 1:1 to the bag. Do not substitute.

### Type

- **Display:** `Anton` (Google Fonts) — heavy condensed sans. Applied italic + skew(-6deg) + orange fill + `#4A1029` drop-shadow to match the "GROUNDID" wordmark on the bag.
- **Body:** `Inter` (Google Fonts), weights 400 / 500 / 600 / 700 / 800.
- **Fallback stack:** `Impact, 'Arial Narrow Bold', sans-serif` for display; system sans for body.

### Signature graphic — the chevron peaks

Four nested triangles recreating the bag's peaked motif. Order (outside → in): **maroon `#6B1D3F` → pink `#ED1E79` → orange `#F26B1F` → peach `#F4B896`.**

Used in three sizes in the page:
- **Large (180px)** — top of hero
- **Medium (120px)** — bottom of hero (inverted)
- **Small (70px)** — section break before subscription panel

The same motif appears in miniature inside each product card as a seal above the wordmark.

---

## 3. Page structure

| # | Section | Background | Purpose |
|---|---|---|---|
| 1 | Header | Black | DR CARA gold logo + "Launching Mid-June 2026" tag |
| 2 | Chevron (large) | Pink base + peaks | Visual bridge; sets brand tone immediately |
| 3 | Hero | Black | Wordmark, promise line, primary CTA, launch date |
| 4 | Chevron (inverted) | Pink base + peaks | Bridge into principle panel |
| 5 | The Principle | Black | "Receive. Perceive. Respond." philosophy block |
| 6 | The Roasts | Black | Two product cards — Espresso + Drip |
| 7 | The RPR Method | Black | Three-column triptych: Receive / Perceive / Respond |
| 8 | Three lines on every bag | Black | Three ethos quotes pulled verbatim from the bag |
| 9 | Chevron (small) | Black base + peaks | Transition into the offer |
| 10 | The Subscription | **Orange** | Inverted color block — the offer, the live sessions, what's included |
| 11 | Final CTA | Black | Italic skewed headline + waitlist button |
| 12 | Footer | Black | Footer quote, links, socials |

---

## 4. Voice & tone (DO NOT soften)

Dr. Cara's voice is **grounded, confident, unhurried, intentional.** It is *not* marketing copy. It is philosophy applied to a product.

- Not stimulation → intentionality
- Not product features → ritual and philosophy
- Not "boost your morning" → "return to yourself"
- Not "exclusive early access" → "priority onboarding"

If a line reads like Canva — remove it. The brand is care.

---

## 5. Copy (locked — do not rewrite)

### Hero
- Eyebrow: **GroundID Coffee · Dr. Cara**
- Wordmark: **GROUNDID**
- Tag: **COFFEE**
- Rule text: **Connect to yourself**
- Promise: **Connect to yourself so you can connect to others.**
- Sub: *"GroundID is the first cue in a daily practice of grounded leadership. Before the calls. Before the decisions. Before the demands of the day — a moment to return to yourself, so you can show up for everyone else."*
- CTA: **Join the Waitlist** → `#waitlist`
- Launch line: **Launching Mid-June 2026 · Monthly Subscription**

### The Principle
- Label: **The Principle**
- Headline: **The only thing you can truly control is how you *receive. perceive. respond.***
- Body: three paragraphs (already in the file) — philosophy, Ground + ID definitions, the ritual framing.

### The Roasts
Product card data (already in the file):

| Roast | Origin | Roast Level | Net Wt. | Tagline |
|---|---|---|---|---|
| ESPRESSO — Whole Bean | Colombia + Brazil | Medium-Dark | 12 oz · 340 g | *Bold, deep, built for the morning that asks a lot of you.* |
| DRIP — Ground | Colombia | Light-Medium | 12 oz · 340 g | *Smooth, bright, steady — for the long, considered day.* |

### The RPR Method

| # | Word | Lead | Body |
|---|---|---|---|
| 01 | RECEIVE | *The cup in your hand is the signal to slow receive.* | Not the next email. Not the group chat. Something warm, earned, and quiet. Your nervous system registers it — and that registration is the opening. |
| 02 | PERCEIVE | *One honest question before you start.* | What part of me is leading right now? The Architect, the Carrier, the Performer, the Sentinel? Perception begins the moment you name what's running the show. |
| 03 | RESPOND | *Enter the day on purpose, not autopilot.* | Response is not reaction. It's the choice that follows naming. One intention. One boundary. One posture — set with something as small as a cup of coffee. |

### Three lines on every bag (ethos cards)
1. **"Connect to yourself so you can connect to others."** — The Principle
2. **"Choose intentionality with each cup of GroundID."** — The Practice
3. **"One can truly only control how they Receive, Perceive, and Respond."** — The Framework

### Subscription
- Headline: **Coffee is the *cue.* Community makes it stick.**
- Meta chips: *Monthly Subscription · Shipped to Your Door · Live Weekly 30-Min Session · Mid-June 2026*
- Body paragraphs + included-items list (5 bullets) — all in the file.

### Final CTA
- Headline: **Start grounded. *Lead from there.***
- Body: *"Join the GroundID Coffee waitlist to be first in line when subscriptions open. Waitlist members get launch pricing, priority onboarding to the live sessions, and the first roast shipped the week of launch."*
- Button: **Join the GroundID Coffee Waitlist**
- Link target (TBD): currently `https://www.drcara.net/groundid-coffee` — designer to replace with the real waitlist form URL or mailto.

### Footer
- Quote: *"Choose intentionality with each cup of GroundID."*
- Info line: Dr. Cara Alexander · Connected Leadership · drcara.net · @drcaraa
- Second line: links to [delphi.ai/drcara](https://delphi.ai/drcara) and [groundid.net](https://www.groundid.net) (Leadership Origin Profile)

---

## 6. Interaction notes

- **CTA button** (`.hero-cta`): pink fill default → orange fill + 2px lift on hover (150ms ease). Used for both hero and final CTAs.
- **Scroll:** `scroll-behavior: smooth` is on the `<html>`; the hero CTA jumps to `#waitlist` which is the final CTA section.
- **No JS.** The page is static.

---

## 7. Responsive behavior

Single breakpoint at **840px**:

- Product grid collapses from 2 columns → 1 column
- RPR triptych collapses from 3 columns → 1 column
- Ethos cards collapse from 3 columns → 1 column
- Header "Launching Mid-June 2026" nav text is hidden (logo only)
- Section padding reduces from 88px → 64px vertical
- Hero wordmark scales fluidly via `clamp(4.5rem, 15vw, 11rem)`

All type is fluid via `clamp()` — nothing needs manual resize at small viewports.

---

## 8. Implementation notes for the designer

### If hosting on Squarespace
Drop the entire file into a new page's Code Injection block, or split it into a Code Block per section. The layout is stateless — any section can stand alone.

### If hosting on Webflow / Framer
Port section-by-section. Colors and fonts are variables at the top of `<style>` (`:root { --pink: #ED1E79; ... }`) — copy those into your design system first.

### If rebuilding natively
- Use the chevron SVGs as-is (four polygons layered, same points). They're the brand signature.
- The wordmark effect is: italic Anton + `transform: skew(-6deg)` + `text-shadow: 6px 6px 0 #4A1029` + `-webkit-text-stroke: 1px #FF7A2E`. Don't replace with a raster — it should stay crisp and resizable.

### Logo asset required
- `DrCara_Logo_LeadershipTag_Gold.png` — 36px tall in the header. Already exists in the repo root. If you need higher-res for retina, request SVG from Dr. Cara.

### Waitlist destination
The hero CTA anchors to `#waitlist` on-page. The final CTA button points to `https://www.drcara.net/groundid-coffee` — **replace this with the real waitlist URL** (Squarespace form, Typeform, mailto, etc.) before launch.

---

## 9. What NOT to do

- ❌ Do not lighten the palette or "soften" the pink/orange. The bag is bold on purpose.
- ❌ Do not replace the chevron peaks with a generic divider. They are the brand.
- ❌ Do not swap Anton for a generic bold sans. The italic + skew + shadow is the GROUNDID wordmark.
- ❌ Do not add stock coffee photography. The page is deliberately typographic — the graphic identity is the chevron + wordmark system, not imagery.
- ❌ Do not add a second CTA style. One pink button. That is the only call to action.
- ❌ Do not shrink or crop copy to "clean up" the layout. The copy length is part of the voice — unhurried, deliberate.

---

## 10. Questions for Dr. Cara before launch

1. **Waitlist form URL** — what is the real destination? (Squarespace form / Typeform / mailto?)
2. **Hosting path** — `drcara.net/coffee`, `groundid.net/coffee`, or a subdomain?
3. **Single roast at launch, or both Espresso + Drip?** (Page currently shows both.)
4. **Open Graph image** — do you have a branded share image yet? If not, we should generate one from the hero (black bg, orange GROUNDID wordmark, chevron) at 1200×630.
5. **Analytics** — add GA4, Meta pixel, or leave clean for first launch?

---

## Deliverables in this handoff

- `coffee-landing.html` — full standalone landing page (working, previewable)
- `DrCara_Logo_LeadershipTag_Gold.png` — logo asset (in repo root)
- `GroundID-Coffee-Landing-Designer-Handoff.md` — this brief

That's it. One file to host, one logo to bundle, one brief to read.
