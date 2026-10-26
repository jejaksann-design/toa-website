"""Extra domicile mapping for older periods: base name -> (display, province key). Region-only entries use region=True names."""
import re
JB, JT, JI, DKI, BT = 'JAWA BARAT', 'JAWA TENGAH', 'JAWA TIMUR', 'DKI JAKARTA', 'PROBANTEN'
SS, SB, SU, AC = 'SUMATERA SELATAN', 'SUMATERA BARAT', 'SUMATERA UTARA', 'DI. ACEH'
KT, KM, KB, KS = 'KALIMANTAN TENGAH', 'KALIMANTAN TIMUR', 'KALIMANTAN BARAT', 'KALIMANTAN SELATAN'
SN, ST, SG = 'SULAWESI SELATAN', 'SULAWESI TENGAH', 'SULAWESI TENGGARA'
B = {
 # Jawa Barat
 'bandung barat': ('Bandung Barat', JB), 'kp lembang rt 01': ('Bandung Barat', JB), 'kuningan': ('Kuningan', JB), 'cianjur': ('Cianjur', JB), 'majalengka': ('Majalengka', JB),
 'sumedang': ('Sumedang', JB), 'indramayu': ('Indramayu', JB), 'subang': ('Subang', JB), 'tasikmalaya': ('Tasikmalaya', JB), 'depok': ('Depok', JB), 'bandung': ('Bandung', JB),
 'bekasi': ('Bekasi', JB), 'bekasi utara': ('Bekasi', JB), 'cikarang': ('Bekasi', JB), 'karawang': ('Karawang', JB), 'cileungsi': ('Bogor', JB), 'bojong gede': ('Bogor', JB),
 'cibinong': ('Bogor', JB), 'bogor': ('Bogor', JB), 'garut': ('Garut', JB), 'sukabumi': ('Sukabumi', JB), 'cirebon': ('Cirebon', JB), 'ciamis': ('Ciamis', JB), 'cimahi': ('Cimahi', JB),
 'jawa barat': ('Jawa Barat', JB, True),
 # DKI / Banten
 'jakarta utara': ('Jakarta', DKI), 'jakarta pusat': ('Jakarta', DKI), 'jakarta selatan': ('Jakarta', DKI), 'jakrta selatan': ('Jakarta', DKI), 'jaksel': ('Jakarta', DKI), 'jaktim': ('Jakarta', DKI),
 'jakarta timur': ('Jakarta', DKI), 'jakarta barat': ('Jakarta', DKI), 'jakarta': ('Jakarta', DKI), 'dki jakarta': ('Jakarta', DKI),
 'tangerang': ('Tangerang', BT), 'tanggerang': ('Tangerang', BT), 'balaraja': ('Tangerang', BT), 'tangerang selatan': ('Tangerang Selatan', BT), 'tanggerang selatan': ('Tangerang Selatan', BT),
 'serang': ('Serang', BT), 'cikande': ('Serang', BT), 'cilegon': ('Cilegon', BT), 'pandeglang': ('Pandeglang', BT), 'lebak': ('Lebak', BT),
 # Jawa Tengah / DIY
 'sukoharjo': ('Sukoharjo', JT), 'cilacap': ('Cilacap', JT), 'demak': ('Demak', JT), 'kudus': ('Kudus', JT), 'tegal': ('Tegal', JT), 'magelang': ('Magelang', JT),
 'banjarnegara': ('Banjarnegara', JT), 'brebes': ('Brebes', JT), 'surakarta': ('Surakarta', JT), 'sragen': ('Sragen', JT), 'kebumen': ('Kebumen', JT), 'wonosobo': ('Wonosobo', JT),
 'jepara': ('Jepara', JT), 'kendal': ('Kendal', JT), 'semarang': ('Semarang', JT), 'karang anyar': ('Karanganyar', JT), 'purwodadi': ('Grobogan', JT),
 'sleman': ('Sleman', 'DAERAH ISTIMEWA YOGYAKARTA'), 'ngaglik': ('Sleman', 'DAERAH ISTIMEWA YOGYAKARTA'), 'bantul': ('Bantul', 'DAERAH ISTIMEWA YOGYAKARTA'), 'jogja': ('Yogyakarta', 'DAERAH ISTIMEWA YOGYAKARTA'),
 # Jawa Timur
 'madiun': ('Madiun', JI), 'blitar': ('Blitar', JI), 'pacitan': ('Pacitan', JI), 'gresik': ('Gresik', JI), 'sumenep': ('Sumenep', JI), 'nganjuk': ('Nganjuk', JI), 'batu': ('Batu', JI),
 'batu malang': ('Batu', JI), 'ngawi': ('Ngawi', JI), 'magetan': ('Magetan', JI), 'mojokerto': ('Mojokerto', JI), 'surabaya': ('Surabaya', JI), 'malang': ('Malang', JI), 'pasuruan': ('Pasuruan', JI),
 # Sumatera
 'batam': ('Batam', 'RIAU'), 'natuna': ('Natuna', 'RIAU'), 'bintan kepulauan riau': ('Bintan', 'RIAU'), 'bintan kepri': ('Bintan', 'RIAU'), 'kepulauan riau': ('Kepulauan Riau', 'RIAU', True), 'kep. riau': ('Kepulauan Riau', 'RIAU', True),
 'rokan hilir': ('Rokan Hilir', 'RIAU'), 'kuantan singingi': ('Kuantan Singingi', 'RIAU'), 'bengkalis': ('Bengkalis', 'RIAU'), 'bengkalis riau': ('Bengkalis', 'RIAU'), 'palalawan': ('Pelalawan', 'RIAU'), 'pelalawan': ('Pelalawan', 'RIAU'), 'pekanbaru': ('Pekanbaru', 'RIAU'),
 'agam': ('Agam', SB), 'agam sumbar': ('Agam', SB), 'maninjau': ('Agam', SB), 'pariaman': ('Pariaman', SB), 'padang pariaman': ('Padang Pariaman', SB), 'solok selatan': ('Solok Selatan', SB),
 'tanah datar': ('Tanah Datar', SB), 'bukittinggi': ('Bukittinggi', SB), 'pasaman barat': ('Pasaman Barat', SB), 'sumatera barat': ('Sumatera Barat', SB, True),
 'medan': ('Medan', SU), 'asahan': ('Asahan', SU), 'labuhanbatu utara': ('Labuhanbatu Utara', SU), 'tobasa': ('Toba', SU), 'padang sidempuan': ('Padangsidimpuan', SU), 'padangsidimpuan': ('Padangsidimpuan', SU), 'binjai': ('Binjai', SU),
 'oku': ('Ogan Komering Ulu', SS), 'oku timur': ('OKU Timur', SS), 'oku timur sumsel': ('OKU Timur', SS), 'okut sumsel': ('OKU Timur', SS),
 'jambi': ('Jambi', 'JAMBI'), 'sungai penuh': ('Sungai Penuh', 'JAMBI'), 'tanjung jabung barat': ('Tanjung Jabung Barat', 'JAMBI'),
 'bengkulu': ('Bengkulu', 'BENGKULU'), 'mukomuko': ('Mukomuko', 'BENGKULU'),
 'pringsewu': ('Pringsewu', 'LAMPUNG'), 'lampung tengah': ('Lampung Tengah', 'LAMPUNG'), 'lampung selatan': ('Lampung Selatan', 'LAMPUNG'), 'metro lampung': ('Metro', 'LAMPUNG'), 'metro': ('Metro', 'LAMPUNG'), 'bandar lampung': ('Bandar Lampung', 'LAMPUNG'),
 'bangka': ('Bangka', 'BANGKA BELITUNG'), 'sungailiat': ('Bangka', 'BANGKA BELITUNG'), 'bangka belitung': ('Bangka Belitung', 'BANGKA BELITUNG', True),
 'takengon': ('Aceh Tengah', AC), 'aceh tengah': ('Aceh Tengah', AC), 'bener meriah': ('Bener Meriah', AC), 'aceh timur': ('Aceh Timur', AC), 'subulussalam': ('Subulussalam', AC),
 'aceh': ('Aceh', AC, True), 'nanggroe aceh darussalam': ('Aceh', AC, True),
 # Kalimantan
 'palangkaraya': ('Palangka Raya', KT), 'kotawaringin barat': ('Kotawaringin Barat', KT), 'pangkalanbun': ('Kotawaringin Barat', KT), 'kumai': ('Kotawaringin Barat', KT), 'seruyan kalteng': ('Seruyan', KT),
 'balikpapan': ('Balikpapan', KM), 'balik papan': ('Balikpapan', KM), 'samarinda': ('Samarinda', KM), 'kutai kartanegara': ('Kutai Kartanegara', KM), 'samboja': ('Kutai Kartanegara', KM),
 'kalimantan timur': ('Kalimantan Timur', KM, True), 'kutai timur': ('Kutai Timur', KM), 'tarakan': ('Tarakan', KM),
 'pontianak': ('Pontianak', KB), 'singkawang': ('Singkawang', KB), 'ketapang kalbar': ('Ketapang', KB), 'kalimantan barat': ('Kalimantan Barat', KB, True),
 'banjarmasin': ('Banjarmasin', KS), 'tanah bumbu': ('Tanah Bumbu', KS), 'tanah bunbu': ('Tanah Bumbu', KS), 'hss': ('Hulu Sungai Selatan', KS),
 # Sulawesi / NTB / Papua
 'pinrang': ('Pinrang', SN), 'bulukumba': ('Bulukumba', SN), 'makasar': ('Makassar', SN), 'enrekang': ('Enrekang', SN), 'soppeng': ('Soppeng', SN), 'walimpong': ('Soppeng', SN), 'wajo': ('Wajo', SN),
 'maros': ('Maros', SN), 'luwu timur': ('Luwu Timur', SN), 'luwu': ('Luwu', SN), 'parepare': ('Parepare', SN), 'pangkep': ('Pangkep', SN), 'barru': ('Barru', SN), 'sidrap': ('Sidrap', SN),
 'mamuju': ('Mamuju', SN), 'sulbar': ('Sulawesi Barat', SN, True),
 'parigi moutong': ('Parigi Moutong', ST), 'palu': ('Palu', ST), 'poso': ('Poso', ST), 'ampana': ('Tojo Una-Una', ST), 'sigi': ('Sigi', ST),
 'kendari': ('Kendari', SG), 'kolaka': ('Kolaka', SG), 'bau - bau': ('Baubau', SG), 'baubau': ('Baubau', SG),
 'sumbawa': ('Sumbawa', 'NUSATENGGARA BARAT'), 'lombok': ('Lombok', 'NUSATENGGARA BARAT'), 'lombok tengah': ('Lombok Tengah', 'NUSATENGGARA BARAT'), 'mataram': ('Mataram', 'NUSATENGGARA BARAT'),
 'sentani': ('Sentani', 'IRIAN JAYA TIMUR'), 'bau': ('Baubau', SG), 'depok jawa barat': ('Depok', JB), 'sleman diy': ('Sleman', 'DAERAH ISTIMEWA YOGYAKARTA'), 'sarolangun': ('Sarolangun', 'JAMBI'),
}
ABR = {'coventry': 'Inggris', 'inggris': 'Inggris', 'uk': 'Inggris', 'gifu': 'Jepang', 'abu dhabi': 'Uni Emirat Arab', 'keddah': 'Malaysia', 'timor leste': 'Timor Leste', 'singapore': 'Singapura'}

