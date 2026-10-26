p = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/quran/kuis-template.html'
s = open(p).read()
assert 'id="s-tes"' not in s

CSS = r'''.tescard{display:grid;grid-template-columns:3.2rem 1fr;gap:14px;align-items:center;text-align:left;background:var(--green-soft);border:1.5px solid var(--green);border-radius:18px;padding:18px;cursor:pointer;width:100%}
.tescard .ic{width:3.2rem;height:3.2rem;border-radius:14px;background:var(--paper);display:grid;place-items:center;font-weight:700;color:var(--green);font-size:1.3rem}
.tescard b{display:block;font-weight:600;font-size:1.05rem}
.tescard span.d{font-size:.9rem;color:var(--muted)}
.tin{font:inherit;font-size:1.3rem;color:var(--ink);background:var(--paper);border:1.5px solid var(--line);border-radius:14px;padding:14px;width:100%;max-width:220px}
.tin:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.tf{display:flex;flex-direction:column;gap:6px;font-weight:600;font-size:.92rem}
.tf input{font:inherit;font-weight:400;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:12px;width:100%}
.pres{background:var(--paper);border:1.5px solid var(--green);border-radius:22px;padding:22px;display:flex;flex-direction:column;gap:14px}
.pres .pn{font-family:var(--display);font-size:2.1rem;line-height:1.1}
.pres .code{align-self:flex-start;background:var(--gold-soft);border-radius:999px;padding:4px 12px;font-weight:700;font-size:.85rem;letter-spacing:.04em}
.pres ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:4px}
.pres dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:.92rem;background:var(--green-soft);border-radius:12px;padding:12px 14px}
.pres dt{font-weight:600}.pres dd{margin:0;color:var(--muted)}
.alt{border:1px dashed var(--line);border-radius:14px;padding:14px;font-size:.92rem;display:flex;flex-direction:column;gap:8px}
'''
a = '.loading{'
assert s.count(a) == 1
s = s.replace(a, CSS + a)

a = '    <div class="modes">'
assert s.count(a) == 1
s = s.replace(a, '''    <button class="tescard" id="tes-card" type="button"><span class="ic">?</span><span><b>Tes Penempatan Program</b><span class="d">Bingung pilih program? Jawab 7 pertanyaan dan 3 sambung ayat, sekitar 5 menit.</span></span></button>
''' + a)

a = '  <!-- Question -->'
assert s.count(a) == 1
s = s.replace(a, '''  <!-- Placement -->
  <section id="s-tes" hidden style="display:flex;flex-direction:column;gap:16px">
    <div class="qtop"><span>Tes Penempatan Program</span><span id="t-step"></span></div>
    <div class="prog"><div id="t-prog" style="width:0"></div></div>
    <div id="t-area" style="display:flex;flex-direction:column;gap:16px"></div>
  </section>

''' + a)

a = "'s-res','s-daily']"
assert s.count(a) == 1
s = s.replace(a, "'s-res','s-daily','s-tes']")

