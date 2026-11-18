# GitHub Pages 用の公開ファイルを作る（埋めこみ再生つき・検索に出ない設定）
# 2026/11/19：劇場のプログラム冊子のデザインに作り直し（表紙＝本日の演目・目次・聴いた記録）
import json, re
from pathlib import Path
D = Path(__file__).parent
S = D / 'site'
HEAD = '''<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="referrer" content="strict-origin-when-cross-origin">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>
'''
TAIL = '\n</body></html>\n'
PAGES = [('classical-playlist.html', 'classical'), ('opera-playlist.html', 'opera'), ('wind-playlist.html', 'wind'), ('mw-playlist.html', 'march-waltz')]

def build(src, dst):
    h = (D / src).read_text(encoding='utf-8')
    assert '"kind":' in h
    # page＝フォルダ名（表紙へもどるリンクを出す・聴いた記録からほかのページの曲へリンクするのに使う）
    h = h.replace('"kind":', '"embed":true,"noEmbed":["bVPBABVYsz8"],"page":"%s","kind":' % dst, 1)
    out = S / dst / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HEAD + h + TAIL, encoding='utf-8')

for src, dst in PAGES:
    build(src, dst)

# ---- 表紙（4つのページの目次・4ジャンルから今日の1曲・聴いた記録） ----
tpl = (D / 'page_template.html').read_text(encoding='utf-8')
css = re.search(r'<style>(.*?)</style>', tpl, re.S).group(1)
art = tpl[tpl.index('/* ---- 線画の絵'):tpl.index('/* ---- 章と曲の対応')]
ALL, INFO = {}, []
for src, dst in PAGES:
    data = json.loads(re.search(r'const DATA = (.*?);\n', (D / src).read_text(encoding='utf-8')).group(1))
    keys = sorted({k for s in data['sections'] for g in s['g'] for k in g[1]})
    for k in keys:
        w = data['works'][k]
        ALL[dst + '/' + k] = dict(c=w['c'], w=w['w'], p=w['p'], pt=w['pt'], len=w['len'], g=data['kind'])
    INFO.append((dst, data['kind'], len(data['works']), len(data['sections'])))
DESC = {'classical': 'バロックから現代まで。教本の章の順に',
        'opera': 'モンテヴェルディから名歌手まで。歌詞の対訳つき',
        'wind': 'マーチ70曲、コンクールの課題曲、ポップスまで',
        'march-waltz': '3つのリストから行進曲とワルツだけを集めて'}
UNIT = {'opera': '場面'}
ROMAN = ['I', 'II', 'III', 'IV']
toc = ''.join(f'<li><a href="{dst}/"><span class="r">{ROMAN[i]}</span><span class="nm">{kind}<small>{DESC[dst]}</small></span><span class="dots"></span><span class="n">{n}<i>{UNIT.get(dst, "曲")}</i></span></a></li>'
              for i, (dst, kind, n, ns) in enumerate(INFO))
