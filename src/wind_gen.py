# 吹奏楽版の曲目表ページを wind_works.txt / wind_videos.tsv / about/w1.json から作る
import json
from pathlib import Path
D = Path(__file__).parent

W = {}
for l in (D/'wind_works.txt').read_text(encoding='utf-8').splitlines():
    if not l.strip() or l.startswith('#'): continue
    k, comp, title, part, q, rng, point, trivia = l.split('|')
    W[k] = dict(c=comp, w=title, p=part, pt=point, tr=trivia)
V = {}
for l in (D/'wind_videos.tsv').read_text(encoding='utf-8').splitlines():
    if not l.strip(): continue
    k, vid, ln, ch = l.split('\t'); V[k] = dict(id=vid, len=ln, ch=ch)

S = [
 ('intro', '入門の12曲', 'まずはここから。マーチ、吹奏楽のための名曲、ポップスを少しずつ', [
   ['', 'stars bogey kameraden olympic holst1 armenian alvamar fumon tanabata takarajima raiders african']]),
 ('march-world', 'マーチ（世界の行進曲）', 'アメリカのマーチ王スーザから、ヨーロッパの軍楽隊、スペインのパソ・ドブレ、映画のマーチまで', [
   ['「マーチ王」スーザ', 'stars washington liberty semper thunderer capitan kingcotton handsacross manhattan cadets invincible blackhorse'],
   ['アメリカのマーチ', 'emblem barnum lassus americanswe onthemall patrol anchors amsalute'],
   ['イギリスのマーチ', 'bogey pomp1 crown orb dambusters knightsbridge seasongs'],
   ['ドイツ・オーストリア・チェコ・ロシア', 'kameraden doppeladler radetzky preussens gladiatoren florentiner gladiators slavianka'],
   ['フランス・ベルギー・スペイン・イタリア', 'sambre arsenal espana amparito aidamarch'],
   ['映画とオリンピックのマーチ', 'raiders imperial superman greatescape longestday olyfanfare']]),
 ('march-japan', 'マーチ（日本の行進曲）', '式典やスポーツでおなじみの名曲と、コンクール課題曲のマーチ', [
   ['日本の名行進曲', 'gunkan olympic sportsshow shukuten ozora eikan akizorani'],
   ['コンクール課題曲のマーチ（年の順）', 'takeoff marine catalonia turnbull shiokemuri kten haruka streetperf kibou harukazemichi aprilleaf bluespring kirameki pegasus yuuki memories marcha']]),
 ('roots', '吹奏楽のルーツ', '吹奏楽が生まれる前から、管楽器のための名曲があった', [
   ['', 'fireworks granpartita dvserenade rsserenade gounod berlioz']]),
 ('classics', '吹奏楽の古典（イギリス・アメリカ）', '「吹奏楽のための芸術作品」のはじまり', [
   ['イギリス：ホルストとヴォーン・ウィリアムズ', 'holst1 holst2 hammersmith folksong toccata'],
   ['イギリス：グレインジャーとジェイコブ', 'lincoln irish shepherd byrd'],
   ['アメリカで生まれた古典', 'schoenberg milhaud hindemith shaker']]),
 ('modern', '現代の名曲（アメリカ・ヨーロッパ）', '日本の吹奏楽部でもおなじみの作曲家たち', [
   ['アルフレッド・リード', 'armenian elcamino russianxmas festprelude hounds punchinello'],
   ['ジェイムズ・バーンズ', 'alvamar barnes3'],
   ['アメリカの名曲', 'festvar eternal korean hymnsong shenandoah blueshades october ride candide'],
   ['今のアメリカの人気作曲家（ティケリ・マッキー・ウィテカー）', 'cajun vesuvius asphalt aurora sleep'],
   ['ヨーロッパの名曲', 'dragon dancemov orient harrison lotr oregon spartacus puszta']]),
 ('japan', '日本の吹奏楽', '日本の作曲家が書いた名曲。祭りや神話を描いた曲も', [
   ['名作の数々', 'passacaglia osaka shinwa gururi japonisme tanabata kushinada magellan hinoboru fuyou gr'],
   ['コンクール課題曲の名曲', 'fumon kazenomai discokid']]),
 ('pops', 'ポップス・映画音楽', '演奏会のアンコールや野球の応援でおなじみ', [
   ['ポップス', 'takarajima omens african cumbanchero mambo5 september jounetsu discokid lupin'],
   ['ジャズ（スウィング）', 'singsing inthemood moonlight'],
   ['映画音楽', 'starwars raiders imperial superman pirates morricone']]),
 ('arrange', 'クラシックの編曲もの', 'オーケストラの名曲を吹奏楽で。コンクールの自由曲の定番', [
   ['', 'feste pini daphnis firebird kiev sabre candide']]),
 ('kadai', '全日本吹奏楽コンクールの課題曲', '毎年えらばれる課題曲から、名曲・人気曲（年の順）', [
   ['', 'shukuten discokid takeoff fumon marine catalonia turnbull shiokemuri kten kazenomai haruka streetperf kibou harukazemichi aprilleaf bluespring kirameki pegasus yuuki memories marcha']]),
 ('scenes', '「あの曲」の正体', '運動会、野球の応援、テレビ、サーカスで聴いたあの曲', [
   ['野球の応援・運動会', 'african cumbanchero takarajima lupin eikan olympic sportsshow sabre longestday'],
   ['テレビ・映画・サーカス・サッカー', 'liberty bogey gladiators gunkan greatescape jounetsu aidamarch radetzky']]),
 ('instruments', '楽器別 この楽器が活躍する曲', '好きな楽器から探す', [
   ['ピッコロ', 'stars florentiner'], ['クラリネット', 'blueshades granpartita'], ['サックス', 'takarajima singsing'],
   ['ホルン', 'festvar rsserenade firebird'], ['トランペット', 'raiders cumbanchero'], ['トロンボーン', 'lassus stars'],
   ['ユーフォニアム・チューバ（低音）', 'doppeladler emblem'], ['打楽器', 'cumbanchero gururi vesuvius sabre'], ['鐘（チャイム）', 'liberty russianxmas']]),
]

