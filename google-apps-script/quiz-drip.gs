// ============================================================
// DR. CARA — Quiz Lead Webhook + Email Drip Campaign
// ============================================================
// Deploy as Web App → receives POST from quiz landing page.
// Writes lead to Google Sheet + sends 3-email drip sequence.
// Day 0: immediate — profile insight + value
// Day 2: deeper pattern + growth edge
// Day 5: CTA to Virtual Mind
//
// SETUP:
// 1. Paste this into Apps Script (Extensions → Apps Script)
// 2. Deploy → New Deployment → Web App
//    - Execute as: Me
//    - Who has access: Anyone
// 3. Copy the Web App URL
// 4. Paste it into the quiz HTML as WEBHOOK_URL
// 5. Add daily trigger: processScheduledQuizEmails → 9-10am
// ============================================================

// ── CONFIG ──────────────────────────────────────────────────
var CONFIG = {
  SHEET_ID: '1uXLJlI7_GowLiUOxGSvORgi3ZpwAk9mFJwWZ5rZxqJA',
  QUIZ_LEADS_TAB: 'Quiz Leads',
  DRIP_SCHEDULE_TAB: 'Quiz Drip Schedule',
  SENDER_NAME: 'Dr. Cara Alexander',
  VIRTUAL_MIND_URL: 'https://www.delphi.ai/drcara',
  VIRTUAL_MIND_CHECKOUT: 'https://buy.stripe.com/YOUR_VM_LINK',  // Update with your Stripe link
  QUIZ_URL: 'https://www.grounid.com'
};

// ── PROFILE DATA ────────────────────────────────────────────
var PROFILES = {
  'Architect': {
    color: '#c84200',
    leadsFrom: 'Mastery',
    pillar: 'Conquer Control',
    tagline: 'You lead from Mastery. And it is both your greatest strength and your heaviest burden.',
    pattern: 'There is a part of you that has been working overtime for a very long time — and it is extraordinarily good at its job. It plans ahead. It catches things before they fall. It holds a standard that very few people around you are even aware of.',
    growthEdge: 'Leading from security, not anticipation of loss',
    rprInsight: 'You process information through a control filter — assessing whether things are "in hand" before you even register what\'s actually happening. This means you systematically underweight what doesn\'t require managing — including people doing fine without your intervention.',
    selfLed: 'The goal is not to dismantle the Architect. It is to let this part take a seat beside you rather than run ahead of you.',
    vmPrompt: 'I\'m The Architect. How does my need for control show up when I\'m delegating to my team?'
  },
  'Carrier': {
    color: '#c89000',
    leadsFrom: 'Connection',
    pillar: 'Recognize Value',
    tagline: 'You lead from Connection. And the weight of it is invisible to everyone but you.',
    pattern: 'You hold the relational temperature of every room you enter. You notice when someone is struggling before they say a word. Your team trusts you genuinely — and the weight of being responsible for that trust has become so familiar you\'ve stopped noticing it is there.',
    growthEdge: 'Caring from worth, not from fear of disconnection',
    rprInsight: 'Before information is processed as content, it has already been processed as relationship. "What does this mean for us? What do they need from me?" Your relational processing consistently precedes truth processing — which means you systematically discount information that threatens the room\'s goodwill.',
    selfLed: 'Self-led leadership is not about caring less. It is about caring from a different address — from the security of knowing who you are, not from fear of disconnection.',
    vmPrompt: 'I\'m The Carrier. How do I stop absorbing everyone else\'s emotions in meetings?'
  },
  'Performer': {
    color: '#d81360',
    leadsFrom: 'Achievement',
    pillar: 'Recognize Value',
    tagline: 'You lead from Achievement. And you\'ve built something remarkable on a foundation that deserves to be rebuilt.',
    pattern: 'The part of you that drives results, holds the standard, and keeps the engine running is not just a professional skill — it has become a deeply ingrained identity. You are the one who delivers. The challenge is that your foundation is not meant to be a performance contract.',
    growthEdge: 'Achieving from identity, not conditional belonging',
    rprInsight: 'Information is assessed through a metric filter: does this move something forward? Is this worth my capacity? Information that doesn\'t map to measurable progress gets deprioritized. The gap appears in responses that require being with something rather than doing something.',
    selfLed: 'Self-led leadership is not about achieving less. It is about achieving from a different address — from the security of knowing that you already are enough.',
    vmPrompt: 'I\'m The Performer. How does my drive for results affect the way my team experiences me?'
  },
  'Sentinel': {
    color: '#df4f0f',
    leadsFrom: 'Protection',
    pillar: 'Embody Grace',
    tagline: 'You lead from Protection. And the intensity that gets things done is also what costs you most.',
    pattern: 'When something is wrong, you feel it first. When a situation is unravelling, you are already moving to contain it. That capacity has served you — it has made you someone people turn to when things are difficult. But there is a cost that shows up in the aftermath: the residue, the replay, the body that absorbed it all.',
    growthEdge: 'Responding from groundedness, not from activation',
    rprInsight: 'Your body knows something is happening before your mind has processed what. Your nervous system is the first instrument of receiving. The gap between Receive and Respond is shorter than it needs to be for the quality of decision you are actually capable of.',
    selfLed: 'Self-led leadership is not about slowing down. It is about building a practice that expands the pause between Receive and Respond — not to hesitate, but to choose.',
    vmPrompt: 'I\'m The Sentinel. How do I lead through a crisis without burning out afterward?'
  }
};

