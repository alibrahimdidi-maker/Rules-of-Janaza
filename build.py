# -*- coding: utf-8 -*-
"""
SHA0302 site builder
--------------------
Run:   python3 build.py
Reads: this folder (00_15weeks.html, topicNN.html, _shell_top.html)
Makes: ../site/index.html  (single self-contained page)
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
rd = lambda n: open(os.path.join(HERE, n), encoding='utf8').read()

# ------------------------------------------------------------------ topics
# (file, label shown on the badge, first topic number used by the release switch)
TOPICS = [
    ('topic01.html',    '1',   1),
    ('topic02.html',    '2',   2),
    ('topic03.html',    '3',   3),
    ('topic04.html',    '4',   4),
    ('topic05.html',    '5',   5),
    ('topic06_07.html', '6-7', 6),
    ('topic08.html',    '8',   8),
    ('topic09.html',    '9',   9),
    ('topic10.html',    '10',  10),
    ('topic11.html',    '11',  11),
    ('topic12.html',    '12',  12),
    ('topic13.html',    '13',  13),
]

# ------------------------------------------------------------------ css scoper
def scope_css(css, prefix):
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            depth += (css[k] == '{') - (css[k] == '}')
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith('@media'):
            out.append(head + '{' + scope_css(body, prefix) + '}')
        else:
            sels = ','.join(prefix + ' ' + s.strip() for s in head.split(','))
            out.append(sels + '{' + body + '}')
        i = k
    return '\n'.join(out)

# ------------------------------------------------------------------ part 1 (15 weeks)
w = rd('00_15weeks.html')
css15 = re.search(r'<style>(.*?)</style>', w, re.S).group(1)
body15 = re.search(r'<body[^>]*>(.*?)</body>', w, re.S).group(1).strip()
body15 = body15.replace('class="wrap"', 'class="p1wrap"', 1)
body15 = body15.replace('onclick="window.print()"', "onclick=\"printPart('p1')\"")
css15 = css15.replace('.wrap{', '.p1wrap{', 1)
css15 = css15.replace('@media print { .printbtn{display:none !important;} }', '')
css15 = scope_css(css15, '#part1')

# ------------------------------------------------------------------ part 2 (topics)
acc = []
for idx, (fn, label, first) in enumerate(TOPICS, 1):
    frag = rd(fn).strip()
    title = re.search(r'<h1[^>]*>(.*?)</h1>', frag, re.S).group(1).strip()
    frag = frag.replace('onclick="window.print()"', "onclick=\"printPart('p2')\"")
    acc.append(
        '<details class="week-acc" id="weekAcc%d" data-topic="%d">\n'
        '  <summary><span class="week-num">ޓޮޕިކް %s</span><span class="week-title">%s</span>'
        '<span class="week-chev">&#9660;</span></summary>\n'
        '  <div class="week-body">\n%s\n  </div>\n</details>\n' % (idx, first, label, title, frag))
acc = '\n'.join(acc)

# ------------------------------------------------------------------ extra css
EXTRA_CSS = r"""
/* ===== v2: two-part layout ===== */
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;}
img,svg,video,iframe{max-width:100%;}
.part-nav{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:0 0 20px;}
.part-nav a{flex:1 1 220px;max-width:340px;text-align:center;text-decoration:none;cursor:pointer;
  background:#fff;color:#08281f;border:2px solid #d4af37;border-radius:30px;padding:10px 16px;
  font-weight:bold;font-size:clamp(13px,1.6vw,16px);box-shadow:0 4px 12px rgba(8,40,31,.15);}
.part-nav a b{display:inline-block;background:#12503a;color:#f4d03f;border-radius:50%;
  width:24px;height:24px;line-height:24px;margin-left:6px;font-size:13px;}
