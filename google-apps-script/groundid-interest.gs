// ============================================================
// DR. CARA — GroundID Leader · Beta Interest Form Webhook
// ============================================================
// Deploy as Web App → receives POST from /groundid-interest.html
// Writes submission to Google Sheet + notifies Dr. Cara + sends
// confirmation acknowledgment to the submitter.
//
// SETUP:
// 1. Open a Google Sheet (or reuse the existing one)
// 2. Extensions → Apps Script → paste this file
// 3. Edit CONFIG below (SHEET_ID + notification email)
// 4. Deploy → New Deployment → Web App
//    - Description: "GroundID Interest Webhook"
//    - Execute as: Me
//    - Who has access: Anyone
// 5. Copy the Web App URL
// 6. Paste it into groundid-interest.html as WEBHOOK_URL
// ============================================================

// ── CONFIG ──────────────────────────────────────────────────
var CONFIG = {
  // Dedicated GroundID Leader Interest sheet
  SHEET_ID: '1nx9hOrQ7WkS9joYenZwGM1Gqk5r_2aCDPBqD_SzKXIg',
  INTEREST_TAB: 'GroundID Interest',
  NOTIFY_EMAIL: 'drcara@drcaraa.com',              // who gets the "new interest" notification
  CC_EMAIL: 'drewh@drcaraa.com',                   // CC on notifications (optional — blank to disable)
  SENDER_NAME: 'Dr. Cara Alexander',
  REPLY_TO: 'drcara@drcaraa.com'
};

var HEADER_ROW = [
  'Timestamp',
  'First Name',
  'Last Name',
  'Email',
  'Phone',
  'Role / Title',
  'Organization',
  'Referred By',
  'Reflection',
  'Schedule Fit',
  'Consent',
  'Status',            // pending / contacted / enrolled / declined
  'Notes',             // Dr. Cara's internal notes
  'Source',
  'User Agent',
  'Submitted At'
];

// ── WEB APP ENDPOINT ────────────────────────────────────────
function doPost(e) {
  try {
    var data = {};
    try {
      data = JSON.parse(e.postData.contents);
    } catch (parseErr) {
      // Fallback: form-encoded
      data = e.parameter || {};
    }

    var firstName = (data.firstName || '').toString().trim();
    var lastName = (data.lastName || '').toString().trim();
    var email = (data.email || '').toString().trim().toLowerCase();
    var phone = (data.phone || '').toString().trim();
    var role = (data.role || '').toString().trim();
    var organization = (data.organization || '').toString().trim();
    var referredBy = (data.referredBy || '').toString().trim();
    var reflection = (data.reflection || '').toString().trim();
    var scheduleFit = (data.scheduleFit || '').toString().trim();
    var consent = (data.consent || '').toString().trim();
    var source = (data.source || 'groundid-interest').toString().trim();
    var userAgent = (data.userAgent || '').toString().trim();
    var submittedAt = (data.submittedAt || new Date().toISOString()).toString();

    if (!email || !firstName) {
      return jsonResponse_({ status: 'error', message: 'Missing first name or email.' });
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return jsonResponse_({ status: 'error', message: 'Invalid email address.' });
    }

    var ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
    var sheet = getOrCreateSheet_(ss);

    // Write row
    sheet.appendRow([
      new Date(),
      firstName,
      lastName,
      email,
      phone,
      role,
      organization,
      referredBy,
      reflection,
      scheduleFit,
      consent,
      'pending',
      '',
      source,
      userAgent,
      submittedAt
    ]);

    // Notify Dr. Cara
    try {
      sendNotification_({
        firstName: firstName,
        lastName: lastName,
        email: email,
        phone: phone,
        role: role,
        organization: organization,
        referredBy: referredBy,
        reflection: reflection,
        scheduleFit: scheduleFit
      });
    } catch (notifyErr) {
      Logger.log('Notification email failed: ' + notifyErr.message);
    }

    // Send acknowledgment to the submitter
    try {
      sendAcknowledgment_(email, firstName);
    } catch (ackErr) {
      Logger.log('Ack email failed: ' + ackErr.message);
    }

    return jsonResponse_({ status: 'ok' });

  } catch (err) {
    Logger.log('doPost error: ' + err.message);
    return jsonResponse_({ status: 'error', message: err.message });
  }
}