index = '''<title>聴くリスト</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap">
<style>''' + css + '''</style>
<div class="wrap"><div class="view">
  <header class="mast">
    <div class="en">Programme · Kiku List</div>
    <h1>聴くリスト</h1>
    <div class="eyebrow">教本に出てくる曲を、聴きどころと豆知識つきで</div>
  </header>
  <div class="meta"><span id="m-date"></span><span>4つのリスト</span></div>

  <div class="sec-h">本日の演目</div>
  <section class="today" id="today" aria-label="今日の1曲"></section>

  <div class="sec-h">目　次</div>
  <ol class="toc">''' + toc + '''</ol>

  <div class="sec-h" id="log">聴いた記録</div>
  <section aria-label="聴いた記録">
    <ul class="week" id="l-week"></ul>
    <p class="lstat" id="l-stat"></p>
    <ol class="stubs" id="l-list"></ol>
    <button type="button" class="more" id="l-more" hidden>もっと見る</button>
  </section>
  <footer>動画はYouTubeの各チャンネルのものです。聴いた記録と好き嫌いは、この端末の中だけに保存されます。</footer>
</div></div>
<script>
const ALL = ''' + json.dumps(ALL, ensure_ascii=False, separators=(',', ':')) + ''';
const esc = s => String(s).replace(/[&<>"]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const pad = n => String(n).padStart(2, "0");
const ymd = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const WD = "日月火水木金土";
const mdw = s => { const d = new Date(s + "T00:00:00"); return `${d.getMonth() + 1}/${d.getDate()}（${WD[d.getDay()]}）`; };
const hash = s => { let h = 2166136261; for (const ch of s) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; } return h; };
const LATIN = {"クラシック":"CLASSICAL","オペラ":"OPERA","吹奏楽":"WIND BAND","マーチとワルツ":"MARCH & WALTZ"};
let W = ALL, GENRE = "";
''' + art + '''
{ const d = new Date(); document.getElementById("m-date").textContent = `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日（${WD[d.getDay()]}）`; }
const keys = Object.keys(ALL).sort(), today = ymd(new Date());
const k = keys[hash(today + "top") % keys.length], t = ALL[k], href = k.replace("/", "/#k-");
GENRE = t.g;
document.getElementById("today").innerHTML = `<div class="in">
  ${plate(k, true, LATIN[t.g] || "")}
  <div class="kicker">— ${esc(t.g)} —</div>
  <div class="comp">${esc(t.w.startsWith("『") ? t.c + t.w : t.c)}</div>
  <div class="ttl">${esc(t.w.startsWith("『") ? t.p : t.w)}</div>
  <div class="part">${esc(t.w.startsWith("『") ? "" : t.p)}</div>
  <p class="pt">${esc(t.pt)}</p>
  <a class="btn" href="${href}"><svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3v18l16-9z" fill="currentColor"/></svg>開演<span class="lat">${t.len}</span></a>
  <div class="stamp" id="t-stamp" hidden><b>聴いた</b><span class="lat">${today.replace(/-/g, ".")}</span></div>
</div>`;
let heard = []; try { const v = JSON.parse(localStorage.getItem("listened-v1") || "[]"); if (Array.isArray(v)) heard = v; } catch {}
document.getElementById("t-stamp").hidden = !heard.some(e => e.p + "/" + e.k === k && e.d === today);
let shown = 5;
function renderLog(){
  const now = new Date(), days = new Set(heard.map(e => e.d)), wk = document.getElementById("l-week");
  let n7 = 0, h = "";
  for (let i = 6; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth(), now.getDate() - i), s = ymd(d), on = days.has(s);
    if (on) n7++;
    h += `<li class="${on ? "on" : ""}${i === 0 ? " now" : ""}" title="${mdw(s)}"><i>${d.getDate()}</i><span>${WD[d.getDay()]}</span></li>`;
  }
  wk.innerHTML = h;
  const month = ymd(now).slice(0, 7);
  const rows = heard.slice().sort((a, b) => (b.d + (b.at || "")).localeCompare(a.d + (a.at || "")));
  document.getElementById("l-stat").textContent = rows.length
    ? `今月${new Set(heard.filter(e => e.d.startsWith(month)).map(e => e.t)).size}曲。これまで${rows.length}回・${new Set(rows.map(e => e.t)).size}曲。`
    : "曲のページで「聴いた」のハンコを押すと、ここに半券が残ります（この端末の中だけ）。";
  document.getElementById("l-list").innerHTML = rows.slice(0, shown).map(e => {
    const d = new Date(e.d + "T00:00:00");
    const inner = `<span class="d"><b>${d.getMonth()+1}.${d.getDate()}</b><span>${WD[d.getDay()]}</span></span><span class="t">${esc(e.t)}<small>${esc(e.g || "")}</small></span>`;
    return `<li>${e.p ? `<a href="${e.p}/#k-${encodeURIComponent(e.k)}">${inner}</a>` : `<span class="nolink">${inner}</span>`}</li>`;
  }).join("");
  document.getElementById("l-more").hidden = rows.length <= shown;
}
document.getElementById("l-more").onclick = () => { shown += 30; renderLog(); };
renderLog();
</script>'''
(S / 'index.html').write_text(HEAD + index + TAIL, encoding='utf-8')
(S / '.nojekyll').write_text('', encoding='utf-8')
print('ok', [str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()], 'top-songs', len(ALL))