.part-head{border-radius:14px;padding:16px 14px;text-align:center;margin:0 0 18px;
  box-shadow:0 8px 24px rgba(8,40,31,.25);border:2px solid #d4af37;color:#fff;}
.part-head .pno{display:inline-block;background:#fff;color:#08281f;border:2px solid #d4af37;
  border-radius:20px;padding:3px 16px;font-weight:bold;font-size:clamp(12px,1.5vw,15px);margin-bottom:8px;}
.part-head h2{margin:0;font-size:clamp(18px,2.6vw,26px);text-shadow:2px 2px 6px rgba(0,0,0,.4);line-height:1.7;}
.part-head p{margin:6px 0 0;color:#f2e6bf;font-size:clamp(13px,1.6vw,16px);line-height:1.8;}
#part1 .part-head{background:linear-gradient(135deg,#7a1f1f 0%,#a3372f 100%);}
#part2 .part-head{background:linear-gradient(135deg,#08281f 0%,#12503a 100%);}
.part-divider{margin:44px 0 34px;text-align:center;}
.part-divider .rule{height:0;border-top:4px double #b7862e;margin:0 auto 18px;max-width:560px;}
.part-divider .note{display:inline-block;max-width:680px;background:#fff8dc;border:2px dashed #b7862e;
  border-radius:14px;padding:14px 18px;color:#5a4319;font-size:clamp(13px,1.6vw,16px);line-height:2;
  box-shadow:0 6px 16px rgba(0,0,0,.1);}
.part-divider .note strong{color:#7a1f1f;}
.part-divider .arrow{display:block;color:#b7862e;font-size:26px;margin-top:8px;line-height:1;}
.to-top{display:block;text-align:center;margin:14px 0 4px;}
.to-top a{color:#12503a;font-weight:bold;font-size:14px;cursor:pointer;text-decoration:underline;}
html{scroll-behavior:smooth;}

/* ===== responsive: phones / tablets ===== */
@media(max-width:900px){
  body{padding:10px 6px 40px;}
  #courseContent{padding:50px 8px 20px;border-radius:14px;}
}
@media(max-width:600px){
  body{padding:8px 4px 70px;}
  #courseContent{padding:46px 6px 16px;border-radius:12px;margin-top:16px;}
  .hero{padding:22px 12px !important;margin:8px auto !important;}
  .hero h1{font-size:clamp(20px,6.2vw,30px) !important;}
  .hero h1 span{font-size:clamp(14px,4.2vw,20px) !important;display:block;}
  .hero h2{font-size:clamp(13px,4vw,18px) !important;}
  .hero img{width:68px !important;height:68px !important;}
  .hero div[style*="width: 320px"]{width:100% !important;max-width:320px;height:auto !important;aspect-ratio:16/9;}
  .hero input#gateInput{width:80px !important;}
  .imam-card details>summary{padding:12px 14px !important;font-size:16px !important;}
  .imam-card .accordion-content{padding:16px 12px 10px !important;font-size:15.5px !important;line-height:2 !important;}
  details.week-acc>summary{padding:11px 10px;gap:8px;}
  .week-num{padding:4px 10px;}
  .week-body{padding:10px 4px;}
  .part-nav a{flex-basis:100%;max-width:none;}
  /* topic slides (inline-styled fragments) */
  .week-body>div{padding:14px 10px !important;margin:6px auto !important;border-width:2px !important;border-radius:12px !important;}
  .week-body>div>div:first-of-type{padding:22px 12px !important;margin-top:34px !important;}
  .week-body>div>a[onclick]{top:8px !important;left:8px !important;padding:6px 10px !important;font-size:12px !important;}
  .week-body details>summary{padding:10px 10px !important;gap:8px !important;}
  .week-body details>div{padding:16px 12px !important;}
  .week-body details ul,.week-body details ol{padding-right:20px !important;}
  .week-body details p{text-align:right !important;}
  /* part 1 */
  #part1 .p1wrap{padding:14px 10px;margin:6px auto;border-width:2px;}
  #part1 .maintitle{padding:22px 12px;margin-top:34px;}
  #part1 .printbtn{top:8px;left:8px;padding:6px 10px;font-size:12px;}
  #part1 .weekbanner{padding:10px 12px;margin:22px 0 12px;}
  #part1 summary.slidehead{padding:10px 10px;gap:8px;}
  #part1 .slidebody{padding:16px 12px;}
  #part1 .slidebody p{text-align:right;}
  #part1 .ulbox{padding-right:20px;text-align:right;}
  /* floating bar -> slim bottom bar */
  #printBar{top:auto !important;bottom:8px;left:8px;right:8px;flex-direction:row;justify-content:center;pointer-events:none;}
  #printBar .btn{display:none;}
  #printBar .btn2{pointer-events:auto;font-size:12px;padding:8px 14px;text-align:center;}
}
/* mind-map: stack on very small screens */
@media(max-width:480px){
  .week-body div[style*="direction:rtl;align-items:center;justify-content:center"]{flex-direction:column !important;}
  .week-body div[style*="direction:rtl;align-items:center;justify-content:center"]>div{
    flex:none !important;width:100% !important;min-width:0 !important;margin:6px 0 !important;padding-left:0 !important;padding-right:0 !important;}
}

/* ===== print ===== */
@media print{
  body:not(.print-all) .hero,body:not(.print-all) .imam-card,body:not(.print-all) .part-nav,
  body:not(.print-all) .part-divider,body:not(.print-all) #part1 .part-head,body:not(.print-all) #part2 .part-head{display:none !important;}
  body:not(.print-all):not(.print-p1) #part1{display:none !important;}
  body.print-p1 #part2,body.print-p1 .part-divider,body.print-p1 .part-nav{display:none !important;}
  body.print-p1 .hero,body.print-p1 .imam-card{display:none !important;}
  #courseContent{padding:0;margin:0;background:none;}
}
"""

# ------------------------------------------------------------------ shell top (head + hero + intro)
top = rd('_shell_top.html')
# font: fonts/ folder next to index.html
top = re.sub(r"src:url\('fonts/Faruma.ttf'\) format\('truetype'\);",
             "src:url('fonts/Faruma.ttf') format('truetype'),local('Faruma'),local('A_Faruma');", top, 1)
# allow pinch-zoom on phones
top = top.replace('touch-action:pan-y;', 'touch-action:pan-y pinch-zoom;', 1)
# theme colour + hero class
top = top.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                  '<meta name="theme-color" content="#08281f">', 1)
top = top.replace('<body>\n<div dir="rtl"\n  style="font-family', '<body>\n<div class="hero" dir="rtl"\n  style="font-family', 1)
assert 'class="hero"' in top, 'hero class patch failed'
part1_css = '\n/* ===== part 1: 15-week file (scoped) ===== */\n' + css15 + '\n'
top = top.replace('</style>', EXTRA_CSS + part1_css + '</style>', 1)

# ------------------------------------------------------------------ course content
content = '''<div class="course-wrap" id="courseContent">

<div class="part-nav no-print">
  <a data-goto="part1"><b>1</b> 15 ހަފްތާގެ ޚުލާޞާ ސްލައިޑްތައް</a>
  <a data-goto="part2"><b>2</b> ޓޮޕިކް ވަކިވަކިން ތަފްޞީލީ ސްލައިޑްތައް</a>
</div>

<!-- ============================ PART 1 ============================ -->
<section id="part1">
<div class="part-head">
  <span class="pno">ބައި 1</span>
  <h2>15 ހަފްތާގެ ޚުލާޞާ ސްލައިޑްތައް</h2>
  <p>ކޯހުގެ 15 ހަފްތާ އެއްކޮށް — ހަފްތާއަކުން ހަފްތާއަކަށް ކުރު ސްލައިޑްތައް</p>
</div>
''' + body15 + '''
</section>

<!-- ============================ DIVIDER ============================ -->
<div class="part-divider">
  <div class="rule"></div>
  <div class="note">
    <strong>ފާހަގަ:</strong> މީގެ މަތީގައި ވަނީ <strong>15 ހަފްތާގެ ޚުލާޞާ ސްލައިޑްތަކެވެ.</strong><br>
    މީގެ ތިރީގައި ވަނީ <strong>ކޮންމެ ޓޮޕިކެއްގެ ތަފްޞީލީ ސްލައިޑްތަކެވެ.</strong>
    <span class="arrow">&#9660;</span>
  </div>
</div>

<!-- ============================ PART 2 ============================ -->
<section id="part2">
<div class="part-head">
  <span class="pno">ބައި 2</span>
  <h2>ޓޮޕިކް ވަކިވަކިން ތަފްޞީލީ ސްލައިޑްތައް</h2>
  <p>Rules of Janazah — SHA0302 · ބޭނުންފުޅުވާ ޓޮޕިކެއް ހުޅުވުމަށް ފިއްތަވާ (އެއް ފަހަރާ ހުޅުވޭނީ އެންމެ ޓޮޕިކެއް)</p>
</div>

''' + acc + '''
<div class="to-top no-print"><a data-goto="part1">&#9650; 15 ހަފްތާގެ ޚުލާޞާ ބައިއަށް ދާން</a></div>
</section>

</div>
'''

# ------------------------------------------------------------------ scripts
bottom = r'''
<script src="config.js"></script>
<script>
(function(){
  var CORRECT_CODE = 'SHA0302';
  var STORAGE_KEY = 'sha0302-course-unlocked';
  var input = document.getElementById('gateInput');
  var msg = document.getElementById('gateMsg');
  var content = document.getElementById('courseContent');

  function unlock(scroll){
    content.style.display = 'block';
    input.value = '';
    input.disabled = true;
    input.style.opacity = '0.5';
    msg.style.color = '#8fd9a8';
    msg.textContent = 'ވަދެވިއްޖެ';
    try{ localStorage.setItem(STORAGE_KEY, '1'); }catch(e){}
    if(scroll){ content.scrollIntoView({behavior:'smooth', block:'start'}); }
  }
  function tryCode(){
    var val = (input.value || '').trim().toUpperCase().replace(/\s+/g,'');
    if(val === CORRECT_CODE){
      unlock(true);
    } else if(val.length){
      msg.style.color = '#ff9e9e';
      msg.textContent = 'ރަނގަޅެއް ނޫން';
      input.classList.remove('shake'); void input.offsetWidth; input.classList.add('shake');
    }
  }
  input.addEventListener('keydown', function(e){ if(e.key === 'Enter') tryCode(); });
  input.addEventListener('blur', tryCode);
  try{ if(localStorage.getItem(STORAGE_KEY) === '1'){ unlock(false); } }catch(e){}
})();

/* jump links (ބައި 1 / ބައި 2) */
document.querySelectorAll('[data-goto]').forEach(function(a){
  a.addEventListener('click', function(e){
    e.preventDefault();
    var t = document.getElementById(a.getAttribute('data-goto'));
    if(t) t.scrollIntoView({behavior:'smooth', block:'start'});
  });
});

/* one topic open at a time (ބައި 2) */
document.querySelectorAll('details.week-acc').forEach(function(d){
  d.addEventListener('toggle', function(){
    if(this.open){
      document.querySelectorAll('details.week-acc').forEach(function(o){ if(o !== d) o.open = false; });
      this.scrollIntoView({behavior:'smooth', block:'start'});
    }
  });
});

/* release switch: value comes from config.js */
var LAST = (typeof LAST_VISIBLE_TOPIC === 'number') ? LAST_VISIBLE_TOPIC : 99;
document.querySelectorAll('details.week-acc').forEach(function(d){
  if(parseInt(d.getAttribute('data-topic'), 10) > LAST){ d.style.display = 'none'; }
});

/* printing */
function expandAllForPrint(){ document.querySelectorAll('details').forEach(function(d){ d.open = true; }); }
function printWith(cls){
  document.body.classList.add(cls);
  var done = function(){ document.body.classList.remove(cls); window.removeEventListener('afterprint', done); };
  window.addEventListener('afterprint', done);
  setTimeout(function(){ window.print(); }, 150);
}
function printPart(p){   /* print button inside a slide file */
  if(p === 'p1'){ document.querySelectorAll('#part1 details').forEach(function(d){ d.open = true; }); printWith('print-p1'); }
  else { window.print(); }
}
</script>

<div id="printBar" class="no-print">
  <div class="btn" id="printBtn">🖨️ <span>ޕްރިންޓް / PDF ސޭވްކުރައްވާ</span></div>
  <div class="btn2" id="tabBtn">📱 <span>ފޯނުން؟ މިތަނަށް ފިއްތަވައި، ވަކި ބްރައުޒަރ ޓެބެއްގައި ހުޅުވާ</span></div>
</div>
<script>
document.getElementById('printBtn').addEventListener('click', function(){
  expandAllForPrint(); printWith('print-all');
});
var isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
var isFramed = (window.top !== window.self);
if(isMobile || isFramed){
  var tabBtn = document.getElementById('tabBtn');
  tabBtn.style.display = 'inline-flex';
  tabBtn.addEventListener('click', function(){
    expandAllForPrint();
    window.open(window.location.href, '_blank');
  });
}
</script>
</body>
</html>
'''

html = top + content + bottom
os.makedirs(SITE, exist_ok=True)
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf8').write(html)
print('built', os.path.join(SITE, 'index.html'), len(html) // 1024, 'KB')
