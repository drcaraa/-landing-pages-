/**
 * Vercel Serverless Function — POST /api/quiz-webhook
 *
 * Receives quiz completion data from the front-end,
 * validates & normalizes the payload, then forwards it
 * to a Google Apps Script Web App that logs leads into
 * a Google Sheet.
 *
 * Environment variable required in Vercel → Settings → Environment Variables:
 *   GOOGLE_SHEET_WEBHOOK_URL  — the deployed Google Apps Script web app URL
 */

// ── Valid quiz outcomes (whitelist) ──────────────────────

const VALID_OUTCOMES = ['Architect', 'Carrier', 'Performer', 'Sentinel'];

// ── Validation ───────────────────────────────────────────

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validate({ email, first_name, quiz_outcome }) {
  const errors = [];

  if (!email || typeof email !== 'string' || !EMAIL_RE.test(email.trim()))
    errors.push('A valid email address is required.');

  if (!first_name || typeof first_name !== 'string' || first_name.trim().length === 0)
    errors.push('first_name must be a non-empty string.');

  if (quiz_outcome && !VALID_OUTCOMES.includes(quiz_outcome.trim()))
    errors.push(`quiz_outcome must be one of: ${VALID_OUTCOMES.join(', ')}`);

  return errors;
}

// ── Normalization ────────────────────────────────────────

function titleCase(s) {
  const trimmed = s.trim().replace(/\s+/g, ' ');
  if (!trimmed) return '';
  return trimmed
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(' ');
}

function normalize(raw) {
  return {
    email:        raw.email.trim().toLowerCase(),
    first_name:   titleCase(raw.first_name || ''),
    quiz_outcome: (raw.quiz_outcome || '').trim(),
    source:       (raw.source || 'lp-assessment-1').trim(),
    timestamp:    raw.timestamp || new Date().toISOString(),
  };
}

// ── Retry-capable POST (300ms × 3 backoff: 300 → 900 → 2700) ─

async function postWithRetry(url, body, max = 3) {
  let attempt = 0;
  let wait = 300;

  while (true) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);

      const res = await fetch(url, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(body),
        signal:  controller.signal,
        redirect: 'follow',   // Google Apps Script redirects on deploy
      });

      clearTimeout(timeout);

      if (res.ok) {
        console.log(`[quiz-webhook] ✓ Logged to Google Sheet (${res.status}) on attempt ${attempt + 1}`);
        return { ok: true, status: res.status };
      }

      if (res.status === 429 || (res.status >= 500 && res.status <= 599)) {
        const errText = await res.text();
        console.warn(`[quiz-webhook] ✗ Attempt ${attempt + 1}/${max} — ${res.status}: ${errText}`);
        if (++attempt >= max) throw new Error(`Google Sheet webhook returned ${res.status} after ${max} attempts`);
        await new Promise(r => setTimeout(r, wait));
        wait *= 3;
        continue;
      }

      const text = await res.text();
      throw new Error(`Google Sheet webhook returned ${res.status}: ${text}`);

    } catch (err) {
      if (err.name === 'AbortError') {
        console.warn(`[quiz-webhook] ✗ Attempt ${attempt + 1}/${max} — request timed out`);
      } else if (!err.message.startsWith('Google Sheet webhook returned')) {
        console.warn(`[quiz-webhook] ✗ Attempt ${attempt + 1}/${max} — ${err.message}`);
      } else {
        throw err;
      }

      if (++attempt >= max) throw new Error(`Failed after ${max} attempts: ${err.message}`);
      await new Promise(r => setTimeout(r, wait));
      wait *= 3;
    }
  }
}

// ── Core logic ───────────────────────────────────────────

async function sendQuizCompletion(payload, webhookUrl) {
  const errors = validate(payload);
  if (errors.length) return { ok: false, status: 422, errors };

  const body = normalize(payload);
  const result = await postWithRetry(webhookUrl, body);
  return result;
}

// ── Vercel handler ───────────────────────────────────────

export default async function handler(req, res) {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Validate first
  const errors = validate(req.body || {});
  if (errors.length) {
    return res.status(422).json({ errors });
  }

  const webhookUrl = process.env.GOOGLE_SHEET_WEBHOOK_URL;
  if (!webhookUrl) {
    console.error('[quiz-webhook] GOOGLE_SHEET_WEBHOOK_URL is not configured');
    return res.status(500).json({ error: 'Google Sheet webhook not configured' });
  }

  try {
    const result = await sendQuizCompletion(req.body, webhookUrl);

    if (!result.ok) {
      return res.status(result.status).json({ errors: result.errors });
    }

    return res.status(200).json({ message: 'Quiz lead logged to Google Sheet', status: result.status });
  } catch (err) {
    console.error('[quiz-webhook] Delivery failed:', err.message);
    return res.status(502).json({ error: 'Google Sheet logging failed', detail: err.message });
  }
}
