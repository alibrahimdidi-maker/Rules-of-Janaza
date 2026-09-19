# -*- coding: utf-8 -*-
"""
SHA0302 site builder
--------------------
Run:   python3 build.py
Reads: this folder (ch1_saleem_w1..w5.html, 00_15weeks.html, sha0302_topic*.html, sha0719_week*.html, _shell_top.html)
Makes: ../site/index.html  (single self-contained page)
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
rd = lambda n: open(os.path.join(HERE, n), encoding='utf8').read()

# ------------------------------------------------------------------ file lists
# (file, badge label, sequence number used by the release switch)
TOPICS = [('sha0302_topic01.html','1',1),('sha0302_topic02.html','2',2),('sha0302_topic03.html','3',3),
          ('sha0302_topic04.html','4',4),('sha0302_topic05.html','5',5),('sha0302_topic06_07.html','6-7',6),
          ('sha0302_topic08.html','8',8),('sha0302_topic09.html','9',9),('sha0302_topic10.html','10',10),
          ('sha0302_topic11.html','11',11),('sha0302_topic12.html','12',12),('sha0302_topic13.html','13',13)]
WEEKS = [('sha0719_week%02d.html' % n, str(n), n) for n in range(1, 16)]

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

SAL = [('ch1_saleem_w%d.html' % n, str(n), n) for n in range(1, 6)]

# ------------------------------------------------------------------ parts 2 & 3
def make_acc(items, prefix, word, printarg, dattr):
    out = []
    for idx, (fn, label, seq) in enumerate(items, 1):
        frag = rd(fn).strip()
        if 'onclick="window.print()"' not in frag:
            frag = re.sub(r'<a\s+style="position: absolute', '<a onclick="window.print()" style="position: absolute', frag, 1)
        title = re.search(r'<h1[^>]*>(.*?)</h1>', frag, re.S).group(1).strip()
        frag = frag.replace('onclick="window.print()"', "onclick=\"printPart('%s')\"" % printarg)
        out.append(
            '<details class="week-acc" id="%sAcc%d" %s="%d">\n'
            '  <summary><span class="week-num">%s %s</span><span class="week-title">%s</span>'
            '<span class="week-count">%d ސްލައިޑް</span>'
            '<span class="week-chev">&#9660;</span></summary>\n'
            '  <div class="week-body">\n%s\n  </div>\n</details>\n' % (prefix, idx, dattr, seq, word, label, title, frag.count('<details'), frag))
    return '\n'.join(out)

acc2 = make_acc(TOPICS, 'topic', 'ޓޮޕިކް', 'p2', 'data-topic')
acc3 = make_acc(WEEKS, 'week', 'ހަފްތާ', 'p3', 'data-week')
acc1 = make_acc(SAL, 'sal', 'ހަފްތާ', 'p0', 'data-sal')

n1 = sum(rd(f).count('<details') for f, _, _ in SAL); n15 = body15.count('<details')
n2 = sum(rd(f).count('<details') for f, _, _ in TOPICS)
n3 = sum(rd(f).count('<details') for f, _, _ in WEEKS)
print('slides: ch1=%d  15weeks=%d  topics=%d  weeks=%d  total=%d' % (n1, n15, n2, n3, n1 + n15 + n2 + n3))

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
#part3 .part-head{background:linear-gradient(135deg,#002D62 0%,#1d5a8a 100%);}
#ch1 .part-head{background:linear-gradient(135deg,#5b3a0a 0%,#a8741f 100%);}
.ch-head{background:linear-gradient(135deg,#08281f 0%,#12503a 100%);border:3px double #d4af37;border-radius:16px;
  text-align:center;color:#fff;padding:22px 14px;margin:0 0 22px;box-shadow:0 10px 28px rgba(8,40,31,.3);}
.ch-head .pno{display:inline-block;background:#d4af37;color:#08281f;border-radius:20px;padding:3px 18px;font-weight:bold;
  font-size:clamp(13px,1.6vw,16px);margin-bottom:8px;}
.ch-head h2{margin:0;font-size:clamp(20px,3vw,30px);line-height:1.7;text-shadow:2px 2px 6px rgba(0,0,0,.4);}
.ch-head p{margin:6px 0 0;color:#f2e6bf;font-size:clamp(13px,1.6vw,16px);line-height:1.8;}
.ch-divider{margin:56px 0 40px;}
.ch-divider .rule{border-top:6px double #b7862e;}
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

/* ===== search + counts ===== */
.week-count{background:rgba(255,255,255,.15);color:#f4d03f;border:1px solid #d4af37;border-radius:14px;padding:2px 10px;
  font-size:12px;white-space:nowrap;flex-shrink:0;}
.site-search{background:#fff;border:2px solid #d4af37;border-radius:14px;padding:12px;margin:0 0 16px;box-shadow:0 4px 12px rgba(8,40,31,.12);}
.site-search .row{display:flex;gap:8px;align-items:center;}
#siteSearch{flex:1;min-width:0;font-family:inherit;font-size:16px;padding:10px 12px;border:2px solid #b7862e;border-radius:10px;direction:rtl;}
#siteSearch:focus{outline:none;box-shadow:0 0 0 3px rgba(212,175,55,.4);}
#searchClear{cursor:pointer;border:0;background:#12503a;color:#fff;border-radius:10px;padding:10px 14px;font-size:15px;font-family:inherit;}
.totals{text-align:center;color:#12503a;font-size:13px;margin:8px 0 0;line-height:1.9;}
#searchResults{margin-top:10px;max-height:340px;overflow:auto;}
#searchResults .hit{display:block;width:100%;text-align:right;background:#faf6e8;border:1px solid #dfd2a8;border-radius:10px;
  padding:8px 12px;margin-bottom:6px;cursor:pointer;font-family:inherit;color:#12241d;}
#searchResults .hit:hover{background:#f3ead1;}
#searchResults .hit .where{display:block;color:#7a1f1f;font-size:12px;font-weight:bold;}
#searchResults .hit .ttl{display:block;font-weight:bold;font-size:15px;line-height:1.7;}
#searchResults .hit .snip{display:block;color:#5a4b2a;font-size:13px;line-height:1.7;}
#searchResults .none{color:#8a7458;font-size:14px;text-align:center;padding:6px;}

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
  body:not(.print-all) .part-divider,body:not(.print-all) .part-head,body:not(.print-all) .ch-head{display:none !important;}
  body:not(.print-all) #ch1,body:not(.print-all) #part1,body:not(.print-all) #part2,body:not(.print-all) #part3{display:none !important;}
  body.print-p0:not(.print-all) #ch1,body.print-p1:not(.print-all) #part1,body.print-p2:not(.print-all) #part2,body.print-p3:not(.print-all) #part3{display:block !important;}
  #courseContent{padding:0;margin:0;background:none;}
}
"""

