# Sets up the routes for all the pages

# 1. 在檔案最上方的 import 區塊加入 OpenAI
from flask import request
from openai import OpenAI
import os

# 2. 初始化 OpenAI Client (請確保您有設定 OPENAI_API_KEY 環境變數)
client = OpenAI()
from flask import Flask, render_template, request, make_response
from flask_caching import Cache
from config import TEMPLATES_PATH, TEXT_PATH
from application.helpers import *


app = Flask(__name__, template_folder=TEMPLATES_PATH)
app.jinja_env.filters["is_active"] = is_active
app.jinja_env.filters["get_language_image"] = get_language_image

app.config["CACHE_TYPE"] = "simple"
app.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache = Cache(app)


@app.route("/")
def loading():
    """Renders the 'Loading' page of the website."""

    #response = make_response(render_template("loading.html"))
    #response.headers["Cache-Control"] = "public, max-age=3"

    #return response
    return render_template("home.html")


@app.route("/home")
@cache.cached()
def home():
    """Renders the 'Home' page of the website."""

    return render_template("home.html")


@app.route("/about")
@cache.cached()
def about():
    """Renders the 'About Me' page of the website."""

    content = read_description(f"{TEXT_PATH}/about.txt")

    return render_template("about.html", content=content)


@app.route("/skills")
@cache.cached()
def skills():
    """Renders the 'Skills' page of the website."""

    skills = get_skills(f"{TEXT_PATH}/skills.json")

    return render_template("skills.html", skills=skills)


@app.route("/portfolio")
@cache.cached()
def portfolio():
    """Renders the 'Portfolio' page of the website."""

    repos = get_repositories()

    return render_template("portfolio.html", repos=repos)


@app.route("/contact", methods=["GET", "POST"])
@cache.cached()
def contact():
    """Renders the 'Contact' page of the website."""

    # User reached route via POST
    if request.method == "POST":
        return render_template("result.html")

    # User reached route via GET
    return render_template("contact.html")


@app.route("/result")
@cache.cached()
def result():
    """Renders the 'Result' page of the website."""

    return render_template("result.html")

@app.route('/ai_chat', methods=['GET', 'POST'])
def ai_chat():
    generated_text = None
    
    # 如果使用者送出表單 (POST)，則呼叫 OpenAI API
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        
        if prompt:
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="gpt-4o-mini",
                    temperature=0.5,
                )
                generated_text = response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"Error: {e}")
                generated_text = f"發生錯誤：{e} (請確認 API 金鑰是否設定正確)"
                
    # 不論是 GET (初次載入) 還是 POST (送出問題後)，都渲染同一個頁面
    return render_template('ai_chat.html', response=generated_text)
