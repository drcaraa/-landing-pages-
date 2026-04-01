/**
 * Vercel Serverless Function — POST /api/quiz-webhook
 *
 * Receives quiz completion data from the front-end,
 * validates & normalizes the payload, then POSTs it
 * to the Delphi Custom API Action endpoint.
 *
 * Delphi upserts a Contact (keyed on email), writes first_name,
 * and applies tags: quiz_taken, outcome_{quiz_outcome}, source:{source}
 *
 * Environment variable required in Vercel → Settings → Environment Variables:
 *   DELPHI_ACTION_URL  — your Custom API Action endpoint from Delphi
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

function toSlug(s) {
  return s.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

function normalize(raw) {
  return {
    email:        raw.email.trim().toLowerCase(),
    first_name:   titleCase(raw.first_name || ''),
    quiz_outcome: (raw.quiz_outcome || '').trim(),
    source:       toSlug(raw.source || 'lp-assessment-1'),
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
      const timeout = setTimeout(() => controller.abort(), 10000); // 10s read timeout

      const res = await fetch(url, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(body),
        signal:  controller.signal,
      });

      clearTimeout(timeout);

      // 2xx — success
      if (res.ok) {
        console.log(`[quiz-webhook] ✓ Delivered to Delphi (${res.status}) on attempt ${attempt + 1}`);
        return { ok: true, status: res.status };
      }

      // 429 or 5xx — retryable
      if (res.status === 429 || (res.status >= 500 && res.status <= 599)) {
        const errText = await res.text();
        console.warn(`[quiz-webhook] ✗ Attempt ${attempt + 1}/${max} — ${res.status}: ${errText}`);
        if (++attempt >= max) throw new Error(`Delphi returned ${res.status} after ${max} attempts`);
        await new Promise(r => setTimeout(r, wait));
        wait *= 3;
        continue;
      }

      // 4xx (not 429) — non-retryable client error
      const text = await res.text();
      throw new Error(`Delphi returned ${res.status}: ${text}`);

    } catch (err) {
      if (err.name === 'AbortError') {
        console.warn(`[quiz-webhook] ✗ Attempt ${attempt + 1}/${max} — request timed out`);
      } else if (!err.message.startsWith('Delphi returned')) {
        console.warn(`[quiz-webhook] ✗ Attempt ${attempt + 1}/${max} — ${err.message}`);
      } else {
        throw err; // non-retryable 4xx, rethrow immediately
      }

      if (++attempt >= max) throw new Error(`Failed after ${max} attempts: ${err.message}`);
      await new Promise(r => setTimeout(r, wait));
      wait *= 3;
    }
  }
}

// ── Core logic ───────────────────────────────────────────

async function sendQuizCompletion(payload, actionUrl) {
  // 1. Validate
  const errors = validate(payload);
  if (errors.length) return { ok: false, status: 422, errors };

  // 2. Normalize & build Delphi payload (no "event" wrapper — flat fields)
  const body = normalize(payload);

  // 3. POST with retry
  const result = await postWithRetry(actionUrl, body);
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

  // Validate payload first (useful errors even before Delphi is configured)
  const errors = validate(req.body || {});
  if (errors.length) {
    return res.status(422).json({ errors });
  }

  const actionUrl = process.env.DELPHI_ACTION_URL;
  if (!actionUrl) {
    console.error('[quiz-webhook] DELPHI_ACTION_URL is not configured');
    return res.status(500).json({ error: 'Delphi Action endpoint not configured' });
  }

  try {
    const result = await sendQuizCompletion(req.body, actionUrl);

    if (!result.ok) {
      return res.status(result.status).json({ errors: result.errors });
    }

    return res.status(200).json({ message: 'Quiz completion sent to Delphi', status: result.status });
  } catch (err) {
    console.error('[quiz-webhook] Delivery failed:', err.message);
    return res.status(502).json({ error: 'Delphi delivery failed', detail: err.message });
  }
}
