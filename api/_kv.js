// Upstash Redis lewat REST (tanpa paket npm). Variabel dari integrasi Vercel Storage.
const URL_ = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
exports.ready = !!(URL_ && TOKEN);
exports.pipe = async function (cmds) {
  const r = await fetch(URL_ + '/pipeline', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(cmds)
  });
  if (!r.ok) throw new Error('kv ' + r.status);
  return (await r.json()).map(function (x) { return x.result; });
};
exports.ip = function (req) {
  return String(req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || 'x').split(',')[0].trim();
};
exports.body = function (req) {
  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch (e) { b = {}; } }
  return b || {};
};
exports.wib = function () { // tanggal hari ini di WIB, YYYYMMDD
  return new Date(Date.now() + 7 * 36e5).toISOString().slice(0, 10).replace(/-/g, '');
};
