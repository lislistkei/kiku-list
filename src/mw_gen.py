# マーチとワルツ版（横断リスト）を作る。
# クラシック・オペラ・吹奏楽の3ページ（先に gen.py / opera_gen.py / wind_gen.py を実行しておく）から
# マーチとワルツを借りてきて、mw_works.txt / mw_videos.tsv の新しい曲と合わせる。
# セクションの中では「c:キー」＝クラシック、「o:」＝オペラ、「w:」＝吹奏楽、「キーだけ」＝新しい曲。
import json, re
from pathlib import Path
D = Path(__file__).parent

def page_data(name):
    h = (D / name).read_text(encoding='utf-8')
    m = re.search(r'^const DATA = (\{.*\});$', h, re.M)
    return json.loads(m.group(1))

SRC = {'c': page_data('classical-playlist.html'), 'o': page_data('opera-playlist.html'), 'w': page_data('wind-playlist.html')}

NEW = {}
for l in (D/'mw_works.txt').read_text(encoding='utf-8').splitlines():
    if not l.strip() or l.startswith('#'): continue
    k, comp, title, part, q, rng, point, trivia = l.split('|')
    NEW[k] = dict(c=comp, w=title, p=part, pt=point, tr=trivia)
for l in (D/'mw_videos.tsv').read_text(encoding='utf-8').splitlines():
    if not l.strip(): continue
    k, vid, ln, ch = l.split('\t'); NEW[k].update(id=vid, len=ln, ch=ch)
assert all('id' in w for w in NEW.values()), [k for k, w in NEW.items() if 'id' not in w]

S = [
 ('intro', '入門の12曲', 'まずはここから。ウィーンのワルツ、行進曲の王様、バレエのワルツ、日本のマーチまで', [
   ['', 'c:danube c:radetzky w:stars skaters c:flowers c:minute c:pomp o:aida-march w:bogey w:olympic c:sleeping c:wedding']]),
 ('waltz-vienna', 'ワルツ（ウィーンのワルツ）', '「ワルツ王」シュトラウス一家と、ウィーンのオペレッタ', [
   ['「ワルツ王」ヨハン・シュトラウス2世', 'c:danube c:kaiserwalzer c:fruhling vblut wald wein rosensud kuenstler accel morgen tausend schatz'],
   ['シュトラウス家と仲間たち', 'lanner c:sphaeren dorfschwalben delirien dynamiden weanermadln'],
   ['オペレッタのワルツ', 'o:fledermaus goldsilber merrywaltz']]),
 ('waltz-world', 'ワルツ（バレエとオーケストラ）', 'フランス、メキシコ、ロシアへ。バレエの舞踏会から、ちょっと怖いワルツまで', [
   ['世界で愛されるワルツ', 'skaters estudiantina olas danubewaves'],
   ['バレエのワルツ', 'c:flowers c:sleeping swanwaltz snowflakes coppelia cinderella'],
   ['オーケストラのワルツ', 'serenadewaltz t5waltz berliozbal valsetriste c:masquerade c:waltz2 c:rosen valsesnobles c:lavalse']]),
 ('waltz-piano', 'ワルツ（ピアノとオペラ）', 'ショパンのピアノのワルツと、オペラの舞台で歌い踊られるワルツ', [
   ['ピアノのワルツ', 'c:minute c:grandev chopin3 chopin7 chopin9 brahms15 c:jetv pluslente'],
   ['オペラのワルツ', 'o:boh-musetta o:romeo-waltz faustwaltz onegin o:rosen-waltz']]),
 ('march-classic', '行進曲（オーケストラ）', '式典の行進曲から、ウィーンの行進曲、異国風、ひょうきんな行進曲まで', [
   ['式典とお祝いの行進曲', 'c:pomp pomp4 c:wedding o:loh-bridal homage karelia coronation'],
   ['ウィーンの行進曲', 'c:radetzky egyptian'],
   ['ピアノから生まれた行進曲', 'c:turkish schubertmarch'],
   ['異国風の行進曲', 'c:bturkish rakoczy c:slavonic sardar'],
   ['おもしろい行進曲・ふしぎな行進曲', 'c:nutmarch oranges marionette c:tell c:mars c:t6-3']]),
 ('march-opera', '行進曲（オペラ）', 'オペラの舞台を、大勢の人が行進していく場面', [
   ['', 'o:aida-march o:carmen-prel tannmarch faustsoldiers priests']]),
 ('funeral', '葬送の行進曲', 'ゆっくり重い足どりの「お葬式の行進曲」。交響曲の中の名曲が多い', [
   ['', 'c:funeral eroica2 o:ring-funeral mahler5 c:ma1 scaffold']]),
 ('march-world', 'マーチ（吹奏楽・世界の行進曲）', 'アメリカのマーチ王スーザから、ヨーロッパの軍楽隊、映画のマーチまで', [
   ['「マーチ王」スーザ', 'w:stars w:washington w:liberty w:semper w:thunderer w:capitan w:kingcotton w:handsacross w:manhattan w:cadets w:invincible w:blackhorse fairest fieldartillery'],
   ['アメリカのマーチ', 'grays w:emblem w:barnum w:lassus w:americanswe w:onthemall w:patrol w:anchors w:amsalute'],
   ['イギリスのマーチ', 'w:bogey quarterdeck w:crown w:orb w:dambusters w:knightsbridge w:seasongs'],
   ['ドイツ・オーストリア・チェコ・ロシア', 'w:kameraden w:doppeladler yorck w:preussens w:gladiatoren w:florentiner w:gladiators w:slavianka'],
   ['フランス・ベルギー・スペイン', 'w:sambre lorraine militaire w:arsenal w:espana w:amparito'],
   ['映画とオリンピックのマーチ', 'w:raiders w:imperial w:superman w:greatescape w:longestday w:olyfanfare']]),
 ('march-japan', 'マーチ（吹奏楽・日本の行進曲）', '明治の行進曲から、式典やスポーツでおなじみの名曲、コンクール課題曲のマーチまで', [
   ['日本の名行進曲', 'battotai kimigayo w:gunkan w:olympic w:sportsshow w:shukuten w:ozora w:eikan w:akizorani'],
   ['コンクール課題曲のマーチ（年の順）', 'w:takeoff w:marine w:catalonia w:turnbull w:shiokemuri w:kten w:haruka w:streetperf w:kibou w:harukazemichi w:aprilleaf w:bluespring w:kirameki w:pegasus w:yuuki w:memories w:marcha']]),
 ('scenes', '「あの曲」の正体', 'ニューイヤーコンサート、結婚式、運動会、テレビで聴いたあの曲', [
   ['ニューイヤーコンサート', 'c:radetzky c:danube egyptian'],
   ['結婚式・卒業式', 'c:wedding o:loh-bridal c:pomp'],
   ['運動会・スポーツ', 'c:tell w:olympic w:sportsshow w:eikan w:gunkan'],
   ['テレビ・映画・サーカス・フィギュアスケート', 'marionette w:gladiators olas skaters c:masquerade w:bogey w:greatescape c:sleeping']]),
]

