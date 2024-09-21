from flask import Flask, render_template, request
from datetime import datetime
from scrape import scrape_stocks, scrape_pm25, get_pm25_json
import json

# print(__name__)

app = Flask(__name__)

books = {
    1: {
        "name": "Python book",
        "price": 299,
        "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
    },
    2: {
        "name": "Java book",
        "price": 399,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
    },
    3: {
        "name": "C# book",
        "price": 499,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
    },
}
today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.route("/")
def index():
    name = ""
    # return f"<h1>Hello Flask!</h1><h2>Hi Flask!</h2><h3>How are you Flask?</h3><h4>Flask {today}!</h4>"
    return render_template("index.html", date=today, name=name)


@app.route("/books")
def showBooks():
    for key in books:
        print(books[key])
    return render_template("books.html", books=books)


@app.route("/book/<int:id>")
def showBook(id):
    if id in books:
        return f"<h1 style='background-color:black; color:white'>編號{id}: {books[id]}</h1>"
    return f"<h1 style='color:red'>無此編號:{id}</h1>"


@app.route("/sum/x=<x>&y=<y>")
def mySum(x=0, y=0):
    try:
        total = eval(x) + eval(y)
        return f"<h2>{x} + {y} = {total}</h2>"
    except Exception as e:
        print(e)
        return "<h2 style='color:red'>輸入參數錯誤</h2>"


@app.route("/bmi/name=<name>&height=<height>&weight=<weight>")
def getBmi(name, height, weight):
    try:
        bmi = eval(weight) / (eval(height) / 100) ** 2
        return f"<h2>姓名: {name}, BMI: {bmi:.2f}</h2>"

    except Exception as e:
        print(e)
        return "<h2 style='color:red'>輸入參數錯誤</h2>"


@app.route("/stocks")
def get_stocks():
    try:
        datas = scrape_stocks()
        return render_template("stocks.html", datas=datas)

    except Exception as e:
        print(e)
        return "<h2 style='color:red'>錯誤</h2>"


@app.route("/pm25", methods=["GET", "POST"])
def get_PM():
    sort = False
    ascending = True
    # GET
    print(request.args)
    # POST
    print(request.form)
    try:
        if request.method == "POST":
            if "sort" in request.form:
                sort = True
                ascending = True if request.form.get("sort") == "true" else False
        columns, values = scrape_pm25(sort, ascending)
        data = {"columns": columns, "values": values, "today": today}
        return render_template("pm25.html", data=data)
    except Exception as e:
        print(e)
        return "<h2 style='color:red'>錯誤</h2>"


@app.route("/pm25-data")
def pm25_data():
    try:
        json_data = get_pm25_json()
        return json.dumps(json_data, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "exception": str(e)})


@app.route("/pm25-chart")
def pm25_chart():
    return render_template("pm25-chart.html")


app.run(debug=True)
