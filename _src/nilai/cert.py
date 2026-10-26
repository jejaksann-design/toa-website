p = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/nilai/lb-section.html'
s = open(p).read()
assert 'lb-cert' not in s

CSS = r'''.lb-certbtn{display:flex;align-items:center;justify-content:center;gap:8px;background:var(--gold-soft);color:var(--ink);border:1.5px solid var(--gold);border-radius:999px;padding:12px 18px;font:inherit;font-weight:600;cursor:pointer}
#lb-cert{border:0;padding:0;background:transparent;max-width:min(760px,calc(100vw - 24px));width:100%}
#lb-cert::backdrop{background:rgba(10,20,12,.6)}
.lb-cbox{background:var(--paper);color:var(--ink);border-radius:20px;padding:16px;display:flex;flex-direction:column;gap:12px;max-height:calc(100vh - 24px);overflow-y:auto}
.lb-cbox img{width:100%;height:auto;border-radius:8px;box-shadow:0 2px 14px rgba(0,0,0,.18);display:block}
.lb-cbox .top{display:flex;justify-content:space-between;align-items:center;gap:10px}
.lb-cbox .acts{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.lb-cbox .acts button.dl{background:var(--green);color:var(--paper);border:0;border-radius:999px;padding:12px 20px;font:inherit;font-weight:600;cursor:pointer}
.lb-cbox .hint{font-size:.84rem;color:var(--muted)}
'''
a = '</style>'
i = s.index(a)
s = s[:i] + CSS + s[i:]

a = '      <div class="lb-reg">'
assert s.count(a) == 1
s = s.replace(a, '      <button class="lb-certbtn" type="button" id="lb-certbtn">🎓 Lihat syahadah digital</button>\n' + a)

a = '<script>'
assert s.count(a) == 1
s = s.replace(a, '''  <dialog id="lb-cert" aria-label="Syahadah digital">
    <div class="lb-cbox">
      <div class="top"><b>Syahadah Digital</b><button class="lb-x" type="button" id="lb-cclose">Tutup</button></div>
      <p class="hint" id="lb-cwait">Menyiapkan syahadah…</p>
      <img id="lb-cimg" alt="" hidden>
      <div class="acts"><button class="dl" type="button" id="lb-cdl" hidden>Unduh syahadah (PNG)</button><span class="hint" id="lb-cmsg"></span></div>
      <p class="hint">Bisa juga tekan lama gambar untuk menyimpan, atau screenshot.</p>
    </div>
  </dialog>

<script>''')

# remember current record in card()
a = "function card(d){\n"
assert s.count(a) == 1
s = s.replace(a, "var CUR=null;\nfunction card(d){\n  CUR=d;\n")

