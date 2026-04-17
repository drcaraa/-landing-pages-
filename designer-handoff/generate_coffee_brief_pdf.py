#!/usr/bin/env python3
"""Generate the GroundID Coffee designer brief PDF from the source content."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)
import os

ORANGE = HexColor('#c84200')
ORANGE_LIGHT = HexColor('#fff9f4')
GOLD = HexColor('#C9A850')
PINK = HexColor('#E8B4B8')
DARK = HexColor('#2A2320')
BODY = HexColor('#4A3F38')
MUTED = HexColor('#A09080')
BORDER = HexColor('#E8E0D8')

h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22, leading=28,
                    textColor=DARK, spaceAfter=6)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=14, leading=20,
                    textColor=ORANGE, spaceBefore=18, spaceAfter=8)
h3 = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11, leading=16,
                    textColor=DARK, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=15,
                      textColor=BODY, spaceAfter=6)
body_small = ParagraphStyle('body_small', fontName='Helvetica', fontSize=9, leading=13,
                            textColor=BODY, spaceAfter=4)
body_muted = ParagraphStyle('body_muted', fontName='Helvetica', fontSize=9, leading=13,
                            textColor=MUTED, spaceAfter=4)
meta = ParagraphStyle('meta', fontName='Helvetica', fontSize=9, leading=13,
                      textColor=MUTED)
bullet = ParagraphStyle('bullet', fontName='Helvetica', fontSize=10, leading=15,
                        textColor=BODY, spaceAfter=3, leftIndent=16, bulletIndent=4)
mono = ParagraphStyle('mono', fontName='Courier', fontSize=8.5, leading=12,
                      textColor=BODY, spaceAfter=4)
quote = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=10, leading=16,
                       textColor=DARK, leftIndent=16, rightIndent=16, spaceAfter=8)


def bullets(items):
    return [Paragraph(f"• {t}", bullet) for t in items]


def rule(color=ORANGE, thickness=2):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceBefore=4, spaceAfter=8)


def build_pdf(out_path):
    doc = SimpleDocTemplate(out_path, pagesize=letter,
                            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch,
                            title="GroundID Coffee — Website Section Designer Brief",
                            author="Dr. Cara Alexander")
    story = []

    # Title
    story.append(Paragraph("GroundID Coffee", h1))
    story.append(Paragraph("Website Section Designer Brief", ParagraphStyle(
        'sub', fontName='Helvetica', fontSize=13, leading=17, textColor=ORANGE, spaceAfter=14)))
    story.append(rule(ORANGE, 2.5))

    # Header meta
    story.append(Paragraph("<b>Client:</b> Dr. Cara Alexander — Connected Leadership", meta))
    story.append(Paragraph("<b>Destination page:</b> drcara.net/drcarahome-1", meta))
    story.append(Paragraph("<b>Product launch:</b> Mid-June 2026", meta))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Deliverables in this handoff:", body))
    story.extend(bullets([
        "<b>drcarahome-coffee-section.html</b> — full mid-page section (primary)",
        "<b>drcarahome-coffee-teaser.html</b> — compact above-the-fold card",
        "This brief (voice, visuals, placement, implementation)",
    ]))

    # 1. What we are adding
    story.append(Paragraph("1 · What we are adding", h2))
    story.append(Paragraph(
        "Two modular, self-contained HTML blocks introducing the new GroundID Coffee "
        "product line on the homepage and driving waitlist signups ahead of the mid-June "
        "2026 launch. Both blocks are self-contained (styles scoped, no external "
        "dependencies) and designed to paste into Squarespace Code Blocks.", body))

    story.append(Paragraph("The full section (primary)", h3))
    story.extend(bullets([
        "Launch tag: “New · Launching Mid-June 2026”",
        "Eyebrow: “GroundID Coffee”",
        "Headline: “Coffee is not the ritual. Returning to yourself is.”",
        "Subhead: positions the product + weekly live community session",
        "3-pillar grid: The Principle / The Practice / The Framework",
        "Subscription “What’s included” box (5 bullets)",
        "Primary CTA: <b>Join the GroundID Coffee Waitlist</b> → mailto with pre-filled subject + body",
        "Fine print: waitlist perks (launch pricing, priority onboarding, first roast)",
    ]))

    story.append(Paragraph("The teaser (compact, optional)", h3))
    story.extend(bullets([
        "Horizontal card — copy on left, button on right",
        "Placement: above the fold, sidebar, or near the bottom of the page",
        "Same waitlist mailto CTA",
        "Collapses to stacked layout on mobile",
    ]))

    # 2. Placement
    story.append(Paragraph("2 · Where each block should live", h2))
    placement_data = [
        [Paragraph("<b>Block</b>", body_small),
         Paragraph("<b>Placement</b>", body_small),
         Paragraph("<b>Purpose</b>", body_small)],
        [Paragraph("Teaser card", body_small),
         Paragraph("Near the top of drcarahome-1, below the hero / above the first major section", body_small),
         Paragraph("Catches returning visitors and new traffic immediately. Signals “something new is here.”", body_small)],
        [Paragraph("Full section", body_small),
         Paragraph("Mid-page, ideally after the main “what I do” or “leadership work” section", body_small),
         Paragraph("Deeper dive for visitors who scroll. Carries the ritual, pillars, and subscription details.", body_small)],
    ]
    t = Table(placement_data, colWidths=[1.1 * inch, 2.3 * inch, 3.2 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Both pieces share one CTA (same waitlist mailto). Visitors should only have one "
        "action to take no matter where they land.", body_small))

    # 3. Voice & tone
    story.append(Paragraph("3 · Voice &amp; tone (must preserve)", h2))
    story.append(Paragraph(
        "The copy is in Dr. Cara’s established voice: <b>grounded, confident, unhurried, "
        "intentional.</b> Do not soften or “marketize” it.", body))
    story.extend(bullets([
        "Not stimulation → intentionality",
        "Not product features → ritual and philosophy",
        "Not slogans → cues for a mindset",
        "Not “wake up energized” copy → “return to yourself before the day runs you”",
    ]))
    story.append(Paragraph(
        "Short declarative sentences. No exclamation marks. No emoji. No "
        "“elevate / unleash / unlock your best self” language.", body))
    story.append(Paragraph(
        "The three packaging lines are permanent and appear verbatim on the bag and in this section:", body))
    story.append(Paragraph("“Connect to yourself so you can connect to others.”  <i>(The Principle)</i>", quote))
    story.append(Paragraph("“Choose intentionality with each cup of GroundID.”  <i>(The Practice)</i>", quote))
    story.append(Paragraph("“You can only control how you Receive, Perceive, and Respond.”  <i>(The Framework)</i>", quote))

    story.append(PageBreak())

    # 4. Visual system
    story.append(Paragraph("4 · Visual system", h2))
    color_data = [
        [Paragraph("<b>Token</b>", body_small), Paragraph("<b>Hex</b>", body_small), Paragraph("<b>Use</b>", body_small)],
        ["Primary orange", "#c84200", "Headlines of interest, CTA buttons, left borders"],
        ["Orange light (hover)", "#e05a1a", "CTA hover"],
        ["Orange pale (tint)", "#fff9f4", "Callout backgrounds, pillar 1 bg"],
        ["Gold", "#C9A850", "Pillar 2 accent, secondary dividers"],
        ["Gold pale", "#FDF9EF", "Pillar 2 background"],
        ["Pink", "#E8B4B8", "Pillar 3 accent"],
        ["Pink pale", "#FBF1F1", "Pillar 3 background"],
        ["Dark text", "#2A2320", "Headlines"],
        ["Body text", "#4A3F38", "Paragraphs"],
        ["Muted", "#A09080", "Fine print"],
    ]
    ct = Table(color_data, colWidths=[1.6 * inch, 1.1 * inch, 3.9 * inch])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(ct)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Typography", h3))
    story.extend(bullets([
        "Serif: <b>EB Garamond</b> (via Google Fonts; falls back to Georgia)",
        "Sans: system UI stack (<font face='Courier'>-apple-system, BlinkMacSystemFont, Segoe UI, Arial, Helvetica, sans-serif</font>)",
    ]))

    story.append(Paragraph("Design philosophy (direct from Dr. Cara)", h3))
    story.append(Paragraph(
        "“Orange as the primary color conveys warmth, confidence, and energy without feeling "
        "aggressive. Pink and gold are used as light accents — supporting, not overpowering. "
        "This balance matters.”", quote))
    story.append(Paragraph(
        "“The design feels confident and intentional, not busy or decorative. It signals "
        "presence and leadership rather than trend or novelty.”", quote))
    story.append(Paragraph(
        "If imagery is added: a single product photo of a GroundID Coffee bag can sit at the "
        "top of the full section. No lifestyle collages. No grid of bean icons. Keep it minimal.", body))

    # 5. Implementation
    story.append(Paragraph("5 · Implementation notes", h2))

    story.append(Paragraph("How to paste into Squarespace", h3))
    story.extend(bullets([
        "Open drcara.net/drcarahome-1 in edit mode",
        "Add a <b>Code Block</b> where each section should live",
        "Paste the entire contents of the .html file",
        "Leave “Display Source” unchecked → Save",
    ]))

    story.append(Paragraph("Scoping", h3))
    story.append(Paragraph(
        "All styles live inside <font face='Courier'>.gid-coffee-section</font> or "
        "<font face='Courier'>.gid-coffee-teaser</font>. They won’t bleed into the "
        "Squarespace theme, and the theme shouldn’t bleed into them — with one caveat below.", body))

    story.append(Paragraph("Known Squarespace gotchas", h3))
    story.extend(bullets([
        "Squarespace link styles may try to override the CTA color. CSS already uses "
        "<font face='Courier'>!important</font> on the CTA’s <font face='Courier'>color</font> and "
        "<font face='Courier'>text-decoration</font> — this is the fix.",
        "If Squarespace’s base &lt;h2&gt; style is aggressive, bump specificity further "
        "(e.g. <font face='Courier'>.gid-coffee-section .gid-headline</font>). Conflicts should be rare.",
        "If EB Garamond isn’t already loaded on the homepage, add the Google Fonts link in "
        "<b>Site Header Code Injection</b> once (see below).",
    ]))
    story.append(Paragraph(
        "&lt;link href=\"https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&amp;display=swap\" rel=\"stylesheet\"&gt;",
        mono))

    story.append(Paragraph("Mobile", h3))
    story.append(Paragraph(
        "Responsive breakpoints at 560px / 640px. The 3-pillar grid collapses to a single "
        "column, and the teaser card stacks with a full-width button.", body))

    # 6. CTA
    story.append(Paragraph("6 · CTA &amp; lead capture", h2))
    story.append(Paragraph("The CTA opens the user’s email client with:", body))
    story.extend(bullets([
        "<b>To:</b> drcara@drcaraa.com",
        "<b>Subject:</b> GroundID Coffee Waitlist",
        "<b>Body (pre-filled):</b> Please add me to the GroundID Coffee waitlist. "
        "Name: ____.  City / Shipping country: ____.  I’d like to be notified when "
        "subscriptions open in mid-June 2026.",
    ]))
    story.append(Paragraph(
        "Intentional for launch. When a proper form + backend is ready, swap the "
        "<font face='Courier'>href</font> in one place "
        "(<font face='Courier'>.gid-cta</font> or <font face='Courier'>.gid-teaser-cta</font>) — "
        "no other changes required.", body))

    # 7. Quality bar
    story.append(Paragraph("7 · Quality bar", h2))
    story.extend(bullets([
        "The coffee section should feel <b>of a piece</b> with the existing funnel "
        "(quiz, profile landing pages, confirmation pages). Not a separate brand expression.",
        "It must not feel Canva-generated. Restraint is the point.",
        "The design should earn the attention it’s asking for: calm, confident, grounded, purposeful.",
    ]))

    # 8. Files
    story.append(Paragraph("8 · Files in this handoff folder", h2))
    story.append(Paragraph(
        "/designer-handoff/<br/>"
        "├── GroundID-Coffee-Section-Designer-Brief.md (source of this PDF)<br/>"
        "├── GroundID-Coffee-Section-Designer-Brief.pdf (this file)<br/>"
        "├── drcarahome-coffee-section.html (full mid-page section)<br/>"
        "└── drcarahome-coffee-teaser.html (compact above-the-fold card)", mono))
    story.append(Paragraph(
        "Both .html files are drop-in ready. Open them in a browser first to QA before "
        "pasting into Squarespace.", body))

    # 9. Contact
    story.append(Paragraph("9 · Contact", h2))
    story.append(Paragraph("<b>Dr. Cara Alexander</b>", body))
    story.extend([
        Paragraph("drcara@drcaraa.com", body_small),
        Paragraph("drcara.net", body_small),
        Paragraph("@drcaraa", body_small),
    ])
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Questions on voice, visual system, or placement — direct to Dr. Cara.", body_muted))

    doc.build(story)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, 'GroundID-Coffee-Section-Designer-Brief.pdf')
    build_pdf(out)
    print(f"Generated: {out}")
