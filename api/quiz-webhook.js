/**
 * Vercel Serverless Function — POST /api/quiz-webhook
 *
 * Receives quiz completion data from the front-end,
 * validates, normalizes, and stores it in Vercel Blob storage.
 * No external services required — everything stays in Vercel.
 *
 * Requires: Vercel Blob store connected to this project
 * (creates BLOB_READ_WRITE_TOKEN automatically)
 */

import { put, list } from '@vercel/blob';

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

  // Validate
  const errors = validate(req.body || {});
  if (errors.length) {
    return res.status(422).json({ errors });
  }

  try {
    // Normalize the payload
    const lead = normalize(req.body);

    // Store each lead as its own blob file (keyed by timestamp + email hash)
    // This avoids race conditions from concurrent writes to a single file
    const key = `leads/${Date.now()}-${lead.email.replace(/[^a-z0-9]/g, '_')}.json`;

    await put(key, JSON.stringify(lead), {
      contentType: 'application/json',
      access: 'public',
    });

    console.log(`[quiz-webhook] ✓ Lead stored: ${lead.email} → ${lead.quiz_outcome}`);

    return res.status(200).json({
      message: 'Lead captured successfully',
      lead: {
        email: lead.email,
        first_name: lead.first_name,
        quiz_outcome: lead.quiz_outcome,
      }
    });

  } catch (err) {
    console.error('[quiz-webhook] Storage failed:', err.message);
    return res.status(500).json({ error: 'Lead storage failed', detail: err.message });
  }
}