function doGet(e) {
  return jsonResponse_({
    status: 'ok',
    message: 'GroundID Interest webhook is live. POST JSON to this URL.'
  });
}

// ── SHEET HELPERS ───────────────────────────────────────────
function getOrCreateSheet_(ss) {
  var sheet = ss.getSheetByName(CONFIG.INTEREST_TAB);
  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.INTEREST_TAB);
    sheet.appendRow(HEADER_ROW);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADER_ROW.length)
      .setFontWeight('bold')
      .setBackground('#E8E0D8')
      .setFontColor('#2A2320');
    // Column widths
    sheet.setColumnWidth(1, 160);   // Timestamp
    sheet.setColumnWidth(2, 110);   // First
    sheet.setColumnWidth(3, 110);   // Last
    sheet.setColumnWidth(4, 200);   // Email
    sheet.setColumnWidth(5, 130);   // Phone
    sheet.setColumnWidth(6, 180);   // Role
    sheet.setColumnWidth(7, 180);   // Org
    sheet.setColumnWidth(8, 160);   // Referred by
    sheet.setColumnWidth(9, 420);   // Reflection
    sheet.setColumnWidth(10, 260);  // Schedule fit
    sheet.setColumnWidth(11, 90);   // Consent
    sheet.setColumnWidth(12, 100);  // Status
    sheet.setColumnWidth(13, 260);  // Notes
    sheet.setColumnWidth(14, 110);  // Source
    sheet.setColumnWidth(15, 260);  // User agent
    sheet.setColumnWidth(16, 170);  // Submitted at
  }
  return sheet;
}

// ── NOTIFICATION EMAIL TO DR. CARA ──────────────────────────
function sendNotification_(d) {
  var name = (d.firstName + ' ' + d.lastName).trim();
  var subject = 'New GroundID Interest — ' + name + (d.referredBy ? ' (ref: ' + d.referredBy + ')' : '');

  var html = [
    '<div style="font-family:Arial,Helvetica,sans-serif;color:#4A3F38;max-width:620px;margin:0 auto;">',
    '  <div style="height:5px;background:#E8600A;"></div>',
    '  <div style="padding:24px 32px 8px;border-bottom:1px solid #EFE6DA;">',
    '    <div style="font-family:Georgia,serif;font-size:16px;font-weight:600;letter-spacing:0.14em;color:#2A2320;text-transform:uppercase;">Dr. Cara Alexander</div>',
    '    <div style="font-size:10px;font-weight:700;letter-spacing:0.22em;color:#C9A850;text-transform:uppercase;margin-top:4px;">New Interest — GroundID Leader Beta</div>',
    '  </div>',
    '  <div style="padding:28px 32px;">',
    '    <h2 style="font-family:Georgia,serif;font-size:22px;font-weight:500;color:#2A2320;margin:0 0 12px 0;">' + escape_(name) + '</h2>',
    '    <p style="margin:0 0 6px 0;"><strong>Email:</strong> <a href="mailto:' + escape_(d.email) + '" style="color:#E8600A;">' + escape_(d.email) + '</a></p>',
    d.phone ? '    <p style="margin:0 0 6px 0;"><strong>Phone:</strong> ' + escape_(d.phone) + '</p>' : '',
    '    <p style="margin:0 0 6px 0;"><strong>Role:</strong> ' + escape_(d.role) + (d.organization ? ' @ ' + escape_(d.organization) : '') + '</p>',
    d.referredBy ? '    <p style="margin:0 0 6px 0;"><strong>Referred by:</strong> ' + escape_(d.referredBy) + '</p>' : '',
    '    <p style="margin:0 0 12px 0;"><strong>Schedule fit:</strong> ' + escape_(d.scheduleFit) + '</p>',
    '    <div style="background:#FFF5EC;border-left:4px solid #E8600A;padding:18px 22px;border-radius:4px;margin:16px 0;">',
    '      <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;color:#C44D00;text-transform:uppercase;margin-bottom:8px;">Reflection</div>',
    '      <div style="font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#4A3F38;white-space:pre-wrap;">' + escape_(d.reflection) + '</div>',
    '    </div>',
    '    <p style="margin:18px 0 0 0;font-size:13px;color:#8A7060;">Status is set to <strong>pending</strong> in the sheet. Update it after you respond.</p>',
    '  </div>',
    '  <div style="height:4px;background:#C9A850;"></div>',
    '</div>'
  ].filter(Boolean).join('\n');

  var options = {
    htmlBody: html,
    name: CONFIG.SENDER_NAME,
    replyTo: d.email  // replying jumps straight to the submitter
  };
  if (CONFIG.CC_EMAIL) options.cc = CONFIG.CC_EMAIL;

  GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL, subject, '', options);
}

