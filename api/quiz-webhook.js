/**
 * Vercel Serverless Function — POST /api/quiz-webhook
 *
 * Receives quiz completion data from the front-end,
 * validates & normalizes the payload, then forwards it
 * to the Delphi (or any external) webhook with retry logic.
 *
 * Environment variable required in Vercel → Settings → Environment Variables:
 *   DELPHI_WEBHOOK_URL  — the destination endpoint
 */

// ── Helpers ──────────────────────────────────────────────

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validatePayload({ email, first_name }) {
  const errors = [];

  if (!email || typeof email !== 'string' || !EMAIL_RE.test(email.trim()))
    errors.push('A valid email address is required.');

  if (!first_name || typeof first_name !== 'string' || first_name.trim().length === 0)
    errors.push('first_name must be a non-empty string.');

  return errors;
}

function normalizePayload(raw) {
  return {
    email:        raw.email.trim().toLowerCase(),
    first_name:   raw.first_name.trim(),
    quiz_outcome: (raw.quiz_outcome || '').trim(),
    source:       (raw.source       || 'leadership-origin-quiz').trim(),
    timestamp:    raw.timestamp || new Date().toISOString(),
  };
}

function buildWebhookBody(normalized) {
  return {
    event:        'quiz_completed',
    email:        normalized.email,
    first_name:   normalized.first_name,
    quiz_outcome: normalized.quiz_outcome,
    source:       normalized.source,
    timestamp:    normalized.timestamp,
  };
}

// ── Retry-capable POST ───────────────────────────────────

async function sendWithRetry(url, body, { maxRetries = 3, baseDelay = 500 } = {}) {
  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const res = await fetch(url, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(body),
      });

      if (res.ok) {                               // 2xx
        const text = await res.text();
        console.log(`[quiz-webhook] ✓ Sent to webhook (${res.status}) on attempt ${attempt + 1}`);
        return { success: true, status: res.status, response: text };
      }

      // Non-2xx — treat as retryable
      const errBody = await res.text();
      lastError = new Error(`HTTP ${res.status}: ${errBody}`);
      console.warn(
        `[quiz-webhook] ✗ Attempt ${attempt + 1}/${maxRetries + 1} failed — ${res.status}`
      );
    } catch (networkErr) {
      lastError = networkErr;
      console.warn(
        `[quiz-webhook] ✗ Attempt ${attempt + 1}/${maxRetries + 1} network error — ${networkErr.message}`
      );
    }

    // Exponential back-off before next retry (skip delay after last attempt)
    if (attempt < maxRetries) {
      const delay = baseDelay * Math.pow(2, attempt);   // 500 → 1000 → 2000 ms
      await new Promise(r => setTimeout(r, delay));
    }
  }

  // All retries exhausted
  throw lastError;
}

// ── Exported entry-point (core logic, framework-agnostic) ─

async function sendQuizToDelphi(payload, webhookUrl) {
  // 1. Validate
  const errors = validatePayload(payload);
  if (errors.length) return { ok: false, status: 422, errors };

  // 2. Normalize
  const normalized = normalizePayload(payload);

  // 3. Build body
  const body = buildWebhookBody(normalized);

  // 4. POST with retry
  const result = await sendWithRetry(webhookUrl, body);
  return { ok: true, ...result };
}

// ── Vercel handler ───────────────────────────────────────

export default async function handler(req, res) {
  // Only accept POST
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const webhookUrl = process.env.DELPHI_WEBHOOK_URL;
  if (!webhookUrl) {
    console.error('[quiz-webhook] DELPHI_WEBHOOK_URL is not configured');
    return res.status(500).json({ error: 'Webhook endpoint not configured' });
  }

  try {
    const result = await sendQuizToDelphi(req.body, webhookUrl);

    if (!result.ok) {
      return res.status(result.status).json({ errors: result.errors });
    }

    return res.status(200).json({ message: 'Quiz submission forwarded', status: result.status });
  } catch (err) {
    console.error('[quiz-webhook] All retries failed:', err.message);
    return res.status(502).json({ error: 'Webhook delivery failed after retries', detail: err.message });
  }
}
