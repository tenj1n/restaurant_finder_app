from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import requests

# .env ファイルを読み込む（APIキーなどの環境変数を使えるようにする）
load_dotenv()

# Flaskアプリのインスタンス作成
app = Flask(__name__)

# .env に定義されたAPIキーを読み込む
API_KEY = os.getenv("HOTPEPPER_API_KEY")

# トップページ（検索フォーム）表示
@app.route('/')
def index():
    return render_template("index.html")

# 検索結果ページ（緯度・経度または都道府県エリアで検索）
@app.route('/search', methods=['POST'])
def search():
    # 緯度・経度（現在地）、検索半径、キーワード、エリアコードをフォームから取得
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    range_km = request.form.get("range")
    keyword = request.form.get("keyword", "")
    large_area = request.form.get("large_area")   # 大エリア(関西など)
    pref_area = request.form.get("pref_area")     # 都道府県（大阪など）
    middle_area = request.form.get("middle_area") # 市区(梅田など)

    # 共通パラメータ
    params = {
        "key": API_KEY,
        "format": "json",
        "count": 10,
        "keyword": keyword
    }

    # 市区が選択されている場合は、それを優先して検索 (大阪市、中央区など)
    if middle_area:
        params["middle_area"] = middle_area

    # 緯度・経度がなければ大エリアで検索（例：関西、東北など）
    elif large_area:
        params["large_area"] = large_area

    # 緯度・経度が取得できている場合は位置情報で検索
    elif lat and lng:
        params["lat"] = lat
        params["lng"] = lng
        params["range"] = range_km

    # APIリクエスト送信
    response = requests.get("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/", params=params)
    data = response.json()

    # 店舗情報を抽出（なければ空リスト）
    shops = data["results"]["shop"] if "results" in data and "shop" in data["results"] else []

    return render_template("results.html", shops=shops)

# 詳細ページ（店舗IDを使って1店舗分の詳細を取得）
@app.route('/detail/<shop_id>')
def detail(shop_id):
    params = {
        "key": API_KEY,
        "id": shop_id,
        "format": "json"
    }
    response = requests.get("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/", params=params)
    data = response.json()
    shop = data["results"]["shop"][0] if "results" in data and "shop" in data["results"] else None

    return render_template("detail.html", shop=shop)

# アプリ実行（このファイルが直接実行されたときのみ）
if __name__ == '__main__':
    app.run(debug=True)
