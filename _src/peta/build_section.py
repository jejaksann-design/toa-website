import json, re
D = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/'
geo = json.load(open(D + 'peta/geo/indonesia-province-simple.json'))
data = json.load(open(D + 'peta/data.json'))
NAME = {'BALI': 'Bali', 'BANGKA BELITUNG': 'Bangka Belitung', 'BENGKULU': 'Bengkulu', 'DAERAH ISTIMEWA YOGYAKARTA': 'DI Yogyakarta', 'DI. ACEH': 'Aceh',
        'DKI JAKARTA': 'DKI Jakarta', 'GORONTALO': 'Gorontalo', 'IRIAN JAYA BARAT': 'Papua Barat', 'IRIAN JAYA TENGAH': 'Papua', 'IRIAN JAYA TIMUR': 'Papua',
        'JAMBI': 'Jambi', 'JAWA BARAT': 'Jawa Barat', 'JAWA TENGAH': 'Jawa Tengah', 'JAWA TIMUR': 'Jawa Timur', 'KALIMANTAN BARAT': 'Kalimantan Barat',
        'KALIMANTAN SELATAN': 'Kalimantan Selatan', 'KALIMANTAN TENGAH': 'Kalimantan Tengah', 'KALIMANTAN TIMUR': 'Kalimantan Timur', 'LAMPUNG': 'Lampung',
        'MALUKU': 'Maluku', 'MALUKU UTARA': 'Maluku Utara', 'NUSA TENGGARA TIMUR': 'Nusa Tenggara Timur', 'NUSATENGGARA BARAT': 'Nusa Tenggara Barat',
        'PROBANTEN': 'Banten', 'RIAU': 'Riau', 'SULAWESI SELATAN': 'Sulawesi Selatan', 'SULAWESI TENGAH': 'Sulawesi Tengah', 'SULAWESI TENGGARA': 'Sulawesi Tenggara',
        'SULAWESI UTARA': 'Sulawesi Utara', 'SUMATERA BARAT': 'Sumatera Barat', 'SUMATERA SELATAN': 'Sumatera Selatan', 'SUMATERA UTARA': 'Sumatera Utara'}
LON0, LON1, LAT0, LAT1, W = 94.8, 141.2, 6.2, -11.2, 1000
H = round((LAT0 - LAT1) / (LON1 - LON0) * W)
def pr(lon, lat): return ((lon - LON0) / (LON1 - LON0) * W, (LAT0 - lat) / (LAT0 - LAT1) * H)
def area(pts):
    return abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2
paths = []
for f in geo['features']:
    k = f['properties']['Propinsi']; g = f['geometry']
    polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    d = []
    for poly in polys:
        ring = [pr(x, y) for x, y in poly[0]]
        if area(ring) < 1.2: continue
        out = []; last = None
        for x, y in ring:
            q = (round(x, 1), round(y, 1))
            if last and abs(q[0] - last[0]) + abs(q[1] - last[1]) < 0.8: continue
            out.append(q); last = q
        if len(out) < 3: continue
        d.append('M' + 'L'.join('%g %g' % p for p in out) + 'Z')
    paths.append((k, ''.join(d)))
