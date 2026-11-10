# 曲目表ページを works.txt / trivia.txt / videos.tsv から作る
import json, re
from pathlib import Path
D = Path(__file__).parent

W = {}
for l in (D/'works.txt').read_text(encoding='utf-8').splitlines():
    if not l.strip() or l.startswith('#'): continue
    k, comp, title, part, q, rng, point = l.split('|')
    W[k] = dict(c=comp, w=title, p=part, pt=point)
# 資料8で使う追加の3曲
W['harold'] = dict(c='ベルリオーズ', w='交響曲「イタリアのハロルド」', p='全曲', pt='独奏ヴィオラが主人公ハロルドを演じる交響曲')
W['bartokvla'] = dict(c='バルトーク', w='ヴィオラ協奏曲', p='全曲', pt='落ち着いた中音域のヴィオラが主役の協奏曲')
W['handelharp'] = dict(c='ヘンデル', w='ハープ協奏曲 変ロ長調 作品4-6', p='全曲', pt='ハープの協奏曲は数が少なく貴重')

T = {}
for l in (D/'trivia.txt').read_text(encoding='utf-8').splitlines():
    if not l.strip() or l.startswith('#'): continue
    k, v = l.split('|', 1); T[k] = v
T['harold'] = 'パガニーニが「自分が弾くヴィオラの協奏曲を」と頼んだが、できた曲はヴィオラの出番が少なく、パガニーニは弾かなかった。のちに曲を聴いたパガニーニは感激し、ベルリオーズに大金を贈ったと伝えられる'
T['bartokvla'] = 'バルトークが白血病で亡くなったとき、スケッチの段階で未完成だった最後の作品。弟子のシェルイが楽譜を仕上げた'
T['handelharp'] = 'オラトリオの幕間に、ヘンデル自身が観客を楽しませるために演奏した協奏曲集の1曲。もとはオルガン協奏曲集（作品4）に入っている'

V = {}
for l in (D/'videos.tsv').read_text(encoding='utf-8').splitlines():
    if not l.strip(): continue
    k, vid, ln, ch = l.split('\t'); V[k] = dict(id=vid, len=ln, ch=ch)
V['harold'] = dict(id='Q4NC4E5RXik', len='43:57', ch='hr-Sinfonieorchester – Frankfurt Radio Symphony')
V['bartokvla'] = dict(id='DIfvuE-WI0w', len='22:45', ch='hr-Sinfonieorchester – Frankfurt Radio Symphony')
V['handelharp'] = dict(id='2ksD9MrSuO0', len='10:23', ch='Singapore National Youth Orchestra')

# 選んだ動画に合わせて「ここを聴く」を直す
P = {
 'hungarian2': 'オーケストラ版', 'firebird': 'カスチェイ王の魔の踊り',
 'bminor': 'キリエ（動画は全曲。冒頭の約12分がキリエ）', 'brand5': '全3楽章（第1楽章から）',
 'bvc': '第1楽章（動画は全曲。はじめの約25分）', 'dvcello': '第1楽章（動画は全曲。はじめの約15分）',
 'mvc': '第1楽章（動画は全曲。はじめの約13分）', 'tpc1': '第1楽章（動画は全曲。はじめの約20分）',
 'gould55': 'アリア（1955年のデビュー盤）', 'casals': 'プレリュード（カザルスの録音）',
 'richter2': '第1楽章（リヒテルの録音）', 'pollini': '作品10-1（ポリーニの録音）',
 'musici': '「春」第1楽章（イ・ムジチの録音）', 'kleiber57': '第7番 全曲（クライバー／ウィーン・フィル）',
 'mrav': '全曲（ムラヴィンスキーの録音）', 'furt9': '全曲（フルトヴェングラーのバイロイト盤）',
 'dupre': '全曲（デュ・プレの録音）', 'heldenleben': '全曲', 'alpine': '全曲',
}
for k, v in P.items(): W[k]['p'] = v
for k, v in json.loads((D/'rewrite'/'points.json').read_text(encoding='utf-8'))['クラシック'].items(): W[k]['pt'] = v
W['kleiber57']['w'] = '交響曲第7番'

