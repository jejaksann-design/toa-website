"""Build a self-hostable TOA website folder (for GitHub -> Vercel) from the published artifact sources.
Usage: python3 build_site.py  -> writes ./toa-website/ and ./toa-website.zip
"""
import os, re, shutil, json
D = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/'
OUT = D + 'site/toa-website/'
LAND_SRC = D + 'artifact-files/90432943-d62f-45ed-a698-3bf019ceffc4/index.html'
KUIS_SRC = D + 'quran/kuis.html'
LAND_URL = 'https://claude.ai/artifact/JpDjVg5i55kfnZjvr6L69R'
KUIS_URL = 'https://claude.ai/artifact/BJWsb8L2PHZ9uoQfeV5r16'

HEAD = ('<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="{desc}">\n'
        '<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n'
        '<meta property="og:image" content="/img/logo-512.png">\n<meta name="theme-color" content="#2F6A23">\n'
        '<link rel="icon" type="image/png" href="/img/logo-160.png">\n<link rel="apple-touch-icon" href="/img/logo-512.png">\n'
        '<style>:root{{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}'
        'body{{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>\n'
        '</head>\n<body>\n')

def body_of(path):
    s = open(path).read()
    if s.lstrip().lower().startswith('<!doctype'):
        s = s.split('<body>', 1)[1]
        s = s.rsplit('</body>', 1)[0]
    return s

def page(body, title, desc):
    body = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', '', body)
    return HEAD.format(title=title, desc=desc) + body + '\n</body>\n</html>\n'

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT + 'kuis', exist_ok=True); os.makedirs(OUT + 'img', exist_ok=True)

# ---------- landing ----------
land = body_of(LAND_SRC)
land = land.replace(KUIS_URL + '#tes', '/kuis/#tes').replace(KUIS_URL, '/kuis/')
# links to the quiz now open in the same site, not a new tab
land = re.sub(r'(href="/kuis/[^"]*")\s+target="_blank"\s+rel="noopener"', r'\1', land)
# syahadah download: plain browser download instead of the Claude downloads capability
old_dl = re.search(r"var DL=null;try\{window\.claude.*?\}catch\(e\)\{\}", land).group(0)
land = land.replace(old_dl, "var DL={save:function(o){return new Promise(function(res){var a=document.createElement('a');a.href=URL.createObjectURL(o.data);a.download=o.filename;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},1500);res({status:'saved'})})}};")
assert 'window.claude' not in land, 'landing still references window.claude'
desc_l = 'Tahfidz Online Academy: menghafal Al-Qur\'an dari mana saja, bersama halaqah dan musyrif/musyrifah. Program, pendaftaran, prestasi santri, dan e-book.'
open(OUT + 'index.html', 'w').write(page(land, 'Tahfidz Online Academy', desc_l))

# ---------- kuis ----------
kuis = body_of(KUIS_SRC)
kuis = kuis.replace(LAND_URL + '#program', '/#program').replace(LAND_URL, '/')
kuis = re.sub(r'(href="/(?:#program)?")\s+target="_blank"\s+rel="noopener"', r'\1', kuis)
kuis = kuis.replace("fetch('quran.json')", "fetch('/kuis/quran.json')")
kuis = kuis.replace('src="img/', 'src="/img/').replace("'img/'+", "'/img/'+")
assert 'claude.ai/artifact' not in kuis
desc_k = 'Kuis TOA: Ayat Hari Ini, Sambung Ayat juz 1–30, Tajwid & Tahsin, Wawasan Keislaman, Tes Penempatan Program, dan Jadwal Murajaah Pintar.'
open(OUT + 'kuis/index.html', 'w').write(page(kuis, 'Kuis TOA', desc_k))

# landing also references img/ relatively — make absolute so it works from any path
s = open(OUT + 'index.html').read().replace('src="img/', 'src="/img/')
s = s.replace("fetch('prestasi.json')", "fetch('/prestasi.json')")
open(OUT + 'index.html', 'w').write(s)

# ---------- data & images ----------
shutil.copy(D + 'nilai/prestasi.json', OUT + 'prestasi.json')
shutil.copy(D + 'quran/quran.json', OUT + 'kuis/quran.json')
for f in os.listdir(D + 'ebook'):
    if f.endswith('.jpg'): shutil.copy(D + 'ebook/' + f, OUT + 'img/' + f)
for n in (160, 512): shutil.copy(D + 'logo/logo-%d.png' % n, OUT + 'img/logo-%d.png' % n)

# ---------- hosting config & docs ----------
json.dump({"cleanUrls": True, "trailingSlash": True,
           "headers": [{"source": "/(.*)\\.json", "headers": [{"key": "Cache-Control", "value": "public, max-age=300"}]},
                       {"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]}]},
          open(OUT + 'vercel.json', 'w'), indent=2)
open(OUT + 'README.md', 'w').write('''# Website Tahfidz Online Academy

Website statis (tanpa build). Deploy ke Vercel dari repo GitHub ini.

- `/` landing page: program, pendaftaran, testimoni, e-book, Prestasi Santri, syahadah, Peta Santri
- `/kuis/` Kuis TOA: Ayat Hari Ini, Tes Penempatan, Sambung Ayat, Tajwid, Wawasan, Jadwal Murajaah
- `prestasi.json` data nilai santri yang lulus (diperbarui tiap akhir periode)
- `kuis/quran.json` teks Al-Qur'an Utsmani dari Tanzil (CC BY 3.0, tanpa perubahan)

Pengaturan Vercel: Framework Preset "Other", Build Command kosong, Output Directory kosong (root).
''')
open(OUT + 'robots.txt', 'w').write('User-agent: *\nAllow: /\n')
shutil.make_archive(D + 'site/toa-website', 'zip', OUT)
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print('built', OUT, round(tot / 1e6, 2), 'MB')
for r, _, fs in os.walk(OUT):
    for f in sorted(fs): print(' ', os.path.relpath(os.path.join(r, f), OUT))
