import os
import openpyxl, glob, re, json, collections
from places2 import lookup
U = '/mnt/user-data/attachments/0e4dbd05-0425-5a72-883f-583c558b89ff/'
AL = json.load(open('/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/nilai/aliases.json'))

# normalized domicile -> (display city, province key in GeoJSON | None, country)
JB, JT, JI, DKI, BT = 'JAWA BARAT', 'JAWA TENGAH', 'JAWA TIMUR', 'DKI JAKARTA', 'PROBANTEN'
M = {
 'karawang': ('Karawang', JB), 'bekasi': ('Bekasi', JB), 'kota bekasi': ('Bekasi', JB), 'bekas': ('Bekasi', JB),
 'bogor': ('Bogor', JB), 'kab bogor': ('Bogor', JB), 'kab. bogor': ('Bogor', JB), 'kabupaten bogor': ('Bogor', JB),
 'jonggol - bogor': ('Bogor', JB), 'jonggol-bogor': ('Bogor', JB), 'jonggol bogor': ('Bogor', JB), 'cibinong kab. bogor': ('Bogor', JB), 'cibinong, bogor': ('Bogor', JB),
 'pekanbaru': ('Pekanbaru', 'RIAU'), 'riau': ('Riau', 'RIAU'), 'kampar': ('Kampar', 'RIAU'), 'bagansiapiapi': ('Bagansiapiapi', 'RIAU'),
 'jakarta': ('Jakarta', DKI), 'jakarta timur': ('Jakarta', DKI), 'jakarta selatan': ('Jakarta', DKI), 'jakarta barat': ('Jakarta', DKI),
 'tangerang': ('Tangerang', BT), 'tangerang selatan': ('Tangerang Selatan', BT), 'tangsel': ('Tangerang Selatan', BT),
 'bandar lampung': ('Bandar Lampung', 'LAMPUNG'), 'bandarlampung': ('Bandar Lampung', 'LAMPUNG'), 'kota bandar lampung': ('Bandar Lampung', 'LAMPUNG'), 'lampung': ('Lampung', 'LAMPUNG'),
 'depok': ('Depok', JB), 'garut': ('Garut', JB), 'tasikmalaya': ('Tasikmalaya', JB), 'ciamis': ('Ciamis', JB), 'bandung': ('Bandung', JB), 'cimahi': ('Cimahi', JB),
 'cirebon': ('Cirebon', JB), 'cirebon, kab.': ('Cirebon', JB), 'sukabumi': ('Sukabumi', JB), 'kota sukabumi': ('Sukabumi', JB), 'kab. sukabumi': ('Sukabumi', JB),
 'yogyakarta': ('Yogyakarta', 'DAERAH ISTIMEWA YOGYAKARTA'), 'jogjakarta': ('Yogyakarta', 'DAERAH ISTIMEWA YOGYAKARTA'), 'gunungkidul': ('Gunungkidul', 'DAERAH ISTIMEWA YOGYAKARTA'),
 'semarang': ('Semarang', JT), 'rembang': ('Rembang', JT), 'salatiga': ('Salatiga', JT), 'wonogiri': ('Wonogiri', JT), 'boyolali': ('Boyolali', JT), 'magelang': ('Magelang', JT),
 'karanganyar': ('Karanganyar', JT), 'batang': ('Batang', JT), 'pati': ('Pati', JT), 'solo': ('Surakarta', JT), 'temanggung': ('Temanggung', JT),
 'sidoarjo': ('Sidoarjo', JI), 'jember': ('Jember', JI), 'pasuruan': ('Pasuruan', JI), 'probolinggo': ('Probolinggo', JI), 'jombang': ('Jombang', JI), 'surabaya': ('Surabaya', JI),
 'malang': ('Malang', JI), 'kota malang': ('Malang', JI), 'lamongan': ('Lamongan', JI), 'pamekasan': ('Pamekasan', JI), 'kediri': ('Kediri', JI), 'mojokerto': ('Mojokerto', JI), 'ponorogo': ('Ponorogo', JI),
 'padang': ('Padang', 'SUMATERA BARAT'), 'palembang': ('Palembang', 'SUMATERA SELATAN'), 'pagar alam': ('Pagar Alam', 'SUMATERA SELATAN'), 'baturaja': ('Baturaja', 'SUMATERA SELATAN'),
 'oku/baturaja': ('Baturaja', 'SUMATERA SELATAN'), 'lahat': ('Lahat', 'SUMATERA SELATAN'),
 'sungai penuh': ('Sungai Penuh', 'JAMBI'), 'kota sungai penuh': ('Sungai Penuh', 'JAMBI'), 'sungaipenuh': ('Sungai Penuh', 'JAMBI'), 'kerinci': ('Kerinci', 'JAMBI'), 'jambi': ('Jambi', 'JAMBI'),
 'palu': ('Palu', 'SULAWESI TENGAH'), 'sigi': ('Sigi', 'SULAWESI TENGAH'), 'sigi, sulteng': ('Sigi', 'SULAWESI TENGAH'),
 'kubu raya': ('Kubu Raya', 'KALIMANTAN BARAT'), 'tanah laut': ('Tanah Laut', 'KALIMANTAN SELATAN'), 'kalimantan': ('Kalimantan', None),
 'maluku': ('Maluku', 'MALUKU'), 'ambon': ('Ambon', 'MALUKU'), 'maluku utara': ('Maluku Utara', 'MALUKU UTARA'),
 'sentani papua': ('Sentani', 'IRIAN JAYA TIMUR'),
 'padangsidimpuan': ('Padangsidimpuan', 'SUMATERA UTARA'), 'padangsidimpuan, sumut': ('Padangsidimpuan', 'SUMATERA UTARA'), 'binjai': ('Binjai', 'SUMATERA UTARA'),
 'batu bara': ('Batu Bara', 'SUMATERA UTARA'), 'labuhanbatu selatan': ('Labuhanbatu Selatan', 'SUMATERA UTARA'),
 'makassar': ('Makassar', 'SULAWESI SELATAN'), 'bone': ('Bone', 'SULAWESI SELATAN'), 'kab. kolaka': ('Kolaka', 'SULAWESI TENGGARA'),
 'mataram': ('Mataram', 'NUSATENGGARA BARAT'), 'lombok barat': ('Lombok Barat', 'NUSATENGGARA BARAT'), 'bima': ('Bima', 'NUSATENGGARA BARAT'),
 'banda aceh': ('Banda Aceh', 'DI. ACEH'), 'denpasar': ('Denpasar', 'BALI'), 'badung': ('Badung', 'BALI'),
}
ABROAD = {'singapore': 'Singapura'}

