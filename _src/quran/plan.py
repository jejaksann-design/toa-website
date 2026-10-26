p = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/quran/kuis-template.html'
s = open(p).read()
assert 'id="s-plan"' not in s

CSS = r'''.plcard{display:grid;grid-template-columns:3.2rem 1fr;gap:14px;align-items:center;text-align:left;background:var(--paper);border:1.5px solid var(--gold);border-radius:18px;padding:18px;cursor:pointer;width:100%}
.plcard .ic{width:3.2rem;height:3.2rem;border-radius:14px;background:var(--gold-soft);display:grid;place-items:center;font-size:1.3rem}
.plcard b{display:block;font-weight:600;font-size:1.05rem}
.plcard span.d{font-size:.9rem;color:var(--muted)}
.pgrid{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.pgrid button{border:1.5px solid var(--line);background:var(--paper);border-radius:12px;padding:10px 0;font-weight:600;cursor:pointer;font-variant-numeric:tabular-nums}
.pgrid button[aria-pressed="true"]{background:var(--green);border-color:var(--green);color:var(--paper)}
@media (max-width:380px){.pgrid{grid-template-columns:repeat(5,1fr)}}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips button{border:1.5px solid var(--line);background:var(--paper);border-radius:999px;padding:8px 14px;font-weight:600;font-size:.9rem;cursor:pointer}
.chips button[aria-pressed="true"]{border-color:var(--green);background:var(--green-soft);color:var(--green)}
.psum{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.psum div{background:var(--green-soft);border-radius:12px;padding:10px 6px;display:flex;flex-direction:column;text-align:center}
.psum b{font-family:var(--display);font-weight:400;font-size:1.7rem;line-height:1.1;font-variant-numeric:tabular-nums}
.psum span{font-size:.74rem;color:var(--muted)}
.days{display:flex;flex-direction:column;border-top:1px solid var(--line)}
.day{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:12px 2px;border-bottom:1px solid var(--line)}
.day input{width:22px;height:22px;accent-color:var(--green)}
.day .w{min-width:0}
.day .w b{display:block;font-weight:600;font-size:.95rem}
.day .w span{font-size:.84rem;color:var(--muted)}
.day .m{font-size:.82rem;color:var(--muted);text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.day.done .w b{text-decoration:line-through;color:var(--muted)}
.warn{font-size:.88rem;background:var(--gold-soft);border-radius:12px;padding:12px 14px}
'''
a = '.loading{'
assert s.count(a) == 1
s = s.replace(a, CSS + a)

a = '    <div class="modes">'
assert s.count(a) == 1
s = s.replace(a, '''    <button class="plcard" id="plan-card" type="button"><span class="ic" aria-hidden="true">📅</span><span><b>Jadwal Murajaah Pintar</b><span class="d">Pilih juz yang sudah kamu hafal, dapatkan jadwal murajaah harian per halaman.</span></span></button>
''' + a)

a = '  <!-- Question -->'
assert s.count(a) == 1
s = s.replace(a, '''  <!-- Plan -->
  <section id="s-plan" hidden style="display:flex;flex-direction:column;gap:18px">
    <button class="link" type="button" data-back>← Kembali</button>
    <div style="display:flex;flex-direction:column;gap:8px"><span class="eyebrow">Jadwal Murajaah Pintar</span><h2>Hafalan terjaga, satu halaman demi satu halaman.</h2></div>
    <div id="pl-form" style="display:flex;flex-direction:column;gap:18px">
      <div style="display:flex;flex-direction:column;gap:10px">
        <b>1. Juz mana saja yang sudah kamu hafal?</b>
        <div class="chips"><button type="button" id="pl-j30">Juz 30 saja</button><button type="button" id="pl-all">Pilih semua</button><button type="button" id="pl-none">Kosongkan</button></div>
        <div class="pgrid" id="pl-grid"></div>
      </div>
      <div style="display:flex;flex-direction:column;gap:10px">
        <b>2. Mau khatam murajaah dalam berapa hari?</b>
        <div class="chips" id="pl-days"></div>
        <label class="tf" for="pl-min" id="pl-minwrap" hidden>Waktu murajaah per hari (menit)<input class="tin" id="pl-min" inputmode="numeric" value="30"></label>
      </div>
      <div style="display:flex;flex-direction:column;gap:10px">
        <b>3. Urutan murajaah</b>
        <div class="chips" id="pl-ord"><button type="button" data-o="desc" aria-pressed="true">Dari Juz 30 ke awal</button><button type="button" data-o="asc" aria-pressed="false">Dari Juz 1 ke akhir</button></div>
      </div>
      <p class="err" id="pl-err" hidden style="color:var(--bad);font-size:.9rem"></p>
      <button class="btn" type="button" id="pl-go" style="align-self:flex-start">Buat jadwal</button>
    </div>
    <div id="pl-out" style="display:flex;flex-direction:column;gap:16px"></div>
  </section>

''' + a)

