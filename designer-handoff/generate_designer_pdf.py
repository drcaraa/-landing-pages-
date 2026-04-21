#!/usr/bin/env python3
"""DR. CARA — Focused Designer Handoff PDF: Post-Purchase Experience + Squarespace Build Specs."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
import os

# ── Colors ──
ORANGE = HexColor('#E8600A')
ORANGE_DARK = HexColor('#C44D00')
ORANGE_LIGHT = HexColor('#FFF0E5')
GOLD = HexColor('#C9A850')
DARK = HexColor('#2A2320')
BODY = HexColor('#4A3F38')
MUTED = HexColor('#A09080')
CREAM = HexColor('#FFFAF5')
BORDER = HexColor('#E8E0D8')
GREEN = HexColor('#2E7D4F')
GREEN_LT = HexColor('#E8F5EC')
WHITE = white

# ── Callout Box ──
class CalloutBox(Flowable):
    def __init__(self, text, border_color=ORANGE, bg_color=ORANGE_LIGHT, width=None, style=None):
        Flowable.__init__(self)
        self.text = text
        self.border_color = border_color
        self.bg_color = bg_color
        self._width = width or 6.5 * inch
        self.style = style or ParagraphStyle('CB', fontName='Helvetica', fontSize=9.5, leading=14, textColor=BODY)
        self.para = Paragraph(text, self.style)
        w, h = self.para.wrap(self._width - 40, 1000)
        self.height = h + 24
    def wrap(self, aW, aH):
        self._width = min(self._width, aW)
        w, h = self.para.wrap(self._width - 40, 1000)
        self.height = h + 24
        return self._width, self.height
    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.rect(0, 0, self._width, self.height, fill=1, stroke=0)
        self.canv.setFillColor(self.border_color)
        self.canv.rect(0, 0, 4, self.height, fill=1, stroke=0)
        self.para.drawOn(self.canv, 20, 12)

class CheckboxItem(Flowable):
    def __init__(self, text, width=6.5*inch):
        Flowable.__init__(self)
        self.text = text
        self._width = width
        self.style = ParagraphStyle('CI', fontName='Helvetica', fontSize=9.5, leading=14, textColor=BODY)
        self.para = Paragraph(text, self.style)
        w, h = self.para.wrap(width - 30, 1000)
        self.height = max(h + 8, 20)
    def wrap(self, aW, aH):
        self._width = min(self._width, aW)
        w, h = self.para.wrap(self._width - 30, 1000)
        self.height = max(h + 8, 20)
        return self._width, self.height
    def draw(self):
        self.canv.setStrokeColor(ORANGE)
        self.canv.setLineWidth(1)
        self.canv.rect(2, self.height - 14, 10, 10, fill=0, stroke=1)
        self.canv.setStrokeColor(BORDER)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, 0, self._width, 0)
        self.para.drawOn(self.canv, 22, 4)


def build_pdf():
    out = os.path.join(os.path.dirname(__file__), 'DR-CARA-Designer-Handoff-Post-Purchase.pdf')
    doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            title='DR. CARA | Post-Purchase Experience — Designer Handoff',
                            author='Dr. Cara Alexander')
    W = doc.width
    story = []

    # ── Styles ──
    title_s = ParagraphStyle('T', fontName='Times-Bold', fontSize=24, textColor=DARK, alignment=TA_CENTER, leading=30)
    sub_s = ParagraphStyle('Sub', fontName='Helvetica', fontSize=14, textColor=MUTED, alignment=TA_CENTER, leading=20)
    meta_s = ParagraphStyle('Meta', fontName='Helvetica', fontSize=10, textColor=MUTED, alignment=TA_CENTER, leading=15)
    h1 = ParagraphStyle('H1', fontName='Times-Bold', fontSize=20, textColor=DARK, leading=26, spaceBefore=20, spaceAfter=6)
    h2 = ParagraphStyle('H2', fontName='Times-Bold', fontSize=16, textColor=DARK, leading=22, spaceBefore=16, spaceAfter=4)
    h3 = ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=12, textColor=ORANGE, leading=16, spaceBefore=12, spaceAfter=4)
    h4 = ParagraphStyle('H4', fontName='Helvetica-Bold', fontSize=10.5, textColor=DARK, leading=14, spaceBefore=10, spaceAfter=3)
    body = ParagraphStyle('B', fontName='Helvetica', fontSize=9.5, textColor=BODY, leading=14, spaceBefore=3, spaceAfter=3)
    bullet = ParagraphStyle('Bul', fontName='Helvetica', fontSize=9.5, textColor=BODY, leading=14, leftIndent=16, bulletIndent=4, spaceBefore=2, spaceAfter=2)
    pre_s = ParagraphStyle('Pre', fontName='Courier', fontSize=8, textColor=HexColor('#FFE8D4'), leading=11, backColor=DARK, leftIndent=12, rightIndent=12, spaceBefore=6, spaceAfter=6)
    footer_s = ParagraphStyle('F', fontName='Helvetica', fontSize=9, textColor=MUTED, alignment=TA_CENTER, leading=13)
    small = ParagraphStyle('Sm', fontName='Helvetica', fontSize=8.5, textColor=MUTED, leading=12, spaceBefore=2)

    def orange_rule():
        story.append(HRFlowable(width='100%', thickness=2.5, color=ORANGE, spaceBefore=4, spaceAfter=4))
    def gold_rule():
        story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceBefore=12, spaceAfter=12))
    def subtle_rule():
        story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceBefore=6, spaceAfter=6))

    def tbl(headers, rows, widths=None):
        data = [headers] + rows
        if not widths: widths = [W / len(headers)] * len(headers)
        t = Table(data, colWidths=widths, repeatRows=1)
        cmds = [
            ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 9),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'), ('FONTSIZE', (0,1), (-1,-1), 9),
            ('TEXTCOLOR', (0,1), (-1,-1), BODY), ('LEADING', (0,0), (-1,-1), 13),
            ('BOTTOMPADDING', (0,0), (-1,0), 8), ('TOPPADDING', (0,0), (-1,0), 8),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6), ('TOPPADDING', (0,1), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,-2), 0.5, BORDER), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0: cmds.append(('BACKGROUND', (0,i), (-1,i), CREAM))
        t.setStyle(TableStyle(cmds))
        return t

    def kv_tbl(pairs, widths=None):
        if not widths: widths = [1.4*inch, W - 1.4*inch]
        t = Table(pairs, colWidths=widths)
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'), ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9), ('TEXTCOLOR', (0,0), (0,-1), DARK),
            ('TEXTCOLOR', (1,0), (1,-1), BODY), ('LEADING', (0,0), (-1,-1), 13),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5), ('TOPPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8), ('LINEBELOW', (0,0), (-1,-2), 0.5, BORDER),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        return t

    # ═══════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════
    story.append(Spacer(1, 1.8*inch))
    story.append(Paragraph('DR. CARA', title_s))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Post-Purchase Experience', sub_s))
    story.append(Paragraph('Designer Handoff', sub_s))
    story.append(Spacer(1, 16))
    orange_rule()
    story.append(Spacer(1, 20))
    story.append(Paragraph('Prepared for: Website Designer', meta_s))
    story.append(Paragraph('Prepared by: Dr. Cara Alexander', meta_s))
    story.append(Paragraph('Date: April 2026  \u2022  Cohort Start: June 3, 2026', meta_s))
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph('This document covers what happens after a client pays,', footer_s))
    story.append(Paragraph('what needs to be built in Squarespace, and how the integrations connect.', footer_s))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # SECTION 1: THE OFFER SUITE
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('1. The Offer Suite', h1))
    orange_rule()
    story.append(Paragraph('Three products, one framework. Each needs a distinct post-purchase experience.', body))
    story.append(Spacer(1, 8))

    story.append(tbl(
        ['Product', 'Price', 'Format', 'Cohort / Limit'],
        [
            ['GroundID Virtual Mind', 'Free to try, then $49/mo', 'AI coaching (Delphi.ai) + weekly live', 'Unlimited'],
            ['GroundID Leader 12-Week', '$3,000/mo ($9,000 total)\nPay in full: $8,500', '12 live 90-min sessions\n+ RPR Deck + Virtual Mind', '10 leaders max'],
            ['GroundID Leader Intensive', '$5,000/mo ($15,000 total)\nPay in full: $14,000', 'Everything in 12-Week\n+ 6 private 1:1 sessions', '8 leaders max'],
        ],
        [1.6*inch, 1.5*inch, 1.8*inch, W-4.9*inch]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph('<i>Private Coaching ($20K\u2013$50K) is handled separately \u2014 not part of this build.</i>', small))
    story.append(Spacer(1, 12))

    # What each product includes (Squarespace access)
    story.append(Paragraph('What Each Client Gets on Squarespace', h3))
    story.append(tbl(
        ['Squarespace Resource', 'Virtual Mind', '12-Week', 'Intensive'],
        [
            ['Replay Vault (/replay-vault)', '\u2713', '\u2713', '\u2713'],
            ['Member Area (/member-area)', '\u2713', '\u2713', '\u2713'],
            ['Prompt Guide (/prompt-guide)', '\u2713', '\u2713', '\u2713'],
            ['GroundID Leader Course (/groundid-leader)', '\u2014', '\u2713', '\u2713'],
            ['Intensive Resources', '\u2014', '\u2014', '\u2713'],
        ],
        [2.4*inch, 1*inch, 1*inch, 1*inch]
    ))
    story.append(Spacer(1, 4))
    story.append(CalloutBox('<b>Note:</b> The Virtual Mind subscription product already exists in Squarespace. The 12-Week and Intensive products + all member content pages still need to be built.'))

    # ═══════════════════════════════════════════════════
    # SECTION 2: POST-PURCHASE FLOWS
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph('2. Post-Purchase Experience Flows', h1))
    orange_rule()
    story.append(Paragraph('What happens the moment a client pays \u2014 and every touchpoint after.', body))
    story.append(Spacer(1, 8))

    # --- FLOW 1: Virtual Mind ---
    story.append(Paragraph('Flow 1: Virtual Mind ($49/month)', h2))
    gold_rule()

    vm_flow = [
        ['INSTANT', 'Stripe processes payment'],
        ['INSTANT', 'Client redirects to confirmation page (Vercel \u2014 already built)'],
        ['INSTANT', 'Stripe webhook \u2192 Google Sheet "VM Subscribers" tab (automatic)'],
        ['< 5 MIN', 'Welcome email sent via Gmail (automatic)\n\u2022 Virtual Mind access link (delphi.ai/drcara)\n\u2022 Replay Vault link (drcara.net/replay-vault)\n\u2022 Prompt Guide link (drcara.net/prompt-guide)\n\u2022 GroundID Live calendar invite'],
        ['DAY 3', 'Email: "Three prompts for The [Profile]"\n\u2022 3 profile-specific conversation starters'],
        ['DAY 7', 'Email: "This week\'s GroundID Live is yours"\n\u2022 Session details + Replay Vault link'],
        ['WEEKLY', 'Client attends GroundID Live (Zoom)\nRecording uploaded to Replay Vault (drcara.net/replay-vault)'],
    ]
    story.append(tbl(
        ['When', 'What Happens'],
        vm_flow,
        [1*inch, W - 1*inch]
    ))
    story.append(Spacer(1, 12))

    # --- FLOW 2: GroundID Leader 12-Week ---
    story.append(Paragraph('Flow 2: GroundID Leader 12-Week ($9,000)', h2))
    gold_rule()

    gid_flow = [
        ['INSTANT', 'Stripe processes payment'],
        ['INSTANT', 'Client redirects to confirmation page (Vercel \u2014 already built)'],
        ['INSTANT', 'Stripe webhook \u2192 Google Sheet "GroundID Cohort" tab (automatic)'],
        ['< 5 MIN', 'Welcome email sent via Gmail (automatic)\n\u2022 Course portal link (drcara.net/groundid-leader)\n\u2022 Leadership Identity Brief intake form\n\u2022 Shipping address form (RPR Practice Deck)\n\u2022 Virtual Mind pre-access link\n\u2022 Calendar invites for all 12 sessions'],
        ['DAY 2', 'Email: "Your Leadership Identity Brief \u2014 complete before we begin"\n\u2022 Links to course portal'],
        ['DAY 5', 'Email: "Your Virtual Mind pre-access \u2014 use it before Session 1"'],
        ['PRE-WEEK 1', 'RPR Practice Deck ships to client\nVirtual Mind pre-access active'],
        ['WEEKS 1\u201312', 'Weekly 90-min sessions (Zoom)\nRecordings posted to course portal after each session'],
        ['POST (90 days)', 'Community access continues\nReplay Vault access continues'],
    ]
    story.append(tbl(
        ['When', 'What Happens'],
        gid_flow,
        [1*inch, W - 1*inch]
    ))
    story.append(Spacer(1, 12))

    # --- FLOW 3: Intensive ---
    story.append(Paragraph('Flow 3: GroundID Leader Intensive ($15,000)', h2))
    gold_rule()
    story.append(Paragraph('Same flow as 12-Week above, plus:', body))
    story.append(Spacer(1, 4))
    story.append(tbl(
        ['When', 'What Happens (In Addition to 12-Week Flow)'],
        [
            ['DAY 0', 'Welcome email includes link to schedule 1:1 sessions\n\u2022 6 private 60-min sessions with Dr. Cara'],
            ['ONGOING', 'Voice note access to Dr. Cara between sessions\nPersonalized Leadership Identity Brief (deeper diagnostic)'],
            ['POST', 'Two-Session + Completion Guarantee applies'],
        ],
        [1*inch, W - 1*inch]
    ))

    # ═══════════════════════════════════════════════════
    # SECTION 3: INTEGRATIONS
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph('3. Integrations \u2014 How the Tools Connect', h1))
    orange_rule()
    story.append(Paragraph('All integrations use platforms we already have. No new paid tools.', body))
    story.append(Spacer(1, 8))

    # Architecture diagram
    arch = """PAYMENT (Stripe)
  |
  +---> Stripe Webhook
          |
          +---> Google Sheets (CRM database)
          |       \u2022 "VM Subscribers" tab
          |       \u2022 "GroundID Cohort" tab
          |       \u2022 "Scheduled Emails" tab
          |       \u2022 "Email Log" tab
          |
          +---> Gmail (automated email sequences)
          |       \u2022 Welcome emails (instant)
          |       \u2022 Follow-up emails (Day 2-7)
          |       \u2022 Sent via Google Apps Script
          |
          +---> Google Calendar
                  \u2022 Session invites for GroundID Live
                  \u2022 12-session schedule for Leader cohorts

