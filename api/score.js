// GET  /api/score?b=all|sambung|tajwid|wawasan&me=<pid>&n=20  -> klasemen n besar (maks 50) (+ posisi saya)
// POST /api/score {tok,pid,name,score}                     -> tambah poin
const kv = require('./_kv');
const BOARDS = ['all', 'sambung', 'tajwid', 'wawasan'];
const MAXS = { sambung: 10, tajwid: 10, wawasan: 10, daily: 3 };
const MINMS = { sambung: 15000, tajwid: 15000, wawasan: 15000, daily: 6000 };
const BAD = /(anjing|anjg|babi|bangsat|bajingan|kontol|kntl|memek|ngentot|ngewe|goblok|tolol|jancok|jancuk|asu\b|tai\b|fuck|shit|bitch|porn|sex|http|www\.|\.com)/i;
function cleanName(s) {
  s = String(s || '').replace(/[\u0000-\u001f<>]/g, '').replace(/\s+/g, ' ').trim().slice(0, 20);
  if (s.length < 2 || !/^[\p{L}\p{M}0-9 .'\-]+$/u.test(s) || BAD.test(s)) return null;
  return s;
}
async function board(b, me, n) {
  n = Math.max(1, Math.min(50, n || 20));
  const k = 'lb:' + b;
  const cmds = [['ZREVRANGE', k, 0, n - 1, 'WITHSCORES'], ['ZCARD', k]];
  if (me) cmds.push(['ZREVRANK', k, me], ['ZSCORE', k, me]);
  const r = await kv.pipe(cmds);
  const flat = r[0] || [], ids = [], pts = [];
  for (let i = 0; i < flat.length; i += 2) { ids.push(flat[i]); pts.push(+flat[i + 1]); }
  const names = ids.length ? (await kv.pipe([['HMGET', 'names'].concat(ids)]))[0] : [];
  const out = { b: b, n: +r[1] || 0, top: ids.map(function (id, i) { return { name: names[i] || 'Santri', pts: pts[i], me: id === me }; }) };
  if (me && r[2] !== null && r[2] !== undefined) out.mine = { rank: +r[2] + 1, pts: +r[3] };
  return out;
}
module.exports = async function (req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!kv.ready) return res.status(200).json({ off: true });
  try {
    if (req.method === 'GET') {
      const b = BOARDS.indexOf(req.query.b) >= 0 ? req.query.b : 'all';
      const me = /^[a-f0-9]{8,32}$/.test(req.query.me || '') ? req.query.me : null;
      return res.status(200).json(await board(b, me, parseInt(req.query.n, 10)));
    }
    if (req.method !== 'POST') return res.status(405).end();
    const p = kv.body(req);
    const pid = /^[a-f0-9]{8,32}$/.test(p.pid || '') ? p.pid : null;
    const name = cleanName(p.name);
    if (!pid) return res.status(400).json({ err: 'pid' });
    if (!name) return res.status(400).json({ err: 'name' });
    const ip = kv.ip(req);
    const [rd, rl] = await kv.pipe([['GETDEL', 'rd:' + String(p.tok || '').slice(0, 40)], ['SET', 'rl:' + ip, 1, 'EX', 5, 'NX']]);
    if (!rd) return res.status(400).json({ err: 'tok' });
    if (rl !== 'OK') return res.status(429).json({ err: 'slow' });
    const mode = rd.split('|')[0], t0 = +rd.split('|')[1];
    if (Date.now() - t0 < MINMS[mode]) return res.status(400).json({ err: 'fast' });
    const sc = Math.max(0, Math.min(MAXS[mode], parseInt(p.score, 10) || 0));
    if (mode === 'daily') {
      const once = await kv.pipe([['SET', 'dly:' + pid + ':' + kv.wib(), 1, 'EX', 172800, 'NX']]);
      if (once[0] !== 'OK') return res.status(200).json(await board('all', pid));
    }
    const cmds = [['HSET', 'names', pid, name], ['ZINCRBY', 'lb:all', sc, pid]];
    if (mode !== 'daily') cmds.push(['ZINCRBY', 'lb:' + mode, sc, pid]);
    await kv.pipe(cmds);
    res.status(200).json(await board(mode === 'daily' ? 'all' : mode, pid));
  } catch (e) { res.status(200).json({ off: true }); }
};
