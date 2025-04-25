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
    large_area = request.form.get("large_area")  # 都道府県などのエリアコード

    # 共通パラメータ
    params = {
        "key": API_KEY,
        "format": "json",
        "count": 10,
        "keyword": keyword
    }

    # 緯度・経度が取得できている場合は位置情報で検索
    if lat and lng:
        params["lat"] = lat
        params["lng"] = lng
        params["range"] = range_km

    # 緯度・経度がなければ都道府県エリアで検索（例：関西、東北など）
    elif large_area:
        params["large_area"] = large_area

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