def norm(d):
    d = d.lower().strip().rstrip('.')
    for sep in (',', '/', '(', ' - ', '-'):
        if sep in d:
            head = d.split(sep)[0].strip()
            if head: d = head
    d = re.sub(r'^(kabupaten\s+|kab\.\s*|kab\s+|kota\s+)', '', d).strip()
    d = re.sub(r'\s+', ' ', d)
    return d

def lookup(d):
    if 'sarulangon' in d: d = 'sarolangun'
    if 'kutai timur' in d: d = 'kutai timur'
    if ' kecamatan ' in d: d = d.split(' kecamatan ')[0]
    if d in ABR: return ('abroad', ABR[d])
    n = norm(d)
    if n in ABR: return ('abroad', ABR[n])
    if n in B: return ('id',) + B[n]
    # try with region suffix kept (e.g. 'bintan kepulauan riau')
    m = re.sub(r'^(kabupaten\s+|kab\.\s*|kab\s+|kota\s+)', '', d.lower().strip().rstrip('.')).replace(',', ' ').strip()
    m = re.sub(r'\s+', ' ', m)
    if m in B: return ('id',) + B[m]
    return None

# ---- additions for TO60–TO70 ----
B.update({
 'pemalang': ('Pemalang', JT), 'banyumas': ('Banyumas', JT), 'purwokerto': ('Banyumas', JT), 'gombong': ('Kebumen', JT), 'bumiayu': ('Brebes', JT), 'magrlang': ('Magelang', JT),
 'tuban': ('Tuban', JI), 'tulungagung': ('Tulungagung', JI), 'bangkalan': ('Bangkalan', JI), 'banyuwangi': ('Banyuwangi', JI), 'bojonegoro': ('Bojonegoro', JI),
 'probolinggo': ('Probolinggo', JI), 'probolibggo': ('Probolinggo', JI),
 'purwakarta': ('Purwakarta', JB), 'bojonggede': ('Bogor', JB), 'gunung putri': ('Bogor', JB), 'jabar': ('Jawa Barat', JB, True), 'kalijati': ('Subang', JB), 'kalijati timur': ('Subang', JB),
 'pelabuhanratu': ('Sukabumi', JB),
 'kulon progo': ('Kulon Progo', 'DAERAH ISTIMEWA YOGYAKARTA'), 'diy': ('DI Yogyakarta', 'DAERAH ISTIMEWA YOGYAKARTA', True), 'yogjakarta': ('Yogyakarta', 'DAERAH ISTIMEWA YOGYAKARTA'), 'yogyakarta': ('Yogyakarta', 'DAERAH ISTIMEWA YOGYAKARTA'),
 'pamulang': ('Tangerang Selatan', BT),
 'deli serdang': ('Deli Serdang', SU), 'padangsidempuan': ('Padangsidimpuan', SU), 'padang sidimpuan': ('Padangsidimpuan', SU), 'padang lawas': ('Padang Lawas', SU), 'langkat': ('Langkat', SU),
 'labura': ('Labuhanbatu Utara', SU), 'simalungun': ('Simalungun', SU), 'sei silau': ('Asahan', SU), 'sumatra utara medan marelan': ('Medan', SU),
 'padang': ('Padang', SB), 'pdg': ('Padang', SB), 'padamg': ('Padang', SB), 'padang panjang': ('Padang Panjang', SB), 'solok': ('Solok', SB), 'pesisir selatan': ('Pesisir Selatan', SB), 'pasaman': ('Pasaman', SB),
 'duri': ('Bengkalis', 'RIAU'), 'indragiri hulu': ('Indragiri Hulu', 'RIAU'), 'kepulauan meranti': ('Kepulauan Meranti', 'RIAU'), 'tanjung pinang': ('Tanjung Pinang', 'RIAU'), 'tanjungpinang': ('Tanjung Pinang', 'RIAU'), 'bintan': ('Bintan', 'RIAU'),
 'musi banyuasin': ('Musi Banyuasin', SS), 'empat lawang': ('Empat Lawang', SS), 'ogan ilir': ('Ogan Ilir', SS), 'lubuk linggau': ('Lubuklinggau', SS), 'ogan komering ulu': ('Ogan Komering Ulu', SS),
 'ogan komering ulu selatan': ('OKU Selatan', SS), 'oku selatan': ('OKU Selatan', SS), 'muaradua': ('OKU Selatan', SS), 'palembang': ('Palembang', SS),
 'pangkal pinang': ('Pangkalpinang', 'BANGKA BELITUNG'), 'pangkalpinang': ('Pangkalpinang', 'BANGKA BELITUNG'), 'muaro jambi': ('Muaro Jambi', 'JAMBI'),
 'lebong': ('Lebong', 'BENGKULU'), 'rejang lebong': ('Rejang Lebong', 'BENGKULU'), 'way kanan': ('Way Kanan', 'LAMPUNG'), 'tanggamus': ('Tanggamus', 'LAMPUNG'),
 'blangpidie': ('Aceh Barat Daya', AC), 'nagan raya': ('Nagan Raya', AC),
 'seruyan': ('Seruyan', KT), 'seruyan tengah': ('Seruyan', KT), 'kutai barat': ('Kutai Barat', KM), 'kalsel': ('Kalimantan Selatan', KS, True), 'kalimantan selatan': ('Kalimantan Selatan', KS, True),
 'takalar': ('Takalar', SN), 'gowa': ('Gowa', SN), 'jeneponto': ('Jeneponto', SN), 'makassar': ('Makassar', SN), 'tosora': ('Wajo', SN), 'luwu utara': ('Luwu Utara', SN),
 'pangkajene dan kepulauan': ('Pangkep', SN), 'sidenreng rappang': ('Sidrap', SN), 'pasangkayu': ('Pasangkayu', SN), 'mamuju tengah': ('Mamuju Tengah', SN), 'sulsel': ('Sulawesi Selatan', SN, True),
 'donggala': ('Donggala', ST), 'tojo una-una': ('Tojo Una-Una', ST), 'tojo una una': ('Tojo Una-Una', ST), 'sulteng': ('Sulawesi Tengah', ST, True),
 'kolaka utara': ('Kolaka Utara', SG), 'muna': ('Muna', SG), 'wakatobi': ('Wakatobi', SG), 'sulawesi tenggara': ('Sulawesi Tenggara', SG, True),
 'gorontalo': ('Gorontalo', 'GORONTALO'),
 'tual': ('Tual', 'MALUKU'), 'tual maluku': ('Tual', 'MALUKU'), 'maluku tenggara': ('Maluku Tenggara', 'MALUKU'), 'tual maluku tenggara': ('Tual', 'MALUKU'), 'maluku barat daya': ('Maluku Barat Daya', 'MALUKU'),
 'tidore': ('Tidore', 'MALUKU UTARA'), 'pulau morotai': ('Pulau Morotai', 'MALUKU UTARA'),
 'jayapura': ('Jayapura', 'IRIAN JAYA TIMUR'), 'sorong': ('Sorong', 'IRIAN JAYA BARAT'),
 'gianyar': ('Gianyar', 'BALI'), 'lombok timur': ('Lombok Timur', 'NUSATENGGARA BARAT'),
 'asahan': ('Asahan', SU), 'medan': ('Medan', SU), 'sleman': ('Sleman', 'DAERAH ISTIMEWA YOGYAKARTA'), 'subang': ('Subang', JB), 'semarang': ('Semarang', JT),
})
ABR.update({'tokyo': 'Jepang', 'nagoya': 'Jepang', 'ryad saudi arabia': 'Arab Saudi', 'al dhannah': 'Uni Emirat Arab', 'singapura': 'Singapura'})
_old_lookup = lookup
def lookup(d, extra=None):
    d0 = d.lower().strip().replace('kan.', 'kab. ').replace('kab,', 'kab. ')
    r = _old_lookup(d0)
    if r: return r
    n = norm(d0)
    w = n.split()
    cands = [n, ' '.join(w[:2]), ' '.join(w[:1]), ' '.join(w[-1:]), ' '.join(w[-2:])]
    for c in cands:
        if not c: continue
        if c in ABR: return ('abroad', ABR[c])
        if c in B: return ('id',) + B[c]
        if extra and c in extra: return ('id',) + tuple(extra[c])
    return None