S = [
 ('intro', '入門12曲', '教本13-4「最初に聴く10曲」。まずはここから', [
   ['', 'b5-1 nw-2 nw-4 b7-1 eine spring gair noct2 heroic tpc1 bolero jupiter']]),
 ('baroque', '第3章 バロック', 'バッハ、ヘンデル、ヴィヴァルディたち', [
   ['バッハ', 'matthew john bminor jesu brand5 wtc1 goldberg cello1 chaconne toccata minuetG'],
   ['ヘンデル', 'hallelujah water fireworks conquering ombra'],
   ['ほかのバロックの名曲', 'orfeo canon albinoni corelli8 tafel rameau scarlatti spring winter']]),
 ('haydn-mozart', '第4章 ハイドンとモーツァルト', '古典派の「交響曲の父」と「神童」', [
   ['ハイドン', 'h45 h94 h100 h101 h103 h104 kaiserq htpt'],
   ['モーツァルト 交響曲とセレナード', 'eine m25 m35 m36 m38 m40 m41'],
   ['モーツァルト 協奏曲と室内楽', 'mpc20 mpc21 mpc23 mpc27 mcl mvc5 mflh mclq mob mbsn mhn4'],
   ['モーツァルト ピアノ曲・声楽・オペラ', 'turkish twinkle lacrimosa avever figaro queen']]),
 ('beethoven', '第4章 ベートーヴェン', '交響曲9曲と、ピアノ・協奏曲・室内楽', [
   ['交響曲（第1〜9番）', 'b1 b2 b3 b4 b5-1 b6 b7-1 b7-2 b8 b9-4'],
   ['ピアノ曲', 'pathetique moonlight appass hammer op111 elise'],
   ['協奏曲・室内楽・声楽', 'emperor bvc bspring kreutzer bturkish grossefuge solemnis fidelio']]),
 ('romantic1', '第5章 ロマン派（前半）', 'シューベルト、メンデルスゾーン、シューマン、リスト', [
   ['シューベルト', 'erlking heiden avemaria standchen lindenbaum mullerin unfinished great trout deathmaiden impromptu d960'],
   ['メンデルスゾーン', 'wedding mvc scottish italian fingal springsong'],
   ['シューマン', 'traumerei sch1 rhenish dichter carnaval kreisler'],
   ['リストとパガニーニ', 'campanella liebestraum hungarian2 feuxfollets sospiro preludes caprice24']]),
 ('chopin', '第5章 ショパン', 'ピアノの詩人の小品から大曲まで', [
   ['短い曲（小品）', 'noct2 noct20 farewell revolution blackkey winterwind minute grandev heroic military mazurka raindrop prelude7'],
   ['大きな曲', 'ballade1 scherzo2 fantimp funeral cpc1 barcarolle polfant ballade4']]),
 ('strauss', '第5章 シュトラウス一家', 'ワルツ王と、ニューイヤーコンサートの名曲', [
   ['', 'radetzky danube wienerwald kaiserwalzer fruhling tritsch sphaeren dorfschw bahnfrei']]),
 ('romantic2', '第6章 ロマン派（後半）', 'ワーグナー、ブラームス、ブルックナー、マーラー、R.シュトラウス', [
   ['ワーグナー', 'rheingold valkyrie siegfriedfun tristan bridal tannhauser meister'],
   ['ブラームス', 'br1 br2 br3 br4 brvc brclq'],
   ['ブルックナー', 'bru4 bru7 bru8 bru9'],
   ['マーラー', 'ma1 ma2 ma3 ma4 adagietto ma6 ma7 ma8 erde ma9 ma10'],
   ['R.シュトラウス', 'zara donjuan till heldenleben donquixote alpine salome rosen abendrot rsob rshn1']]),
 ('national', '第7章 国民楽派とロシア・イギリス', 'チャイコフスキー、ロシア、チェコ、北欧、イギリス', [
   ['チャイコフスキー', 't4 t5 t6-3 t6-4 tpc1 tvc y1812 serenade cantabile slavonic capriccio june october'],
   ['チャイコフスキーの三大バレエ', 'swanscene cygnets sleeping nutmarch sugarplum flowers trepak'],
   ['ロシアの名曲', 'pictures baldmt polovtsian scheherazade bumblebee sabre masquerade'],
   ['チェコ', 'moldau nw-2 nw-4 dvcello american humoresque mother slavdance'],
   ['北欧', 'morning hall solveig troldhaugen finlandia'],
   ['イギリス', 'pomp salut nimrod elgarcello mars jupiter neptune']]),
 ('modern', '第8章 近代・20世紀', 'フランス、ラフマニノフ、ストラヴィンスキー、ソ連、アメリカ、日本', [
   ['ドビュッシー', 'clair flax arabesque reverie golliwog faune lamer fetes syrinx'],
   ['ラヴェル', 'bolero pavane daphnis jeux scarbo lavalse ravelpc'],
   ['サティとフランスの仲間', 'gymno gnoss jetv swan elephant organ macabre apresunreve sicilienne carmen farandole arlminuet cancan sorcerer'],
   ['ラフマニノフ', 'rach2 rach3 paganini18 rachsym2 bells vocalise'],
   ['ストラヴィンスキー', 'firebird petrushka rite pulcinella'],
   ['プロコフィエフとショスタコーヴィチ', 'peter montagues classical propc3 shos5 shos7 waltz2'],
   ['アメリカ・日本・現代', 'rhapsody barber wss verklarte cfo mspc barbaro fortuna aranjuez november godzilla tapkaara spiegel reich18 glass cage gorecki']]),
 ('highlights', '第9章 名曲の聴きどころ', '「ここを聴く」がはっきりしている名曲', [
   ['9-1〜9-7', 'b9-4 b5-1 nw-2 nw-4 t6-3 t6-4 bolero rite adagietto'],
   ['9-8 名曲ミニガイド', 'tpc1 rach2 mvc br1 b7-2 unfinished pictures mars neptune moldau winter']]),
 ('records', '第13章 名盤を聴く', '会話によく出る歴史的名盤', [
   ['', 'furt9 kleiber57 mrav gould55 casals richter2 dupre pollini musici']]),
 ('anokyoku', '第14章「あの曲」の正体', '運動会、卒業式、結婚式、テレビで聴いたあの曲', [
   ['運動会・卒業式・表彰式', 'cancan csikos tell pomp canon gair conquering'],
   ['結婚式', 'wedding bridal salut jesu'],
   ['街角・テレビ・映画', 'nw-2 maiden elise b9-4 radetzky danube zara valkyrie adagietto'],
   ['フィギュアスケート・ポップス', 'ballade1 bells masquerade scheherazade jupiter']]),
 ('seasons', '季節の12か月', '教本第14章の「月ごとのおすすめ」', [
   ['1月', 'danube radetzky'], ['2月', 'winter'], ['3月', 'bspring'], ['4月', 'sch1 spring'],
   ['5月', 'fruhling springsong'], ['6月', 'wedding june'], ['7月', 'water'], ['8月', 'faune lamer'],
   ['9月', 'clair'], ['10月', 'october'], ['11月', 'brclq'], ['12月', 'b9-4 sugarplum hallelujah']]),
 ('instruments', '資料8 楽器別 まず聴きたい曲', '好きな楽器から探す', [
   ['ヴァイオリン', 'mvc chaconne'], ['ヴィオラ', 'harold bartokvla'], ['チェロ', 'dvcello cello1 swan'],
   ['コントラバス', 'elephant'], ['フルート', 'mflh syrinx'], ['オーボエ', 'mob rsob'],
   ['クラリネット', 'mcl mclq'], ['ファゴット', 'mbsn sorcerer'], ['ホルン', 'mhn4 rshn1'],
   ['トランペット', 'htpt'], ['ハープ', 'handelharp mflh'], ['打楽器', 'bolero'], ['ギター', 'aranjuez'],
   ['オルガン', 'toccata organ'], ['ピアノ', 'ballade1 emperor rach2'], ['歌（歌曲）', 'erlking lindenbaum']]),
]

