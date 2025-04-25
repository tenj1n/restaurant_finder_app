# Flask本体とテンプレート・リクエスト機能を読み込む
from flask import Flask, render_template, request

# OSモジュールと .env の読み込み用
import os
from dotenv import load_dotenv

# API呼び出し用のHTTPクライアントライブラリ
import requests

# .env ファイルを読み込み（環境変数を使えるようにする）
load_dotenv()

# Flaskアプリケーションを作成
app = Flask(__name__)

# .env に保存した APIキーを読み込む
API_KEY = os.getenv("HOTPEPPER_API_KEY")

# 🔹 トップページ（検索フォーム）表示
@app.route('/')
def index():
    # templates/index.html を読み込んでブラウザに表示
    return render_template("index.html")

# 🔹 検索結果ページ（APIで取得した飲食店一覧）
@app.route('/search', methods=['POST'])  # ← POSTメソッドでのみ受け付ける
def search():
    # フォームから送信された値を取得
    lat = request.form.get("lat")        # 緯度
    lng = request.form.get("lng")        # 経度
    range_km = request.form.get("range") # 検索半径
    keyword = request.form.get("keyword", "")  # キーワード（例：ラーメン）

    # ホットペッパーグルメサーチAPIのクエリパラメータを準備
    params = {
        "key": API_KEY,          # 認証用APIキー
        "lat": lat,
        "lng": lng,
        "range": range_km,
        "keyword": keyword,
        "format": "json",        # 結果形式：JSON
        "count": 10              # 最大10件取得
    }

    # ホットペッパーAPIにGETリクエストを送る
    response = requests.get("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/", params=params)

    # JSON形式でレスポンスを受け取る
    data = response.json()

    # 店舗情報だけを取り出す（なければ空リスト）
    shops = data["results"]["shop"] if "results" in data and "shop" in data["results"] else []

    # templates/results.html に店舗リスト（shops）を渡して表示
    return render_template("results.html", shops=shops)



#  アプリを実行（このファイルが直接実行されたときのみ）
if __name__ == '__main__':
    # Flaskの開発用サーバーをデバッグモードで起動
    app.run(debug=True)