prov = data['prov']
def lvl(n): return 0 if n == 0 else 1 if n < 10 else 2 if n < 30 else 3 if n < 80 else 4
svg = ''.join('<path class="pv l%d" data-k="%s" d="%s"><title>%s: %d santri</title></path>' % (lvl(prov.get(k, 0)), k, d, NAME[k], prov.get(k, 0)) for k, d in paths)
INFO = {k: {'n': NAME[k], 'c': prov.get(k, 0), 'cities': data['provCities'].get(k, [])[:6]} for k, _ in paths}
# merge Papua parts for display
nprov = len({NAME[k] for k in prov})
REGION = set(data['region'])
ncity = len([c for c, _ in data['cities'] if c not in REGION])
top = data['cities'][:10]; mx = top[0][1]
bars = ''.join('<div class="pt-row"><span class="pt-c">%s</span><span class="pt-bar"><i style="width:%.1f%%"></i></span><b>%d</b></div>' % (c, n / mx * 100, n) for c, n in top)
abroad = ', '.join(a for a, _ in data['abroad'])
sec = '''<!-- PETA:START -->
  <section id="peta">
<style>
:root{--m0:#E4EAE1;--m1:#CBE2C1;--m2:#97C786;--m3:#5A9A48;--m4:#2F6A23}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--m0:#1D2920;--m1:#28462B;--m2:#3D7537;--m3:#69AB58;--m4:#A6DA94}}
:root[data-theme="dark"]{--m0:#1D2920;--m1:#28462B;--m2:#3D7537;--m3:#69AB58;--m4:#A6DA94}
.pt-stats{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
.pt-stats div{grid-column:span 2}
.pt-stats div.hl{grid-column:span 3;background:var(--gold-soft);border-color:var(--gold)}
.pt-stats div{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:12px 8px;display:flex;flex-direction:column;text-align:center}
.pt-stats b{font-family:var(--display);font-weight:400;font-size:2rem;line-height:1.05;font-variant-numeric:tabular-nums}
.pt-stats span{font-size:.78rem;color:var(--muted);line-height:1.3}
@media (max-width:480px){.pt-stats div,.pt-stats div.hl{grid-column:span 3}.pt-stats div:last-child{grid-column:1/-1}}
.pt-map{position:relative;background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:12px}
.pt-map svg{width:100%;height:auto;display:block}
.pv{stroke:var(--paper);stroke-width:.8;stroke-linejoin:round;cursor:pointer;transition:opacity .15s}
.pv.l0{fill:var(--m0)}.pv.l1{fill:var(--m1)}.pv.l2{fill:var(--m2)}.pv.l3{fill:var(--m3)}.pv.l4{fill:var(--m4)}
.pt-map svg:hover .pv:not(:hover){opacity:.75}
.pv.on{stroke:var(--gold);stroke-width:2.2}
.pt-leg{display:flex;flex-wrap:wrap;gap:12px;align-items:center;font-size:.8rem;color:var(--muted);margin-top:8px}
.pt-leg span{display:inline-flex;align-items:center;gap:5px}
.pt-leg i{width:14px;height:14px;border-radius:4px;display:inline-block}
.pt-tip{background:var(--green-soft);border-radius:12px;padding:12px 14px;font-size:.92rem;min-height:3.2em}
.pt-tip b{display:block}
.pt-abroad{display:inline-flex;align-items:center;gap:8px;background:var(--gold-soft);border-radius:999px;padding:6px 14px;font-size:.88rem;font-weight:600;align-self:flex-start}
.pt-rows{display:flex;flex-direction:column;gap:8px}
.pt-row{display:grid;grid-template-columns:8.5rem 1fr 2rem;gap:10px;align-items:center;font-size:.9rem}
.pt-c{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pt-bar{height:10px;background:var(--line);border-radius:999px;overflow:hidden}
.pt-bar i{display:block;height:100%;background:var(--m3);border-radius:0 4px 4px 0}
.pt-row b{font-variant-numeric:tabular-nums;text-align:right}
</style>
    <span class="eyebrow">Peta Santri TOA</span>
    <h2>Dari Aceh sampai Papua, hingga Jepang, Inggris, dan Selandia Baru.</h2>
    <p class="lead">Setiap hari, santri TOA menyetor hafalan dari rumahnya masing-masing. Tap provinsi untuk melihat kotanya.</p>
    <div class="pt-stats"><div class="hl"><b>±30.000</b><span>peserta halaqah sejak TO1</span></div><div class="hl"><b>4.000+</b><span>santri</span></div><div><b>%(nc)d</b><span>kota/kabupaten</span></div><div><b>%(np)d</b><span>provinsi</span></div><div><b>%(nn)d</b><span>negara</span></div></div>
    <p style="font-size:.84rem;color:var(--muted)">Peserta dihitung per periode (satu santri yang ikut 10 periode terhitung 10 kali), santri dihitung per orang. Keduanya perkiraan untuk program halaqah Tahfidz Online: %(n)s santri dan 8.303 peserta tercatat di arsip TO54–TO98, Untuk periode yang arsipnya sudah tidak ada, peserta diperkirakan dari catatan pengurus (TO1–20 sekitar 400–500 per periode, TO21–50 sekitar 300–500), dan santri dari porsi santri baru per periode di arsip. Peta di bawah memakai data domisili yang tercatat saja.</p>
    <div class="pt-map">
      <svg viewBox="0 0 %(w)d %(h)d" role="img" aria-label="Peta sebaran santri TOA per provinsi">%(svg)s</svg>
      <div class="pt-leg"><span><i style="background:var(--m0)"></i>0</span><span><i style="background:var(--m1)"></i>1–9</span><span><i style="background:var(--m2)"></i>10–29</span><span><i style="background:var(--m3)"></i>30–79</span><span><i style="background:var(--m4)"></i>80+ santri</span></div>
    </div>
    <div class="pt-tip" id="pt-tip" aria-live="polite"><b>Tap salah satu provinsi</b><span style="color:var(--muted)">Jawa Barat paling banyak, disusul Jawa Tengah dan Jawa Timur.</span></div>
    <span class="pt-abroad">🌏 Juga dari luar negeri: %(abroad)s</span>
    <p style="font-weight:600">Kota dengan santri terbanyak</p>
    <div class="pt-rows">%(bars)s</div>
    <p style="font-size:.8rem;color:var(--muted)">Data santri halaqah TO54–TO98 dan registrasi ulang TO99, MO55, TOSP48, dan TOK46 yang mencantumkan domisili. Santri yang pernah pindah domisili tercatat di setiap tempatnya.</p>
<script>
(function(){
var INFO=%(info)s;
var tip=document.getElementById('pt-tip'),svg=document.querySelector('#peta svg');
svg.querySelectorAll('.pv').forEach(function(p){p.addEventListener('click',function(){
  svg.querySelectorAll('.pv.on').forEach(function(x){x.classList.remove('on')});p.classList.add('on');
  var i=INFO[p.dataset.k];tip.textContent='';var b=document.createElement('b');b.textContent=i.n+' · '+i.c+' santri';tip.appendChild(b);
  var s=document.createElement('span');s.style.color='var(--muted)';s.textContent=i.c?i.cities.map(function(c){return c[0]+' ('+c[1]+')'}).join(', '):'Belum ada santri dari provinsi ini. Jadilah yang pertama!';tip.appendChild(s);
})});
})();
</script>
  </section>

<!-- PETA:END -->
'''
VALS = {'n': '{:,}'.format(data['total']).replace(',', '.'), 'nc': ncity, 'np': nprov, 'nn': 1 + len(data['abroad']), 'w': W, 'h': H, 'svg': svg, 'abroad': abroad, 'bars': bars,
       'info': json.dumps(INFO, ensure_ascii=False)}
sec = re.sub(r'%\((\w+)\)[ds]', lambda m: str(VALS[m.group(1)]), sec)
LAND = D + 'artifact-files/90432943-d62f-45ed-a698-3bf019ceffc4/index.html'
s = open(LAND).read()
if '<!-- PETA:START -->' in s:
    s = re.sub(r'<!-- PETA:START -->.*?<!-- PETA:END -->\n', lambda m: sec, s, flags=re.S)
else:
    i = s.index('<section id="testimoni"'); j = s.index('</section>\n', i) + len('</section>\n')
    s = s[:j] + '\n' + sec + s[j:]
open(LAND, 'w').write(s)
print('svg KB', len(svg) // 1024, 'H', H, 'nprov', nprov, 'ncity', ncity)
for i, js in enumerate(re.findall(r'<script>(.*?)</script>', s, re.S)):
    open(D + 'peta/c%d.js' % i, 'w').write(js)