// ── ACKNOWLEDGMENT EMAIL TO SUBMITTER ───────────────────────
function sendAcknowledgment_(email, firstName) {
  var greeting = firstName ? firstName : 'there';
  var subject = 'I have your note — GroundID Leader Beta';

  var html = [
    '<div style="font-family:Arial,Helvetica,sans-serif;color:#4A3F38;max-width:620px;margin:0 auto;background:#FFFFFF;">',
    '  <div style="height:5px;background:#E8600A;"></div>',
    '  <div style="padding:28px 40px 20px;border-bottom:1px solid #EFE6DA;">',
    '    <div style="font-family:Georgia,serif;font-size:18px;font-weight:600;letter-spacing:0.14em;color:#2A2320;text-transform:uppercase;">Dr. Cara Alexander</div>',
    '    <div style="font-size:10px;font-weight:700;letter-spacing:0.22em;color:#C9A850;text-transform:uppercase;margin-top:4px;">Connected Leadership</div>',
    '  </div>',
    '  <div style="padding:36px 40px;font-family:Georgia,serif;font-size:16px;line-height:1.8;color:#4A3F38;">',
    '    <p style="margin:0 0 18px 0;">Hi ' + escape_(greeting) + ',</p>',
    '    <p style="margin:0 0 18px 0;">Thank you for the note. It is with me now — I read every one of these myself.</p>',
    '    <p style="margin:0 0 18px 0;">If there is a fit, you will hear from me within 48 hours to book a short conversation. If the timing or shape is not right for this cohort, I will tell you that honestly too.</p>',
    '    <p style="margin:0 0 18px 0;">In the meantime, whoever forwarded this to you did so for a reason. That matters.</p>',
    '    <p style="font-family:Georgia,serif;font-style:italic;color:#9A603F;margin:28px 0 4px 0;">With respect and intention,</p>',
    '    <p style="font-family:Georgia,serif;font-size:18px;font-weight:600;color:#2A2320;margin:0 0 2px 0;">Dr. Cara Alexander</p>',
    '    <p style="font-size:11px;color:#8A7060;letter-spacing:0.06em;margin:0;">Connected Leadership &nbsp;·&nbsp; <a href="http://drcara.net" style="color:#8A7060;">drcara.net</a> &nbsp;·&nbsp; @drcaraa</p>',
    '  </div>',
    '  <div style="height:4px;background:#C9A850;"></div>',
    '</div>'
  ].join('\n');

  GmailApp.sendEmail(email, subject, '', {
    htmlBody: html,
    name: CONFIG.SENDER_NAME,
    replyTo: CONFIG.REPLY_TO
  });
}

// ── UTILS ───────────────────────────────────────────────────
function jsonResponse_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function escape_(s) {
  if (s == null) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// ── TEST (run manually in Apps Script) ──────────────────────
function testInterestSubmission() {
  var mockEvent = {
    postData: {
      contents: JSON.stringify({
        firstName: 'Test',
        lastName: 'Leader',
        email: 'dr.caraalex@gmail.com',
        phone: '555-0100',
        role: 'Head of Operations',
        organization: 'Test Co',
        referredBy: 'Colleague',
        reflection: 'I run a team of 40 in a growing company. Lately I am carrying the weight of people decisions that never feel clean. I would want to walk away knowing what is actually mine to hold.',
        scheduleFit: 'Yes — Wednesdays 3:30 PM ET works for all 12 weeks',
        consent: 'Yes',
        source: 'groundid-interest',
        userAgent: 'test-script',
        submittedAt: new Date().toISOString()
      })
    }
  };
  var result = doPost(mockEvent);
  Logger.log(result.getContent());
}
