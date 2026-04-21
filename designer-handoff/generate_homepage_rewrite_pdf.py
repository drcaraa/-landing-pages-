#!/usr/bin/env python3
"""Generate the drcara.net Homepage Rewrite Spec PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)
import os

ARCHITECT = HexColor('#c84200')
CARRIER = HexColor('#c89000')
PERFORMER = HexColor('#d81360')
SENTINEL = HexColor('#df4f0f')
ORANGE_LIGHT = HexColor('#fff9f4')
DARK = HexColor('#2A2320')
BODY = HexColor('#4A3F38')
MUTED = HexColor('#A09080')
BORDER = HexColor('#E8E0D8')

h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22, leading=28,
                    textColor=DARK, spaceAfter=6)
sub = ParagraphStyle('sub', fontName='Helvetica', fontSize=13, leading=17,
                     textColor=ARCHITECT, spaceAfter=14)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=14, leading=20,
                    textColor=ARCHITECT, spaceBefore=18, spaceAfter=8)
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
copy_block = ParagraphStyle('copy', fontName='Helvetica', fontSize=10.5, leading=16,
                            textColor=DARK, leftIndent=12, rightIndent=12,
                            spaceBefore=4, spaceAfter=8,
                            backColor=ORANGE_LIGHT, borderPadding=8)


def bullets(items):
    return [Paragraph(f"• {t}", bullet) for t in items]


def rule(color=ARCHITECT, thickness=2):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=4, spaceAfter=8)


def build_pdf(out_path):
    doc = SimpleDocTemplate(out_path, pagesize=letter,
                            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch,
                            title="drcara.net Homepage — Rewrite Spec",
                            author="Dr. Cara Alexander")
    story = []

    # Title
    story.append(Paragraph("drcara.net Homepage", h1))
    story.append(Paragraph("Rewrite Spec — Reduce Redundancy, Increase Curiosity, Lift Conversion", sub))
    story.append(rule(ARCHITECT, 2.5))

    story.append(Paragraph("<b>Page:</b> drcara.net/drcarahome-1", meta))
    story.append(Paragraph("<b>Goal:</b> reduce redundancy, open curiosity loops, push more visitors into the assessment funnel and (secondarily) the Virtual Mind paid tier.", meta))
    story.append(Spacer(1, 10))

    cta_data = [
        [Paragraph("<b>CTA priority</b>", body_small), Paragraph("<b>Action</b>", body_small)],
        [Paragraph("Primary", body_small), Paragraph("Take the Leadership Origin Profile (free, 3 min)", body_small)],
        [Paragraph("Secondary", body_small), Paragraph("Try the Virtual Mind (free, no email)", body_small)],
        [Paragraph("Tertiary", body_small), Paragraph("See the Framework", body_small)],
    ]
    t = Table(cta_data, colWidths=[1.2 * inch, 5.4 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)

    # New section order
    story.append(Paragraph("New Section Order", h2))
    story.extend(bullets([
        "Hero",
        "Five Tensions <i>(moved up from position 6)</i>",
        "Leadership Origin Profile assessment (with 4 profile teasers)",
        "Proof bar (stats reframed) + 1 testimonial",
        "About Dr. Cara (short)",
        "Virtual Mind (paid on-ramp)",
        "Final CTA",
        "Footer",
    ]))
    story.append(Paragraph(
        "<b>Cut entirely:</b> the standalone About/Value Proposition block under the hero "
        "(duplicates hero + Problem section). Cut the standalone “What's actually happening” "
        "section — its job is now done by the Five Tensions block.", body))

    # Section 1 - Hero
    story.append(Paragraph("Section 1 — Hero", h2))
    story.append(Paragraph("Eyebrow (small caps, above headline)", h3))
    story.append(Paragraph("CONNECTED LEADERSHIP · DR. CARA ALEXANDER", copy_block))

    story.append(Paragraph("Headline (H1)", h3))
    story.append(Paragraph("The leaders everyone relies on burn out first.<br/>There’s a reason — and it isn’t workload.", copy_block))

    story.append(Paragraph("Subhead (1 line)", h3))
    story.append(Paragraph("Find out which of 4 protective patterns is running your leadership right now.", copy_block))

    story.append(Paragraph("Primary CTA button", h3))
    story.append(Paragraph("See Your Pattern — 3 Min →", copy_block))

    story.append(Paragraph("Secondary link (under button, smaller)", h3))
    story.append(Paragraph("or try the Virtual Mind free, no email →", copy_block))

    story.append(Paragraph("Hero image", h3))
    story.append(Paragraph(
        "Keep current image OR swap for a portrait of Dr. Cara (eye contact, neutral background). "
        "Portraits convert better than abstract art.", body))

    story.append(Paragraph("Trust strip directly under hero (replaces current paragraph block)", h3))
    story.append(Paragraph("25+ years clinical &amp; executive · Tested across 4 continents · 7× average coaching ROI", copy_block))

    # Section 2 - Five Tensions
    story.append(Paragraph("Section 2 — Five Tensions <i>(moved up from position 6)</i>", h2))
    story.append(Paragraph("Headline", h3))
    story.append(Paragraph("Five tensions every high-performing leader knows.", copy_block))
    story.append(Paragraph("Subhead", h3))
    story.append(Paragraph("And rarely names out loud.", copy_block))

    story.append(Paragraph(
        "Keep the existing 5 cards (Broken Rung, Personality Tax, Double Bind, Invisible Load, "
        "Ambition Tension). Tighten each card to ONE sentence + ONE stat where possible. Example:", body))
    story.append(Paragraph("<b>The Invisible Load</b><br/>"
                           "You absorb 44% more non-promotable work than peers — and it never "
                           "shows up in your review.", copy_block))
    story.append(Paragraph("CTA at bottom of section", h3))
    story.append(Paragraph("Which tension is running yours? → See Your Pattern (3 min)", copy_block))

    story.append(PageBreak())

    # Section 3 - Origin Profile
    story.append(Paragraph("Section 3 — Leadership Origin Profile (the assessment)", h2))
    story.append(Paragraph("Headline", h3))
    story.append(Paragraph("Four leaders. Four origins. One is running yours.", copy_block))
    story.append(Paragraph("Subhead", h3))
    story.append(Paragraph(
        "A free 3-minute diagnostic that names the protective pattern shaping your daily decisions — "
        "and gives you the first move to lead without it.", copy_block))

    story.append(Paragraph("Four profile teaser cards (grid, 2x2 or 4-across)", h3))
    profile_data = [
        [Paragraph("<b>Profile</b>", body_small),
         Paragraph("<b>Color</b>", body_small),
         Paragraph("<b>One-line tease</b>", body_small)],
        [Paragraph("The Architect", body_small),
         Paragraph("#c84200", mono),
         Paragraph("Builds the system everyone else depends on — and can’t stop revising it.", body_small)],
        [Paragraph("The Carrier", body_small),
         Paragraph("#c89000", mono),
         Paragraph("Holds what no one else will touch. Pays for it in private.", body_small)],
        [Paragraph("The Performer", body_small),
         Paragraph("#d81360", mono),
         Paragraph("Reads every room before they enter it. Never stops calibrating.", body_small)],
        [Paragraph("The Sentinel", body_small),
         Paragraph("#df4f0f", mono),
         Paragraph("Sees the risk first. Carries the weight of preventing it.", body_small)],
    ]
    pt = Table(profile_data, colWidths=[1.3 * inch, 0.9 * inch, 4.4 * inch])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TEXTCOLOR', (0, 1), (0, 1), ARCHITECT),
        ('TEXTCOLOR', (0, 2), (0, 2), CARRIER),
        ('TEXTCOLOR', (0, 3), (0, 3), PERFORMER),
        ('TEXTCOLOR', (0, 4), (0, 4), SENTINEL),
        ('FONT', (0, 1), (0, -1), 'Helvetica-Bold', 9),
    ]))
    story.append(pt)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Primary CTA", h3))
    story.append(Paragraph(
        "Take the Free Assessment →<br/>"
        "<i>12 questions · 3 minutes · No account · You’ll get your profile + a 3-page "
        "playbook instantly</i>", copy_block))

    # Section 4 - Proof
    story.append(Paragraph("Section 4 — Proof", h2))
    story.append(Paragraph("Stats bar (reframe with specificity)", h3))
    story.extend(bullets([
        "<b>25+ years</b> — clinical psychology + executive coaching",
        "<b>4 continents</b> — where the GroundID framework has been tested in cohorts",
        "<b>85% completion</b> — GroundID cohorts vs. 5% industry average for self-paced programs",
        "<b>7× ROI</b> — average reported by Fortune-level coaching clients (2024)",
    ]))

    story.append(Paragraph("Testimonial block (single named quote, large type)", h3))
    story.append(Paragraph(
        "“I stopped overthinking decisions inside two weeks. The framework gave me a place "
        "to set things down.”<br/>— [Name], [Title], [Company]", quote))
    story.append(Paragraph(
        "<i>If a current testimonial isn’t usable verbatim, ask client for a one-line approval.</i>",
        body_muted))

    # Section 5 - About
    story.append(Paragraph("Section 5 — About Dr. Cara (short)", h2))
    story.append(Paragraph("Headline", h3))
    story.append(Paragraph("Why this works.", copy_block))
    story.append(Paragraph("Body (3-4 sentences max)", h3))
    story.append(Paragraph(
        "Dr. Cara Alexander spent 25 years as a clinical psychologist before building "
        "GroundID — the framework she now teaches to executives across 4 continents. "
        "She doesn’t coach behavior. She helps you understand the protective pattern "
        "underneath it, so the change actually holds.", copy_block))
    story.append(Paragraph("CTA link (text, not button)", h3))
    story.append(Paragraph("Read the full story →", copy_block))

    story.append(PageBreak())

    # Section 6 - Virtual Mind
    story.append(Paragraph("Section 6 — GroundID Virtual Mind (paid on-ramp)", h2))
    story.append(Paragraph("Eyebrow", h3))
    story.append(Paragraph("ALWAYS AVAILABLE", copy_block))
    story.append(Paragraph("Headline", h3))
    story.append(Paragraph("Your 24/7 thinking partner.", copy_block))
    story.append(Paragraph("Subhead", h3))
    story.append(Paragraph(
        "Trained on 25 years of Dr. Cara’s clinical and executive expertise. The Virtual "
        "Mind walks you through Receive → Perceive → Respond in real time, the moment "
        "you need it.", copy_block))

    story.append(Paragraph("Simplify pricing display — two columns, not three", h3))
    pricing_data = [
        [Paragraph("<b>Try It Free</b>", body_small),
         Paragraph("<b>Premium — $49/mo</b>", body_small)],
        [Paragraph("5 minutes · Email required", body_small),
         Paragraph("Unlimited 24/7 access", body_small)],
        [Paragraph("Full RPR walkthrough", body_small),
         Paragraph("Weekly GroundID Live sessions", body_small)],
        [Paragraph("", body_small),
         Paragraph("Premium Prompt Guide", body_small)],
        [Paragraph("<b>Try the Virtual Mind →</b>", body_small),
         Paragraph("<b>Start Premium →</b>", body_small)],
    ]
    pricing_table = Table(pricing_data, colWidths=[3.3 * inch, 3.3 * inch])
    pricing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE_LIGHT),
        ('BACKGROUND', (0, -1), (-1, -1), ORANGE_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(pricing_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Move the “2 minutes / no email” tier inside the product itself as a pre-signup "
        "demo. Two visible options on the homepage converts better than three.</i>",
        body_muted))

    # Section 7 - Final CTA
    story.append(Paragraph("Section 7 — Final CTA", h2))
    story.append(Paragraph("Headline", h3))
    story.append(Paragraph("You lead well. Now lead free.", copy_block))
    story.append(Paragraph("Subhead", h3))
    story.append(Paragraph(
        "Start with the 3-minute assessment. You’ll know your pattern by the time your "
        "coffee’s cold.", copy_block))
    story.append(Paragraph("Primary button", h3))
    story.append(Paragraph("See Your Pattern →", copy_block))
    story.append(Paragraph("Secondary link", h3))
    story.append(Paragraph("or talk to Dr. Cara about coaching →", copy_block))

    # Section 8 - Footer
    story.append(Paragraph("Section 8 — Footer", h2))
    story.append(Paragraph(
        "Keep current footer. One change: move the email/phone above the social icons "
        "(people scan top-down).", body))

    story.append(PageBreak())

    # Copy rules
    story.append(Paragraph("Copy rules for whoever implements this", h2))
    story.extend(bullets([
        "The “weight / carry / pressure” metaphor appears only <b>twice</b> on the page — "
        "hero subhead and final CTA. Strip it everywhere else.",
        "Every CTA on the page should be one of three verbs: <b>See</b> (assessment), "
        "<b>Try</b> (Virtual Mind), <b>Read</b> (about/framework). No “Lead Free Now” "
        "buttons — too abstract for a click.",
        "No paragraph longer than <b>3 lines on desktop</b>. Break with line returns.",
        "Every stat needs a <b>year, source, or qualifier</b>. “7× ROI” alone is "
        "unbelievable. “7× ROI — average across 2024 Fortune-level clients” is.",
        "<b>Mobile:</b> the Five Tensions and 4 Profile cards should each be a horizontal "
        "swipe carousel, not a stacked list — they’re scannable assets, not paragraphs.",
    ]))

    # What was removed and why
    story.append(Paragraph("What was removed and why", h2))
    removed_data = [
        [Paragraph("<b>Removed element</b>", body_small),
         Paragraph("<b>Reason</b>", body_small)],
        [Paragraph("“About/Value Proposition” block under hero", body_small),
         Paragraph("Duplicates hero message; no new info", body_small)],
        [Paragraph("“What’s actually happening” Problem section", body_small),
         Paragraph("Five Tensions does this job better with proof", body_small)],
        [Paragraph("“Lead Free Now” button copy", body_small),
         Paragraph("Abstract verb; doesn’t tell user what happens on click", body_small)],
        [Paragraph("3rd Virtual Mind tier (“2 min, no email”)", body_small),
         Paragraph("Choice paralysis on homepage; move inside product", body_small)],
        [Paragraph("“Connected Leadership” + “Lead free” + "
                   "“lead from clarity” as separate brand phrases", body_small),
         Paragraph("Pick one per section; rotating them dilutes recognition", body_small)],
    ]
    rt = Table(removed_data, colWidths=[2.6 * inch, 4.0 * inch])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(rt)

    # Quick wins
    story.append(Paragraph("Quick wins (under 30 minutes each)", h2))
    story.extend(bullets([
        "Cut the “About/Value Proposition Section” entirely — replace with a testimonial.",
        "Rewrite the hero subhead to include a curiosity gap (sample on page 1).",
        "Move “Five Tensions” to position #2.",
        "Change one of the three “free” CTAs in the upper half to a different verb "
        "(e.g. “See your pattern in 3 min”).",
        "Add a specific named testimonial above the Virtual Mind pricing.",
    ]))

    # Contact
    story.append(Paragraph("Contact", h2))
    story.append(Paragraph("<b>Dr. Cara Alexander</b>", body))
    story.append(Paragraph("drcara@drcaraa.com", body_small))
    story.append(Paragraph("drcara.net", body_small))
    story.append(Paragraph("@drcaraa", body_small))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Source: <font face='Courier'>designer-handoff/Homepage-Rewrite-Spec.md</font>",
        body_muted))

    doc.build(story)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, 'DR-CARA-Homepage-Rewrite-Spec.pdf')
    build_pdf(out)
    print(f"Generated: {out}")
