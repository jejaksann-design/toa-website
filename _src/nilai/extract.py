"""Usage: python3 extract.py TO95 akhwat.xlsx ikhwan.xlsx  -> data/TO95.json (public-safe)"""
import openpyxl, json, sys, os
per, fa, fi = sys.argv[1:4]
out = []
for f, g in [(fa, 'A'), (fi, 'I')]:
    if f == 'NONE': continue
    ws = openpyxl.load_workbook(f, data_only=True, read_only=True)['LAPORAN']
    rows = [r[3:11] for r in ws.iter_rows(min_row=8, values_only=True)
            if r and len(r) > 10 and isinstance(r[3], (int, float)) and r[5] not in (None, '#N/A', '')]
    n = 0
    def num(v):
        try: return float(str(v).strip())
        except Exception: return 0.0
    for rk, hk, nm, s, a, i, t, k in rows:
        s, a, i, t = map(num, (s, a, i, t))
        if str(k).strip().upper() == 'LULUS': assert abs(s*.3 + a*.5 + i*.2 - t) < 0.02, nm
        nm = " ".join(str(nm).split()); hk = str(hk).strip()
        if str(k).strip().upper() == 'LULUS':
            n += 1
            out.append({"g": g, "rank": n, "hk": hk, "nama": nm, "setoran": round(s, 2), "adab": round(a, 2), "imtak": round(i, 2), "akhir": round(t, 2), "lulus": True})
        else:
            out.append({"g": g, "hk": hk, "nama": nm, "lulus": False})
d = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(f'{d}/data/{per}.json', 'w'), ensure_ascii=False)
print(per, {g: (sum(1 for x in out if x['g'] == g and x['lulus']), sum(1 for x in out if x['g'] == g)) for g in 'AI'})
