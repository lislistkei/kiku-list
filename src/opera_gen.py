# オペラ版の曲目表ページを opera_works.txt / opera_videos.tsv から作る
import json
from pathlib import Path
D = Path(__file__).parent

W = {}
for l in (D/'opera_works.txt').read_text(encoding='utf-8').splitlines():
    if not l.strip() or l.startswith('#'): continue
    k, comp, work, part, q, rng, point, trivia = l.split('|')
    W[k] = dict(c=comp, w=work, p=part, pt=point, tr=trivia)
for k, v in json.loads((D/'rewrite'/'points.json').read_text(encoding='utf-8'))['オペラ'].items(): W[k]['pt'] = v
V = {}
for l in (D/'opera_videos.tsv').read_text(encoding='utf-8').splitlines():
    if not l.strip(): continue
    k, vid, ln, ch = l.split('\t'); V[k] = dict(id=vid, len=ln, ch=ch)

S = [
 ('intro', '入門の13曲', '教本 序-3「最初の1本と、入門の順番」の作品から、まず聴きたい場面', [
   ['', 'boh-gelida boh-mimi trav-brindisi trav-sempre carmen-habanera carmen-toreador fig-ov mf-queen tosca-vissi mb-unbel aida-march tur-nessun ring-ride']]),
 ('voices', '資料3 声種別 まず聴きたいアリア', '好きな声の種類から探す', [
   ['ソプラノ', 'boh-mimi mb-unbel tosca-vissi babbino trav-sempre rig-caronome norma lucia mf-queen rusalka'],
   ['メゾソプラノ', 'carmen-habanera carmen-seguidilla bar-unavoce fig-voiche'],
   ['テノール', 'tur-nessun boh-gelida tosca-stelle rig-donna aida-celeste elisir pag-vesti carmen-flower'],
   ['バリトン', 'bar-largo rig-cortigiani carmen-toreador'],
   ['バス', 'dg-catalog bar-calunnia mf-hallen']]),
 ('history', '第3章 オペラの誕生とバロック', 'モンテヴェルディ、ヘンデル、グルック', [
   ['', 'orfeo-t lascia chefaro']]),
 ('mozart', '第4章 モーツァルト', '4大オペラの名場面', [
   ['『フィガロの結婚』', 'fig-ov fig-ballare fig-nonso fig-voiche fig-porgi fig-fin2 fig-letter fig-dove fig-deh fig-perdono'],
   ['『ドン・ジョヴァンニ』', 'dg-ov dg-catalog dg-champagne dg-batti dg-finestra dg-tesoro'],
   ['『コジ・ファン・トゥッテ』', 'cosi-soave cosi-scoglio cosi-aura'],
   ['『魔笛』', 'mf-vogel mf-bildnis mf-zittre mf-queen mf-hallen mf-ach mf-papagena']]),
 ('belcanto', '第5章 ベルカント', 'ロッシーニ、ドニゼッティ、ベッリーニ', [
   ['『セビリアの理髪師』', 'bar-ov bar-ecco bar-largo bar-unavoce bar-calunnia'],
   ['ロッシーニのほかの作品', 'tell-ov'],
   ['ドニゼッティとベッリーニ', 'elisir lucia norma']]),
 ('verdi', '第5章 ヴェルディ', 'イタリア・オペラの大家', [
   ['『ナブッコ』『リゴレット』', 'nabucco rig-questa rig-caronome rig-cortigiani rig-donna'],
   ['『イル・トロヴァトーレ』', 'trov-anvil trov-stride trov-pira'],
   ['『椿姫』', 'trav-prel trav-brindisi trav-undi trav-sempre trav-pura trav-amami trav-parigi'],
   ['『アイーダ』', 'aida-celeste aida-ritorna aida-march aida-patria aida-terra'],
   ['そのほかの名作と晩年の傑作', 'macbeth forza-ov forza-pace carlo ballo otello-esultate otello-credo falstaff']]),
 ('puccini', '第6章 プッチーニとヴェリズモ', '甘い旋律と、強いドラマ', [
   ['『ラ・ボエーム』', 'boh-gelida boh-mimi boh-soave boh-musetta boh-addio boh-zimarra'],
   ['『トスカ』', 'tosca-recondita tosca-tedeum tosca-vissi tosca-stelle'],
   ['『蝶々夫人』', 'mb-dovunque mb-love mb-unbel mb-humming mb-addio mb-tutu'],
   ['『トゥーランドット』', 'tur-signore tur-nonpiangere tur-reggia tur-nessun tur-tuchedigel'],
   ['『ジャンニ・スキッキ』『マノン・レスコー』', 'babbino manon-int'],
   ['ヴェリズモ（カヴァ・パリほか）', 'cav-int cav-easter cav-voilo pag-vesti chenier']]),
 ('wagner', '第7章 ワーグナー', '楽劇と『ニーベルングの指環』', [
   ['『指環』より前の作品', 'dutch-ov tann-pilgrim tann-abend loh-act3 loh-bridal'],
   ['『トリスタン』『マイスタージンガー』『パルジファル』', 'tristan-pl meis-prel parsifal'],
   ['『ニーベルングの指環』4部作', 'ring-rheingold ring-valhalla ring-winter ring-ride ring-wotan ring-forge ring-forest ring-rhine ring-funeral ring-immolation']]),
 ('carmen', '第8章 ビゼー『カルメン』', '知っている曲の連続', [
   ['', 'carmen-prel carmen-habanera carmen-seguidilla carmen-gypsy carmen-toreador carmen-flower carmen-entracte carmen-micaela carmen-final']]),
 ('world', '第8章 世界の名作', 'フランス、ドイツ語、R.シュトラウス、ロシア・東欧、英米と日本', [
   ['フランスの名作', 'faust-jewel romeo-waltz pearl dalila hoffmann-barc hoffmann-doll lakme manon-adieu werther thais'],
   ['ドイツ語の名作とオペレッタ', 'fidelio-ov freischutz hansel fledermaus merrywidow wozzeck'],
   ['R.シュトラウス', 'salome-dance elektra ariadne rosen-mono rosen-waltz rosen-trio rosen-final'],
   ['ロシア・東欧', 'boris queenspades igor rusalka jenufa'],
   ['イギリス・アメリカ・日本', 'dido grimes summertime yuzuru']]),
 ('singers', '第9章 名歌手で聴く', 'カラスと三大テノール', [
   ['', 'callas-casta tosca-vissi three-nessun pavarotti-pira domingo-otello']]),
 ('movies', '資料8 映画・CM・スポーツで流れるオペラ', 'どこかで聴いたあの曲', [
   ['', 'ring-ride tur-nessun fig-letter lucia trav-brindisi boh-soave babbino chenier pag-vesti cav-int tosca-tedeum lakme tell-ov aida-march loh-bridal hoffmann-barc']]),
]

