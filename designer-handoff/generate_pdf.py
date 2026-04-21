#!/usr/bin/env python3
"""Generate the DR. CARA Designer Handoff PDF using ReportLab."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable
import os

# ── Colors ──
ORANGE = HexColor('#E8600A')
ORANGE_DARK = HexColor('#C44D00')
ORANGE_LIGHT = HexColor('#FFF0E5')
GOLD = HexColor('#C9A850')
DARK = HexColor('#2A2320')
BODY_TEXT = HexColor('#4A3F38')
MUTED = HexColor('#A09080')
CREAM = HexColor('#FFFAF5')
BORDER = HexColor('#E8E0D8')
GREEN = HexColor('#2E7D4F')
GREEN_LIGHT = HexColor('#E8F5EC')
WHITE = white

# ── Color Swatch Flowable ──
class ColorSwatch(Flowable):
    def __init__(self, color, size=12):
        Flowable.__init__(self)
        self.color = HexColor(color) if isinstance(color, str) else color
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.setStrokeColor(HexColor('#E8E0D8'))
        self.canv.setLineWidth(0.5)
        self.canv.roundRect(0, 0, self.size, self.size, 2, fill=1, stroke=1)

# ── Callout Box ──
class CalloutBox(Flowable):
    def __init__(self, text, border_color=ORANGE, bg_color=ORANGE_LIGHT, width=None):
        Flowable.__init__(self)
        self.text = text
        self.border_color = border_color
        self.bg_color = bg_color
        self._width = width or 6.5 * inch
        self.style = ParagraphStyle(
            'CalloutText', fontName='Helvetica', fontSize=9.5,
            leading=14, textColor=BODY_TEXT
        )
        self.para = Paragraph(text, self.style)
        w, h = self.para.wrap(self._width - 40, 1000)
        self.height = h + 24

    def wrap(self, availWidth, availHeight):
        self._width = min(self._width, availWidth)
        w, h = self.para.wrap(self._width - 40, 1000)
        self.height = h + 24
        return self._width, self.height

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.rect(0, 0, self._width, self.height, fill=1, stroke=0)
        self.canv.setFillColor(self.border_color)
        self.canv.rect(0, 0, 4, self.height, fill=1, stroke=0)
        self.para.drawOn(self.canv, 20, 12)

# ── Checkbox Item ──
class CheckboxItem(Flowable):
    def __init__(self, text, width=6.5*inch):
        Flowable.__init__(self)
        self.text = text
        self._width = width
        self.style = ParagraphStyle(
            'CheckItem', fontName='Helvetica', fontSize=9.5,
            leading=14, textColor=BODY_TEXT
        )
        self.para = Paragraph(text, self.style)
        w, h = self.para.wrap(width - 30, 1000)
        self.height = max(h + 8, 20)

    def wrap(self, availWidth, availHeight):
        self._width = min(self._width, availWidth)
        w, h = self.para.wrap(self._width - 30, 1000)
        self.height = max(h + 8, 20)
        return self._width, self.height

    def draw(self):
        # Draw checkbox
        self.canv.setStrokeColor(ORANGE)
        self.canv.setLineWidth(1)
        self.canv.rect(2, self.height - 14, 10, 10, fill=0, stroke=1)
        # Draw bottom border
        self.canv.setStrokeColor(BORDER)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, 0, self._width, 0)
        # Draw text
        self.para.drawOn(self.canv, 22, 4)


def build_pdf():
    output_path = os.path.join(os.path.dirname(__file__), 'DR-CARA-Post-Purchase-Designer-Handoff.pdf')

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch,
        title='DR. CARA | Post-Purchase Experience — Designer Handoff',
        author='Dr. Cara Alexander'
    )

    styles = getSampleStyleSheet()
    W = doc.width

    # ── Custom Styles ──
    title_style = ParagraphStyle('DocTitle', fontName='Times-Bold', fontSize=24, textColor=DARK, alignment=TA_CENTER, leading=30)
    subtitle_style = ParagraphStyle('DocSubtitle', fontName='Helvetica', fontSize=14, textColor=MUTED, alignment=TA_CENTER, leading=20)
    meta_style = ParagraphStyle('DocMeta', fontName='Helvetica', fontSize=10, textColor=MUTED, alignment=TA_CENTER, leading=15)
    h1_style = ParagraphStyle('H1', fontName='Times-Bold', fontSize=20, textColor=DARK, leading=26, spaceBefore=24, spaceAfter=8)
    h2_style = ParagraphStyle('H2', fontName='Times-Bold', fontSize=16, textColor=DARK, leading=22, spaceBefore=20, spaceAfter=6)
    h3_style = ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=12, textColor=ORANGE, leading=16, spaceBefore=14, spaceAfter=4)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9.5, textColor=BODY_TEXT, leading=14, spaceBefore=4, spaceAfter=4)
    bold_body = ParagraphStyle('BoldBody', fontName='Helvetica-Bold', fontSize=9.5, textColor=DARK, leading=14, spaceBefore=4, spaceAfter=4)
    bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9.5, textColor=BODY_TEXT, leading=14, leftIndent=16, bulletIndent=4, spaceBefore=2, spaceAfter=2)
    code_style = ParagraphStyle('Code', fontName='Courier', fontSize=8.5, textColor=HexColor('#C44D00'), leading=12, backColor=ORANGE_LIGHT, leftIndent=4, rightIndent=4)
    pre_style = ParagraphStyle('Pre', fontName='Courier', fontSize=8, textColor=HexColor('#FFE8D4'), leading=11, backColor=DARK, leftIndent=12, rightIndent=12, spaceBefore=8, spaceAfter=8)
    footer_style = ParagraphStyle('Footer', fontName='Helvetica', fontSize=9, textColor=MUTED, alignment=TA_CENTER, leading=13)

    story = []

    def add_orange_rule():
        story.append(HRFlowable(width='100%', thickness=2.5, color=ORANGE, spaceBefore=4, spaceAfter=4))

    def add_gold_rule():
        story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceBefore=16, spaceAfter=16))

    def add_subtle_rule():
        story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceBefore=8, spaceAfter=8))

    def make_table(headers, rows, col_widths=None):
        data = [headers] + rows
        if col_widths is None:
            col_widths = [W / len(headers)] * len(headers)
        t = Table(data, colWidths=col_widths, repeatRows=1)
        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), DARK),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TEXTCOLOR', (0, 1), (-1, -1), BODY_TEXT),
            ('LEADING', (0, 0), (-1, -1), 13),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        # Alternate row backgrounds
        for i in range(1, len(data)):
            if i % 2 == 0:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), CREAM))
        t.setStyle(TableStyle(style_cmds))
        return t

    def make_kv_table(pairs, col_widths=None):
        """Key-value table without header row."""
        data = pairs
        if col_widths is None:
            col_widths = [1.2*inch, W - 1.2*inch]
        t = Table(data, colWidths=col_widths)
        style_cmds = [
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), DARK),
            ('TEXTCOLOR', (1, 0), (1, -1), BODY_TEXT),
            ('LEADING', (0, 0), (-1, -1), 13),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        t.setStyle(TableStyle(style_cmds))
        return t

    # ═══════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph('DR. CARA | Post-Purchase Experience', title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Website Designer Handoff Document', subtitle_style))
    story.append(Spacer(1, 16))
    add_orange_rule()
    story.append(Spacer(1, 20))
    story.append(Paragraph('Prepared for: Website Designer', meta_style))
    story.append(Paragraph('Prepared by: Dr. Cara Alexander', meta_style))
    story.append(Paragraph('Date: April 2026', meta_style))
    story.append(Paragraph('Project: Post-Purchase Client Experience \u2014 Squarespace Build', meta_style))
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph('<b>DR. CARA</b> \u00b7 Connected Leadership \u00b7 drcara.net', footer_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PART 1: HIGH-LEVEL OVERVIEW
    # ═══════════════════════════════════════════════
    story.append(Paragraph('PART 1: HIGH-LEVEL OVERVIEW', h1_style))
    add_orange_rule()
    story.append(Spacer(1, 12))

    # Section 1
    story.append(Paragraph('1. Project Summary', h2_style))
    add_gold_rule()
    story.append(Paragraph(
        'We need to build the post-purchase client experience on our existing Squarespace Business site '
        '(<b>drcara.net</b>). When a client purchases one of our two products, they are redirected to a '
        'confirmation page (hosted on Vercel) and receive an automated email sequence (handled by Google '
        'Apps Script). Their ongoing content access \u2014 session recordings, course materials, and premium '
        'resources \u2014 lives on Squarespace.', body_style))
    story.append(Spacer(1, 8))
    story.append(CalloutBox('<b>Your job is to build the Squarespace pages. Everything else is already built or automated.</b>'))
    story.append(Spacer(1, 12))

    # Section 2
    story.append(Paragraph('2. Scope of Work', h2_style))
    add_gold_rule()
    story.append(Paragraph('YOU ARE BUILDING (Squarespace):', h3_style))
    for item in ['Replay Vault course page (session recordings)', 'GroundID Leader course page (12-week cohort content)', 'Member Area (premium gated content)', 'Prompt Guide page (downloadable PDFs)']:
        story.append(Paragraph(f'\u2022  {item}', bullet_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph('ALREADY BUILT (Do NOT touch):', h3_style))
    for item in ['Landing pages and quiz (Vercel \u2014 separate hosting)', 'Confirmation pages after purchase (Vercel)', 'Payment processing (Stripe)', 'Automated email sequences (Google Apps Script)', 'Virtual Mind AI platform (Delphi.ai \u2014 external tool)']:
        story.append(Paragraph(f'\u2022  {item}', bullet_style))
    story.append(Spacer(1, 12))

    # Section 3
    story.append(Paragraph('3. System Architecture', h2_style))
    add_gold_rule()
    arch_text = """CLIENT JOURNEY:

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
    +---> Google Sheet CRM (automatic)
    |
    +---> Welcome Email (Gmail - automatic)
    |
    +---> Squarespace Access  <-- WHAT YOU ARE BUILDING
            |
            +---> /replay-vault        [Squarespace Course]
            +---> /groundid-leader     [Squarespace Course]
            +---> /member-area         [Squarespace Member Site]
            +---> /prompt-guide        [Squarespace Page]"""
    for line in arch_text.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_style))
    story.append(Spacer(1, 12))

    # Section 4
    story.append(Paragraph('4. What to Build \u2014 Summary', h2_style))
    add_gold_rule()
    story.append(make_table(
        ['#', 'Page', 'URL Slug', 'Squarespace Type', 'Access Level'],
        [
            ['1', 'Replay Vault', '/replay-vault', 'Course', 'All paying members'],
            ['2', 'GroundID Leader', '/groundid-leader', 'Course', 'GroundID enrollees only'],
            ['3', 'Member Area', '/member-area', 'Member Site', 'All paying members'],
            ['4', 'Prompt Guide', '/prompt-guide', 'Member Page', 'All paying members'],
        ],
        [0.3*inch, 1.2*inch, 1.3*inch, 1.2*inch, W-4*inch]
    ))
    story.append(Spacer(1, 12))

    # Section 5 - Brand Reference
    story.append(Paragraph('5. Brand Reference', h2_style))
    add_gold_rule()

    story.append(Paragraph('Primary Brand Colors', h3_style))
    story.append(make_table(
        ['Color', 'Hex', 'Usage'],
        [
            ['Primary Orange', '#E8600A', 'CTAs, buttons, highlights, accent borders'],
            ['Orange Dark', '#C44D00', 'Button hover states'],
            ['Orange Light', '#FFF0E5', 'Callout backgrounds'],
            ['Gold', '#C9A850', 'Footer borders, premium accent'],
        ],
        [1.5*inch, 1*inch, W-2.5*inch]
    ))

    story.append(Paragraph('Profile-Specific Accent Colors', h3_style))
    story.append(make_table(
        ['Profile', 'Hex', 'Character'],
        [
            ['The Architect', '#c84200', 'Deep burnt orange'],
            ['The Carrier', '#c89000', 'Golden amber'],
            ['The Performer', '#d81360', 'Deep magenta'],
            ['The Sentinel', '#df4f0f', 'Orange-red'],
        ],
        [1.5*inch, 1*inch, W-2.5*inch]
    ))

    story.append(Paragraph('Text &amp; Background Colors', h3_style))
    story.append(make_table(
        ['Color', 'Hex', 'Usage'],
        [
            ['Dark', '#2A2320', 'Primary headings'],
            ['Body Text', '#4A3F38', 'Paragraph text'],
            ['Muted', '#A09080', 'Captions, footer text'],
            ['Cream', '#FFFAF5', 'Content boxes, summaries'],
            ['Border', '#E8E0D8', 'Dividers, box borders'],
            ['Green', '#2E7D4F', 'Confirmation states, guarantees'],
        ],
        [1.5*inch, 1*inch, W-2.5*inch]
    ))

    story.append(Paragraph('Fonts', h3_style))
    story.append(make_table(
        ['Type', 'Font', 'Fallback'],
        [
            ['Headlines', 'EB Garamond (400, 500, 600, 700)', 'Georgia, Times New Roman'],
            ['Body', 'System stack', '-apple-system, Segoe UI, Arial'],
        ],
        [1*inch, 2.5*inch, W-3.5*inch]
    ))

    story.append(Paragraph('Tone &amp; Voice', h3_style))
    for item in [
        'Clinical but warm. Direct but not cold.',
        'Speaks to leaders as equals, not students.',
        'Uses "you" and "the work" frequently.',
        'Avoids hype, urgency, or exclamation points.',
        'Framework language: RPR (Receive-Perceive-Respond), Leadership Origin Profile, GroundID, Virtual Mind.',
    ]:
        story.append(Paragraph(f'\u2022  {item}', bullet_style))
    story.append(Spacer(1, 12))

    # Section 6 - Products
    story.append(Paragraph('6. Two Products \u2014 What Each Client Gets', h2_style))
    add_gold_rule()

    story.append(Paragraph('Product 1: Virtual Mind ($49/month)', h3_style))
    story.append(make_kv_table([
        ['Price', '$49/month, cancel anytime'],
        ['Access', '24/7 unlimited AI coaching conversations'],
        ['Platform', 'Delphi.ai (external \u2014 not on Squarespace)'],
        ['Squarespace', 'Replay Vault + Member Area + Prompt Guide'],
        ['Live', 'Weekly GroundID Live sessions (Zoom)'],
    ]))

    story.append(Paragraph('Product 2: GroundID Leader ($9,000)', h3_style))
    story.append(make_kv_table([
        ['Price', '$9,000 total ($3,000/month x 3)'],
        ['Format', '12 live 90-minute sessions with Dr. Cara'],
        ['Structure', '20 min teaching + 30 min dialogue + 40 min RPR coaching'],
        ['Cohort', 'Maximum 10 leaders, quarterly enrollment'],
        ['Squarespace', 'GroundID Leader course + Replay Vault + Member Area + Prompt Guide'],
        ['Physical', 'RPR Practice Deck shipped before Week 1'],
        ['Bonus', '30-day Virtual Mind pre-access'],
        ['Post-program', '90-day community access'],
        ['Guarantee', '2 sessions, full Month 1 refund'],
    ]))

    # ═══════════════════════════════════════════════
    # PART 2: DETAILED BUILD SPECS
    # ═══════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph('PART 2: DETAILED BUILD SPECS', h1_style))
    add_orange_rule()
    story.append(Spacer(1, 12))

    # Appendix A
    story.append(Paragraph('Appendix A: Replay Vault \u2014 Squarespace Course', h2_style))
    add_gold_rule()
    story.append(make_kv_table([
        ['URL', 'drcara.net/replay-vault'],
        ['Type', 'Squarespace Course'],
        ['Access', 'Members only (all paying members)'],
        ['Purpose', 'Houses recorded GroundID Live sessions for on-demand viewing'],
    ]))

    story.append(Paragraph('Course Structure', h3_style))
    vault_struct = """REPLAY VAULT
  |
  +-- Section: [Month Year] (e.g., "April 2026")
  |     +-- Lesson: "GroundID Live - [Date] - [Topic]"
  |     +-- Lesson: "GroundID Live - [Date] - [Topic]"
  |
  +-- Section: [Month Year] (e.g., "March 2026")
  |     +-- Lesson: "GroundID Live - [Date] - [Topic]"
  |     +-- ..."""
    for line in vault_struct.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_style))

    story.append(Paragraph('Content Per Lesson', h3_style))
    for item in ['<b>Video:</b> Zoom recording (uploaded weekly after each session)', '<b>Description:</b> 2-3 sentences about what was covered', 'No quizzes, no completion tracking needed']:
        story.append(Paragraph(f'\u2022  {item}', bullet_style))

    story.append(Paragraph('Weekly Upload Workflow', h3_style))
    for i, item in enumerate(['Dr. Cara records GroundID Live on Zoom (weekly)', 'Downloads recording from Zoom', 'Uploads to Squarespace as a new lesson under the current month', 'Members see it immediately'], 1):
        story.append(Paragraph(f'{i}.  {item}', bullet_style))

    story.append(Spacer(1, 6))
    story.append(CalloutBox('<b>Design note:</b> Clean, minimal layout. Organized reverse-chronologically (newest first). Each section = one month. This is a library, not a course to complete \u2014 no progress tracking needed.'))
    story.append(Spacer(1, 12))

    # Appendix B
    story.append(Paragraph('Appendix B: GroundID Leader \u2014 Squarespace Course', h2_style))
    add_gold_rule()
    story.append(make_kv_table([
        ['URL', 'drcara.net/groundid-leader'],
        ['Type', 'Squarespace Course'],
        ['Access', 'GroundID Leader enrollees only'],
        ['Purpose', 'Central hub for the 12-week cohort experience'],
    ]))

    story.append(Paragraph('Course Structure', h3_style))
    gid_struct = """GROUNDID LEADER
  |
  +-- Module 1: PRE-WORK (Available immediately)
  |     +-- "Welcome to GroundID Leader" (text + video)
  |     +-- "Leadership Identity Brief" (link to intake form)
  |     +-- "Shipping Address" (form for RPR Practice Deck)
  |     +-- "Your Virtual Mind Pre-Access" (link)
  |     +-- "Session Schedule & Zoom Links"
  |
  +-- Module 2: SESSIONS (Added weekly)
  |     +-- "Session 1 - [Topic]" (recording + notes)
  |     +-- ... through Session 12
  |
  +-- Module 3: RESOURCES
        +-- "RPR Practice Deck - Digital Companion" (PDF)
        +-- "Your Leadership Origin Profile" (link)
        +-- "Premium Prompt Guide" (PDF)
        +-- "Post-Program Community" (90-day info)"""
    for line in gid_struct.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_style))

    story.append(Spacer(1, 6))
    story.append(CalloutBox(
        '<b>Design notes:</b><br/>'
        '\u2022  Module 1 (Pre-Work) should feel urgent/action-oriented<br/>'
        '\u2022  Module 2 (Sessions) starts empty and fills over 12 weeks<br/>'
        '\u2022  Module 3 (Resources) is the evergreen reference library<br/>'
        '\u2022  Overall feel: premium, cohort-specific, exclusive'
    ))
    story.append(Spacer(1, 12))

    # Appendix C
    story.append(Paragraph('Appendix C: Member Area \u2014 Squarespace Member Site', h2_style))
    add_gold_rule()
    story.append(make_kv_table([
        ['URL', 'drcara.net/member-area'],
        ['Type', 'Squarespace Member Site'],
        ['Access', 'All paying members'],
        ['Purpose', 'Premium content hub with downloadable resources'],
    ]))

    story.append(Paragraph('Pages to Create', h3_style))
    member_struct = """MEMBER AREA
  |
  +-- Page: "Premium Prompt Guides"
  |     +-- The Architect Prompt Guide (PDF)
  |     +-- The Carrier Prompt Guide (PDF)
  |     +-- The Performer Prompt Guide (PDF)
  |     +-- The Sentinel Prompt Guide (PDF)
  |
  +-- Page: "Resources"
  |     +-- RPR Framework Overview (PDF)
  |     +-- Leadership Origin Profile Guide (link)
  |     +-- Virtual Mind Quick Start (text + link)
  |
  +-- Page: "Member Insights" (Optional)
        +-- Member-only articles from Dr. Cara"""
    for line in member_struct.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_style))

    story.append(Spacer(1, 6))
    story.append(CalloutBox('<b>Design notes:</b> Clean, library-style layout. PDFs easy to find and download. Each Prompt Guide visually distinguished using profile accent colors. Feels exclusive but not complicated.'))
    story.append(Spacer(1, 12))

    # Appendix D
    story.append(Paragraph('Appendix D: Post-Purchase Email Flow (Context Only)', h2_style))
    add_gold_rule()
    story.append(CalloutBox(
        '<b>The designer does NOT build this.</b> It is automated via Google Apps Script + Gmail. '
        'But you need to understand what clients receive so the Squarespace experience is consistent with the emails.',
        border_color=GREEN, bg_color=GREEN_LIGHT
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph('Virtual Mind Email Sequence', h3_style))
    story.append(make_table(
        ['Day', 'Subject', 'Links to Squarespace'],
        [
            ['0', '"Welcome to Virtual Mind \u2014 Your access is live"', 'drcara.net/replay-vault, drcara.net/prompt-guide'],
            ['3', '"Three prompts for The [Profile]"', '\u2014'],
            ['7', '"This week\'s GroundID Live is yours"', 'drcara.net/replay-vault'],
        ],
        [0.5*inch, 2.8*inch, W-3.3*inch]
    ))

    story.append(Paragraph('GroundID Leader Email Sequence', h3_style))
    story.append(make_table(
        ['Day', 'Subject', 'Links to Squarespace'],
        [
            ['0', '"Welcome to GroundID Leader \u2014 You are in"', 'drcara.net/groundid-leader'],
            ['2', '"Your Leadership Identity Brief \u2014 complete before we begin"', 'drcara.net/groundid-leader'],
            ['5', '"Your Virtual Mind pre-access \u2014 use it before Session 1"', '\u2014'],
        ],
        [0.5*inch, 2.8*inch, W-3.3*inch]
    ))

    story.append(Spacer(1, 6))
    story.append(CalloutBox('<b>Why this matters:</b> Clients arrive at your Squarespace pages via links in these emails within their first week. The landing experience must match the tone and visual quality of the emails. First impressions matter.'))
    story.append(Spacer(1, 12))

    # Appendix E
    story.append(PageBreak())
    story.append(Paragraph('Appendix E: Client Journey Maps', h2_style))
    add_gold_rule()

    story.append(Paragraph('Journey 1: Virtual Mind Subscriber', h3_style))
    vm_journey = """DAY 0: Purchase ($49/month)
  +---> Sees confirmation page (Vercel)
  +---> Receives welcome email with access links
  +---> Opens Virtual Mind (delphi.ai/drcara)
  +---> Visits Member Area for Prompt Guide