# ---- additions for TO71–TO80 ----
B.update({
 'rohil': ('Rokan Hilir', 'RIAU'), 'pekan baru': ('Pekanbaru', 'RIAU'), 'kepri': ('Kepulauan Riau', 'RIAU', True), 'indragiri hilir': ('Indragiri Hilir', 'RIAU'),
 'sumsel': ('Sumatera Selatan', SS, True), 'pagaralam': ('Pagar Alam', SS), 'martapura okut': ('OKU Timur', SS),
 'payakumbuh': ('Payakumbuh', SB), 'tapanuli selatan': ('Tapanuli Selatan', SU), 'sinabang': ('Simeulue', AC),
 'tapin': ('Tapin', KS), 'binuang': ('Tapin', KS), 'tanah bambu': ('Tanah Bumbu', KS), 'kubar': ('Kutai Barat', KM), 'kaltim': ('Kalimantan Timur', KM, True),
 'sekadau': ('Sekadau', KB), 'sambas': ('Sambas', KB), 'kalbar': ('Kalimantan Barat', KB, True),
 'sukolilo': ('Surabaya', JI), 'madura': ('Madura', JI, True), 'purworejo': ('Purworejo', JT), 'jawa tengah': ('Jawa Tengah', JT, True),
 'cibubur': ('Jakarta', DKI), 'cipulir kebayoran lama': ('Jakarta', DKI), 'tangrang': ('Tangerang', BT),
 'parigi': ('Parigi Moutong', ST), 'moutong': ('Parigi Moutong', ST), 'majene': ('Majene', SN), 'ternate': ('Ternate', 'MALUKU UTARA'), 'moa': ('Maluku Barat Daya', 'MALUKU'),
 'sangihe': ('Kepulauan Sangihe', 'SULAWESI UTARA'), 'kep. singihe': ('Kepulauan Sangihe', 'SULAWESI UTARA'), 'kepulauan sangihe': ('Kepulauan Sangihe', 'SULAWESI UTARA'),
 'kupang': ('Kupang', 'NUSA TENGGARA TIMUR'), 'sidorejo': ('Lampung Timur', 'LAMPUNG'),
})
ABR.update({'new zealand': 'Selandia Baru', 'kanazawa': 'Jepang'})