used = set(); sections = []
for sid, title, lead, groups in S:
    gs = []
    for gname, keys in groups:
        ks = keys.split()
        for k in ks:
            assert k in W, ('no work', k); assert k in V, ('no video', k); used.add(k)
        gs.append([gname, ks])
    sections.append(dict(id=sid, t=title, lead=lead, g=gs))
assert not (set(W) - used), set(W) - used

works = {k: dict(**W[k], id=V[k]['id'], len=V[k]['len'], ch=V[k]['ch']) for k in W}
data = json.dumps(dict(works=works, sections=sections, kind='オペラ',
                       weakSections=['intro', 'voices', 'movies', 'singers'], stapleSections=['intro', 'movies']),
                  ensure_ascii=False, separators=(',', ':'))
TIPS = '''<h2>オペラの聴き方のコツ（教本より）</h2>
    <ul>
      <li><b>まず有名なアリア1曲から</b>。全幕は長いので、知っている曲が入った場面から入ります。</li>
      <li><b>どんな場面かを読んでから聴く</b>。「だれが、だれに、何を歌っているか」がわかると、言葉がわからなくても伝わります。</li>
      <li><b>映像で見る</b>。オペラは歌うお芝居。表情や衣装、舞台も楽しみのうちです。</li>
      <li><b>聴いたら「好き・ふつう・苦手」を押す</b>。上の「あなたへのおすすめ」に次の曲が出ます。</li>
      <li><b>続けて再生のリストは一時的</b>。YouTubeで開いたあと「保存」を押すと、マイリストに残ります。</li>
    </ul>'''
tpl = (D/'page_template.html').read_text(encoding='utf-8')
html = (tpl.replace('__TITLE__', 'オペラ教本 聴くリスト')
           .replace('__EYEBROW__', 'オペラの教本に出てくる名場面を、YouTubeで')
           .replace('__LEAD__', '教本の章ごとに、聴いてほしいアリアや場面を並べました。曲ごとに「聴きどころ」と「豆知識」つき。章の見出しをタップすると開きます。')
           .replace('__TIPS__', TIPS)
           .replace('曲名・作曲家・ことばで探す（例：ショパン、運動会、のだめ）', '作品名・作曲家・ことばで探す（例：椿姫、プッチーニ、映画）')
           .replace('__DATA__', data))
(D/'opera-playlist.html').write_text(html, encoding='utf-8')
print('works', len(works), 'cards', sum(len(g[1]) for s in sections for g in s['g']), 'sections', len(sections))
