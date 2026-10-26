var QARI=[['Alafasy_128kbps','Mishary Rasyid Alafasy (Kuwait)'],['Husary_64kbps','Mahmud Khalil Al-Husary (Mesir)'],['Minshawy_Murattal_128kbps','Muhammad Shiddiq Al-Minsyawi (Mesir)'],['Abdurrahmaan_As-Sudais_192kbps','Abdurrahman As-Sudais (Makkah)'],['Saood_ash-Shuraym_128kbps','Su\'ud Asy-Syuraim (Makkah)'],['Abu_Bakr_Ash-Shaatree_128kbps','Abu Bakr Asy-Syatiri (Saudi)'],['Hani_Rifai_192kbps','Hani Ar-Rifa\'i (Saudi)']];
var AR='٠١٢٣٤٥٦٧٨٩';function arn(n){return String(n).replace(/\d/g,function(d){return AR[d]})}
function E(id){return document.getElementById(id)}
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
var Q=null,PG=__PAGES__,IDX={},P=0,OPEN=[],HINT=false;
// --- picker
var jg=E('jgrid');for(var j=1;j<=30;j++){(function(j){var b=document.createElement('button');b.type='button';b.textContent=j;b.setAttribute('aria-label','Juz '+j);b.addEventListener('click',function(){pickJuz(j,b)});jg.appendChild(b)})(j)}
function pickJuz(j,btn){jg.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===btn)});
  var g=E('pgrid2');g.textContent='';E('pg-h').textContent='Juz '+j+': pilih halaman';
  PG.pages.forEach(function(x,i){if(x[2]!==j)return;var b=document.createElement('button');b.type='button';b.textContent=i+1;b.setAttribute('aria-label','Halaman '+(i+1));b.addEventListener('click',function(){openPage(i+1)});g.appendChild(b)});
  E('pgwrap').hidden=false;E('pgwrap').scrollIntoView({behavior:'smooth',block:'nearest'})}
E('pk-tabs').querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){
  E('pk-tabs').querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
  E('pk-juz').hidden=b.dataset.t!=='juz';E('pk-surah').hidden=b.dataset.t!=='surah';E('pk-surah').style.display=b.dataset.t==='surah'?'flex':'';E('pk-surah').style.flexDirection='column';E('pk-surah').style.gap='10px'})});
PG.names.forEach(function(n,i){var o=document.createElement('option');o.value=i+1;o.textContent=(i+1)+'. '+n;E('ssel').appendChild(o)});
E('sgo').addEventListener('click',function(){var s=+E('ssel').value;for(var i=PG.pages.length-1;i>=0;i--){var x=PG.pages[i];if(x[0]<s||(x[0]===s&&x[1]<=1)){openPage(i+1);return}}});
QARI.forEach(function(q){var o=document.createElement('option');o.value=q[0];o.textContent=q[1];E('qsel').appendChild(o)});
if(ls('toa-qari'))E('qsel').value=ls('toa-qari');
E('qsel').addEventListener('change',function(){ls('toa-qari',E('qsel').value);stopAudio()});
// --- data
function loadQ(){if(Q)return Promise.resolve();return fetch('/kuis/quran.json').then(function(r){return r.json()}).then(function(d){Q=d;d.v.forEach(function(v,i){IDX[v[0]*1000+v[1]]=i})})}
function range(p){var a=PG.pages[p-1],b=PG.pages[p],i0=IDX[a[0]*1000+a[1]],i1=b?IDX[b[0]*1000+b[1]]:Q.v.length;return [i0,i1]}
function splitBas(v){var w=v[3].split(' ');if(v[1]===1&&v[0]!==1&&v[0]!==9)return [w.slice(0,4).join(' '),w.slice(4).join(' ')];return [null,v[3]]}
// --- viewer
function openPage(p){if(!(history.state&&history.state.toa))history.pushState({toa:1},'');E('picker').hidden=true;E('viewer').hidden=false;E('ayat').innerHTML='<p class="muted">Membuka mushaf…</p>';
  loadQ().then(function(){render(p);E('viewer').scrollIntoView({behavior:'smooth'})}).catch(function(){E('ayat').innerHTML='<p class="err">Teks Al-Qur\'an belum termuat. Periksa koneksi, lalu coba lagi.</p>'})}