DAY 3: Follow-up email with profile-specific prompts
  +---> Returns to Virtual Mind

DAY 7: GroundID Live reminder
  +---> Attends GroundID Live (Zoom)
  +---> OR visits Replay Vault (drcara.net/replay-vault)

ONGOING (Weekly):
  +---> GroundID Live (Zoom)
  +---> Virtual Mind (delphi.ai/drcara)
  +---> Replay Vault (drcara.net/replay-vault)"""
    for line in vm_journey.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph('Journey 2: GroundID Leader Enrollee', h3_style))
    gid_journey = """DAY 0: Enrollment ($9,000)
  +---> Sees confirmation page (Vercel)
  +---> Receives welcome email with 5 action items
  +---> Logs into course portal (drcara.net/groundid-leader)

DAYS 1-2: Onboarding
  +---> Completes Leadership Identity Brief
  +---> Submits shipping address for RPR Deck
  +---> Opens Virtual Mind pre-access

DAY 5: Virtual Mind reminder email

PRE-WEEK 1:
  +---> RPR Practice Deck arrives (shipped)
  +---> All 12 sessions added to calendar

WEEKS 1-12: Active Program
  +---> Weekly 90-minute sessions (Zoom)
  +---> Session recordings posted to course portal
  +---> Virtual Mind available between sessions

