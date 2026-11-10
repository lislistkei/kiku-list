# GitHub Pages 用の公開ファイルを作る（埋めこみ再生つき・検索に出ない設定）
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

def build(src, dst):
    h = (D / src).read_text(encoding='utf-8')
    assert '"kind":' in h
    h = h.replace('"kind":', '"embed":true,"noEmbed":["bVPBABVYsz8"],"kind":', 1)
    h = h.replace('▶ この曲を聴く', '▶ 再生')
    h = h.replace('<footer>', '<footer><a href="../">← 聴くリストのトップへ</a>　', 1)
    out = S / dst / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HEAD + h + TAIL, encoding='utf-8')

build('classical-playlist.html', 'classical')
build('opera-playlist.html', 'opera')
build('wind-playlist.html', 'wind')

(S / 'index.html').write_text(HEAD + '''<title>聴くリスト</title>
<style>
:root{--bg:#f6f4f0;--paper:#fff;--ink:#1d2433;--muted:#5f6675;--line:#e1ddd4;--accent:#8a2433}
@media (prefers-color-scheme: dark){:root{--bg:#15171d;--paper:#1e2129;--ink:#ecebe7;--muted:#a6a9b3;--line:#2f333d;--accent:#e0798a;color-scheme:dark}}
body{background:var(--bg);color:var(--ink);font-family:"Hiragino Sans","Yu Gothic",system-ui,sans-serif;line-height:1.7;
  padding:32px max(16px,env(safe-area-inset-right,0px)) 48px max(16px,env(safe-area-inset-left,0px))}
main{max-width:560px;margin:0 auto;display:flex;flex-direction:column;gap:16px}
h1{font-family:"Hiragino Mincho ProN","Yu Mincho",serif;font-size:30px;margin:0}
p{margin:0;color:var(--muted)}
a.card{display:block;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:18px;text-decoration:none;color:var(--ink)}
a.card b{display:block;font-family:"Hiragino Mincho ProN","Yu Mincho",serif;font-size:21px;color:var(--accent)}
</style>
<main>
  <h1>聴くリスト</h1>
  <p>教本に出てくる曲を、聴きどころと豆知識つきで。▶を押すと、ページの中で再生できます。</p>
  <a class="card" href="classical/"><b>クラシック</b>308曲・15のリスト</a>
  <a class="card" href="opera/"><b>オペラ</b>157の名場面・12のリスト</a>
  <a class="card" href="wind/"><b>吹奏楽</b>95曲（マーチ36曲）・12のリスト</a>
  <p style="font-size:12px">好き嫌いの記録は、この端末の中だけに保存されます。</p>
</main>''' + TAIL, encoding='utf-8')
(S / '.nojekyll').write_text('', encoding='utf-8')
print('ok', [str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()])
