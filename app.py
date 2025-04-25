from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# .envファイルからAPIキーなどの環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# 環境変数からAPIキーを取得
API_KEY = os.getenv("HOTPEPPER_API_KEY")

# トップページ（検索フォーム）
@app.route('/')
def index():
    # クエリパラメータをparamsとしてテンプレートに渡す
    return render_template('index.html', params=request.args)

# 検索結果ページ
@app.route('/search', methods=['GET'])
def search():
    # フォームの入力値（GETパラメータ）を取得
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    range_km = request.args.get("range")
    keyword = request.args.get("keyword", "")
    large_area = request.args.get("large_area")
    pref_area = request.args.get("pref_area")
    middle_area = request.args.get("middle_area")

    # APIに渡すパラメータを準備
    params = {
        "key": API_KEY,
        "format": "json",
        "count": 10,
        "keyword": keyword
    }

    # 入力条件に応じてエリア情報を設定
    if middle_area:
        params["middle_area"] = middle_area
    elif large_area:
        params["large_area"] = large_area
    elif lat and lng:
        params["lat"] = lat
        params["lng"] = lng
        params["range"] = range_km

    # ホットペッパーAPIにGETリクエストを送信
    response = requests.get("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/", params=params)
    data = response.json()

    # 結果から店舗情報リストを取得（なければ空リスト）
    shops = data["results"].get("shop", [])

    # 結果と元の検索条件をテンプレートに渡す
    return render_template("results.html", shops=shops, search_params=request.args)

# サーバー起動
if __name__ == "__main__":
    app.run(debug=True)
