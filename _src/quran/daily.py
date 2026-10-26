p = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/quran/kuis-template.html'
s = open(p).read()
assert 'id="s-daily"' not in s

CSS = r'''.daily{display:flex;flex-direction:column;gap:6px;text-align:left;background:var(--gold-soft);border:1.5px solid var(--gold);border-radius:20px;padding:20px;cursor:pointer;width:100%}
.daily:hover{transform:translateY(-1px)}
.daily b{font-family:var(--display);font-weight:400;font-size:1.8rem;line-height:1.1}
.daily .sub{font-size:.92rem;color:var(--muted)}
.daily .go{align-self:flex-start;margin-top:4px;background:var(--green);color:var(--paper);border-radius:999px;padding:8px 16px;font-weight:600;font-size:.9rem}
.dots{display:flex;gap:6px;font-size:1.3rem;line-height:1;min-height:1.3rem}
.dsteps{display:flex;gap:8px}
.dsteps span{flex:1;height:8px;border-radius:999px;background:var(--line)}
.dsteps span.ok{background:var(--good)}.dsteps span.no{background:var(--bad)}.dsteps span.now{background:var(--gold)}
.dres{background:var(--paper);border:1.5px solid var(--green);border-radius:22px;padding:24px;display:flex;flex-direction:column;gap:14px;text-align:center}
.dres .emo{font-size:2.6rem;letter-spacing:.15em;line-height:1.2}
.dres .chain{font-size:.9rem;color:var(--muted)}
.stats4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.stats4 div{background:var(--green-soft);border-radius:12px;padding:10px 4px;display:flex;flex-direction:column}
.stats4 b{font-family:var(--display);font-weight:400;font-size:1.7rem;line-height:1.1;font-variant-numeric:tabular-nums}
.stats4 span{font-size:.7rem;color:var(--muted);line-height:1.3}
.cd{font-variant-numeric:tabular-nums;font-weight:700;font-size:1.3rem}
.sharebox{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85rem;white-space:pre-wrap;text-align:left;background:var(--bg);border:1px dashed var(--line);border-radius:12px;padding:12px;user-select:all}
'''
a = '.loading{'
assert s.count(a) == 1
s = s.replace(a, CSS + a)

a = '    <div class="modes">'
assert s.count(a) == 1
s = s.replace(a, '''    <button class="daily" id="daily-card" type="button">
      <span class="eyebrow" id="dc-no">Ayat Hari Ini</span>
      <b>Ayat Hari Ini</b>
      <span class="sub" id="dc-sub">3 ayat berantai, satu kesempatan. Soal sama untuk semua orang, berganti setiap hari.</span>
      <span class="dots" id="dc-dots" aria-hidden="true"></span>
      <span class="go" id="dc-go">Main sekarang</span>
    </button>
''' + a)

a = '  <!-- Question -->'
assert s.count(a) == 1
s = s.replace(a, '''  <!-- Daily -->
  <section id="s-daily" hidden style="display:flex;flex-direction:column;gap:16px">
    <button class="link" type="button" data-back>← Kembali</button>
    <div class="qtop"><span id="d-title"></span><span id="d-step"></span></div>
    <div class="dsteps" id="d-steps"><span></span><span></span><span></span></div>
    <div id="d-area"></div>
  </section>

''' + a)

a = "function show(id){['s-menu','s-juz','s-q','s-res']"
assert s.count(a) == 1
s = s.replace(a, "function show(id){['s-menu','s-juz','s-q','s-res','s-daily']")