def dup_ch1(css):
    out = []
    for line in css.split('\n'):
        m = re.match(r'^(\s*)(\.week-body[^{]*)\{(.*)$', line)
        if m and m.group(2).strip() != '.week-body':
            sels = [x for x in m.group(2).split(',')]
            more = [x.replace('.week-body', '#ch1', 1) for x in sels]
            line = m.group(1) + ','.join(sels + more) + '{' + m.group(3)
        out.append(line)
    return '\n'.join(out)
EXTRA_CSS = dup_ch1(EXTRA_CSS)

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

# password window (full-screen) replaces the small code chip in the hero
chip = re.search(r'<div\s+style="background-color: rgba\(0, 0, 0, 0.4\)[^"]*">\s*<svg.*?<span>:ކޯޑު</span></div>', top, re.S)
assert chip, 'gate chip not found'
top = top.replace(chip.group(0), '', 1)
top = re.sub(r'<div id="gateMsg"[^>]*></div>', '', top, 1)
avatar = re.search(r'<img src="(data:image/jpeg;base64,[^"]+)"', top).group(1)
GATE_CSS = """
/* ===== password window ===== */
body.locked{overflow:hidden;}
#gateOverlay{position:fixed;inset:0;z-index:2000;display:flex;align-items:center;justify-content:center;
  padding:16px;background:linear-gradient(135deg,#002D62 0%,#004B23 100%);overflow:auto;transition:opacity .35s ease;}
#gateOverlay.hide{opacity:0;pointer-events:none;}
#gateCard{width:100%;max-width:400px;background:#fffdf5;border:3px double #d4af37;border-radius:18px;
  padding:26px 20px 22px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.45);direction:rtl;}
#gateCard img{width:84px;height:84px;border-radius:50%;object-fit:cover;border:3px solid #d4af37;box-shadow:0 6px 16px rgba(0,0,0,.3);}
#gateCard h1{margin:12px 0 2px;font-size:clamp(19px,5.4vw,25px);color:#08281f;line-height:1.7;}
#gateCard .en{font-family:Tahoma,Arial,sans-serif;color:#8a7a3d;font-size:14px;margin-bottom:2px;}
#gateCard .uni{font-family:Tahoma,Arial,sans-serif;color:#12503a;font-size:13px;margin-bottom:16px;}
#gateCard .lbl{display:block;color:#08281f;font-weight:bold;font-size:15px;margin-bottom:8px;}
#gateForm{display:flex;flex-direction:column;gap:10px;}
#gateInput{width:100%;text-align:center;font-family:Tahoma,Arial,sans-serif;font-size:18px;font-weight:bold;letter-spacing:2px;
  color:#08281f;background:#fff;border:2px solid #b7862e;border-radius:10px;padding:11px 10px;text-transform:uppercase;box-sizing:border-box;}
#gateInput:focus{outline:none;border-color:#b7862e;box-shadow:0 0 0 3px rgba(212,175,55,.4);}
#gateBtn{cursor:pointer;border:2px solid #d4af37;border-radius:10px;padding:11px;font-size:17px;font-weight:bold;
  font-family:inherit;color:#f4d03f;background:linear-gradient(135deg,#08281f 0%,#12503a 100%);}
#gateMsg{min-height:20px;margin-top:10px;font-size:14px;color:#a3372f;}
"""
top = top.replace('</style>', GATE_CSS + '</style>', 1)
top = top.replace('<body>', '<body class="locked">', 1)
GATE_HTML = """<div id="gateOverlay">
  <div id="gateCard">
    <img src="%s" alt="">
    <h1>ކަށުކަމާކެމީގެ ފިޤުހީ ޙުކުމްތައް</h1>
    <div class="en">Rules of Janazah — SHA0302</div>
    <div class="uni">Islamic University of Maldives</div>
    <form id="gateForm" onsubmit="return false;" autocomplete="off">
      <label class="lbl" for="gateInput">ޕާސްވޯޑް ޖައްސަވާ</label>
      <input type="password" id="gateInput" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="••••••••" inputmode="text">
      <button type="button" id="gateBtn">ވަދޭ</button>
    </form>
    <div id="gateMsg" role="alert"></div>
  </div>
</div>
""" % avatar
top = top.replace('<body class="locked">', '<body class="locked">\n' + GATE_HTML, 1)

