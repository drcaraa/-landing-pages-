#!/usr/bin/env python3
"""Generate the Dr. Cara website link audit PDF for designer handoff."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether,
)

# Brand palette — matches existing handoff docs
ORANGE = HexColor('#c84200')
ORANGE_BRIGHT = HexColor('#E8600A')
ORANGE_LIGHT = HexColor('#FFF0E5')
RED = HexColor('#b33a1e')
AMBER = HexColor('#c89000')
GREEN = HexColor('#2d7a4f')
DARK = HexColor('#2A2320')
BODY = HexColor('#4A3F38')
MUTED = HexColor('#A09080')
BORDER = HexColor('#E8E0D8')
ROW_ALT = HexColor('#FAF6F1')

h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22, leading=27,
                    textColor=DARK, spaceAfter=4)
sub = ParagraphStyle('sub', fontName='Helvetica', fontSize=12, leading=16,
                     textColor=ORANGE, spaceAfter=14)
meta = ParagraphStyle('meta', fontName='Helvetica', fontSize=9, leading=13,
                      textColor=MUTED, spaceAfter=2)
section_h = ParagraphStyle('sh', fontName='Helvetica-Bold', fontSize=14, leading=18,
                           textColor=ORANGE, spaceBefore=14, spaceAfter=4)
section_h_red = ParagraphStyle('shr', fontName='Helvetica-Bold', fontSize=14, leading=18,
                               textColor=RED, spaceBefore=14, spaceAfter=4)
section_h_amber = ParagraphStyle('sha', fontName='Helvetica-Bold', fontSize=14, leading=18,
                                 textColor=AMBER, spaceBefore=14, spaceAfter=4)
section_h_green = ParagraphStyle('shg', fontName='Helvetica-Bold', fontSize=14, leading=18,
                                 textColor=GREEN, spaceBefore=14, spaceAfter=4)
item_h = ParagraphStyle('ih', fontName='Helvetica-Bold', fontSize=11, leading=14,
                        textColor=DARK, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13,
                      textColor=BODY, spaceAfter=4)
note = ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=9, leading=12,
                      textColor=MUTED, spaceAfter=4)
cell = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=11.5,
                      textColor=BODY)
cell_bold = ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=8.8,
                           leading=11.5, textColor=DARK)
cell_mono = ParagraphStyle('cellm', fontName='Courier', fontSize=8, leading=11,
                           textColor=BODY)


def P(text, style=body):
    return Paragraph(text, style)


def rule(color=ORANGE, thickness=2):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=4, spaceAfter=8)


def detail_table(rows, header_color=ORANGE):
    """Two-column key/value table for a single fix item."""
    data = [[P(k, cell_bold), P(v, cell)] for k, v in rows]
    t = Table(data, colWidths=[1.4 * inch, 5.6 * inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (0, -1), ORANGE_LIGHT),
        ('LINEBELOW', (0, 0), (-1, -2), 0.25, BORDER),
        ('BOX', (0, 0), (-1, -1), 0.5, header_color),
    ]))
    return t


def url_map_table(rows):
    header = [P('Anchor text', cell_bold), P('Should always point to', cell_bold)]
    data = [header] + [[P(a, cell), P(u, cell_mono)] for a, u in rows]
    t = Table(data, colWidths=[3.0 * inch, 4.0 * inch], repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, BORDER),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), ROW_ALT))
    # Wrap header row text with white style by overriding paragraph color
    data[0] = [Paragraph(f'<font color="white">{x}</font>', cell_bold)
               for x in ['Anchor text', 'Should always point to']]
    t = Table(data, colWidths=[3.0 * inch, 4.0 * inch], repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def checkbox():
    return P('☐', ParagraphStyle('cb', fontName='Helvetica', fontSize=12,
                                 textColor=DARK))


def build(out_path):
    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch,
        title="Dr. Cara Website — Link Audit & Fix List",
        author="Dr. Cara Alexander",
    )
    story = []

    # ===== TITLE =====
    story.append(P("Dr. Cara Website", h1))
    story.append(P("Link Audit &amp; Fix List for Web Designer", sub))
    story.append(rule(ORANGE, 2.5))

    story.append(P("<b>Client:</b> Dr. Cara Alexander — Connected Leadership", meta))
    story.append(P("<b>Prepared:</b> May 26, 2026", meta))
    story.append(P("<b>Scope:</b> drcara.net (Squarespace) plus linked properties: "
                   "groundid.net, grounid.com, delphi.ai/drcara", meta))
    story.append(P("<b>Pages crawled:</b> 9 on drcara.net &middot; "
                   "<b>Unique URLs checked:</b> 31", meta))
    story.append(P("<b>Total items:</b> 16 (4 Critical &middot; 6 Important &middot; "
                   "6 Housekeeping)", meta))
    story.append(Spacer(1, 14))

    # ===== HOW TO USE =====
    story.append(P("How to Use This Document", section_h))
    story.append(P(
        "This is a designer worklist, not a content review. Each item is one "
        "concrete fix with the exact &lsquo;from &rarr; to&rsquo; change. "
        "Work top-down — Critical first, then Important, then Housekeeping. "
        "When all four Critical fixes are live, the site&rsquo;s broken-link "
        "bleed stops.", body))
    story.append(P(
        "The &lsquo;Where to find it&rsquo; row in each item tells you which "
        "Squarespace page to open and where on the page to look. Check items "
        "off as you complete them.", body))
    story.append(Spacer(1, 10))

    # ===== CRITICAL =====
    story.append(rule(RED, 2))
    story.append(P("CRITICAL &mdash; Broken or Wrong Destination", section_h_red))
    story.append(P("These are confirmed broken (HTTP 404) or sending traffic to the "
                   "wrong place. Fix these first.", note))

    # C1
    story.append(P("☐ &nbsp; C1. Site nav &lsquo;Lead Free Now&rsquo; link is broken on every page",
                   item_h))
    story.append(detail_table([
        ("Where to find it", "Squarespace &rarr; Design &rarr; Site Header &rarr; Main Navigation"),
        ("Element", "Nav item labeled &lsquo;Lead Free Now&rsquo;"),
        ("Current", '<font name="Courier" color="#b33a1e">/drcara-lead-free-now</font> &rarr; <b>HTTP 404</b>'),
        ("Fix to", '<font name="Courier" color="#2d7a4f">/lead-free-now</font> (the real page; returns HTTP 200)'),
        ("Why it matters", "This is in the global nav, so every page on the site has a broken "
                           "link in its header. Highest-impact fix."),
        ("Done when", "Clicking &lsquo;Lead Free Now&rsquo; in the nav from any page loads "
                      "the real Lead Free Now page."),
    ], header_color=RED))

    # C2
    story.append(P("☐ &nbsp; C2. &lsquo;Explore Ways to Work Together&rsquo; button on /contact is broken",
                   item_h))
    story.append(detail_table([
        ("Where to find it", "Squarespace &rarr; Pages &rarr; /contact &rarr; scroll to the "
                             "&lsquo;Explore Ways to Work Together&rsquo; button"),
        ("Element", "Button labeled &lsquo;Explore Ways to Work Together&rsquo;"),
        ("Current", '<font name="Courier" color="#b33a1e">/drcara-work-together</font> &rarr; <b>HTTP 404</b>'),
        ("Fix to", '<font name="Courier" color="#2d7a4f">/work-together</font> (the real page; returns HTTP 200)'),
        ("Done when", "Clicking the button on /contact loads the Work Together page."),
    ], header_color=RED))

    # C3
    story.append(P("☐ &nbsp; C3. Homepage &lsquo;Take the Free Assessment&rsquo; CTAs point to wrong tool",
                   item_h))
    story.append(detail_table([
        ("Where to find it", "Squarespace &rarr; Pages &rarr; Home &rarr; <b>two</b> places: "
                             "(a) the &lsquo;Five Tensions&rsquo; section, "
                             "(b) the &lsquo;Profile assessment&rsquo; section"),
        ("Element", "Two buttons both labeled &lsquo;Take the Free Assessment &rarr;&rsquo;"),
        ("Current", 'Both link to <font name="Courier" color="#b33a1e">delphi.ai/drcara/talk?q=&hellip;</font> &mdash; '
                    "that&rsquo;s the Virtual Mind <b>chat tool</b>, not the assessment"),
        ("Fix to", '<font name="Courier" color="#2d7a4f">https://groundid.net</font> '
                   "(the Leadership Origin Profile quiz)"),
        ("Why it matters", "The label says &lsquo;Assessment&rsquo; but the link goes to a "
                           "chat. Visitors land on the wrong tool. /lead-free-now and "
                           "/framework already do this correctly &mdash; the homepage is the outlier."),
        ("Done when", "Both homepage &lsquo;Take the Free Assessment&rsquo; buttons land on "
                      "https://groundid.net."),
    ], header_color=RED))

    # C4
    story.append(P("☐ &nbsp; C4. Homepage Virtual Mind CTA uses an outdated Delphi URL",
                   item_h))
    story.append(detail_table([
        ("Where to find it", "Squarespace &rarr; Pages &rarr; Home &rarr; hero section &rarr; "
                             "&lsquo;Virtual Mind &mdash; Try It Free, No Email&rsquo; CTA"),
        ("Element", "&lsquo;Virtual Mind &mdash; Try It Free&rsquo; button"),
        ("Current", '<font name="Courier">delphi.ai/drcara/<font color="#b33a1e">talk</font>?q=What+should+I+do+next</font> '
                    "&mdash; Delphi renamed /talk to /chat and currently 301-redirects"),
        ("Fix to", '<font name="Courier">delphi.ai/drcara/<font color="#2d7a4f">chat</font>?q=What+should+I+do+next</font>'),
        ("Why it matters", "Works today because of Delphi&rsquo;s redirect, but redirects "
                           "can be removed any time. Update now to remove the dependency."),
        ("Done when", "The CTA URL contains /chat directly, no redirect involved."),
    ], header_color=RED))

    story.append(PageBreak())

    # ===== IMPORTANT =====
    story.append(rule(AMBER, 2))
    story.append(P("IMPORTANT &mdash; Works, but Needs Cleanup", section_h_amber))
    story.append(P("These don&rsquo;t 404, but they&rsquo;re confusing, inconsistent, or "
                   "unverified.", note))

    # I1
    story.append(P("☐ &nbsp; I1. RPR Coffee launch date contradicts itself", item_h))
    story.append(detail_table([
        ("Where to find it", "Two locations: (a) Homepage RPR Coffee section, "
                             "(b) groundid.net/coffee landing page"),
        ("Issue", "Homepage says &lsquo;Coming <b>July 2026</b>&rsquo;. "
                  "The /coffee page says <b>June 2026</b> for the same product."),
        ("Action", "Decide which month is correct, then update whichever page is "
                   "wrong. Both must agree."),
        ("Done when", "Both pages show the same launch month for RPR Coffee."),
    ], header_color=AMBER))

    # I2
    story.append(P("☐ &nbsp; I2. Footer has two distinct labels pointing to the same URL",
                   item_h))
    story.append(detail_table([
        ("Where to find it", "Footer (visible on every page) &mdash; &lsquo;Coaching "
                             "Disclaimer&rsquo; and &lsquo;Professional Services "
                             "Disclaimer&rsquo; stacked on top of each other"),
        ("Issue", 'Both links go to <font name="Courier">/coaching-disclaimer</font>. '
                  "Two different labels, one destination."),
        ("Action", "Either (a) create a real /professional-services-disclaimer page "
                   "with separate content, or (b) remove the duplicate footer link."),
        ("Done when", "Each visible footer link goes to its own unique page."),
    ], header_color=AMBER))

    # I3
    story.append(P("☐ &nbsp; I3. &lsquo;Login Account&rsquo; nav item is a dead link", item_h))
    story.append(detail_table([
        ("Where to find it", "Site nav (visible on every page)"),
        ("Issue", 'Nav item &lsquo;Login Account&rsquo; has <font name="Courier">'
                  'href="#"</font> &mdash; clicking it does nothing'),
        ("Action", "Either (a) wire it to the Squarespace member-area login URL if "
                   "member accounts are intended, or (b) remove the nav item entirely."),
        ("Done when", "Clicking &lsquo;Login Account&rsquo; either logs the user in "
                      "or the item is gone."),
    ], header_color=AMBER))

    # I4
    story.append(P("☐ &nbsp; I4. &lsquo;Take the Free Assessment&rsquo; label is split "
                   "across two destinations site-wide", item_h))
    story.append(detail_table([
        ("Where to find it", "Every page that uses this anchor text"),
        ("Issue", "Sometimes &lsquo;Take the Free Assessment&rsquo; goes to "
                  "groundid.net (correct), sometimes to Delphi (wrong &mdash; see C3)"),
        ("Action", "Standardize anchor text &rarr; destination mapping site-wide:<br/>"
                   "&bull; &lsquo;Take the Free Assessment&rsquo; = always &rarr; "
                   "groundid.net<br/>"
                   "&bull; &lsquo;Try the Virtual Mind&rsquo; = always &rarr; "
                   "delphi.ai/drcara/chat<br/>"
                   "Audit every page and unify."),
        ("Done when", "Each label points to exactly one destination across the entire site."),
    ], header_color=AMBER))

    # I5
    story.append(P("☐ &nbsp; I5. &lsquo;Take the Assessment | Contact Dr. Cara&rsquo; link "
                   "is half-dead on /work-together", item_h))
    story.append(detail_table([
        ("Where to find it", "Squarespace &rarr; Pages &rarr; /work-together"),
        ("Element", "A single link reading &lsquo;Take the Assessment | "
                    "Contact Dr. Cara&rsquo;"),
        ("Issue", "The whole label is one link going only to /contact. The &lsquo;Take "
                  "the Assessment&rsquo; half of the label points nowhere &mdash; it&rsquo;s "
                  "just text."),
        ("Action", "Split into two separate links: &lsquo;Take the Assessment&rsquo; "
                   "&rarr; https://groundid.net, &lsquo;Contact Dr. Cara&rsquo; "
                   "&rarr; /contact. Or drop the unused half."),
        ("Done when", "Each labeled action is clickable and goes to its own destination."),
    ], header_color=AMBER))

    # I6
    story.append(P("☐ &nbsp; I6. Checkout cart CTAs need manual verification", item_h))
    story.append(detail_table([
        ("Where to find it", "Homepage and /work-together &mdash; three CTAs: "
                             "&lsquo;Start Free &rarr;&rsquo;, &lsquo;Claim a Founding "
                             "Seat &rarr;&rsquo;, &lsquo;Apply Now &rarr;&rsquo;"),
        ("Issue", "All three URLs return HTTP 200, but Squarespace renders cart contents "
                  "in the browser. Audit could not verify the right product loads at the "
                  "right price. Cart tokens silently invalidate when products are edited "
                  "or deleted."),
        ("Action", "Click each CTA in an incognito window. Confirm: (a) the cart opens, "
                   "(b) the right product is in it, (c) the price is correct. Pay special "
                   "attention to &lsquo;Claim a Founding Seat&rsquo; &mdash; limited-time "
                   "pricing is most likely to drift."),
        ("Done when", "All three carts open with the correct product and price."),
    ], header_color=AMBER))

    story.append(PageBreak())

    # ===== HOUSEKEEPING =====
    story.append(rule(GREEN, 2))
    story.append(P("HOUSEKEEPING &mdash; Nice to Clean Up", section_h_green))
    story.append(P("Not bugs. Worth knowing about, and quietly fixing if there&rsquo;s "
                   "time.", note))

    # H1
    story.append(P("☐ &nbsp; H1. Add a redirect for /drcarahome (no &lsquo;-1&rsquo;)", item_h))
    story.append(P("The homepage&rsquo;s canonical URL is /drcarahome-1. Someone typing "
                   "/drcarahome (without the -1) gets a 404. No active link points "
                   "there today, but it&rsquo;s a typo trap. Add a Squarespace URL "
                   "redirect: <font name=\"Courier\">/drcarahome &rarr; /</font>.", body))

    # H2
    story.append(P("&#10003; &nbsp; H2. Mailto address uses double-a (drcaraa.com) "
                   "&mdash; verified working", item_h))
    story.append(P("The &lsquo;Email to Discuss&rsquo; CTA on /contact and the RPR Coffee "
                   "waitlist CTA both use <font name=\"Courier\">drcara@drcaraa.com</font>. "
                   "The double-a is <b>intentional</b> (matches Instagram dr.caraa, "
                   "LinkedIn drcaraa) and verified working via Google Workspace MX records. "
                   "<b>No action</b> &mdash; just document so a future editor doesn&rsquo;t "
                   "&lsquo;correct&rsquo; it to a single-a address that doesn&rsquo;t exist.", body))

    # H3
    story.append(P("&#10003; &nbsp; H3. The typo domain grounid.com is a working mirror "
                   "&mdash; keep it renewed", item_h))
    story.append(P("grounid.com (single-d) is a byte-for-byte mirror of groundid.net on "
                   "Vercel. It catches real typo traffic. <b>No action</b> needed, but "
                   "make sure this domain stays renewed at the registrar &mdash; losing "
                   "it would drop the typo safety net.", body))

    # H4
    story.append(P("&#10003; &nbsp; H4. LinkedIn footer link blocks audit probes "
                   "(not actually broken)", item_h))
    story.append(P("The LinkedIn icon in the footer returns HTTP 405 to automated checks. "
                   "This is LinkedIn rate-limiting, not a broken link &mdash; the profile "
                   "loads in a browser. <b>No action</b> needed.", body))

    # H5
    story.append(P("☐ &nbsp; H5. Quiz-result archetype pages need a per-profile spot-check",
                   item_h))
    story.append(P("The Leadership Origin Profile quiz on groundid.net routes the user to "
                   "a profile-specific landing page (Architect / Carrier / Performer / "
                   "Sentinel) after they submit. The link is generated in JavaScript at "
                   "runtime, so it can&rsquo;t be checked from outside the live quiz. "
                   "Recommend taking the quiz four times (or temporarily forcing each "
                   "result in dev tools) to confirm all four archetype landing pages "
                   "load correctly.", body))

    # H6
    story.append(P("&#10003; &nbsp; H6. The /cart page is reachable but not in the main nav",
                   item_h))
    story.append(P("/cart is reachable via the cart icon in the header. It&rsquo;s not "
                   "orphaned &mdash; just worth noting that it doesn&rsquo;t show up in "
                   "the main nav, which is correct Squarespace behavior. <b>No action</b>.", body))

    story.append(PageBreak())

    # ===== COULD NOT VERIFY =====
    story.append(rule(MUTED, 1))
    story.append(P("What We Could Not Verify Automatically", section_h))
    story.append(P("Three items needed a real browser session and weren&rsquo;t testable "
                   "from outside. A human pass on these closes out the audit.", note))
    for txt in [
        "<b>1. Cart contents and prices</b> behind the three checkout CTAs "
        "(Squarespace renders these client-side).",
        "<b>2. Each archetype&rsquo;s landing page</b> at the end of the GroundID "
        "quiz (JavaScript-routed).",
        "<b>3. The &lsquo;Login Account&rsquo; intent</b> &mdash; whether it should be "
        "wired up or removed (a UX call, not a link-health call).",
    ]:
        story.append(P(txt, body))

    story.append(Spacer(1, 14))

    # ===== URL MAP =====
    story.append(rule(ORANGE, 1.5))
    story.append(P("Quick Reference &mdash; Anchor Text to URL Map", section_h))
    story.append(P("When in doubt during any fix, cross-check the destination against "
                   "this table.", note))
    story.append(url_map_table([
        ("Take the Free Assessment", "https://groundid.net"),
        ("Try the Virtual Mind / Talk to the Virtual Mind", "https://www.delphi.ai/drcara/chat"),
        ("Lead Free Now", "/lead-free-now"),
        ("Work Together / Explore Ways to Work Together", "/work-together"),
        ("Contact Dr. Cara / Contact", "/contact"),
        ("The Framework", "/framework"),
        ("About", "/about"),
        ("Coffee / RPR Coffee", "https://groundid.net/coffee"),
    ]))

    story.append(Spacer(1, 14))

    # ===== SIGN-OFF =====
    story.append(rule(ORANGE, 1.5))
    story.append(P("Sign-off", section_h))
    story.append(P("When all Critical and Important items are done, please reply to "
                   "Dr. Cara with:", body))
    for txt in [
        "&bull; &nbsp; A list of the items completed (by ID &mdash; C1, C2, etc.)",
        "&bull; &nbsp; Any items you couldn&rsquo;t complete and why",
        "&bull; &nbsp; Date and time the changes went live",
    ]:
        story.append(P(txt, body))
    story.append(Spacer(1, 6))
    story.append(P("A re-audit will be run shortly after to confirm.", note))

    doc.build(story)


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "DR-CARA-Website-Link-Audit.pdf")
    build(out)
    print(f"Wrote {out}")
