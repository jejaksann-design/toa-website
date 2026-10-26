# Sumber website TOA (tidak ikut dideploy)

Folder ini berisi bahan mentah dan skrip pembangun website. `.vercelignore` mengecualikannya dari deploy.

- `landing/index.html` sumber landing page
- `quran/kuis-template.html` + `ebook/apply.py` membangun halaman kuis
- `nilai/` ekstrak nilai dari Excel LAPORAN (`extract.py`) lalu gabung ke `prestasi.json` (`merge.py`)
- `peta/` membangun bagian Peta Santri (data.json hanya berisi hitungan per kota, tanpa data pribadi)
- `site/build_site.py` merakit folder website siap deploy

Catatan: skrip memakai path absolut sesi lama (scratchpad); sesuaikan variabel D/ROOT sebelum menjalankan.
Data per periode (nama santri yang belum lulus), alias nama, dan file registrasi ulang sengaja TIDAK disimpan di repo publik ini.
