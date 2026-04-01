/**
 * Google Apps Script — Quiz Lead Webhook
 *
 * SETUP INSTRUCTIONS:
 * 1. Go to https://sheets.new → creates a new Google Sheet
 * 2. Rename it "Leadership Origin Quiz Leads"
 * 3. In Row 1, add these headers:
 *      A1: Timestamp  |  B1: First Name  |  C1: Email  |  D1: Profile  |  E1: Source
 * 4. Click Extensions → Apps Script
 * 5. Delete any existing code and paste THIS ENTIRE FILE
 * 6. Click Deploy → New deployment
 *    - Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 7. Click Deploy → Authorize → Allow
 * 8. Copy the Web app URL (looks like: https://script.google.com/macros/s/AKfy.../exec)
 * 9. Paste that URL into Vercel:
 *    vercel.com/ground-id/landing-pages/settings/environment-variables
 *    Key: GOOGLE_SHEET_WEBHOOK_URL
 *    Value: (the URL you copied)
 *    Save → done!
 *
 * Each quiz completion adds a new row:
 * | Timestamp            | First Name | Email              | Profile   | Source         |
 * | 2026-04-01 19:00:00 | Cara       | cara@example.com   | Architect | lp-assessment-1|
 */

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Add headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'First Name', 'Email', 'Profile', 'Source']);
      sheet.getRange(1, 1, 1, 5).setFontWeight('bold');
    }

    // Check for duplicate email (skip if already exists)
    var emails = sheet.getRange(1, 3, Math.max(sheet.getLastRow(), 1), 1).getValues();
    var isDuplicate = emails.some(function(row) {
      return row[0].toString().toLowerCase() === data.email.toLowerCase();
    });

    if (isDuplicate) {
      return ContentService
        .createTextOutput(JSON.stringify({ result: 'duplicate', email: data.email }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // Append new lead row
    sheet.appendRow([
      data.timestamp || new Date().toISOString(),
      data.first_name || '',
      data.email || '',
      data.quiz_outcome || '',
      data.source || ''
    ]);

    // Auto-resize columns for readability
    sheet.autoResizeColumns(1, 5);

    return ContentService
      .createTextOutput(JSON.stringify({ result: 'success', row: sheet.getLastRow() }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'error', message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function — run this in Apps Script editor to verify it works
function testDoPost() {
  var testPayload = {
    postData: {
      contents: JSON.stringify({
        email: 'test@example.com',
        first_name: 'Test User',
        quiz_outcome: 'Architect',
        source: 'lp-assessment-1',
        timestamp: new Date().toISOString()
      })
    }
  };

  var result = doPost(testPayload);
  Logger.log(result.getContent());
}
