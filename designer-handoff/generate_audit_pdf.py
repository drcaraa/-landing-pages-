#!/usr/bin/env python3
"""Generate the Dr. Cara landing pages audit PDF (v2 — with new findings + Coffee)."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)

ORANGE = HexColor('#c84200')
ORANGE_LIGHT = HexColor('#fff9f4')
RED = HexColor('#b33a1e')
AMBER = HexColor('#c89000')
PINK = HexColor('#d81360')
GREEN = HexColor('#2d7a4f')
DARK = HexColor('#2A2320')
BODY = HexColor('#4A3F38')
MUTED = HexColor('#A09080')
BORDER = HexColor('#E8E0D8')
ROW_ALT = HexColor('#FAF6F1')
COFFEE = HexColor('#6B3410')

h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22, leading=28,
                    textColor=DARK, spaceAfter=4)
sub = ParagraphStyle('sub', fontName='Helvetica', fontSize=12, leading=16,
                     textColor=ORANGE, spaceAfter=14)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13, leading=18,
                    textColor=ORANGE, spaceBefore=16, spaceAfter=6)
h2_coffee = ParagraphStyle('h2c', fontName='Helvetica-Bold', fontSize=13, leading=18,
                           textColor=COFFEE, spaceBefore=16, spaceAfter=6)
body = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13,
                      textColor=BODY, spaceAfter=4)
meta = ParagraphStyle('meta', fontName='Helvetica', fontSize=9, leading=13,
                      textColor=MUTED, spaceAfter=2)
cell = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=11,
                      textColor=BODY)
cell_bold = ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=8.5,
                           leading=11, textColor=DARK)
cell_mono = ParagraphStyle('cellm', fontName='Courier', fontSize=8, leading=11,
                           textColor=BODY)
bullet = ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.5, leading=13,
                        textColor=BODY, spaceAfter=2, leftIndent=14, bulletIndent=4)


def rule(color=ORANGE, thickness=2):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=4, spaceAfter=8)


def P(text, style=cell):
    return Paragraph(text, style)


def audit_table(rows, col_widths, header_color=ORANGE):
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, BORDER),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def build(out_path):
    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=0.55 * inch, rightMargin=0.55 * inch,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch,
        title="Dr. Cara Landing Pages — Revision Chart",
        author="Dr. Cara Alexander",
    )
    story = []

    # Title
    story.append(P("Dr. Cara Landing Pages", h1))
    story.append(P("Revision Chart &amp; Designer Handoff", sub))
    story.append(rule(ORANGE, 2.5))

    story.append(P("<b>Client:</b> Dr. Cara Alexander — Connected Leadership", meta))
    story.append(P("<b>Prepared:</b> April 17, 2026", meta))
    story.append(P("<b>Scope:</b> Audit of 6 drcara.net landing pages + GroundID Coffee integration", meta))
    story.append(P("<b>Total items:</b> 25 audit revisions + 1 new feature (Coffee)", meta))
    story.append(Spacer(1, 12))

    story.append(P("Pages Audited", h2))
    pages = [
        "/drcarahome-1 — Home",
        "/drcara-framework — Framework",
        "/drcara-work-together — Work Together",
        "/drcara-about — About",
        "/drcara-lead-free-now — Lead Free Now",
        "/drcara-contact-new — Contact",
    ]
    for p in pages:
        story.append(Paragraph(f"• {p}", bullet))
    story.append(Spacer(1, 6))

    # ------------------------------------------------------------------
    # Priority 1 — Broken links / wrong destinations
    # ------------------------------------------------------------------
    story.append(P("Priority 1 — Broken Links, Wrong Destinations &amp; Missing Links", h2))
    story.append(P("Critical. These either send users to the wrong page, to outdated content, or are missing entirely.", body))

    p1_rows = [
        [P("#", cell_bold), P("Page", cell_bold), P("Element", cell_bold),
         P("Current State", cell_bold), P("Required Fix", cell_bold)],
        [P("1", cell), P("Work Together", cell),
         P("Logo / Home link", cell),
         P("Points to <font face='Courier'>/drcarahome</font> — older page w/ outdated framework", cell),
         P("Change to <font face='Courier'>/drcarahome-1</font>", cell)],
        [P("2", cell), P("Lead Free Now", cell),
         P("&quot;Try the Virtual Mind Free&quot; button", cell),
         P("Links to <font face='Courier'>groundid.net</font> (assessment)", cell),
         P("Link to <font face='Courier'>delphi.ai/drcara</font>", cell)],
        [P("3", cell), P("Lead Free Now", cell),
         P("&quot;Explore Ways to Work Together&quot; button", cell),
         P("Links to <font face='Courier'>groundid.net</font>", cell),
         P("Link to <font face='Courier'>/drcara-work-together</font>", cell)],
        [P("4", cell), P("Work Together", cell),
         P("&quot;Enroll Now&quot; button (GroundID Leader Program, orange section)", cell),
         P("Incorrect destination — points to assessment instead of enrollment", cell),
         P("Link to enrollment / Stripe / <font face='Courier'>/drcara-contact-new</font>", cell)],
        [P("5", cell), P("Work Together", cell),
         P("&quot;Contact Dr. Cara&quot; button", cell),
         P("Links to <font face='Courier'>groundid.net</font>", cell),
         P("Link to <font face='Courier'>/drcara-contact-new</font>", cell)],
        [P("6", cell), P("Home", cell),
         P("&quot;See the Framework →&quot; button", cell),
         P("Links to <font face='Courier'>http://delphi.ai/...</font> — Virtual Mind, insecure HTTP, label mismatch", cell),
         P("Relabel to &quot;Try the Virtual Mind&quot; OR relink to <font face='Courier'>/drcara-framework</font>; upgrade to HTTPS", cell)],
        [P("20", cell), P("Work Together", cell),
         P("Virtual Mind mention in orange section", cell),
         P("<b>No link at all</b> — paragraph describes Virtual Mind but doesn&apos;t link to it", cell),
         P("Add link to <font face='Courier'>delphi.ai/drcara</font>", cell)],
        [P("21", cell), P("Lead Free Now", cell),
         P("Virtual Mind reference link", cell),
         P("Incorrect destination", cell),
         P("Point to <font face='Courier'>delphi.ai/drcara</font>", cell)],
        [P("22", cell), P("Lead Free Now", cell),
         P("&quot;Go Deeper&quot; link", cell),
         P("Incorrect destination", cell),
         P("Confirm intended target — likely <font face='Courier'>/drcara-work-together</font> or <font face='Courier'>/drcara-framework</font>", cell)],
        [P("23", cell), P("Contact", cell),
         P("LinkedIn link", cell),
         P("Wrong URL", cell),
         P("Correct to <font face='Courier'>linkedin.com/in/drcaraa/</font>", cell)],
    ]
    story.append(audit_table(
        p1_rows,
        col_widths=[0.3 * inch, 1.0 * inch, 1.5 * inch, 2.3 * inch, 2.3 * inch],
        header_color=RED,
    ))

    story.append(PageBreak())

    # ------------------------------------------------------------------
    # Priority 2 — Design & Visual Fixes (NEW)
    # ------------------------------------------------------------------
    story.append(P("Priority 2 — Design &amp; Visual Fixes", h2))
    p2_rows = [
        [P("#", cell_bold), P("Page", cell_bold),
         P("Issue", cell_bold), P("Required Fix", cell_bold)],
        [P("24", cell), P("Framework", cell),
         P("Only the <b>last box</b> in the framework section is highlighted — others appear un-highlighted / inconsistent", cell),
         P("Highlight all 4 framework boxes consistently (The Architect, The Carrier, The Performer, The Sentinel)", cell)],
        [P("25", cell), P("About", cell),
         P("AI-generated photo at bottom of page looks low quality / uncanny", cell),
         P("Replace with real photo of Dr. Cara or remove entirely", cell)],
    ]
    story.append(audit_table(
        p2_rows,
        col_widths=[0.3 * inch, 1.1 * inch, 3.6 * inch, 2.4 * inch],
        header_color=PINK,
    ))

    # ------------------------------------------------------------------
    # Priority 3 — Data Inconsistencies
    # ------------------------------------------------------------------
    story.append(P("Priority 3 — Data Inconsistencies", h2))
    p3_rows = [
        [P("#", cell_bold), P("Issue", cell_bold),
         P("Where It Appears", cell_bold), P("Required Fix", cell_bold)],
        [P("7", cell),
         P("Email address mismatch: <font face='Courier'>cara@drcaraa.com</font> vs <font face='Courier'>drcara@drcaraa.com</font>", cell),
         P("Home / Framework / About use <font face='Courier'>cara@</font>; Contact uses <font face='Courier'>drcara@</font>", cell),
         P("Confirm correct address, apply across all 6 pages", cell)],
        [P("8", cell),
         P("Domain mismatch: site is <font face='Courier'>drcara.net</font> but email domain is <font face='Courier'>drcaraa.com</font> (two a&apos;s)", cell),
         P("Sitewide", cell),
         P("Verify intentional; if typo, fix", cell)],
        [P("9", cell),
         P("Instagram handle: copy says <font face='Courier'>@drcaraa</font>, actual handle is <font face='Courier'>@dr.caraa</font>", cell),
         P("Contact page body copy", cell),
         P("Update copy to <font face='Courier'>@dr.caraa</font>", cell)],
    ]
    story.append(audit_table(
        p3_rows,
        col_widths=[0.3 * inch, 2.5 * inch, 2.3 * inch, 2.3 * inch],
        header_color=ORANGE,
    ))

    # ------------------------------------------------------------------
    # Priority 4 — Navigation & Structure
    # ------------------------------------------------------------------
    story.append(P("Priority 4 — Navigation &amp; Structure", h2))
    p4_rows = [
        [P("#", cell_bold), P("Page", cell_bold),
         P("Issue", cell_bold), P("Required Fix", cell_bold)],
        [P("10", cell), P("Home", cell),
         P("Top nav includes &quot;Home&quot; item; other pages do not", cell),
         P("Remove &quot;Home&quot; from top nav (logo handles it)", cell)],
        [P("11", cell), P("All pages", cell),
         P("&quot;Contact&quot; only in footer, not primary nav", cell),
         P("Add Contact to top nav across all pages", cell)],
        [P("12", cell), P("<font face='Courier'>/drcarahome</font>", cell),
         P("Old page still live with outdated framework copy", cell),
         P("Redirect to <font face='Courier'>/drcarahome-1</font> or delete", cell)],
    ]
    story.append(audit_table(
        p4_rows,
        col_widths=[0.3 * inch, 1.3 * inch, 2.9 * inch, 2.9 * inch],
        header_color=AMBER,
    ))

    story.append(PageBreak())

    # ------------------------------------------------------------------
    # Priority 5 — Copy & Brand Consistency
    # ------------------------------------------------------------------
    story.append(P("Priority 5 — Copy &amp; Brand Consistency", h2))
    p5_rows = [
        [P("#", cell_bold), P("Issue", cell_bold),
         P("Where", cell_bold), P("Required Fix", cell_bold)],
        [P("13", cell),
         P("Brand name inconsistent: &quot;Ground ID&quot; vs &quot;GroundID&quot; vs &quot;groundid&quot;", cell),
         P("Sitewide", cell),
         P("Standardize to &quot;GroundID&quot;", cell)],
        [P("14", cell),
         P("Copyright reads &quot;Copyright @ 2026 | Dr. Cara | All Right Reserved&quot;", cell),
         P("Contact page footer", cell),
         P("Change to &quot;© 2026 | Dr. Cara | All Rights Reserved&quot;", cell)],
        [P("15", cell),
         P("Framework naming varies: &quot;Receive · Perceive · Respond&quot; vs &quot;RPR Framework&quot;", cell),
         P("Multiple pages", cell),
         P("Pick one canonical format, apply sitewide", cell)],
    ]
    story.append(audit_table(
        p5_rows,
        col_widths=[0.3 * inch, 3.0 * inch, 1.5 * inch, 2.6 * inch],
        header_color=AMBER,
    ))

    # ------------------------------------------------------------------
    # Priority 6 — Security, Link Hygiene & Legal
    # ------------------------------------------------------------------
    story.append(P("Priority 6 — Security, Link Hygiene &amp; Legal", h2))
    p6_rows = [
        [P("#", cell_bold), P("Issue", cell_bold),
         P("Where", cell_bold), P("Required Fix", cell_bold)],
        [P("16", cell), P("Pinterest link uses <font face='Courier'>http://</font>", cell),
         P("Every page footer", cell),
         P("Change to <font face='Courier'>https://</font>", cell)],
        [P("17", cell),
         P("YouTube URL has tracking param on some pages, clean on others", cell),
         P("Footer varies by page", cell),
         P("Standardize to clean <font face='Courier'>youtube.com/@drcaraa</font>", cell)],
        [P("18", cell),
         P("&quot;See the Framework&quot; button uses insecure <font face='Courier'>http://</font>", cell),
         P("Home page", cell),
         P("Change to <font face='Courier'>https://</font>", cell)],
        [P("19", cell),
         P("<b>Legal pages need to be updated</b> — Privacy Policy &amp; Terms &amp; Conditions incomplete, unwired, or outdated", cell),
         P("Footer, every page", cell),
         P("Draft/refresh Privacy + Terms, wire up footer links sitewide", cell)],
    ]
    story.append(audit_table(
        p6_rows,
        col_widths=[0.3 * inch, 2.8 * inch, 1.7 * inch, 2.6 * inch],
        header_color=AMBER,
    ))

    story.append(PageBreak())

    # ------------------------------------------------------------------
    # NEW FEATURE — GroundID Coffee section
    # ------------------------------------------------------------------
    story.append(P("New Feature — GroundID Coffee Section", h2_coffee))
    story.append(P(
        "A dedicated <b>GroundID Coffee</b> section must be integrated into the site for the mid-June 2026 product launch. "
        "The designer handoff has already been prepared and is located in this same folder. Implement per the existing brief.",
        body,
    ))

    coffee_rows = [
        [P("Deliverable", cell_bold), P("File", cell_bold), P("Purpose", cell_bold)],
        [P("Full mid-page section", cell),
         P("drcarahome-coffee-section.html", cell_mono),
         P("Primary section to drop into the Home page", cell)],
        [P("Above-the-fold teaser card", cell),
         P("drcarahome-coffee-teaser.html", cell_mono),
         P("Compact teaser linking into the section", cell)],
        [P("Designer brief (full spec)", cell),
         P("GroundID-Coffee-Section-Designer-Brief.pdf / .md", cell_mono),
         P("Voice, visuals, placement, implementation", cell)],
        [P("Zipped handoff bundle", cell),
         P("GroundID-Coffee-Designer-Handoff.zip", cell_mono),
         P("All above files packaged", cell)],
    ]
    story.append(audit_table(
        coffee_rows,
        col_widths=[1.9 * inch, 2.7 * inch, 2.6 * inch],
        header_color=COFFEE,
    ))

    story.append(Spacer(1, 8))
    story.append(P("<b>Placement:</b> Mid-page on <font face='Courier'>/drcarahome-1</font>, with the teaser card above the fold.", body))
    story.append(P("<b>Destination for Coffee CTAs:</b> <font face='Courier'>drcara.net/drcarahome-1</font> — confirm it is wired to the new home, NOT the old <font face='Courier'>/drcarahome</font>.", body))
    story.append(P("<b>Launch:</b> Mid-June 2026. Build now, reveal at launch.", body))
    story.append(P("<b>Tone / palette:</b> Connected Leadership voice; GroundID orange (#c84200) with warm neutrals. Do not treat as a generic product card.", body))

    # ------------------------------------------------------------------
    # Verified working
    # ------------------------------------------------------------------
    story.append(P("Verified Working — No Action Needed", h2))
    ok_rows = [
        [P("Element", cell_bold), P("Destination", cell_bold), P("Status", cell_bold)],
        [P("Main nav: Framework", cell), P("/drcara-framework", cell_mono), P("Working", cell)],
        [P("Main nav: Work Together", cell), P("/drcara-work-together", cell_mono), P("Working", cell)],
        [P("Main nav: About", cell), P("/drcara-about", cell_mono), P("Working", cell)],
        [P("Main nav: Lead Free Now", cell), P("/drcara-lead-free-now", cell_mono), P("Working", cell)],
        [P("Footer: Contact", cell), P("/drcara-contact-new", cell_mono), P("Working", cell)],
        [P("&quot;Take the Free Assessment&quot; buttons", cell), P("https://groundid.net", cell_mono), P("Working", cell)],
        [P("Virtual Mind announcement bar", cell), P("https://www.delphi.ai/drcara", cell_mono), P("Working", cell)],
        [P("Instagram", cell), P("instagram.com/dr.caraa", cell_mono), P("Working", cell)],
        [P("Phone", cell), P("301-852-9424", cell_mono), P("Working", cell)],
        [P("Pricing ($49/mo, $9,000)", cell), P("Consistent sitewide", cell), P("Working", cell)],
    ]
    story.append(audit_table(
        ok_rows,
        col_widths=[2.6 * inch, 2.8 * inch, 1.8 * inch],
        header_color=GREEN,
    ))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    story.append(P("Summary", h2))
    story.append(Paragraph("• <b>10</b> broken / mislinked / missing links (Priority 1)", bullet))
    story.append(Paragraph("• <b>2</b> design &amp; visual issues (Priority 2)", bullet))
    story.append(Paragraph("• <b>3</b> data inconsistencies (Priority 3)", bullet))
    story.append(Paragraph("• <b>3</b> navigation / structure issues (Priority 4)", bullet))
    story.append(Paragraph("• <b>3</b> copy / brand inconsistencies (Priority 5)", bullet))
    story.append(Paragraph("• <b>4</b> link hygiene, security &amp; legal issues (Priority 6)", bullet))
    story.append(Paragraph("• <b>1</b> new feature — GroundID Coffee section to integrate", bullet))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Total: 25 audit items + 1 new feature.</b> "
        "Recommended order: Priority 1 → 2 → 3 → 4 → 5 → 6 → Coffee integration.",
        body,
    ))

    doc.build(story)


if __name__ == "__main__":
    out = "/Users/dr.caraalexander/Claude Code Landing pages for DR. Cara/designer-handoff/DR-CARA-Landing-Pages-Audit.pdf"
    build(out)
    print(f"Wrote {out}")