# ---- additions for TO81–TO94 ----
B.update({
 'yogya': ('Yogyakarta', 'DAERAH ISTIMEWA YOGYAKARTA'), 'salatga': ('Salatiga', JT), 'blora': ('Blora', JT), 'klaten': ('Klaten', JT),
 'jonggol': ('Bogor', JB), 'pasar minggu': ('Jakarta', DKI),
 'muara enim': ('Muara Enim', SS), 'karo': ('Karo', SU), 'siak': ('Siak', 'RIAU'),
 'polman': ('Polewali Mandar', SN), 'polewali mandar': ('Polewali Mandar', SN), 'maross': ('Maros', SN),
 'sulawesi tengah': ('Sulawesi Tengah', ST, True), 'luwuk banggai': ('Banggai', ST), 'banggai': ('Banggai', ST),
 'pagatan': ('Tanah Bumbu', KS), 'ntb': ('Nusa Tenggara Barat', 'NUSATENGGARA BARAT', True),
 'papua': ('Papua', 'IRIAN JAYA TIMUR', True), 'biak': ('Biak Numfor', 'IRIAN JAYA TENGAH'),
})
ABR.update({'gombak': 'Malaysia'})
B.update({'arga makmur': ('Bengkulu Utara', 'BENGKULU'), 'cikupa': ('Tangerang', BT)})