def key(g, n):
    n = AL[g].get(n, n)
    return g + '|' + re.sub(r'[^a-z]', '', re.sub(r'^h\.\s*', '', n.lower()))

files = sorted([f for f in glob.glob(U + '*.xlsx') if re.search(r'(Nilai|Input).*TO\d+', f)], key=lambda f: int(re.search(r'TO(\d+)', f).group(1)))
person = {}
unk = collections.Counter()
for f in files:
    g = 'I' if 'Ikhwan' in f else 'A'
    ws = openpyxl.load_workbook(f, data_only=True, read_only=True)['Santri']
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c).strip().lower() if c else '' for c in rows[0]]
    if 'domisili' in hdr or 'alamat' in hdr:
        di = hdr.index('domisili') if 'domisili' in hdr else hdr.index('alamat'); body = rows[1:]
        if hdr[1] in ('nama', 'nama lengkap'): pass
    else:
        di = 2; body = rows
    for r in body:
        if not r[1] or str(r[1]).strip().lower() in ('nama', 'nama lengkap', 'hk ganjil'): continue
        nm = ' '.join(str(r[1]).split()); d = r[di]
        k = key(g, nm)
        d = ' '.join(str(d).split()).lower() if d not in (None, '') else ''
        person.setdefault(k, set())
        if d and not d.isdigit():
            person[k].add(d)
# ---- registrasi ulang (RU_*.xlsx): domicile only, no personal data kept ----
ru_stats = {}
for f in sorted(glob.glob(U + '*RU_*.xlsx')):
    wb = openpyxl.load_workbook(f, data_only=True, read_only=True)
    fname = os.path.basename(f)
    for sn in wb.sheetnames:
        rows = [r for r in wb[sn].iter_rows(values_only=True) if r and any(c not in (None, '') for c in r)]
        hi = next(i for i, r in enumerate(rows) if r[0] == 'No')
        hdr = [str(c).strip().lower() if c else '' for c in rows[hi]]
        ni = next(i for i, h in enumerate(hdr) if h.startswith('nama'))
        di = next(i for i, h in enumerate(hdr) if 'domisili' in h)
        gi = next((i for i, h in enumerate(hdr) if h in ('kategori', 'ikhwan / akhwat')), None)
        n = 0
        for r in rows[hi + 1:]:
            if not r[ni]: continue
            n += 1
            nm = ' '.join(str(r[ni]).split())
            if 'IKHWAN' in fname: g = 'I'
            elif 'AKHWAT' in fname: g = 'A'
            elif gi is not None and r[gi]: g = 'I' if 'ikhwan' in str(r[gi]).lower() else 'A'
            else: g = None
            if g: k = key(g, nm)
            else:
                ka, ki = key('A', nm), key('I', nm)
                k = ka if ka in person else ki if ki in person else 'X|' + ka[2:]
            d = r[di]; d = ' '.join(str(d).split()).lower() if d not in (None, '') else ''
            person.setdefault(k, set())
            if d and not d.isdigit(): person[k].add(d)
        ru_stats[fname.split('-', 1)[1] + ':' + sn] = n
print('RU', ru_stats)
REG = set(); cities = collections.Counter(); prov = collections.Counter(); provCities = collections.defaultdict(collections.Counter); abroad = collections.Counter()
for k, ds in person.items():
  seenC=set()
  for d in ds:
    if d in ABROAD: r = ('abroad', ABROAD[d])
    elif d in M: r = ('id',) + M[d]
    else: r = lookup(d, M)
    if not r: unk[d] += 1; continue
    if r[0] == 'abroad':
        if r[1] not in seenC: seenC.add(r[1]); abroad[r[1]] += 1
        continue
    c, p = r[1], r[2]
    if len(r) > 3 or c in ('Riau', 'Lampung', 'Maluku', 'Maluku Utara', 'Kalimantan'): REG.add(c)
    if c in seenC: continue
    seenC.add(c); cities[c] += 1
    if p: prov[p] += 1; provCities[p][c] += 1
print('santri unik', len(person), 'dengan domisili', sum(1 for v in person.values() if v), 'multi', sum(1 for v in person.values() if len(v)>1))
print('belum terpetakan', unk)
print('kota', len(cities), 'provinsi', len(prov), 'luar negeri', dict(abroad))
print(prov.most_common())
print(cities.most_common(12))
json.dump({'total': len(person), 'withDom': sum(1 for v in person.values() if v), 'prov': prov, 'provCities': {p: v.most_common() for p, v in provCities.items()},
           'cities': cities.most_common(), 'abroad': abroad.most_common(), 'region': sorted(REG)}, open('data.json', 'w'), ensure_ascii=False)