POST-PROGRAM (90 days):
  +---> Community access continues
  +---> Replay Vault access continues"""
    for line in gid_journey.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_style))
    story.append(Spacer(1, 12))

    # Appendix F
    story.append(Paragraph('Appendix F: URL Structure &amp; Navigation', h2_style))
    add_gold_rule()

    story.append(Paragraph('Complete URL Map', h3_style))
    story.append(make_table(
        ['URL', 'Type', 'Purpose', 'Who Sees It'],
        [
            ['drcara.net', 'Main site', 'Homepage, about, services', 'Everyone'],
            ['drcara.net/replay-vault', 'Course', 'GroundID Live recordings', 'All paying members'],
            ['drcara.net/groundid-leader', 'Course', '12-week cohort content', 'GroundID enrollees only'],
            ['drcara.net/member-area', 'Member Site', 'Premium resources hub', 'All paying members'],
            ['drcara.net/prompt-guide', 'Member Page', 'Profile-specific PDFs', 'All paying members'],
        ],
        [1.7*inch, 0.9*inch, 1.7*inch, W-4.3*inch]
    ))

    story.append(Paragraph('External URLs (Not on Squarespace)', h3_style))
    story.append(make_table(
        ['URL', 'Platform', 'Purpose'],
        [
            ['delphi.ai/drcara', 'Delphi.ai', 'Virtual Mind AI coaching'],
            ['grounid.com', 'GrounID', 'Leadership Origin Profile sharing'],
            ['Landing pages + quiz', 'Vercel', 'Lead generation (separate hosting)'],
        ],
        [1.7*inch, 1.2*inch, W-2.9*inch]
    ))

    story.append(Paragraph('Navigation Recommendation', h3_style))
    story.append(Paragraph('Add to Squarespace main navigation <b>(logged-in members only)</b>:', body_style))
    for item in ['"Member Area" \u2192 /member-area', '"Replay Vault" \u2192 /replay-vault', '"Virtual Mind" \u2192 delphi.ai/drcara (external link)']:
        story.append(Paragraph(f'\u2022  {item}', bullet_style))
    story.append(Paragraph('GroundID Leader enrollees also see:', body_style))
    story.append(Paragraph('\u2022  "My Program" \u2192 /groundid-leader', bullet_style))

    # ═══════════════════════════════════════════════
    # DESIGNER CHECKLIST
    # ═══════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph('Designer Checklist', h1_style))
    add_orange_rule()
    story.append(Paragraph('Use this to track progress. Check off each item as completed:', body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph('Replay Vault', h3_style))
    for item in [
        'Set up Squarespace Course at /replay-vault',
        'Configure member-only access',
        'Create first month section with placeholder lessons',
        'Test video upload workflow',
    ]:
        story.append(CheckboxItem(item, W))

    story.append(Spacer(1, 8))
    story.append(Paragraph('GroundID Leader', h3_style))
    for item in [
        'Set up Squarespace Course at /groundid-leader',
        'Create Module 1: Pre-Work (5 lessons)',
        'Create Module 2: Sessions (empty, to be filled weekly)',
        'Create Module 3: Resources (4 lessons)',
        'Configure enrollee-only access',
    ]:
        story.append(CheckboxItem(item, W))

    story.append(Spacer(1, 8))
    story.append(Paragraph('Member Area', h3_style))
    for item in [
        'Set up Squarespace Member Site at /member-area',
        'Create Prompt Guides page with 4 PDF downloads',
        'Create Resources page',
        'Configure member-only access',
    ]:
        story.append(CheckboxItem(item, W))

    story.append(Spacer(1, 8))
    story.append(Paragraph('Integration &amp; Testing', h3_style))
    for item in [
        'Connect Stripe to Squarespace (Commerce \u2192 Payments)',
        'Test member login flow',
        'Test course access for both member tiers',
        'Add member navigation links (logged-in users only)',
        'Review mobile responsiveness for all new pages',
        'Brand check: colors, fonts, and tone match existing site',
    ]:
        story.append(CheckboxItem(item, W))

    # Footer
    story.append(Spacer(1, 24))
    add_gold_rule()
    story.append(Spacer(1, 12))
    story.append(Paragraph('<b>DR. CARA</b> \u00b7 Connected Leadership \u00b7 drcara.net', footer_style))
    story.append(Paragraph('Questions? Reply directly in this document or email Dr. Cara.', footer_style))

    # ── Build ──
    doc.build(story)
    print(f'PDF generated: {output_path}')
    return output_path


if __name__ == '__main__':
    build_pdf()