used = set(); sections = []
for sid, title, lead, groups in S:
    gs = []
    for gname, keys in groups:
        ks = keys.split()
        assert len(ks) == len(set(ks)), ('dup', sid, gname)
        for k in ks:
            assert k in W, ('no work', k); assert k in V, ('no video', k); used.add(k)
        gs.append([gname, ks])
    sections.append(dict(id=sid, t=title, lead=lead, g=gs))
assert not (set(W) - used), set(W) - used

works = {k: dict(**W[k], id=V[k]['id'], len=V[k]['len'], ch=V[k]['ch']) for k in W}
ABOUT = {}
for f in sorted((D/'about').glob('w[0-9]*.json')):
    ABOUT.update(json.loads(f.read_text(encoding='utf-8')))
ABOUT = {a: v for a, v in ABOUT.items() if any(w['c'] + '|' + w['w'] == a for w in works.values())}
print('about', len(ABOUT), 'of', len({w['c'] + '|' + w['w'] for w in works.values()}))
data = json.dumps(dict(works=works, sections=sections, about=ABOUT, kind='吹奏楽',
                       weakSections=['intro', 'kadai', 'scenes', 'instruments'], stapleSections=['intro', 'scenes']),
                  ensure_ascii=False, separators=(',', ':'))
TIPS = '''<h2>吹奏楽の聴き方のコツ</h2>
    <ul>
      <li><b>マーチは「3つの部分」を聴きわける</b>。元気な第1マーチ・第2マーチのあと、まん中で「トリオ」というおだやかな部分に変わり、最後にまた盛り上がります。</li>
      <li><b>同じ曲を楽団を変えて聴く</b>。アメリカの軍楽隊、日本の学校の吹奏楽部、プロの楽団で、同じマーチでも響きがかなり違います。</li>
      <li><b>主役の楽器を1つ決めて追いかける</b>。ピッコロ、トロンボーン、低音など、吹奏楽はどの楽器にも見せ場があります。</li>
      <li><b>聴いたら「好き・ふつう・苦手」を押す</b>。上の「あなたへのおすすめ」に次の曲が出ます。</li>
      <li><b>続けて再生のリストは一時的</b>。YouTubeで開いたあと「保存」を押すと、マイリストに残ります。</li>
    </ul>'''
tpl = (D/'page_template.html').read_text(encoding='utf-8')
html = (tpl.replace('__TITLE__', '吹奏楽 聴くリスト')
           .replace('__EYEBROW__', '吹奏楽の名曲とマーチを、YouTubeで')
           .replace('__LEAD__', 'マーチを中心に、吹奏楽のための名曲、コンクールの課題曲、ポップスまで。曲ごとに「聴きどころ」と豆知識つき。見出しをタップすると開きます。')
           .replace('__TIPS__', TIPS)
           .replace('曲名・作曲家・ことばで探す（例：ショパン、運動会、のだめ）', '曲名・作曲家・ことばで探す（例：スーザ、課題曲、野球）')
           .replace('__DATA__', data))
(D/'wind-playlist.html').write_text(html, encoding='utf-8')
print('works', len(works), 'cards', sum(len(g[1]) for s in sections for g in s['g']), 'sections', len(sections))