JS = r'''
/* ===== Tes Penempatan ===== */
var ADMIN='6282314090180';
var PROG={TO:{per:'100',nama:'Tahfidz Online 30 Juz',jadwal:'Senin–Jumat ziyadah, Sabtu–Ahad murajaah'},
  MO:{per:'56',nama:'Murojaah Online',jadwal:"Senin–Ahad murajaah, tasmi' menyesuaikan jadwal"},
  TOSP:{per:'49',nama:'Tahfidz Surah-Surah Pilihan',jadwal:'3× pertemuan sepekan'},
  TOK:{per:'47',nama:'Tahfidz Online for Kids',jadwal:'Senin–Jumat ziyadah, Sabtu murajaah'}};
var HAF=[[0,'Belum ada / baru mulai'],[0.5,'Sebagian Juz 30'],[1,'Sekitar 1 juz'],[3,'2–5 juz'],[10,'6–15 juz'],[20,'16–29 juz'],[30,'30 juz']];
var T={},TI=0;
function kid(){return !!(T.usia&&T.usia<=12)}
function you(){return T.who==='anak'?'anak':'kamu'}
var TSTEPS=[
 {k:'who',q:function(){return 'Tes ini untuk siapa?'},o:function(){return [['self','Untuk saya sendiri'],['anak','Untuk anak saya']]}},
 {k:'usia',q:function(){return T.who==='anak'?'Berapa usia anak?':'Berapa usiamu?'},input:true},
 {k:'jk',q:function(){return T.who==='anak'?'Anak laki-laki atau perempuan?':'Ikhwan atau akhwat?'},o:function(){return T.who==='anak'?[['Ikhwan','Laki-laki'],['Akhwat','Perempuan']]:[['Ikhwan','Ikhwan'],['Akhwat','Akhwat']]}},
 {k:'haf',q:function(){return 'Berapa hafalan '+you()+' saat ini?'},o:function(){return HAF}},
 {k:'goal',skip:kid,q:function(){return 'Apa tujuan utamamu?'},o:function(){return [['tambah','Menambah hafalan, target 30 juz'],['jaga','Menjaga dan menguatkan hafalan yang sudah ada'],['pilihan','Menghafal surat pilihan: Al-Mulk, Yasin, Ar-Rahman, dan lainnya'],['mulai','Mulai pelan-pelan dari surat pendek']]}},
 {k:'time',skip:kid,q:function(){return 'Berapa waktu yang bisa kamu sisihkan untuk Al-Qur\'an setiap hari?'},o:function(){return [[10,'Kurang dari 15 menit'],[20,'15–30 menit'],[45,'30–60 menit'],[90,'Lebih dari 1 jam']]}},
 {k:'style',q:function(){return T.who==='anak'?'Anak lebih cocok belajar dengan cara…':'Kamu lebih nyaman belajar dengan cara…'},o:function(){return [['halaqah','Bareng teman dalam halaqah'],['private','Satu santri, satu musyrif/musyrifah (private)'],['?','Belum tahu']]}}
];
function tvisible(){return TSTEPS.filter(function(x){return !(x.skip&&x.skip())})}
function tstart(){T={test:[]};TI=0;show('s-tes');trender()}
E('tes-card').addEventListener('click',tstart);
function tprog(i,n){E('t-prog').style.width=(i/n*100)+'%'}
function trender(){
  var V=tvisible(),A=E('t-area');A.textContent='';
  if(TI>=V.length){return ttestIntro()}
  var st=V[TI];E('t-step').textContent='Pertanyaan '+(TI+1)+' dari '+V.length;tprog(TI,V.length+1);
  var h=document.createElement('h2');h.textContent=st.q();A.appendChild(h);
  if(st.input){
    var w=document.createElement('div');w.style.cssText='display:flex;flex-direction:column;gap:10px';
    w.innerHTML='<label class="tf" for="t-usia">Usia (tahun)<input class="tin" id="t-usia" inputmode="numeric" placeholder="Contoh: 24"></label><p class="err" id="t-err" hidden style="color:var(--bad);font-size:.9rem"></p><button class="btn" type="button" style="align-self:flex-start">Lanjut</button>';
    A.appendChild(w);var inp=w.querySelector('input');if(T.usia)inp.value=T.usia;
    function go(){var v=parseInt(inp.value,10),er=E('t-err');if(!(v>=3&&v<=90)){er.textContent='Masukkan usia dalam angka, misalnya 24.';er.hidden=false;return}T.usia=v;TI++;trender()}
    w.querySelector('button').addEventListener('click',go);inp.addEventListener('keydown',function(e){if(e.key==='Enter')go()});
    setTimeout(function(){inp.focus()},50);
  }else{
    var O=document.createElement('div');O.className='opts';
    st.o().forEach(function(x){var b=document.createElement('button');b.type='button';b.className='opt';b.textContent=x[1];
      if(T[st.k]===x[0])b.style.borderColor='var(--green)';
      b.addEventListener('click',function(){T[st.k]=x[0];TI++;trender();window.scrollTo({top:0,behavior:'smooth'})});O.appendChild(b)});
    A.appendChild(O);
  }
  var bk=document.createElement('button');bk.type='button';bk.className='link';bk.textContent=TI?'← Pertanyaan sebelumnya':'← Kembali ke menu';
  bk.addEventListener('click',function(){if(TI){TI--;trender()}else show('s-menu')});A.appendChild(bk);
}
function tjuz(){return T.haf<=0.5?[30,30,30]:T.haf<=1?[30,30,30]:T.haf<=5?[30,29,30]:[30,29,1]}
function ttestIntro(){
  if(kid()||T.haf<0.5){return tresult()}
  var A=E('t-area');A.textContent='';E('t-step').textContent='Tes sambung ayat';tprog(1,1.15);
  var J=tjuz().filter(function(v,i,a){return a.indexOf(v)===i});
  A.innerHTML='<span class="eyebrow">Langkah terakhir</span><h2>Tes singkat: 3 sambung ayat</h2><p class="muted"></p>';
  A.querySelector('p').textContent='Seperti imtihan di TOA: muncul satu ayat, pilih sambungannya. Soal diambil dari '+J.map(function(j){return 'Juz '+j}).join(' dan ')+'. Santai saja, ini untuk mencocokkan program, bukan untuk lulus atau gagal.';
  var r=document.createElement('div');r.className='row';
  r.innerHTML='<button class="btn" type="button">Mulai tes</button><button class="btn ghost" type="button">Lewati tes</button>';
  var bs=r.querySelectorAll('button');
  bs[0].addEventListener('click',function(){A.innerHTML='<p class="loading">Membuka mushaf…</p>';loadQuran().then(function(){T.qs=tbuild();T.test=[];tq()}).catch(function(){tresult()})});
  bs[1].addEventListener('click',function(){T.skipTest=true;tresult()});
  A.appendChild(r);
}
function tbuild(){
  var V=Q.v,out=[],used={};
  tjuz().forEach(function(j){
    var pool=[],pr=[];
    for(var i=0;i<V.length;i++){if(V[i][2]!==j||V[i][1]<2)continue;if(T.haf<=0.5&&j===30&&V[i][0]<93)continue;pool.push(i)}
    pool.forEach(function(i){var n=V[i+1];if(n&&n[0]===V[i][0]&&n[1]>1&&!used[i])pr.push(i)});
    var i=pr[Math.floor(Math.random()*pr.length)];used[i]=1;
    var cur=V[i],nx=V[i+1],seen={},opts=[{t:head(nx[3],7),ok:true}];seen[opts[0].t]=1;seen[head(cur[3],7)]=1;
    shuffle(pool).some(function(k){if(k===i||k===i+1)return false;var t=head(V[k][3],7);if(seen[t])return false;seen[t]=1;opts.push({t:t,ok:false});return opts.length===4});
    out.push({ref:'QS '+Q.names[cur[0]-1]+': '+cur[1],ayah:tail(cur[3],24),opts:shuffle(opts)});
  });
  return out;
}
function tq(){
  var k=T.test.length,q=T.qs[k],A=E('t-area');A.textContent='';E('t-step').textContent='Sambung ayat '+(k+1)+' dari 3';
  var box=document.createElement('div');box.className='qbox';
  box.innerHTML='<span class="ref"></span><p class="qtext">Lanjutkan ayat berikut:</p><p class="ayah" lang="ar"></p>';
  box.querySelector('.ref').textContent=q.ref;box.querySelector('.ayah').textContent=q.ayah;A.appendChild(box);
  var O=document.createElement('div');O.className='opts';
  q.opts.forEach(function(o){var b=document.createElement('button');b.type='button';b.className='opt ar';b.lang='ar';b.textContent=o.t;
    b.addEventListener('click',function(){O.querySelectorAll('button').forEach(function(x,j){x.disabled=true;if(q.opts[j].ok)x.classList.add('good')});if(!o.ok)b.classList.add('bad');
      T.test.push(o.ok?1:0);setTimeout(function(){if(T.test.length<3){tq();window.scrollTo({top:0,behavior:'smooth'})}else tresult()},900)});
    O.appendChild(b)});
  A.appendChild(O);
}
function tdecide(){
  var why=[],p,alt=null,hl=HAF.filter(function(h){return h[0]===T.haf})[0][1].toLowerCase();
  var tested=T.test.length===3,sc=T.test.reduce(function(a,b){return a+b},0);
  if(kid()){p='TOK';why.push('Usia '+T.usia+' tahun cocok untuk program anak (6–12 tahun).');why.push('Hafalan dimulai bertahap dari surat-surat pendek, didampingi orang tua.');
    if(T.usia<6)why.push('Untuk usia di bawah 6 tahun, admin akan membantu menilai kesiapan ananda terlebih dulu.');}
  else if(T.goal==='pilihan'){p='TOSP';why.push('Sesuai tujuanmu menghafal surat-surat pilihan seperti Al-Mulk, Yasin, dan Ar-Rahman.');why.push('Cukup 3× pertemuan sepekan, ringan dijalani di sela kesibukan.')}
  else if(T.goal==='jaga'){
    if(T.haf>=1){p='MO';why.push('Hafalanmu sudah '+hl+', dan program ini fokus menjaga serta menguatkannya.');why.push('Murajaah setiap hari, tasmi\' menyesuaikan kesiapanmu.')}
    else{p='TOSP';why.push('Murojaah Online mensyaratkan minimal hafal 1 juz. Sambil menuju ke sana, mulailah dari surat-surat pilihan.');alt='TO'}}
  else{
    if(T.time<15){p='TOSP';why.push('Dengan waktu luang kurang dari 15 menit sehari, 3× pertemuan sepekan lebih realistis untuk istiqamah.');alt='TO'}
    else{p='TO';why.push(T.goal==='mulai'?'Program ini membimbing dari awal, setoran rutin bersama halaqah.':'Kamu siap menambah hafalan dengan target 30 juz.');why.push('Waktu luangmu cukup untuk setoran Senin–Jumat.')}
    if(tested&&T.haf>=1&&sc<=1){alt=p;p='MO';why.unshift('Hasil tes sambung ayat menunjukkan hafalanmu perlu dikuatkan dulu sebelum menambah. Hafalan yang kokoh membuat ziyadah lebih ringan.')}
  }
  if(tested&&sc===3&&p!=='TOK')why.push('Tes sambung ayatmu sempurna, masyaAllah. Hafalanmu siap untuk melangkah.');
  var priv=T.style==='private';
  if(priv)why.push('Kamu memilih belajar satu-satu dengan musyrif/musyrifah: jadwal lebih fleksibel dan bisa mulai kapan saja.');
  return {p:p,priv:priv,alt:alt,why:why.filter(Boolean),tested:tested,sc:sc};
}
function tresult(ov){
  var ovFrom=!!ov;
  tprog(1,1);E('t-step').textContent='Hasil';
  var R=tdecide();if(ovFrom){R.p=ov.p;R.priv=ov.priv;R.alt=null;R.why=[ov.why]}
  var P=PROG[R.p],A=E('t-area');A.textContent='';
  var code=R.priv?'Private '+R.p:R.p+P.per;
  var box=document.createElement('div');box.className='pres';
  box.innerHTML='<span class="eyebrow">Hasil tes penempatan</span><p class="muted"></p><div class="pn"></div><span class="code"></span><ul></ul><dl><dt>Jadwal setoran</dt><dd></dd><dt>Biaya</dt><dd></dd><dt>Status</dt><dd></dd></dl><p class="muted tt" style="font-size:.9rem"></p>'+
    '<b>Daftar sekarang</b><label class="tf" for="t-nama">Nama lengkap<input id="t-nama" autocomplete="name" placeholder="Contoh: Fatimah Azzahra"></label><label class="tf" for="t-dom">Domisili (kota/negara)<input id="t-dom" placeholder="Contoh: Makassar, atau Istanbul, Turki"></label>'+
    '<p class="err" id="t-err2" hidden style="color:var(--bad);font-size:.9rem"></p><button class="btn" type="button" id="t-wa">Daftar via WhatsApp</button><p class="muted" style="font-size:.82rem">Admin TOA: +62 823-1409-0180</p>';
  box.querySelector('p.muted').textContent=T.who==='anak'?'Program yang paling cocok untuk ananda:':'Program yang paling cocok untukmu:';
  box.querySelector('.pn').textContent=(R.priv?'Private · ':'')+P.nama;
  box.querySelector('.code').textContent='Kode daftar: '+code;
  var ul=box.querySelector('ul');R.why.forEach(function(w){var li=document.createElement('li');li.textContent=w;ul.appendChild(li)});
  var dd=box.querySelectorAll('dd');
  dd[0].textContent=R.priv?'Senin–Kamis ziyadah, Jumat murajaah (menyesuaikan kesepakatan)':P.jadwal;
  dd[1].textContent=R.priv?'Rp 350 rb':'Pendaftaran Rp 50 rb + Rp 50 rb per periode (4–5 minggu)';
  dd[2].textContent=R.priv?'Buka setiap saat, bisa langsung mulai':'Periode sedang berjalan. Kamu masuk waiting list dan dihubungi saat periode berikutnya dibuka.';
  box.querySelector('.tt').textContent=R.tested?'Tes sambung ayat: '+R.sc+'/3 '+T.test.map(function(x){return x?'✅':'❌'}).join(''):(T.skipTest?'Tes sambung ayat dilewati.':'');
  A.appendChild(box);
  E('t-wa').addEventListener('click',function(){
    var n=E('t-nama').value.trim(),d=E('t-dom').value.trim(),er=E('t-err2');
    if(!n||!d){er.textContent='Lengkapi nama dan domisili dulu.';er.hidden=false;return}er.hidden=true;
    var msg=[code,n,T.usia,T.jk,d].join(' # ');
    var a=document.createElement('a');a.href='https://wa.me/'+ADMIN+'?text='+encodeURIComponent(msg);a.target='_blank';a.rel='noopener';document.body.appendChild(a);a.click();a.remove();
  });
  var alt=document.createElement('div');alt.className='alt';
  var ov=R.priv?{p:R.p,priv:false,why:'Belajar bersama 5–10 santri dalam satu halaqah, lebih hemat.',t:'Pilihan lebih hemat: halaqah '+P.nama,d:'Rp 50 rb per periode, bersama teman satu halaqah.'}:
    {p:R.p,priv:true,why:'Satu santri satu musyrif/musyrifah, bisa mulai kapan saja tanpa menunggu periode baru.',t:'Tidak mau menunggu periode baru? Private '+P.nama,d:'Bisa mulai kapan saja. Rp 350 rb.'};
  if(R.alt&&!R.priv)ov={p:R.alt,priv:false,why:'Pilihan yang kamu ambil setelah tes penempatan.',t:'Pilihan lain: '+PROG[R.alt].nama,d:R.alt==='MO'?'Fokus menjaga hafalan yang sudah ada.':R.alt==='TO'?'Kalau ingin langsung menambah hafalan dengan target 30 juz.':'Surat-surat pilihan, 3× sepekan.'};
  alt.innerHTML='<b></b><span class="muted"></span><button class="link" type="button">Pakai pilihan ini →</button>';
  alt.querySelector('b').textContent=ov.t;alt.querySelector('span').textContent=ov.d;
  if(!ovFrom)alt.querySelector('button').addEventListener('click',function(){tresult(ov)});else alt.hidden=true;
  A.appendChild(alt);
  var r=document.createElement('div');r.className='row';
  r.innerHTML='<button class="btn ghost" type="button">Ulangi tes</button><a class="btn ghost" href="__LANDING__#program" target="_blank" rel="noopener">Lihat semua program</a>';
  r.querySelector('button').addEventListener('click',tstart);A.appendChild(r);
  window.scrollTo({top:0,behavior:'smooth'});
}
if(location.hash==='#tes')tstart();
'''
i = s.rfind('</script>')
s = s[:i] + JS + s[i:]
open(p, 'w').write(s)
print('ok')