// ── WEB APP ENDPOINT (receives POST from quiz page) ────────
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var email = (data.email || '').trim();
    var name = (data.name || '').trim();
    var profile = (data.profile || '').trim().replace(/^The\s+/i, '');
    var source = (data.source || 'quiz').trim();

    if (!email || !profile) {
      return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: 'Missing email or profile' }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    var ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);

    // 1. Write lead to Quiz Leads sheet
    var quizSheet = ss.getSheetByName(CONFIG.QUIZ_LEADS_TAB);
    if (!quizSheet) {
      quizSheet = ss.insertSheet(CONFIG.QUIZ_LEADS_TAB);
      quizSheet.appendRow(['Timestamp', 'Email', 'First Name', 'Profile', 'Source']);
      quizSheet.setFrozenRows(1);
      quizSheet.getRange(1, 1, 1, 5).setFontWeight('bold').setBackground('#E8E0D8');
    }
    quizSheet.appendRow([new Date(), email, name, profile, source]);

    // 2. Check for duplicate in drip schedule
    var scheduleSheet = getOrCreateScheduleSheet_(ss);
    var existingEmails = scheduleSheet.getLastRow() > 1
      ? scheduleSheet.getRange(2, 1, scheduleSheet.getLastRow() - 1, 1).getValues().flat()
      : [];

    if (existingEmails.indexOf(email) > -1) {
      Logger.log('Lead logged, drip skipped (duplicate): ' + email);
      return ContentService.createTextOutput(JSON.stringify({ status: 'ok', drip: 'skipped-duplicate' }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // 3. Send Day 0 email immediately
    var day0 = getProfileEmailContent_(profile, 0, name);
    sendDripEmail_(email, name, day0.subject, day0.body);

    // 4. Schedule Day 2 and Day 5 emails
    var today = new Date();
    var day2Date = new Date(today.getTime() + 2 * 24 * 60 * 60 * 1000);
    var day5Date = new Date(today.getTime() + 5 * 24 * 60 * 60 * 1000);

    scheduleSheet.appendRow([email, name, profile, 0, formatDate_(today), 'sent', new Date()]);
    scheduleSheet.appendRow([email, name, profile, 2, formatDate_(day2Date), 'pending', '']);
    scheduleSheet.appendRow([email, name, profile, 5, formatDate_(day5Date), 'pending', '']);

    Logger.log('Quiz drip started for: ' + email + ' (' + profile + ')');

    return ContentService.createTextOutput(JSON.stringify({ status: 'ok', drip: 'started' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    Logger.log('doPost error: ' + err.message);
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Allow GET requests for testing (visit the Web App URL in browser)
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'ok',
    message: 'DR. CARA Quiz Drip webhook is live. Send POST with {email, name, profile, source}.'
  })).setMimeType(ContentService.MimeType.JSON);
}

// ── DAILY SCHEDULED EMAIL PROCESSOR ─────────────────────────
// Set up: Triggers → Add Trigger → processScheduledQuizEmails → Time-driven → Day timer → 9-10am
function processScheduledQuizEmails() {
  var ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
  var sheet = ss.getSheetByName(CONFIG.DRIP_SCHEDULE_TAB);
  if (!sheet || sheet.getLastRow() < 2) return;

  var today = formatDate_(new Date());
  var data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 7).getValues();
  var sent = 0;

  for (var i = 0; i < data.length; i++) {
    var email = data[i][0];
    var name = data[i][1];
    var profile = data[i][2];
    var day = data[i][3];
    var sendDate = data[i][4];
    var status = data[i][5];

    if (status === 'pending' && sendDate === today) {
      try {
        var content = getProfileEmailContent_(profile, day, name);
        sendDripEmail_(email, name, content.subject, content.body);

        // Mark as sent (row = i + 2 because of header)
        sheet.getRange(i + 2, 6).setValue('sent');
        sheet.getRange(i + 2, 7).setValue(new Date());
        sent++;
      } catch (err) {
        Logger.log('Failed to send Day ' + day + ' to ' + email + ': ' + err.message);
        sheet.getRange(i + 2, 6).setValue('error: ' + err.message);
      }
    }
  }

  Logger.log('Processed quiz drip emails. Sent: ' + sent);
}

// ── EMAIL CONTENT BY PROFILE × DAY ─────────────────────────
function getProfileEmailContent_(profileName, day, firstName) {
  var p = PROFILES[profileName];
  if (!p) {
    Logger.log('Unknown profile: ' + profileName);
    p = PROFILES['Architect']; // fallback
  }

  var greeting = firstName ? firstName : 'there';

  if (day === 0) {
    return {
      subject: 'Your Leadership Origin Profile: The ' + profileName,
      body: buildEmailHtml_(p.color, [
        '<p style="font-size:18px;color:#2A2320;">Hi ' + greeting + ',</p>',
        '<p>Thank you for taking the Leadership Origin Profile assessment. Your result reveals something important about how you lead — and more importantly, what that leadership pattern is protecting.</p>',
        '<div style="border-left:4px solid ' + p.color + ';padding:16px 20px;margin:24px 0;background:#FFFAF5;">',
        '  <p style="font-size:13px;font-weight:700;color:' + p.color + ';text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Your Profile</p>',
        '  <p style="font-size:22px;font-weight:600;color:#2A2320;margin-bottom:8px;">The ' + profileName + '</p>',
        '  <p style="font-style:italic;color:#4A3F38;">' + p.tagline + '</p>',
        '</div>',
        '<p><strong>The Pattern:</strong></p>',
        '<p>' + p.pattern + '</p>',
        '<p style="margin-top:20px;"><strong>Your Growth Edge:</strong> <em>' + p.growthEdge + '</em></p>',
        '<p style="margin-top:20px;">This is not a label. Every leader carries all four profiles — the Architect, the Carrier, the Performer, and the Sentinel. Your dominant profile reveals which part is leading your decisions <em>right now</em>.</p>',
        '<p style="margin-top:20px;">Over the next few days, I\'ll share what this means for the way you receive information, make decisions, and show up under pressure.</p>',
        '<p style="margin-top:24px;">With intention,<br><strong>Dr. Cara Alexander</strong></p>'
      ])
    };
  }

  if (day === 2) {
    return {
      subject: 'What The ' + profileName + ' Misses — And How to See It',
      body: buildEmailHtml_(p.color, [
        '<p style="font-size:18px;color:#2A2320;">Hi ' + greeting + ',</p>',
        '<p>Two days ago, your assessment revealed you as <strong>The ' + profileName + '</strong> — leading from ' + p.leadsFrom + '. Today I want to go deeper into what that actually means for how you process the world.</p>',
        '<div style="border-left:4px solid ' + p.color + ';padding:16px 20px;margin:24px 0;background:#FFFAF5;">',
        '  <p style="font-size:13px;font-weight:700;color:' + p.color + ';text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Your RPR Pattern</p>',
        '  <p style="color:#4A3F38;">' + p.rprInsight + '</p>',
        '</div>',
        '<p>This is the Receive-Perceive-Respond framework in action. Every leader has a default sequence — and yours has been running so long it feels like truth rather than pattern.</p>',
        '<p style="margin-top:16px;"><strong>The anchor for your profile is: ' + p.pillar + '</strong></p>',
        '<p style="margin-top:16px;">' + p.selfLed + '</p>',
        '<p style="margin-top:20px;">In my next email, I\'ll show you exactly how to start working with this pattern — not against it, not around it, but <em>with</em> it.</p>',
        '<p style="margin-top:20px;">Meanwhile, try asking yourself today: <em>"Am I responding to what\'s actually happening, or to what my pattern says is happening?"</em></p>',
        '<p style="margin-top:24px;">With intention,<br><strong>Dr. Cara Alexander</strong></p>'
      ])
    };
  }

  if (day === 5) {
    return {
      subject: 'Your Next Step as The ' + profileName,
      body: buildEmailHtml_(p.color, [
        '<p style="font-size:18px;color:#2A2320;">Hi ' + greeting + ',</p>',
        '<p>You\'ve seen the pattern. You\'ve seen what it protects. Now the question becomes: <em>what do you do with this?</em></p>',
        '<p>Most leadership development stops at awareness. The Connected Leadership framework goes further — into the practice of leading from your center rather than from your protective pattern.</p>',
        '<div style="border-left:4px solid ' + p.color + ';padding:16px 20px;margin:24px 0;background:#FFFAF5;">',
        '  <p style="font-size:13px;font-weight:700;color:' + p.color + ';text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Try This With the Virtual Mind</p>',
        '  <p style="color:#4A3F38;font-style:italic;">"' + p.vmPrompt + '"</p>',
        '  <p style="margin-top:12px;color:#4A3F38;">The Virtual Mind is trained on the Connected Leadership framework and all four profiles. It can coach you through real scenarios — conflict, delegation, decision-making — using the RPR method in real time.</p>',
        '</div>',
        '<p><strong>Try it free right now:</strong></p>',
        '<div style="text-align:center;margin:28px 0;">',
        '  <a href="' + CONFIG.VIRTUAL_MIND_URL + '" style="display:inline-block;padding:14px 36px;background:' + p.color + ';color:#FFFFFF;text-decoration:none;font-weight:700;font-size:15px;letter-spacing:0.05em;border-radius:0;">Talk to the Virtual Mind</a>',
        '</div>',
        '<p style="text-align:center;font-size:13px;color:#A09080;">Free — no account required</p>',
        '<p style="margin-top:24px;">The assessment named the pattern. The Virtual Mind helps you work with it. And when you\'re ready to go deeper — the GroundID Leadership Program is where this work transforms how you lead.</p>',
        '<p style="margin-top:24px;">With intention,<br><strong>Dr. Cara Alexander</strong></p>'
      ])
    };
  }

  // Fallback
  return { subject: 'From Dr. Cara Alexander', body: '' };
}

// ── EMAIL HTML BUILDER ──────────────────────────────────────
function buildEmailHtml_(accentColor, contentParts) {
  return [
    '<!DOCTYPE html>',
    '<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>',
    '<body style="margin:0;padding:0;background:#F5F0EB;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Arial,Helvetica,sans-serif;">',
    '<table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F0EB;padding:32px 16px;">',
    '<tr><td align="center">',
    '<table width="600" cellpadding="0" cellspacing="0" style="background:#FFFFFF;max-width:600px;width:100%;">',
    // Header bar
    '<tr><td style="height:4px;background:' + accentColor + ';"></td></tr>',
    // Logo area
    '<tr><td style="padding:28px 40px 20px;border-bottom:1px solid #E8E0D8;">',
    '  <span style="font-size:14px;font-weight:700;color:#2A2320;letter-spacing:0.15em;text-transform:uppercase;">DR. CARA</span>',
    '  <span style="font-size:12px;color:#A09080;margin-left:8px;">Connected Leadership</span>',
    '</td></tr>',
    // Content
    '<tr><td style="padding:32px 40px;color:#4A3F38;font-size:15px;line-height:1.7;">',
    contentParts.join('\n'),
    '</td></tr>',
    // Footer
    '<tr><td style="padding:24px 40px;border-top:1px solid #E8E0D8;background:#FFFAF5;">',
    '  <p style="font-size:12px;color:#A09080;line-height:1.6;margin:0;">',
    '    Dr. Cara Alexander | Connected Leadership<br>',
    '    You\'re receiving this because you took the Leadership Origin Profile assessment.<br>',
    '    <a href="mailto:dr.caraalex@gmail.com?subject=Unsubscribe" style="color:#A09080;">Unsubscribe</a>',
    '  </p>',
    '</td></tr>',
    '</table>',
    '</td></tr></table>',
    '</body></html>'
  ].join('\n');
}

// ── SEND EMAIL VIA GMAIL ────────────────────────────────────
function sendDripEmail_(to, name, subject, htmlBody) {
  GmailApp.sendEmail(to, subject, '', {
    htmlBody: htmlBody,
    name: CONFIG.SENDER_NAME,
    replyTo: 'dr.caraalex@gmail.com'
  });
  Logger.log('Sent: "' + subject + '" to ' + to);
}

// ── HELPERS ─────────────────────────────────────────────────
function getOrCreateScheduleSheet_(ss) {
  var sheet = ss.getSheetByName(CONFIG.DRIP_SCHEDULE_TAB);
  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.DRIP_SCHEDULE_TAB);
    sheet.appendRow(['Email', 'Name', 'Profile', 'Day', 'Send Date', 'Status', 'Sent At']);
    sheet.setFrozenRows(1);
    // Format header
    sheet.getRange(1, 1, 1, 7).setFontWeight('bold').setBackground('#E8E0D8');
  }
  return sheet;
}

