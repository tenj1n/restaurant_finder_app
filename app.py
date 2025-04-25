from flask import Flask
import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# Flask アプリ作成
app = Flask(__name__)

# APIキーを読み込む
API_KEY = os.getenv("HOTPEPPER_API_KEY")

@app.route('/')
def index():
    return f'Flask アプリが動いています！APIキーは {API_KEY[:4]}**** です。'

if __name__ == '__main__':
    app.run(debug=True)
