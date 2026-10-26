import re, json
D = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/'
STORE = 'https://lynk.id/academytahfidzonline'
BOOKS = [
    {"id": "pergi-ke-mana", "u": "https://lynk.id/academytahfidzonline/1vzgnnlev4ye", "t": "Pergi ke Mana Hafalanku Dulu?", "s": "Renungan & tips buat balikin hafalanmu lagi."},
    {"id": "merawat-hafalanmu", "u": "https://lynk.id/academytahfidzonline/7vx5z4zq3z52", "t": "Trik & Hack Merawat Hafalanmu", "s": "Panduan murajaah bagi orang sibuk."},
    {"id": "murajaah-planner", "u": "https://lynk.id/academytahfidzonline/kxdqnk240y6g", "t": "Murajaah Planner", "s": "Workbook evaluasi untuk memetakan, merawat, dan memantau hafalan Al-Qur'anmu."},
    {"id": "pernah-penghafal", "u": "https://lynk.id/academytahfidzonline/72ge115nvd7m", "t": "Aku Pernah Menjadi Penghafal Al-Qur'an", "s": "Renungan untuk yang pernah dekat dengan hafalan, lalu merasa jauh darinya."},
    {"id": "menemani-si-kecil", "u": "https://lynk.id/academytahfidzonline/jql3ywr9w4ek", "t": "Menemani Si Kecil Menghafal Al-Qur'an dari Rumah", "s": "Tips mendampingi anak menghafal Al-Qur'an sejak dini."},
]

# ---------- Landing page: e-book shelf ----------
LAND = D + 'artifact-files/90432943-d62f-45ed-a698-3bf019ceffc4/index.html'
s = open(LAND).read()
cards = ''.join(
    f'<a class="eb" href="{b["u"]}" target="_blank" rel="noopener"><img src="img/{b["id"]}.jpg" alt="Sampul e-book {b["t"]}" loading="lazy" width="640" height="640"><b>{b["t"]}</b><span>{b["s"]}</span></a>'
    for b in BOOKS)
shelf = f'''<!-- EBOOK:START -->
  <section id="ebook">
<style>
.shelf{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}}
.eb{{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:var(--ink);min-width:0}}
.eb img{{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;border-radius:14px;background:var(--paper);transition:transform .2s}}
.eb:hover img{{transform:translateY(-3px)}}
.eb b{{font-weight:600;font-size:.95rem;line-height:1.3}}
.eb span{{font-size:.84rem;color:var(--muted);line-height:1.4}}
.eb:focus-visible{{outline:3px solid var(--gold);outline-offset:3px;border-radius:14px}}
@media (prefers-reduced-motion:reduce){{.eb img{{transition:none}}}}
</style>
    <span class="eyebrow">E-book TOA</span>
    <h2>Teman belajar di luar halaqah.</h2>
    <p class="lead">Ditulis oleh Ustadz San Malique dari pengalaman lebih dari 10 tahun membersamai para penghafal di TOA.</p>
    <div class="shelf">{cards}</div>
    <div><a class="btn ghost" href="{STORE}" target="_blank" rel="noopener">Lihat semua di Lynk</a></div>
  </section>

<!-- EBOOK:END -->
'''
if '<!-- EBOOK:START -->' in s:
    s = re.sub(r'<!-- EBOOK:START -->.*?<!-- EBOOK:END -->\n', lambda m: shelf, s, flags=re.S)
else:
    assert s.count('  <section id="kuis">') == 1
    s = s.replace('  <section id="kuis">', shelf + '  <section id="kuis">')
open(LAND, 'w').write(s)

# ---------- Quiz: real covers + score-based pick + other titles ----------
QT = D + 'quran/kuis-template.html'
q = open(QT).read()
q = re.sub(r'    <div class="ebook">.*?\n    </div>\n    <div class="cta">',
           '''    <div class="ebook">
      <img class="cv" id="eb-img" src="img/pergi-ke-mana.jpg" alt="" width="640" height="640">
      <div class="tx">
        <span class="eyebrow">E-book TOA · Ustadz San Malique</span>
        <b class="h" id="eb-h"></b>
        <p id="eb-p"></p>
        <div><a class="btn" href="https://lynk.id/academytahfidzonline" target="_blank" rel="noopener" id="eb-a">Lihat e-book di Lynk</a></div>
      </div>
      <div class="more"><span>E-book TOA lainnya</span><div id="eb-more"></div></div>
    </div>
    <div class="cta">''', q, flags=re.S)
