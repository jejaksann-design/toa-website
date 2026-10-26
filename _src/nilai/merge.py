"""Inject leaderboard (all periods in data/) into the landing page and the standalone page."""
import json, re, glob, os
D = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/'
N = D + 'nilai/'
CYCLES = [["TO54", "TO55", "TO56"], ["TO57", "TO58", "TO59"], ["TO60", "TO61", "TO62"], ["TO63", "TO64", "TO65"], ["TO66", "TO67", "TO68"], ["TO69", "TO70", "TO71"], ["TO72", "TO73", "TO74"], ["TO75", "TO76", "TO77"], ["TO78", "TO79", "TO80"], ["TO81", "TO82", "TO83"], ["TO84", "TO85", "TO86"], ["TO87", "TO88", "TO89"], ["TO90", "TO91", "TO92"], ["TO93", "TO94"], ["TO95", "TO96", "TO97"], ["TO98", "TO99", "TO100"]]
DATA = {os.path.basename(f)[:-5]: json.load(open(f)) for f in sorted(glob.glob(N + 'data/*.json'))}
AL = json.load(open(N + 'aliases.json'))
for rows in DATA.values():
    for r in rows:
        r['nama'] = AL[r['g']].get(r['nama'], r['nama'])
sec = open(N + 'lb-section.html').read() \
    .replace('__CYCLES__', json.dumps(CYCLES))
DATA = {k: DATA[k] for k in sorted(DATA, key=lambda p: int(p[2:]))}
json.dump(DATA, open(N + 'prestasi.json', 'w'), ensure_ascii=False, separators=(',', ':'))
block = '<!-- PRESTASI:START -->\n' + sec + '<!-- PRESTASI:END -->\n'
LAND = D + 'artifact-files/90432943-d62f-45ed-a698-3bf019ceffc4/index.html'
STAND = N + 'nilai-to98.html'
for path in (LAND, STAND):
    s = open(path).read()
    s = re.sub(r'<!-- PRESTASI:START -->.*?<!-- PRESTASI:END -->\n', lambda m: block, s, flags=re.S)
    open(path, 'w').write(s)
    for i, js in enumerate(re.findall(r'<script>(.*?)</script>', s, re.S)):
        open(f'{N}chk_{os.path.basename(path)}_{i}.js', 'w').write(js)
print('merged', sorted(DATA))
