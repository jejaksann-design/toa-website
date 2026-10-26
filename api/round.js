// Memulai satu ronde kuis: memberi token sekali pakai supaya skor tidak bisa dikirim sembarangan.
const kv = require('./_kv');
const crypto = require('crypto');
const MODES = ['sambung', 'tajwid', 'wawasan', 'daily'];
module.exports = async function (req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!kv.ready || req.method !== 'POST') return res.status(200).json({ off: true });
  const b = kv.body(req);
  if (MODES.indexOf(b.mode) < 0) return res.status(400).json({ err: 'mode' });
  const tok = crypto.randomBytes(12).toString('hex');
  try {
    await kv.pipe([['SET', 'rd:' + tok, b.mode + '|' + Date.now(), 'EX', 3600]]);
    res.status(200).json({ tok: tok });
  } catch (e) { res.status(200).json({ off: true }); }
};