JS = r'''
/* ===== Ayat Hari Ini ===== */
var SITE='https://claude.ai/artifact/BJWsb8L2PHZ9uoQfeV5r16';
var DAY0=Date.UTC(2026,9,24)/864e5, DSURAH=[18,36,55,56,67], DKEY='toa-ayat-hari-ini';
function dayNo(){return Math.floor((Date.now()+7*36e5)/864e5)-DAY0+1}
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function sshuf(a,r){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(r()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function dload(){try{return JSON.parse(localStorage.getItem(DKEY))||{}}catch(e){return {}}}
function dsave(o){try{localStorage.setItem(DKEY,JSON.stringify(o))}catch(e){}}
var D={n:0,steps:[],res:[]};
function buildDaily(n){
  var r=rng(n*7919+17),V=Q.v,starts=[];
  for(var i=0;i+3<V.length;i++){var s=V[i][0];
    if((V[i][2]===30||DSURAH.indexOf(s)>-1)&&V[i][1]>=2&&V[i+3][0]===s&&V[i+3][1]===V[i][1]+3)starts.push(i)}
  var i0=starts[Math.floor(r()*starts.length)],steps=[];
  for(var k=0;k<3;k++){(function(ci){
    var cur=V[ci],nx=V[ci+1],sur=[],juz=[],seen={},opts=[{t:head(nx[3],7),ok:true}];
    seen[opts[0].t]=1;seen[head(cur[3],7)]=1;
    V.forEach(function(v,x){if(v[1]<2||x===ci||x===ci+1)return;if(v[0]===cur[0])sur.push(x);else if(v[2]===cur[2])juz.push(x)});
    sshuf(sur,r).concat(sshuf(juz,r)).some(function(x){var t=head(V[x][3],7);if(seen[t])return false;seen[t]=1;opts.push({t:t,ok:false});return opts.length===4});
    steps.push({ref:'QS '+Q.names[cur[0]-1]+': '+cur[1],ayah:tail(cur[3],24),opts:sshuf(opts,r),full:nx[3],fullRef:'QS '+Q.names[nx[0]-1]+': '+nx[1]});
  })(i0+k)}
  return {n:n,steps:steps,chain:'QS '+Q.names[V[i0][0]-1]+': '+V[i0][1]+'–'+V[i0+3][1]};
}
function emo(res){return res.map(function(x){return x?'🟩':'🟥'}).join('')}
function dcard(){
  var n=dayNo(),st=dload(),done=st.last===n&&st.res&&st.res.length===3;
  E('dc-no').textContent='Ayat Hari Ini #'+n;
  E('dc-dots').textContent=st.last===n&&st.res?emo(st.res):'';
  E('dc-go').textContent=done?'Lihat hasil hari ini':(st.last===n&&st.res&&st.res.length?'Lanjutkan':'Main sekarang');
}
E('daily-card').addEventListener('click',function(){
  var n=dayNo();show('s-daily');E('d-title').textContent='Ayat Hari Ini #'+n;E('d-step').textContent='';
  E('d-area').innerHTML='<p class="loading">Membuka mushaf…</p>';
  loadQuran().then(function(){
    var g=buildDaily(n),st=dload();D={n:n,steps:g.steps,chain:g.chain,res:st.last===n&&st.res?st.res.slice():[]};
    if(D.res.length>=3)dresult();else dstep();
  }).catch(function(){E('d-area').innerHTML='<p class="loading">Teks Al-Qur\'an belum termuat. Periksa koneksi, lalu coba lagi.</p>'});
});
function dbar(cur){E('d-steps').querySelectorAll('span').forEach(function(sp,k){sp.className=k<D.res.length?(D.res[k]?'ok':'no'):(k===cur?'now':'')})}
function dstep(){
  var k=D.res.length,q=D.steps[k],A=E('d-area');A.textContent='';
  E('d-step').textContent='Ayat '+(k+1)+' dari 3';dbar(k);
  var box=document.createElement('div');box.className='qbox';
  box.innerHTML='<span class="ref"></span><p class="qtext">Lanjutkan ayat berikut:</p><p class="ayah" lang="ar"></p>';
  box.querySelector('.ref').textContent=q.ref;box.querySelector('.ayah').textContent=q.ayah;A.appendChild(box);
  var O=document.createElement('div');O.className='opts';
  q.opts.forEach(function(o){var b=document.createElement('button');b.type='button';b.className='opt ar';b.lang='ar';b.textContent=o.t;
    b.addEventListener('click',function(){
      O.querySelectorAll('button').forEach(function(x,j){x.disabled=true;if(q.opts[j].ok)x.classList.add('good')});
      if(!o.ok)b.classList.add('bad');
      D.res.push(o.ok?1:0);var st=dload();st.last=D.n;st.res=D.res.slice();
      if(D.res.length===3)stats(st);dsave(st);dbar(-1);
      var f=document.createElement('div');f.className='fb '+(o.ok?'good':'bad');
      f.innerHTML='<b></b><span class="muted" style="font-size:.85rem"></span><p class="ayah" lang="ar"></p>';
      f.querySelector('b').textContent=o.ok?'Benar, masyaAllah!':'Belum tepat.';
      f.querySelector('span').textContent='Ayat lengkapnya, '+q.fullRef+':';f.querySelector('.ayah').textContent=q.full;
      var nb=document.createElement('button');nb.type='button';nb.className='btn';nb.style.alignSelf='flex-start';nb.style.marginTop='6px';
      nb.textContent=D.res.length<3?'Ayat berikutnya':'Lihat hasil';
      nb.addEventListener('click',function(){if(D.res.length<3){dstep();window.scrollTo({top:0,behavior:'smooth'})}else dresult()});
      f.appendChild(nb);A.appendChild(f);nb.focus({preventScroll:true});f.scrollIntoView({behavior:'smooth',block:'nearest'});
    });O.appendChild(b)});
  A.appendChild(O);
}
function stats(st){
  if(st.counted===D.n)return;st.counted=D.n;
  st.played=(st.played||0)+1;if(D.res.every(Boolean))st.perfect=(st.perfect||0)+1;
  st.streak=st.prevDay===D.n-1?(st.streak||0)+1:1;st.prevDay=D.n;st.best=Math.max(st.best||0,st.streak);
}
var cdTimer=null;
function dresult(){
  dbar(-1);E('d-step').textContent='Selesai';
  var st=dload(),sc=D.res.reduce(function(a,b){return a+b},0),A=E('d-area');A.textContent='';
  var msg=sc===3?['Masya Allah, sempurna!','Tiga ayat tersambung semua. Jaga streak-mu besok.']:sc===2?['Hampir sempurna!','Satu ayat lagi menuju 🟩🟩🟩. Besok ada rangkaian baru.']:sc===1?['Tetap semangat!','Murajaah sedikit demi sedikit, besok coba lagi.']:['Yuk murajaah lagi!','Tidak apa-apa. Baca ulang rangkaian hari ini, besok insyaAllah lebih lancar.'];
  var share='Ayat Hari Ini #'+D.n+' · Kuis TOA\n'+emo(D.res)+'\n'+sc+'/3 ayat tersambung\n\nMain juga: '+SITE;
  var R=document.createElement('div');R.className='dres';
  R.innerHTML='<span class="eyebrow"></span><div class="emo"></div><h3></h3><p class="muted"></p><p class="chain"></p>'+
    '<div class="stats4"><div><b></b><span>Dimainkan</span></div><div><b></b><span>Streak</span></div><div><b></b><span>Streak terbaik</span></div><div><b></b><span>Sempurna</span></div></div>'+
    '<div class="sharebox"></div><div class="row" style="justify-content:center"><button class="btn" type="button">Salin hasil</button><a class="btn ghost" target="_blank" rel="noopener">Bagikan ke WhatsApp</a></div>'+
    '<p class="muted" style="font-size:.88rem">Ayat berikutnya dalam <span class="cd"></span></p>';
  R.querySelector('.eyebrow').textContent='Ayat Hari Ini #'+D.n;R.querySelector('.emo').textContent=emo(D.res);
  R.querySelector('h3').textContent=msg[0];R.querySelector('p.muted').textContent=msg[1];
  R.querySelector('.chain').textContent='Rangkaian hari ini: '+D.chain;
  var bs=R.querySelectorAll('.stats4 b');[st.played||1,st.streak||1,st.best||1,st.perfect||0].forEach(function(v,k){bs[k].textContent=v});
  var sb=R.querySelector('.sharebox');sb.textContent=share;
  var cb=R.querySelector('button.btn');cb.addEventListener('click',function(){
    navigator.clipboard.writeText(share).then(function(){cb.textContent='Tersalin ✓'},function(){var rg=document.createRange();rg.selectNodeContents(sb);var se=getSelection();se.removeAllRanges();se.addRange(rg);cb.textContent='Teks dipilih, salin manual'});
    setTimeout(function(){cb.textContent='Salin hasil'},2500)});
  R.querySelector('a.btn').href='https://wa.me/?text='+encodeURIComponent(share);
  A.appendChild(R);
  var more=document.createElement('div');more.className='row';
  more.innerHTML='<button class="btn ghost" type="button">Main kuis lainnya</button>';
  more.querySelector('button').addEventListener('click',function(){show('s-menu')});A.appendChild(more);
  var cd=R.querySelector('.cd');clearInterval(cdTimer);
  function tick(){var now=Date.now()+7*36e5,left=864e5-now%864e5,h=Math.floor(left/36e5),m=Math.floor(left%36e5/6e4),s=Math.floor(left%6e4/1e3);
    cd.textContent=[h,m,s].map(function(x){return String(x).padStart(2,'0')}).join(':');if(left<1500)setTimeout(function(){dcard()},1600)}
  tick();cdTimer=setInterval(tick,1000);
  dcard();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('[data-back]').forEach(function(b){b.addEventListener('click',function(){clearInterval(cdTimer);dcard()})});
dcard();
'''
i = s.rfind('</script>')
s = s[:i] + JS + s[i:]
open(p, 'w').write(s)
print('ok')