function formatDate_(date) {
  return Utilities.formatDate(date, Session.getScriptTimeZone(), 'yyyy-MM-dd');
}

// ── SETUP: CREATE DAILY TRIGGER ─────────────────────────────
// Run this ONCE to create the 9am daily trigger. Then delete this function.
function createDailyTrigger() {
  // Remove any existing triggers for this function first
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'processScheduledQuizEmails') {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }
  // Create new daily trigger at 9am
  ScriptApp.newTrigger('processScheduledQuizEmails')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
  Logger.log('Daily trigger created: processScheduledQuizEmails will run at 9am every day.');
}

// ── TEST FUNCTIONS ──────────────────────────────────────────
// Run these manually in Apps Script to test each email

function testDay0Email() {
  var content = getProfileEmailContent_('Architect', 0, 'Cara');
  sendDripEmail_('dr.caraalex@gmail.com', 'Cara', content.subject, content.body);
}

function testDay2Email() {
  var content = getProfileEmailContent_('Carrier', 2, 'Cara');
  sendDripEmail_('dr.caraalex@gmail.com', 'Cara', content.subject, content.body);
}

function testDay5Email() {
  var content = getProfileEmailContent_('Performer', 5, 'Cara');
  sendDripEmail_('dr.caraalex@gmail.com', 'Cara', content.subject, content.body);
}

function testFullDrip() {
  // Simulates a form submission for testing
  var ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
  var quizSheet = ss.getSheetByName(CONFIG.QUIZ_LEADS_TAB);

  // Add a test row
  quizSheet.appendRow([new Date(), 'dr.caraalex@gmail.com', 'Cara', 'Architect', 'test']);

  // Trigger the drip
  onFormSubmit(null);

  Logger.log('Test drip initiated — check your inbox and Quiz Drip Schedule tab');
}
