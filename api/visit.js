const kv = require('./_kv');
module.exports = async function (req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!kv.ready) return res.status(200).json({ off: true });
  try {
    const d = 'v:d:' + kv.wib();
    let r;
    if (req.method === 'POST') r = await kv.pipe([['INCR', 'v:total'], ['INCR', d], ['EXPIRE', d, 259200]]);
    else r = await kv.pipe([['GET', 'v:total'], ['GET', d]]);
    res.status(200).json({ total: +r[0] || 0, today: +r[1] || 0 });
  } catch (e) { res.status(200).json({ off: true }); }
};