function render(p){stopAudio();P=p;ls('toa-blank-page',p);var r=range(p),A=E('ayat');A.textContent='';OPEN=[];
  var surs={};for(var i=r[0];i<r[1];i++)surs[Q.v[i][0]]=1;
  E('v-h').textContent='Halaman '+p+' · Juz '+PG.pages[p-1][2];E('v-s').textContent=Object.keys(surs).map(function(s){return Q.names[s-1]}).join(' · ');
  E('prev').disabled=p<=1;E('next').disabled=p>=604;
  for(var i=r[0];i<r[1];i++){(function(i){var v=Q.v[i],sp=splitBas(v);
    if(v[1]===1){var h=document.createElement('div');h.className='sh';h.textContent='Surah '+Q.names[v[0]-1];A.appendChild(h);
      if(sp[0]){var bs=document.createElement('div');bs.className='bas';bs.lang='ar';bs.textContent=sp[0];A.appendChild(bs)}}
    var b=document.createElement('button');b.type='button';b.className='ay closed';b.dataset.i=i;
    var tx=document.createElement('span');tx.className='tx';tx.lang='ar';var no=document.createElement('span');no.className='no';no.textContent=v[1];
    b.append(tx,no);b._t=sp[1];b.addEventListener('click',function(){setOpen(b,b.classList.contains('closed'))});A.appendChild(b);OPEN.push(b);paint(b)})(i)}
}
function paint(b){var tx=b.firstChild,closed=b.classList.contains('closed');tx.textContent='';
  if(!closed){tx.textContent=b._t+' ﴿'+arn(b.lastChild.textContent)+'﴾';return}
  var w=b._t.split(' ');if(HINT){tx.append(w[0]+' ')}
  var n=Math.max(1,Math.min(6,Math.round(w.length/3)));for(var k=0;k<n;k++){var s=document.createElement('span');s.className='blank';s.style.width=(2.2+((k*37)%3))+'em';s.style.marginInline='.18em';tx.appendChild(s)}}
function setOpen(b,o){b.classList.toggle('closed',!o);paint(b)}
E('t-next').addEventListener('click',function(){var b=OPEN.filter(function(x){return x.classList.contains('closed')})[0];if(b){setOpen(b,true);b.scrollIntoView({behavior:'smooth',block:'center'})}});
E('t-all').addEventListener('click',function(){OPEN.forEach(function(b){setOpen(b,true)})});
E('t-none').addEventListener('click',function(){OPEN.forEach(function(b){setOpen(b,false)})});
E('t-hint').addEventListener('click',function(){HINT=!HINT;E('t-hint').setAttribute('aria-pressed',HINT);OPEN.forEach(paint)});
E('prev').addEventListener('click',function(){if(P>1)render(P-1)});E('next').addEventListener('click',function(){if(P<604)render(P+1)});
// --- recorder
var MR=null,CH=[],T0=0,TM=null,BLOB=null;
function fmt(s){return Math.floor(s/60)+':'+('0'+Math.floor(s%60)).slice(-2)}
E('r-btn').addEventListener('click',function(){
  if(MR&&MR.state==='recording'){MR.stop();return}
  E('r-err').hidden=true;
  if(!navigator.mediaDevices||!window.MediaRecorder){E('r-err').textContent='Browser ini belum bisa merekam. Coba buka di Safari atau Chrome terbaru.';E('r-err').hidden=false;return}
  navigator.mediaDevices.getUserMedia({audio:true}).then(function(st){
    var mt=MediaRecorder.isTypeSupported&&MediaRecorder.isTypeSupported('audio/mp4')?'audio/mp4':'';
    MR=new MediaRecorder(st,mt?{mimeType:mt}:undefined);CH=[];
    MR.ondataavailable=function(e){if(e.data.size)CH.push(e.data)};
    MR.onstop=function(){st.getTracks().forEach(function(t){t.stop()});clearInterval(TM);E('r-btn').classList.remove('recording');E('r-btn').textContent='Rekam ulang';
      BLOB=new Blob(CH,{type:MR.mimeType||'audio/mp4'});var u=URL.createObjectURL(BLOB);E('r-audio').src=u;
      var ext=/webm/.test(BLOB.type)?'webm':'m4a';E('r-dl').href=u;E('r-dl').download='setoran-halaman-'+P+'.'+ext;E('r-out').hidden=false;E('r-out').style.display='flex'};
    MR.start();T0=Date.now();E('r-btn').classList.add('recording');E('r-btn').textContent='⏹ Berhenti';
    TM=setInterval(function(){E('r-time').textContent='● '+fmt((Date.now()-T0)/1000)},500);
  }).catch(function(){E('r-err').textContent='Izin mikrofon ditolak. Aktifkan mikrofon untuk website ini di pengaturan browser.';E('r-err').hidden=false})});