# ------------------------------------------------------------------ course content
content = '''<div class="course-wrap" id="courseContent">

<div class="site-search no-print">
  <div class="row">
    <input id="siteSearch" type="search" placeholder="ހުރިހާ ސްލައިޑްތަކުން ހޯދާ — މިސާލަކަށް: ސީޣާ، ދުޢާ، ހިނެއުން" autocomplete="off">
    <button id="searchClear" type="button">×</button>
  </div>
  <div id="searchResults"></div>
  <div class="totals">ޖުމްލަ ސްލައިޑް: <b>__TOT__</b> &nbsp;·&nbsp; ބާބު 1: __N1__ &nbsp;·&nbsp; ބާބު 2: __N15__ + __N2__ &nbsp;·&nbsp; ބާބު 3: __N3__</div>
</div>

<div class="part-nav no-print">
  <a data-goto="ch1"><b>1</b> ބާބު 1 — އައްޝެއިޚް އަޙްމަދު ސަލީމް</a>
  <a data-goto="ch2"><b>2</b> ބާބު 2 — SHA0302</a>
  <a data-goto="part3"><b>3</b> ބާބު 3 — SHA0719</a>
</div>

<!-- ============================ CHAPTER 1 ============================ -->
<section id="ch1">
<div class="part-head">
  <span class="pno">ބާބު 1</span>
  <h2>އައްޝެއިޚް އަޙްމަދު ސަލީމްގެ ނޯޓްތައް</h2>
  <p>«ކަށުކަމާކެމީކަން ދަސްކުރާ ކޯހުގެ އަތްމަތީ ފޮތް» — ހަފްތާ 1 ން 5 އަށް (ޞ. 2–30) · ބޭނުންފުޅުވާ ހަފްތާއެއް ހުޅުވުމަށް ފިއްތަވާ</p>
</div>
''' + acc1 + '''
</section>

<div class="part-divider ch-divider">
  <div class="rule"></div>
  <div class="note">
    <strong>ފާހަގަ:</strong> މީގެ މަތީގައި ވަނީ <strong>ބާބު 1 (އައްޝެއިޚް އަޙްމަދު ސަލީމްގެ ސްލައިޑް).</strong><br>
    މީގެ ތިރީގައި ވަނީ <strong>ބާބު 2 — SHA0302 ގެ ސްލައިޑްތަކެވެ.</strong>
    <span class="arrow">&#9660;</span>
  </div>
</div>

<!-- ============================ CHAPTER 2 (SHA0302) ============================ -->
<div id="ch2">
<div class="ch-head">
  <span class="pno">ބާބު 2</span>
  <h2>ކަށުކަމާކެމީގެ ފިޤުހީ ޙުކުމްތައް — SHA0302</h2>
  <p>Rules of Janazah · ބައި 1: 15 ހަފްތާގެ ޚުލާޞާ · ބައި 2: ޓޮޕިކް ވަކިވަކިން ތަފްޞީލީ ސްލައިޑްތައް</p>
</div>

<section id="part1">
<div class="part-head">
  <span class="pno">ބައި 1</span>
  <h2>15 ހަފްތާގެ ޚުލާޞާ ސްލައިޑްތައް</h2>
  <p>ކޯހުގެ 15 ހަފްތާ އެއްކޮށް — ހަފްތާއަކުން ހަފްތާއަކަށް ކުރު ސްލައިޑްތައް</p>
</div>
''' + body15 + '''
</section>

<div class="part-divider">
  <div class="rule"></div>
  <div class="note">
    <strong>ފާހަގަ:</strong> މީގެ މަތީގައި ވަނީ <strong>15 ހަފްތާގެ ޚުލާޞާ ސްލައިޑްތަކެވެ.</strong><br>
    މީގެ ތިރީގައި ވަނީ <strong>ޓޮޕިކް ވަކިވަކިން ތަފްޞީލީ ސްލައިޑްތަކެވެ.</strong>
    <span class="arrow">&#9660;</span>
  </div>
</div>

<section id="part2">
<div class="part-head">
  <span class="pno">ބައި 2</span>
  <h2>ޓޮޕިކް ވަކިވަކިން ތަފްޞީލީ ސްލައިޑްތައް</h2>
  <p>Rules of Janazah — SHA0302 · ބޭނުންފުޅުވާ ޓޮޕިކެއް ހުޅުވުމަށް ފިއްތަވާ (އެއް ފަހަރާ ހުޅުވޭނީ އެންމެ ޓޮޕިކެއް)</p>
</div>

''' + acc2 + '''
</section>
</div>

<div class="part-divider ch-divider">
  <div class="rule"></div>
  <div class="note">
    <strong>ފާހަގަ:</strong> މީގެ މަތީގައި ވަނީ <strong>ބާބު 2 — SHA0302 ގެ ސްލައިޑްތަކެވެ.</strong><br>
    މީގެ ތިރީގައި ވަނީ <strong>ބާބު 3 — SHA0719 ގެ ހަފްތާ ވަކިވަކިން ސްލައިޑްތަކެވެ.</strong>
    <span class="arrow">&#9660;</span>
  </div>
</div>

<!-- ============================ CHAPTER 3 (SHA0719) ============================ -->
<section id="part3">
<div class="part-head">
  <span class="pno">ބާބު 3 · SHA0719</span>
  <h2>ހަފްތާ ވަކިވަކިން ތަފްޞީލީ ސްލައިޑްތައް</h2>
  <p>Fiqh of Janaza Rules — SHA0719 · ބޭނުންފުޅުވާ ހަފްތާއެއް ހުޅުވުމަށް ފިއްތަވާ (އެއް ފަހަރާ ހުޅުވޭނީ އެންމެ ހަފްތާއެއް)</p>
</div>

''' + acc3 + '''
<div class="to-top no-print"><a data-goto="ch1">&#9650; އެންމެ މަތީގެ ބާބަށް ދާން</a></div>
</section>

</div>
'''