CLIENT CONTENT ACCESS:
  Squarespace (drcara.net)    \u2190 WHAT YOU BUILD
    \u2022 /replay-vault
    \u2022 /groundid-leader
    \u2022 /member-area
    \u2022 /prompt-guide

  Delphi.ai (delphi.ai/drcara)  \u2190 ALREADY EXISTS
    \u2022 Virtual Mind AI coaching

  Zoom  \u2190 ALREADY EXISTS
    \u2022 Weekly GroundID Live sessions
    \u2022 12-week Leader sessions
    \u2022 1:1 Intensive sessions"""
    for line in arch.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_s))
    story.append(Spacer(1, 12))

    # Integration details
    story.append(Paragraph('Integration Details', h3))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Stripe \u2192 Google Sheets (Webhook)', h4))
    story.append(Paragraph('A Google Apps Script deployed as a web app receives Stripe payment events and writes client data to Google Sheets. This is already built \u2014 the script file is <font face="Courier" color="#C44D00">stripe-webhook.gs</font> in the project repo.', body))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Google Sheets (CRM Database)', h4))
    story.append(Paragraph('Google Sheets serves as the client database. Tabs:', body))
    for item in [
        '<b>Quiz Leads</b> \u2014 from the Leadership Origin quiz (Google Forms, already connected)',
        '<b>VM Subscribers</b> \u2014 auto-populated when Virtual Mind payment processes',
        '<b>GroundID Cohort</b> \u2014 auto-populated when Leader/Intensive payment processes',
        '<b>Scheduled Emails</b> \u2014 pending follow-up emails with send dates',
        '<b>Email Log</b> \u2014 record of all emails sent',
    ]:
        story.append(Paragraph(f'\u2022  {item}', bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Gmail (Automated Email Sequences)', h4))
    story.append(Paragraph('Google Apps Script sends personalized HTML emails from Dr. Cara\'s Gmail. Each email is profile-specific (Architect, Carrier, Performer, or Sentinel) and links to Squarespace member pages. A daily time-based trigger (9am) processes scheduled follow-up emails.', body))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Google Calendar', h4))
    story.append(Paragraph('Calendar invites are sent for GroundID Live (weekly, all members) and the 12-session Leader schedule (cohort-specific). Zoom links are embedded in the calendar events.', body))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Stripe \u2192 Squarespace', h4))
    story.append(Paragraph('Squarespace integrates natively with Stripe via Commerce \u2192 Payments. This connection handles member access gating \u2014 when a client pays, Squarespace can auto-grant access to the appropriate courses and member areas.', body))
    story.append(Spacer(1, 4))

    story.append(CalloutBox(
        '<b>What the designer needs to do:</b> Connect Stripe to Squarespace (Commerce \u2192 Payments) and configure access rules for each course and member area. Everything else is already automated.',
    ))

    # ═══════════════════════════════════════════════════
    # SECTION 4: WHAT TO BUILD IN SQUARESPACE
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph('4. What to Build in Squarespace', h1))
    orange_rule()
    story.append(Spacer(1, 4))

    story.append(CalloutBox(
        '<b>The Virtual Mind subscription product already exists in Squarespace.</b> The items below are what still needs to be created.',
    ))
    story.append(Spacer(1, 12))

    # --- 4A: Products ---
    story.append(Paragraph('4A. Products to Create', h2))
    gold_rule()

    story.append(tbl(
        ['Product', 'Price', 'Squarespace Type', 'Notes'],
        [
            ['GroundID Leader\n12-Week Experience', '$3,000/mo x 3\n($8,500 pay in full)', 'Subscription or\nOne-time product', 'Enrollment grants access to\n/groundid-leader course +\nall member content'],
            ['GroundID Leader\nIntensive', '$5,000/mo x 3\n($14,000 pay in full)', 'Subscription or\nOne-time product', 'Enrollment grants access to\n/groundid-leader course +\nIntensive resources +\nall member content'],
        ],
        [1.5*inch, 1.3*inch, 1.2*inch, W-4*inch]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph('<i>Virtual Mind ($49/mo) \u2014 already exists as a subscription product in Squarespace. No action needed.</i>', small))
    story.append(Spacer(1, 12))

    # --- 4B: Replay Vault ---
    story.append(Paragraph('4B. Replay Vault', h2))
    gold_rule()
    story.append(kv_tbl([
        ['URL', 'drcara.net/replay-vault'],
        ['Type', 'Squarespace Course'],
        ['Access', 'All paying members (VM + Leader + Intensive)'],
        ['Purpose', 'Library of recorded GroundID Live sessions'],
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Structure:', h4))
    struct = """REPLAY VAULT
  +-- Section: "June 2026"
  |     +-- Lesson: "GroundID Live - Jun 4 - [Topic]"
  |     +-- Lesson: "GroundID Live - Jun 11 - [Topic]"
  +-- Section: "May 2026"
  |     +-- Lesson: "GroundID Live - May 28 - [Topic]"
  +-- (newest month first)"""
    for line in struct.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_s))
    story.append(Spacer(1, 4))
    for item in ['Video per lesson (Zoom recording, uploaded weekly)', 'Brief description per lesson (2-3 sentences)', 'No quizzes or completion tracking \u2014 this is a library', 'Organized reverse-chronologically (newest first)']:
        story.append(Paragraph(f'\u2022  {item}', bullet))
    story.append(Spacer(1, 12))

    # --- 4C: GroundID Leader Course ---
    story.append(Paragraph('4C. GroundID Leader Course', h2))
    gold_rule()
    story.append(kv_tbl([
        ['URL', 'drcara.net/groundid-leader'],
        ['Type', 'Squarespace Course'],
        ['Access', 'Leader + Intensive enrollees only'],
        ['Purpose', 'Central hub for 12-week cohort experience'],
        ['Cohort Start', 'June 3, 2026  (12 sessions, Tuesdays 90 min)'],
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Structure:', h4))
    gid_s = """GROUNDID LEADER
  +-- Module 1: PRE-WORK (available immediately)
  |     +-- "Welcome to GroundID Leader" (video)
  |     +-- "Leadership Identity Brief" (intake form link)
  |     +-- "Shipping Address" (form for RPR Deck)
  |     +-- "Your Virtual Mind Pre-Access" (link)
  |     +-- "Session Schedule & Zoom Links"
  |
  +-- Module 2: SESSIONS (added weekly)
  |     +-- "Session 1 - [Topic]" (recording)
  |     +-- ... through Session 12
  |
  +-- Module 3: RESOURCES
        +-- "RPR Practice Deck" (digital PDF)
        +-- "Premium Prompt Guide" (PDF)
        +-- "Post-Program Community" (90-day info)"""
    for line in gid_s.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_s))
    story.append(Spacer(1, 4))
    story.append(CalloutBox(
        '<b>Design notes:</b><br/>'
        '\u2022  Module 1 (Pre-Work) feels urgent \u2014 action items to complete before Session 1<br/>'
        '\u2022  Module 2 (Sessions) starts empty, fills weekly with recordings<br/>'
        '\u2022  Module 3 (Resources) is the evergreen reference library<br/>'
        '\u2022  Intensive enrollees see everything here + additional resources below'
    ))
    story.append(Spacer(1, 12))

    # --- 4D: Member Area ---
    story.append(Paragraph('4D. Member Area', h2))
    gold_rule()
    story.append(kv_tbl([
        ['URL', 'drcara.net/member-area'],
        ['Type', 'Squarespace Member Site'],
        ['Access', 'All paying members'],
        ['Purpose', 'Premium content hub + downloadable resources'],
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Pages to create:', h4))
    mem_s = """MEMBER AREA
  +-- "Premium Prompt Guides"
  |     +-- Architect Prompt Guide (PDF)
  |     +-- Carrier Prompt Guide (PDF)
  |     +-- Performer Prompt Guide (PDF)
  |     +-- Sentinel Prompt Guide (PDF)
  |
  +-- "Resources"
  |     +-- RPR Framework Overview (PDF)
  |     +-- Virtual Mind Quick Start (link)
  |
  +-- "Member Insights" (optional, for future)
        +-- Member-only articles from Dr. Cara"""
    for line in mem_s.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;', pre_s))
    story.append(Spacer(1, 4))
    for item in ['Each Prompt Guide should use its profile accent color for visual distinction', 'Clean, library-style layout \u2014 feels exclusive but not complicated']:
        story.append(Paragraph(f'\u2022  {item}', bullet))
    story.append(Spacer(1, 12))

    # --- 4E: Navigation ---
    story.append(Paragraph('4E. Navigation Updates', h2))
    gold_rule()
    story.append(Paragraph('Add to Squarespace navigation <b>(logged-in members only)</b>:', body))
    story.append(Spacer(1, 4))
    story.append(tbl(
        ['Nav Item', 'URL', 'Visible To'],
        [
            ['"Member Area"', '/member-area', 'All paying members'],
            ['"Replay Vault"', '/replay-vault', 'All paying members'],
            ['"Virtual Mind"', 'delphi.ai/drcara (external)', 'All paying members'],
            ['"My Program"', '/groundid-leader', 'Leader + Intensive enrollees only'],
        ],
        [1.3*inch, 2.2*inch, W-3.5*inch]
    ))

    # ═══════════════════════════════════════════════════
    # SECTION 5: URL MAP
    # ═══════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph('5. Complete URL Map', h1))
    orange_rule()

    story.append(Paragraph('Squarespace (drcara.net) \u2014 What You Build', h3))
    story.append(tbl(
        ['URL', 'Type', 'Purpose'],
        [
            ['drcara.net/replay-vault', 'Course', 'GroundID Live session recordings'],
            ['drcara.net/groundid-leader', 'Course', '12-week cohort content'],
            ['drcara.net/member-area', 'Member Site', 'Premium content + PDF downloads'],
            ['drcara.net/prompt-guide', 'Member Page', 'Profile-specific prompt guides'],
        ],
        [2.2*inch, 1*inch, W-3.2*inch]
    ))

    story.append(Paragraph('External Platforms (Already Exist)', h3))
    story.append(tbl(
        ['URL / Platform', 'Purpose', 'Status'],
        [
            ['delphi.ai/drcara', 'Virtual Mind AI coaching', 'Live'],
            ['Stripe', 'Payment processing', 'Live'],
            ['Google Sheets', 'CRM + client database', 'Configured'],
            ['Gmail + Apps Script', 'Automated email sequences', 'Built'],
            ['Google Calendar', 'Session scheduling + invites', 'Live'],
            ['Zoom', 'Live sessions (weekly + cohort)', 'Live'],
            ['grounid.com', 'Leadership Origin Profile sharing', 'Live'],
        ],
        [1.7*inch, 2.2*inch, W-3.9*inch]
    ))

    # ═══════════════════════════════════════════════════
    # CHECKLIST
    # ═══════════════════════════════════════════════════
    story.append(Spacer(1, 16))
    story.append(Paragraph('Designer Checklist', h1))
    orange_rule()
    story.append(Spacer(1, 4))

    story.append(Paragraph('Products', h3))
    for item in [
        'Create GroundID Leader 12-Week product ($3,000/mo or $8,500 one-time)',
        'Create GroundID Leader Intensive product ($5,000/mo or $14,000 one-time)',
        'Configure access rules: each product grants appropriate course/member access',
    ]:
        story.append(CheckboxItem(item, W))

    story.append(Spacer(1, 6))
    story.append(Paragraph('Replay Vault', h3))
    for item in [
        'Create Squarespace Course at /replay-vault',
        'Configure member-only access (all paying members)',
        'Create first month section with placeholder lesson',
    ]:
        story.append(CheckboxItem(item, W))

    story.append(Spacer(1, 6))
    story.append(Paragraph('GroundID Leader Course', h3))
    for item in [
        'Create Squarespace Course at /groundid-leader',
        'Create Module 1: Pre-Work (5 lessons)',
        'Create Module 2: Sessions (empty, filled weekly)',
        'Create Module 3: Resources (3 lessons)',
        'Configure access: Leader + Intensive enrollees only',
    ]:
        story.append(CheckboxItem(item, W))

    story.append(Spacer(1, 6))
    story.append(Paragraph('Member Area', h3))
    for item in [
        'Create Squarespace Member Site at /member-area',
        'Create Prompt Guides page (4 profile PDFs)',
        'Create Resources page',
        'Configure member-only access',
    ]:
        story.append(CheckboxItem(item, W))

    story.append(Spacer(1, 6))
    story.append(Paragraph('Integration + Testing', h3))
    for item in [
        'Connect Stripe to Squarespace (Commerce \u2192 Payments)',
        'Test member login flow',
        'Test access tiers (VM vs Leader vs Intensive)',
        'Add member-only navigation links',
        'Mobile responsiveness check on all new pages',
    ]:
        story.append(CheckboxItem(item, W))

    # Footer
    story.append(Spacer(1, 24))
    gold_rule()
    story.append(Spacer(1, 8))
    story.append(Paragraph('<b>DR. CARA</b> \u00b7 Connected Leadership \u00b7 drcara.net', footer_s))

    doc.build(story)
    print(f'PDF generated: {out}')
    return out

if __name__ == '__main__':
    build_pdf()
