# 聴くリストの元データ

公開ページ：https://amamanogaeru.github.io/kiku-list/ （検索に出ない設定）

## ファイル
- works.txt / trivia.txt / videos.tsv … クラシックの曲・豆知識・動画
- opera_works.txt / opera_videos.tsv … オペラの名場面（豆知識つき）と動画
- rewrite/points.json … 聴きどころ（情景たっぷり版。works の聴きどころを上書きする）
- page_template.html … ページのひな形（目次・好き嫌い・おすすめ・埋めこみ再生）
- gen.py / opera_gen.py … Claudeのページ用 HTML を作る
- make_site.py … 公開用（site/）の HTML を作る

## 作り直し方
src の中身を1つのフォルダに置き、`python gen.py` → `python opera_gen.py` → `python make_site.py` の順に実行。
できた site/ の中身（index.html, classical/, opera/）をこのリポジトリに入れて push する。
