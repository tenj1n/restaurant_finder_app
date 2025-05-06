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

@app.route('/search', methods=['GET'])
def search():
    # フォームからの検索条件を取得
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    range_km = request.args.get("range")
    keyword = request.args.get("keyword", "")
    large_area = request.args.get("large_area")
    pref_area = request.args.get("pref_area")  # 使わないけど取得だけしておく
    middle_area = request.args.get("middle_area")

    # ホットペッパーAPIに渡す基本パラメータ
    params = {
        "key": API_KEY,
        "format": "json",
        "count": 10,
        "keyword": keyword
    }

    #  地域検索の優先順位（middle_area > large_area > 緯度経度）
    if middle_area:
        params["middle_area"] = middle_area
    elif large_area:
        params["large_area"] = large_area
    elif lat and lng and lat.lower() != "none" and lng.lower() != "none":
        # 緯度経度による検索（位置情報が有効な場合）
        params["lat"] = lat
        params["lng"] = lng
        params["range"] = range_km

    #  APIリクエスト送信
    response = requests.get("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/", params=params)
    data = response.json()

    #  店舗リストを取得（なければ空リスト）
    shops = data["results"].get("shop", [])

    #  結果と検索条件をテンプレートへ渡して表示
    return render_template("results.html", shops=shops, search_params=request.args)

# サーバー起動
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
