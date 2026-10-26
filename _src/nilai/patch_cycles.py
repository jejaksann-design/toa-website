p = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/nilai/lb-section.html'
s = open(p).read()
rep = [
    ("var SIKLUS=__SIKLUS__;", "var CYCLES=__CYCLES__;\nvar SIKLUS=[].concat.apply([],CYCLES);"),
    (r"function key(d){return d.g+'|'+d.nama.toLowerCase().replace(/^h\.\s*/,'').replace(/\s+/g,' ').trim()}",
     r"function key(d){return d.g+'|'+d.nama.toLowerCase().replace(/^h\.\s*/,'').replace(/[^a-z]/g,'')}"),
    ("  var A=E('lb-acc');A.textContent='';var have=SIKLUS.filter(function(p){return DATA[p]});",
     "  var C=CYCLES.filter(function(c){return c.indexOf(st.per)>-1})[0];\n  var A=E('lb-acc');A.textContent='';var have=C.filter(function(p){return DATA[p]});"),
    ("  SIKLUS.forEach(function(p){var x=document.createElement('span');", "  C.forEach(function(p){var x=document.createElement('span');"),
    ("  if(have.length<SIKLUS.length){", "  if(have.length<C.length){"),
    ("SIKLUS[SIKLUS.length-1]", "C[C.length-1]"),
    ("rata-rata nilai akhir '+SIKLUS.join(', ')", "rata-rata nilai akhir '+C.join(', ')"),
    ("  var M={};SIKLUS.forEach(function(p){", "  var M={};C.forEach(function(p){"),
    ("return x.n.length===SIKLUS.length", "return x.n.length===C.length"),
]
for a, b in rep:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
assert 'SIKLUS.length' not in s and 'SIKLUS[' not in s
open(p, 'w').write(s)

# standalone page shell sharing the landing page's look
L = open('/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/artifact-files/90432943-d62f-45ed-a698-3bf019ceffc4/index.html').read()
import re
style = re.findall(r'<style>\n/\* Layout.*?</style>', L, re.S)[0]
brand = re.findall(r'<div class="brand">.*?</div>\n    </div>', L, re.S)[0]
shell = ('<title>Nilai Santri TOA</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
         '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Amiri:wght@400;700&display=swap">\n'
         + style + '\n<div class="wrap">\n  <header>\n    ' + brand + '\n  </header>\n'
         '<!-- PRESTASI:START -->\n<!-- PRESTASI:END -->\n'
         '  <footer>Tahfidz Online Academy · Bobot nilai: Setoran 30% · Adab &amp; Keaktifan 50% · Imtihan Akbar 20%</footer>\n</div>\n')
open('/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/nilai/nilai-to98.html', 'w').write(shell)
print('patched')