works, about, used, sections = {}, {}, set(), []
def take(ref):
    src, _, k = ref.rpartition(':')
    w = dict(SRC[src]['works'][k]) if src else dict(NEW[k])
    if k in works:
        assert works[k]['id'] == w['id'], ('key collision', ref)
    works[k] = w
    if src:
        a = w['c'] + '|' + w['w']
        if a in SRC[src].get('about', {}): about[a] = SRC[src]['about'][a]
    return k

for sid, title, lead, groups in S:
    gs = []
    for gname, refs in groups:
        ks = [take(r) for r in refs.split()]
        assert len(ks) == len(set(ks)), ('dup', sid, gname)
        gs.append([gname, ks])
    sections.append(dict(id=sid, t=title, lead=lead, g=gs))
assert not (set(NEW) - set(works)), set(NEW) - set(works)
assert len({w['id'] for w in works.values()}) == len(works), 'same video twice'

data = json.dumps(dict(works=works, sections=sections, about=about, kind='マーチとワルツ',
                       weakSections=['intro', 'scenes'], stapleSections=['intro', 'scenes']),
                  ensure_ascii=False, separators=(',', ':'))
TIPS = '''<h2>マーチとワルツの聴き方のコツ</h2>
    <ul>
      <li><b>マーチは「1、2、1、2」の2拍子</b>。歩く足どりに合わせた音楽です。元気な前半のあと、まん中で「トリオ」というおだやかな部分に変わり、最後にまた盛り上がります。</li>
      <li><b>ワルツは「ズン・チャッ・チャッ」の3拍子</b>。1拍目が強く、2・3拍目は軽く。くるくる回りながら踊るための音楽です。</li>
      <li><b>ウィンナ・ワルツは「2拍目が少し早い」</b>。ウィーンの楽団は、2拍目をわずかに前に出して弾くくせがあり、それが独特の揺れになります。</li>
      <li><b>ウィンナ・ワルツはいくつかのワルツのつなぎ合わせ</b>。序奏のあと、小さなワルツが4〜5つ続き、最後に全部をふり返って終わります。</li>
      <li><b>同じ「行進曲」でも気分はさまざま</b>。お祝い、軍隊、お葬式、おもちゃの行進まで。気分の違いを聴きくらべると楽しめます。</li>
      <li><b>聴いたら「好き・ふつう・苦手」を押す</b>。上の「あなたへのおすすめ」に次の曲が出ます。</li>
    </ul>'''
tpl = (D/'page_template.html').read_text(encoding='utf-8')
html = (tpl.replace('__TITLE__', 'マーチとワルツ 聴くリスト')
           .replace('__EYEBROW__', '行進曲とワルツだけを集めて、YouTubeで')
           .replace('__LEAD__', 'クラシック・オペラ・吹奏楽から、マーチ（行進曲）とワルツだけを集めました。ウィーンのワルツ、バレエのワルツ、スーザのマーチ、日本の行進曲まで。見出しをタップすると開きます。')
           .replace('__TIPS__', TIPS)
           .replace('曲名・作曲家・ことばで探す（例：ショパン、運動会、のだめ）', '曲名・作曲家・ことばで探す（例：シュトラウス、スーザ、運動会）')
           .replace('__DATA__', data))
(D/'mw-playlist.html').write_text(html, encoding='utf-8')
nm = sum(1 for k in works if not any(k in g[1] for s in sections if s['id'].startswith('waltz') for g in s['g']))
nw = sum(1 for k in works if any(k in g[1] for s in sections if s['id'].startswith('waltz') for g in s['g']))
print('works', len(works), 'waltz', nw, 'march', nm, 'new', len(NEW), 'about', len(about), 'sections', len(sections))