JS = r'''
/* ===== Syahadah digital ===== */
var DL=null;try{window.claude&&window.claude.use&&window.claude.use('downloads').then(function(x){DL=x}).catch(function(){})}catch(e){}
var CBLOB=null,CNAME='';
function fitText(ctx,t,max,size,font){var z=size;do{ctx.font=font.replace('{z}',z);if(ctx.measureText(t).width<=max)break;z-=4}while(z>40);return z}
function drawCert(d){
  var W=2000,H=1414,c=document.createElement('canvas');c.width=W;c.height=H;var x=c.getContext('2d');
  var A=d.g==='A',total=passed().length,nm=d.nama,per=st.per,pr=pred(d);
  var G='#2F6A23',GD='#B8871A',INK='#17231A',MU='#5B6A5F';
  x.fillStyle='#FBFAF4';x.fillRect(0,0,W,H);
  var bg=x.createRadialGradient(W/2,H/2,200,W/2,H/2,1100);bg.addColorStop(0,'rgba(184,135,26,0)');bg.addColorStop(1,'rgba(184,135,26,.10)');x.fillStyle=bg;x.fillRect(0,0,W,H);
  x.strokeStyle=GD;x.lineWidth=10;x.strokeRect(50,50,W-100,H-100);
  x.strokeStyle=G;x.lineWidth=3;x.strokeRect(78,78,W-156,H-156);
  [[78,78],[W-78,78],[78,H-78],[W-78,H-78]].forEach(function(p){x.save();x.translate(p[0],p[1]);x.rotate(Math.PI/4);x.fillStyle=GD;x.fillRect(-16,-16,32,32);x.fillStyle='#FBFAF4';x.fillRect(-7,-7,14,14);x.restore()});
  // logo
  x.save();x.translate(W/2-50,120);x.scale(1,1);
  var lg=x.createLinearGradient(0,100,100,0);lg.addColorStop(0,'#E0B53A');lg.addColorStop(.45,'#E0B53A');lg.addColorStop(.6,'#3B6E1F');lg.addColorStop(1,'#2F5F1C');
  x.strokeStyle=lg;x.lineWidth=11;x.lineCap='round';x.beginPath();x.arc(50,50,38,Math.atan2(38,-3),Math.atan2(37,12)+Math.PI*2,false);x.stroke();
  x.fillStyle='#E0B53A';[[39.5,46.5],[57.5,46.5]].forEach(function(q){x.save();x.translate(q[0],q[1]);x.rotate(Math.PI/4);x.fillRect(-6.5,-6.5,13,13);x.restore()});
  x.restore();
  x.textAlign='center';x.textBaseline='alphabetic';
  x.fillStyle=INK;x.font='700 30px "Plus Jakarta Sans", sans-serif';
  if(x.letterSpacing!==undefined)x.letterSpacing='6px';x.fillText('TAHFIDZ ONLINE ACADEMY',W/2,280);if(x.letterSpacing!==undefined)x.letterSpacing='0px';
  x.fillStyle=G;x.font='700 120px "Amiri", serif';x.direction='rtl';x.fillText('شَهَادَة',W/2,430);x.direction='ltr';
  x.fillStyle=GD;x.font='600 30px "Plus Jakarta Sans", sans-serif';if(x.letterSpacing!==undefined)x.letterSpacing='8px';x.fillText('SYAHADAH KELULUSAN',W/2,495);if(x.letterSpacing!==undefined)x.letterSpacing='0px';
  x.fillStyle=MU;x.font='400 36px "Plus Jakarta Sans", sans-serif';x.fillText('Diberikan kepada',W/2,590);
  var z=fitText(x,nm,W-460,130,'400 {z}px "Instrument Serif", Georgia, serif');x.fillStyle=INK;x.fillText(nm,W/2,720);
  x.strokeStyle=GD;x.lineWidth=2;x.beginPath();x.moveTo(W/2-420,760);x.lineTo(W/2+420,760);x.stroke();
  x.fillStyle=MU;x.font='400 36px "Plus Jakarta Sans", sans-serif';
  x.fillText('atas kelulusannya pada Program Tahfidz Online, Periode '+per+', dengan predikat',W/2,835);
  x.fillStyle=GD;x.font='italic 400 112px "Instrument Serif", Georgia, serif';x.fillText(pr,W/2,965);
  var cols=[['NILAI AKHIR',fmt(d.akhir)],['PERINGKAT','ke-'+d.rank+' dari '+total+' santri '+(A?'akhwat':'ikhwan')],['HALAQAH',d.hk]],cx=[W/2-520,W/2,W/2+520];
  cols.forEach(function(cl,i){x.fillStyle=MU;x.font='600 24px "Plus Jakarta Sans", sans-serif';if(x.letterSpacing!==undefined)x.letterSpacing='4px';x.fillText(cl[0],cx[i],1045);if(x.letterSpacing!==undefined)x.letterSpacing='0px';
    x.fillStyle=INK;x.font=(i===0?'400 58px "Instrument Serif", Georgia, serif':'600 32px "Plus Jakarta Sans", sans-serif');x.fillText(cl[1],cx[i],i===0?1105:1095)});
  x.fillStyle=G;x.font='400 54px "Amiri", serif';x.direction='rtl';x.fillText(A?'بَارَكَ اللهُ فِيكِ وَنَفَعَ بِكِ':'بَارَكَ اللهُ فِيكَ وَنَفَعَ بِكَ',W/2,1195);x.direction='ltr';
  x.textAlign='left';x.fillStyle=INK;x.font='400 46px "Instrument Serif", Georgia, serif';x.fillText('Ustadz San Malique',170,1290);
  x.strokeStyle=INK;x.lineWidth=1.5;x.beginPath();x.moveTo(170,1240);x.lineTo(560,1240);x.stroke();
  x.fillStyle=MU;x.font='400 24px "Plus Jakarta Sans", sans-serif';x.fillText('Founder Tahfidz Online Academy',170,1328);
  x.textAlign='right';var no='TOA/'+per+'/'+(A?'A':'I')+'/'+String(d.rank).padStart(3,'0');
  x.fillStyle=MU;x.font='600 24px "Plus Jakarta Sans", sans-serif';x.fillText('No. Syahadah: '+no,W-170,1290);
  x.font='400 24px "Plus Jakarta Sans", sans-serif';x.fillText('@tahfidzonline.academy',W-170,1328);
  CNAME='Syahadah-TOA-'+per+'-'+nm.replace(/[^A-Za-z0-9]+/g,'-').replace(/^-|-$/g,'')+'.png';
  return c;
}
function openCert(){
  if(!CUR)return;var dl=E('lb-cert'),img=E('lb-cimg'),w=E('lb-cwait'),b=E('lb-cdl'),m=E('lb-cmsg');
  img.hidden=true;w.hidden=false;b.hidden=true;m.textContent='';CBLOB=null;
  var dd=E('lb-dlg');if(dd.open&&dd.close)dd.close();
  if(dl.showModal)dl.showModal();else dl.setAttribute('open','');
  var fl=document.fonts&&document.fonts.load?Promise.all(['400 130px "Instrument Serif"','italic 400 112px "Instrument Serif"','700 120px "Amiri"','400 54px "Amiri"','600 30px "Plus Jakarta Sans"','400 36px "Plus Jakarta Sans"','700 30px "Plus Jakarta Sans"'].map(function(f){return document.fonts.load(f,'Aa شَهَادَة')})).catch(function(){}):Promise.resolve();
  fl.then(function(){
    var c=drawCert(CUR);
    c.toBlob(function(bl){CBLOB=bl;img.src=URL.createObjectURL(bl);img.alt='Syahadah digital '+CUR.nama;img.hidden=false;w.hidden=true;b.hidden=!DL},'image/png');
  });
}
E('lb-certbtn').addEventListener('click',openCert);
E('lb-cclose').addEventListener('click',function(){var dl=E('lb-cert');dl.close?dl.close():dl.removeAttribute('open')});
E('lb-cert').addEventListener('click',function(e){if(e.target===this)this.close()});
E('lb-cdl').addEventListener('click',function(){
  if(!DL||!CBLOB)return;var m=E('lb-cmsg');m.textContent='';
  DL.save({filename:CNAME,data:CBLOB}).then(function(r){m.textContent=r.status==='saved'?'Tersimpan ✓':''}).catch(function(e){
    var c=e&&e.code;if(c==='declined'){m.textContent='Unduhan dibatalkan.'}else if(c==='rate_limited'){m.textContent='Tunggu sebentar, lalu coba lagi.'}else{E('lb-cdl').hidden=true;m.textContent='Unduhan belum tersedia di sini. Tekan lama gambar untuk menyimpan.'}});
});
'''
a = "render();\n})();"
assert s.count(a) == 1
s = s.replace(a, JS + "render();\n})();")
open(p, 'w').write(s)
print('ok')