a = "'s-daily','s-tes']"
assert s.count(a) == 1
s = s.replace(a, "'s-daily','s-tes','s-plan']")

JS = r'''
/* ===== Jadwal Murajaah Pintar ===== */
var PG=__PAGES__, MPP=3, PKEY='toa-jadwal-murajaah';
var JR={};PG.pages.forEach(function(p,i){var j=p[2];if(!JR[j])JR[j]=[i+1,i+1];JR[j][1]=i+1});
var PL={juz:{},days:14,ord:'desc'};
function pload(){try{return JSON.parse(localStorage.getItem(PKEY))||null}catch(e){return null}}
function psave(o){try{localStorage.setItem(PKEY,JSON.stringify(o))}catch(e){}}
var pg=E('pl-grid');
for(var jj=1;jj<=30;jj++){(function(j){var b=document.createElement('button');b.type='button';b.textContent=j;b.setAttribute('aria-pressed','false');b.setAttribute('aria-label','Juz '+j);
  b.addEventListener('click',function(){PL.juz[j]=!PL.juz[j];b.setAttribute('aria-pressed',!!PL.juz[j])});pg.appendChild(b)})(jj)}
function psync(){pg.querySelectorAll('button').forEach(function(b,k){b.setAttribute('aria-pressed',!!PL.juz[k+1])})}
E('pl-j30').addEventListener('click',function(){PL.juz={30:true};psync()});
E('pl-all').addEventListener('click',function(){PL.juz={};for(var j=1;j<=30;j++)PL.juz[j]=true;psync()});
E('pl-none').addEventListener('click',function(){PL.juz={};psync()});
var pd=E('pl-days');
[[7,'7 hari'],[14,'14 hari'],[30,'30 hari'],[0,'Sesuai waktuku']].forEach(function(x){var b=document.createElement('button');b.type='button';b.textContent=x[1];b.dataset.d=x[0];
  b.setAttribute('aria-pressed',x[0]===PL.days);b.addEventListener('click',function(){PL.days=x[0];pd.querySelectorAll('button').forEach(function(y){y.setAttribute('aria-pressed',+y.dataset.d===x[0])});E('pl-minwrap').hidden=x[0]!==0});pd.appendChild(b)});
E('pl-ord').querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){PL.ord=b.dataset.o;E('pl-ord').querySelectorAll('button').forEach(function(y){y.setAttribute('aria-pressed',y===b)})})});
E('plan-card').addEventListener('click',function(){
  show('s-plan');var sv=pload();
  if(sv&&sv.plan){PL.juz=sv.juz;PL.days=sv.days;PL.ord=sv.ord;psync();prender(sv)}else{E('pl-out').textContent='';E('pl-form').hidden=false}
});
function pages(){
  var js=Object.keys(PL.juz).filter(function(j){return PL.juz[j]}).map(Number).sort(function(a,b){return PL.ord==='desc'?b-a:a-b}),out=[];
  js.forEach(function(j){for(var p=JR[j][0];p<=JR[j][1];p++)out.push(p)});return out;
}
function seg(list){
  var parts=[],cur=null;
  list.forEach(function(p){var j=PG.pages[p-1][2];if(cur&&cur.j===j&&p===cur.b+1){cur.b=p}else{cur={j:j,a:p,b:p};parts.push(cur)}});
  return parts.map(function(x){return 'Juz '+x.j+' hlm. '+(x.a===x.b?x.a:x.a+'–'+x.b)}).join(' + ');
}
function startRef(p){var q=PG.pages[p-1];return 'mulai QS '+PG.names[q[0]-1]+': '+q[1]}
E('pl-go').addEventListener('click',function(){
  var L=pages(),er=E('pl-err');er.hidden=true;
  if(!L.length){er.textContent='Pilih minimal satu juz yang sudah kamu hafal.';er.hidden=false;return}
  var D=PL.days;
  if(D===0){var m=parseInt(E('pl-min').value,10);if(!(m>=5&&m<=600)){er.textContent='Isi waktu per hari dalam menit, misalnya 30.';er.hidden=false;return}D=Math.ceil(L.length*MPP/m)}
  D=Math.max(1,Math.min(D,L.length));
  var base=Math.floor(L.length/D),rem=L.length%D,plan=[],k=0;
  for(var d=0;d<D;d++){var n=base+(d<rem?1:0);plan.push(L.slice(k,k+n));k+=n}
  var t=new Date();t.setHours(0,0,0,0);
  var sv={juz:PL.juz,days:PL.days,ord:PL.ord,start:t.getTime(),plan:plan,done:{}};psave(sv);prender(sv);
});
function prender(sv){
  E('pl-form').hidden=true;var O=E('pl-out');O.textContent='';
  var tot=sv.plan.reduce(function(a,x){return a+x.length},0),D=sv.plan.length,ppd=Math.ceil(tot/D);
  var sum=document.createElement('div');sum.className='psum';
  sum.innerHTML='<div><b></b><span>halaman</span></div><div><b></b><span>hari khatam</span></div><div><b></b><span>menit/hari (perkiraan)</span></div>';
  var bs=sum.querySelectorAll('b');bs[0].textContent=tot;bs[1].textContent=D;bs[2].textContent='±'+ppd*MPP;O.appendChild(sum);
  if(ppd>20){var w=document.createElement('p');w.className='warn';w.textContent='Lebih dari 1 juz per hari. Kalau terasa berat, coba target hari yang lebih panjang supaya bisa istiqamah.';O.appendChild(w)}
  var done=Object.keys(sv.done).filter(function(k){return sv.done[k]}).length;
  var pr=document.createElement('div');pr.className='dsteps';pr.style.cssText='height:8px';
  pr.innerHTML='<span class="ok" style="flex:'+(done||0.0001)+'"></span><span style="flex:'+((D-done)||0.0001)+'"></span>';O.appendChild(pr);
  var cap=document.createElement('p');cap.className='muted';cap.style.fontSize='.88rem';cap.textContent=done+' dari '+D+' hari selesai. Centang setiap kali selesai murajaah.';O.appendChild(cap);
  var list=document.createElement('div');list.className='days';
  sv.plan.forEach(function(ps,i){
    var dt=new Date(sv.start+i*864e5),lab=dt.toLocaleDateString('id-ID',{weekday:'short',day:'numeric',month:'short'});
    var row=document.createElement('label');row.className='day'+(sv.done[i]?' done':'');
    row.innerHTML='<input type="checkbox"><span class="w"><b></b><span></span></span><span class="m"></span>';
    row.querySelector('input').checked=!!sv.done[i];
    row.querySelector('b').textContent='Hari '+(i+1)+' · '+lab;
    row.querySelector('.w span').textContent=seg(ps)+' ('+startRef(ps[0])+')';
    row.querySelector('.m').textContent=ps.length+' hlm · ±'+ps.length*MPP+' mnt';
    row.querySelector('input').addEventListener('change',function(){sv.done[i]=this.checked;psave(sv);prender(sv)});
    list.appendChild(row)});
  O.appendChild(list);
  if(done===D){var c=document.createElement('p');c.className='warn';c.textContent='Masya Allah, satu putaran murajaah selesai! Buat jadwal baru untuk putaran berikutnya.';O.appendChild(c)}
  var txt='Jadwal Murajaah · Kuis Tahfidz Online Academy\nKhatam '+tot+' halaman dalam '+D+' hari\n\n'+sv.plan.map(function(ps,i){return 'Hari '+(i+1)+': '+seg(ps)}).join('\n')+'\n\nBuat jadwalmu sendiri: s.id/KuisTOA';
  var r=document.createElement('div');r.className='row';
  r.innerHTML='<a class="btn" target="_blank" rel="noopener">Kirim jadwal ke WhatsApp</a><button class="btn ghost" type="button">Buat jadwal baru</button>';
  r.querySelector('a').href='https://wa.me/?text='+encodeURIComponent(txt);
  r.querySelector('button').addEventListener('click',function(){E('pl-out').textContent='';E('pl-form').hidden=false;window.scrollTo({top:0,behavior:'smooth'})});
  O.appendChild(r);
  var eb=document.createElement('div');eb.className='cta';
  eb.innerHTML='<b>Mau lebih rapi lagi?</b><p>Workbook <i style="font-style:normal;font-weight:600">Murajaah Planner</i> karya Ustadz San Malique membantumu memetakan, merawat, dan memantau hafalan dengan lembar evaluasi.</p><div><a class="btn" href="https://lynk.id/academytahfidzonline/kxdqnk240y6g" target="_blank" rel="noopener">Lihat Murajaah Planner</a></div>';
  O.appendChild(eb);
  var nt=document.createElement('p');nt.className='muted';nt.style.fontSize='.8rem';
  nt.textContent='Nomor halaman mengikuti Mushaf Madinah 604 halaman. Perkiraan waktu ±3 menit per halaman. Progres tersimpan di perangkat ini.';O.appendChild(nt);
  window.scrollTo({top:0,behavior:'smooth'});
}
'''
i = s.rfind('</script>')
s = s[:i] + JS + s[i:]
open(p, 'w').write(s)

ap = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/ebook/apply.py'
a2 = open(ap).read()
if '__PAGES__' not in a2:
    old = ".replace('__BOOKS__', json.dumps(BOOKS, ensure_ascii=False))"
    assert a2.count(old) == 1
    a2 = a2.replace(old, old + " \\\n     .replace('__PAGES__', open(D + 'quran/pages.json').read())")
    open(ap, 'w').write(a2)
print('ok')