q = re.sub(r'\.ebook \.cv\{.*?\n\.ebook \.cv span\{[^\n]*\n',
           '.ebook .cv{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;border-radius:10px}\n'
           '.ebook .more{grid-column:1/-1;display:flex;flex-direction:column;gap:8px;border-top:1px dashed var(--line);padding-top:12px}\n'
           '.ebook .more>span{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:600}\n'
           '#eb-more{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}\n'
           '#eb-more a{display:block;border-radius:8px;overflow:hidden}\n#eb-more img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;display:block}\n'
           '#eb-more a:focus-visible{outline:3px solid var(--gold);outline-offset:2px}\n', q, flags=re.S)
q = q.replace('.ebook{background:var(--paper);border:1.5px solid var(--gold);border-radius:18px;padding:20px;display:grid;grid-template-columns:84px 1fr;',
              '.ebook{background:var(--paper);border:1.5px solid var(--gold);border-radius:18px;padding:20px;display:grid;grid-template-columns:110px 1fr;')
q = q.replace('@media (max-width:380px){.ebook{grid-template-columns:1fr}.ebook .cv{width:84px}}',
              '@media (max-width:380px){.ebook{grid-template-columns:1fr}.ebook .cv{width:140px}}')
old_js = re.findall(r"  var eb=s>=9\?.*?E\('eb-h'\)\.textContent=eb\[0\];E\('eb-p'\)\.innerHTML=eb\[1\];", q, re.S)
if old_js:
  pass
new_js = """  var B=__BOOKS__;
  var pick=s>=9?['murajaah-planner','Jaga yang sudah kamu raih','Hafalan yang lancar hari ini tetap butuh dirawat. Workbook <i>Murajaah Planner</i> membantumu memetakan, merawat, dan memantau hafalan secara rutin.']:
           s>=5?['merawat-hafalanmu','Biar hafalanmu nggak cuma lancar hari ini','Sibuk tapi tetap ingin hafalan terjaga? <i>Trik & Hack Merawat Hafalanmu</i> adalah panduan murajaah untuk orang sibuk.']:
                ['pergi-ke-mana','Hafalan sering hilang di tengah jalan?','Kamu nggak sendirian. <i>Pergi ke Mana Hafalanku Dulu?</i> berisi renungan dan tips buat balikin hafalanmu lagi.'];
  var main=B.filter(function(b){return b.id===pick[0]})[0];
  E('eb-img').src='img/'+main.id+'.jpg';E('eb-img').alt='Sampul e-book '+main.t;
  E('eb-h').textContent=pick[1];E('eb-p').innerHTML=pick[2];
  var M=E('eb-more');M.textContent='';
  B.filter(function(b){return b.id!==main.id}).forEach(function(b){var a=document.createElement('a');a.href='https://lynk.id/academytahfidzonline';a.target='_blank';a.rel='noopener';a.title=b.t;
    var im=document.createElement('img');im.src='img/'+b.id+'.jpg';im.alt='Sampul e-book '+b.t;im.loading='lazy';a.appendChild(im);M.appendChild(a)});"""
if old_js: q = q.replace(old_js[0], new_js)
q = q.replace("E('eb-h').textContent=pick[1];", "E('eb-a').href=main.u;E('eb-h').textContent=pick[1];") if "E('eb-a').href=main.u" not in q else q
q = q.replace("a.href='https://lynk.id/academytahfidzonline';a.target", "a.href=b.u;a.target")
open(QT, 'w').write(q)
bank = json.load(open(D + 'quran/bank.json'))
h = q.replace('__BANK__', json.dumps(bank, ensure_ascii=False, separators=(',', ':'))) \
     .replace('__LANDING__', 'https://claude.ai/artifact/JpDjVg5i55kfnZjvr6L69R') \
     .replace('__BOOKS__', json.dumps(BOOKS, ensure_ascii=False)) \
     .replace('__PAGES__', open(D + 'quran/pages.json').read())
open(D + 'quran/kuis.html', 'w').write(h)
for name, txt in (('land', s), ('kuis', h)):
    for i, js in enumerate(re.findall(r'<script>(.*?)</script>', txt, re.S)):
        open(f'{D}ebook/{name}{i}.js', 'w').write(js)
print('ok')
