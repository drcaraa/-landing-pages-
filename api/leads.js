/**
 * Vercel Serverless Function — GET /api/leads
 *
 * Returns all quiz leads as downloadable CSV.
 * Reads individual lead files from Vercel Blob storage.
 *
 * Usage:
 *   https://your-domain.com/api/leads          → CSV download
 *   https://your-domain.com/api/leads?format=json → JSON array
 *
 * Protect this endpoint by adding a secret key:
 *   https://your-domain.com/api/leads?key=YOUR_SECRET
 *
 * Set LEADS_API_KEY in Vercel env vars to enable protection.
 */

import { list } from '@vercel/blob';

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Optional API key protection
  const apiKey = process.env.LEADS_API_KEY;
  if (apiKey && req.query.key !== apiKey) {
    return res.status(401).json({ error: 'Unauthorized. Provide ?key=YOUR_SECRET' });
  }

  try {
    // List all lead blobs
    const allBlobs = [];
    let cursor = undefined;

    do {
      const result = await list({ prefix: 'leads/', cursor, limit: 1000 });
      allBlobs.push(...result.blobs);
      cursor = result.cursor;
    } while (cursor);

    if (allBlobs.length === 0) {
      return res.status(200).json({ message: 'No leads yet', count: 0 });
    }

    // Fetch and parse each lead
    const leads = [];
    for (const blob of allBlobs) {
      try {
        const response = await fetch(blob.url);
        const lead = await response.json();
        leads.push(lead);
      } catch (e) {
        console.warn(`[leads] Skipping malformed blob: ${blob.pathname}`);
      }
    }

    // Sort by timestamp (newest first)
    leads.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    // JSON format
    if (req.query.format === 'json') {
      return res.status(200).json({ count: leads.length, leads });
    }

    // CSV format (default)
    const csvHeader = 'Timestamp,First Name,Email,Profile,Source';
    const csvRows = leads.map(l =>
      `"${l.timestamp}","${l.first_name}","${l.email}","${l.quiz_outcome}","${l.source}"`
    );
    const csv = [csvHeader, ...csvRows].join('\n');

    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename="quiz-leads.csv"');
    return res.status(200).send(csv);

  } catch (err) {
    console.error('[leads] Failed to retrieve leads:', err.message);
    return res.status(500).json({ error: 'Failed to retrieve leads', detail: err.message });
  }
}