used = set()
sections = []
for sid, title, lead, groups in S:
    gs = []
    for gname, keys in groups:
        ks = keys.split()
        for k in ks:
            assert k in W and k in V and k in T, k
            used.add(k)
        gs.append([gname, ks])
    sections.append(dict(id=sid, t=title, lead=lead, g=gs))
unused = set(W) - used
assert not unused, unused

works = {k: dict(c=W[k]['c'], w=W[k]['w'], p=W[k]['p'], pt=W[k]['pt'], tr=T[k], id=V[k]['id'], len=V[k]['len'], ch=V[k]['ch']) for k in W}
data = json.dumps(dict(works=works, sections=sections, kind='クラシック', weakSections=['intro', 'seasons', 'highlights', 'anokyoku'], stapleSections=['intro', 'highlights', 'anokyoku']), ensure_ascii=False, separators=(',', ':'))
tpl = (D/'page_template.html').read_text(encoding='utf-8')
TIPS = '''<h2>聴き方のコツ（教本13-4より）</h2>
    <ul>
      <li><b>まず1つの楽章だけ</b>。交響曲は長くても、1つの楽章は10分前後です。</li>
      <li><b>同じ曲を3回聴く</b>。2回目から「さっきのメロディが戻ってきた」と分かります。</li>
      <li><b>耳の目印を1つ決める</b>。「最初のメロディ」「主役の楽器」などを追いかけます。</li>
      <li><b>聴いたら「好き・ふつう・苦手」を押す</b>。上の「あなたへのおすすめ」に次の曲が出ます。</li>
      <li><b>続けて再生のリストは一時的</b>。YouTubeで開いたあと「保存」を押すと、マイリストに残ります。</li>
    </ul>'''
html = (tpl.replace('__TITLE__', 'クラシック教本 聴くリスト')
           .replace('__EYEBROW__', 'クラシック音楽の教本に出てくる曲を、YouTubeで')
           .replace('__LEAD__', '教本の章ごとに、聴いてほしい曲を並べました。曲ごとに「聴きどころ」と、話のたねになる豆知識つき。章の見出しをタップすると開きます。')
           .replace('__TIPS__', TIPS)
           .replace('__DATA__', data))
(D/'classical-playlist.html').write_text(html, encoding='utf-8')
n_cards = sum(len(g[1]) for s in sections for g in s['g'])
print('works', len(works), 'cards', n_cards, 'sections', len(sections))