E('r-share').addEventListener('click',function(){if(!BLOB)return;var ext=/webm/.test(BLOB.type)?'webm':'m4a';
  var f=new File([BLOB],'setoran-halaman-'+P+'.'+ext,{type:BLOB.type});
  if(navigator.canShare&&navigator.canShare({files:[f]}))navigator.share({files:[f],title:'Setoran halaman '+P,text:'Setoran hafalan halaman '+P+' (Mushaf Blank, tahfidzonline.com/hafalan)'}).catch(function(){});
  else E('r-dl').click()});
// --- murattal
var AU=new Audio(),QU=[],QI=0,PLAY=false,REP=false,SHOW=true;AU.preload='auto';
function url(s,a){return 'https://everyayah.com/data/'+E('qsel').value+'/'+('00'+s).slice(-3)+('00'+a).slice(-3)+'.mp3'}
function queue(){var r=range(P),q=[];for(var i=r[0];i<r[1];i++){var v=Q.v[i];if(v[1]===1&&v[0]!==1&&v[0]!==9)q.push({s:1,a:1,b:null});q.push({s:v[0],a:v[1],b:OPEN[i-r[0]]})}return q}
function hl(b){OPEN.forEach(function(x){x.classList.toggle('playing',x===b)});if(b){if(SHOW)setOpen(b,true);b.scrollIntoView({behavior:'smooth',block:'center'})}}
function playI(){var it=QU[QI];if(!it){if(REP){QI=0;return playI()}stopAudio();E('m-now').textContent='Selesai satu halaman ✓';return}
  AU.src=url(it.s,it.a);AU.play().catch(function(){});hl(it.b);E('m-now').textContent=it.b?Q.names[it.s-1]+' : '+it.a:'Basmalah'}
AU.addEventListener('ended',function(){if(PLAY){QI++;playI()}});
AU.addEventListener('error',function(){if(!PLAY)return;E('m-err').textContent='Audio qari ini belum bisa diputar. Coba qari lain atau periksa koneksi.';E('m-err').hidden=false;stopAudio()});
function stopAudio(){PLAY=false;AU.pause();E('m-btn').textContent='▶ Putar halaman ini';hl(null);E('m-now').textContent=''}
E('m-btn').addEventListener('click',function(){if(!Q)return;E('m-err').hidden=true;
  if(PLAY){PLAY=false;AU.pause();E('m-btn').textContent='▶ Lanjutkan';return}
  if(E('m-btn').textContent.indexOf('Lanjutkan')>=0&&AU.src){PLAY=true;AU.play();E('m-btn').textContent='⏸ Jeda';return}
  QU=queue();QI=0;PLAY=true;E('m-btn').textContent='⏸ Jeda';playI()});
E('m-rep').addEventListener('click',function(){REP=!REP;E('m-rep').setAttribute('aria-pressed',REP)});
E('m-show').addEventListener('click',function(){SHOW=!SHOW;E('m-show').setAttribute('aria-pressed',SHOW)});
// resume last page
var last=+ls('toa-blank-page');if(last>=1&&last<=604){E('pg-h').textContent='';var lb=document.createElement('button');lb.type='button';lb.className='btn ghost';lb.style.alignSelf='flex-start';lb.textContent='Lanjutkan halaman '+last;lb.addEventListener('click',function(){openPage(last)});E('picker').appendChild(lb)}
if(/^#p\d+$/.test(location.hash))openPage(Math.min(604,Math.max(1,+location.hash.slice(2))));

function backPick(){stopAudio();E('viewer').hidden=true;E('picker').hidden=false;window.scrollTo({top:0,behavior:'smooth'})}
E('v-back').addEventListener('click',function(){if(history.state&&history.state.toa)history.back();else backPick()});
window.addEventListener('popstate',backPick);