for k, v in (('__TOT__', n1 + n15 + n2 + n3), ('__N1__', n1), ('__N15__', n15), ('__N2__', n2), ('__N3__', n3)):
    content = content.replace(k, str(v))

# ------------------------------------------------------------------ scripts
bottom = r'''
<script src="config.js"></script>
<script>
(function(){
  var CORRECT_CODE = 'SHA0302';
  var STORAGE_KEY = 'sha0302-course-unlocked';
  var input = document.getElementById('gateInput');
  var btn = document.getElementById('gateBtn');
  var msg = document.getElementById('gateMsg');
  var overlay = document.getElementById('gateOverlay');
  var content = document.getElementById('courseContent');

  function unlock(scroll){
    content.style.display = 'block';
    document.body.classList.remove('locked');
    overlay.classList.add('hide');
    setTimeout(function(){ overlay.style.display = 'none'; }, 400);
    try{ localStorage.setItem(STORAGE_KEY, '1'); }catch(e){}
    if(scroll){ setTimeout(function(){ content.scrollIntoView({behavior:'smooth', block:'start'}); }, 420); }
  }
  function tryCode(){
    var val = (input.value || '').trim().toUpperCase().replace(/\s+/g,'');
    if(val === CORRECT_CODE){
      unlock(true);
    } else {
      msg.textContent = val.length ? 'ޕާސްވޯޑް ރަނގަޅެއް ނޫން' : 'ޕާސްވޯޑް ޖައްސަވާ';
      input.classList.remove('shake'); void input.offsetWidth; input.classList.add('shake');
      input.select();
    }
  }
  input.addEventListener('keydown', function(e){ if(e.key === 'Enter'){ e.preventDefault(); tryCode(); } });
  btn.addEventListener('click', tryCode);
  try{ if(localStorage.getItem(STORAGE_KEY) === '1'){ unlock(false); overlay.style.display = 'none'; } else { setTimeout(function(){ input.focus(); }, 100); } }catch(e){}
})();

/* jump links (ބައި 1 / ބައި 2) */
document.querySelectorAll('[data-goto]').forEach(function(a){
  a.addEventListener('click', function(e){
    e.preventDefault();
    var t = document.getElementById(a.getAttribute('data-goto'));
    if(t) t.scrollIntoView({behavior:'smooth', block:'start'});
  });
});

/* one accordion open at a time, per part */
document.querySelectorAll('details.week-acc').forEach(function(d){
  d.addEventListener('toggle', function(){
    if(this.open){
      var sec = d.closest('section');
      sec.querySelectorAll('details.week-acc').forEach(function(o){ if(o !== d) o.open = false; });
      this.scrollIntoView({behavior:'smooth', block:'start'});
    }
  });
});

/* release switches: values come from config.js */
var LT = (typeof LAST_VISIBLE_TOPIC === 'number') ? LAST_VISIBLE_TOPIC : 99;
var LW = (typeof LAST_VISIBLE_WEEK === 'number') ? LAST_VISIBLE_WEEK : 99;
document.querySelectorAll('details.week-acc').forEach(function(d){
  var t = d.getAttribute('data-topic'), w = d.getAttribute('data-week');
  if((t && parseInt(t, 10) > LT) || (w && parseInt(w, 10) > LW)){ d.style.display = 'none'; }
});

/* ===== search across every slide ===== */
(function(){
  var box = document.getElementById('siteSearch'), out = document.getElementById('searchResults'), clr = document.getElementById('searchClear');
  var slides = null;
  function norm(t){ return (t||'').replace(/[\u064B-\u065F\u0670\u0640]/g,'').replace(/\s+/g,' ').toLowerCase(); }
  function where(d){
    var acc = d.closest('details.week-acc');
    if(acc){ var n = acc.querySelector('.week-num'); var sec = d.closest('section');
      return (sec && sec.id === 'part3' ? 'ބާބު 3 · ' : (sec && sec.id === 'ch1' ? 'ބާބު 1 · ' : 'ބާބު 2 · ')) + (n ? n.textContent : ''); }
    if(d.closest('#part1')) return 'ބާބު 2 · 15 ހަފްތާގެ ޚުލާޞާ';
    return '';
  }
  function build(){
    slides = [];
    document.querySelectorAll('#courseContent details:not(.week-acc)').forEach(function(d){
      var sm = d.querySelector('summary'); var title = sm ? Array.prototype.map.call(sm.children, function(x){ return x.textContent.trim(); }).filter(Boolean).join(' ') : '';
      var txt = d.textContent.replace(/\s+/g,' ').trim();
      slides.push({d:d, title:title, txt:txt, n:norm(txt), where:where(d)});
    });
  }
  function go(d){
    var acc = d.closest('details.week-acc');
    if(acc){ acc.open = true; }
    d.open = true;
    setTimeout(function(){ d.scrollIntoView({behavior:'smooth', block:'start'}); }, 450);
  }
  function run(){
    var q = norm(box.value.trim()); out.innerHTML = '';
    if(q.length < 2) return;
    if(!slides) build();
    var hits = 0, frag = document.createDocumentFragment();
    for(var i = 0; i < slides.length && hits < 60; i++){
      var s = slides[i], k = s.n.indexOf(q);
      if(k < 0) continue;
      hits++;
      var b = document.createElement('button'); b.type = 'button'; b.className = 'hit';
      var raw = s.txt, st = Math.max(0, k - 30);
      b.innerHTML = '<span class="where"></span><span class="ttl"></span><span class="snip"></span>';
      b.children[0].textContent = s.where; b.children[1].textContent = s.title;
      b.children[2].textContent = '… ' + raw.substr(st, 110) + ' …';
      (function(d){ b.addEventListener('click', function(){ go(d); }); })(s.d);
      frag.appendChild(b);
    }
    if(!hits){ out.innerHTML = '<div class="none">ނުފެނުނު</div>'; }
    else { var h = document.createElement('div'); h.className = 'none'; h.textContent = hits + (hits >= 60 ? '+' : '') + ' ސްލައިޑް'; out.appendChild(h); out.appendChild(frag); }
  }
  box.addEventListener('input', run);
  clr.addEventListener('click', function(){ box.value = ''; out.innerHTML = ''; box.focus(); });
})();

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
  else { printWith('print-' + p); }
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
