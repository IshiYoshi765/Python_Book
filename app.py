from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "".join(random.choices(string.ascii_letters, k=256))


@app.route("/", methods=["GET"])
def index():
    msg = request.args.get("msg")

    if msg == None:
        return render_template("index.html")
    else:
        return render_template("index.html", msg=msg)


@app.route("/", methods=["POST"])
def login():
    mail = request.form.get("mail")
    password = request.form.get("password")

    # ログイン判定
    if db.login(mail, password):
        session["user"] = True  # session にキー：'user', バリュー:True を追加
        session.permanent = True  # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=5)  # session の有効期限を 5 分に設定
        return redirect(url_for("mypage"))
    else:
        error = "メールアドレスまたはパスワードが違います。"

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {"mail": mail, "password": password}
        return render_template("index.html", error=error, data=input_data)


@app.route("/mypage", methods=["GET"])
def mypage():
    # session にキー：'user' があるか判定
    if "user" in session:
        return render_template("mypage.html")  # session があれば mypage.html を表示
    else:
        return redirect(url_for("index"))  # session がなければログイン画面にリダイレクト


@app.route("/logout")
def logout():
    session.pop("user", None)  # session の破棄
    return redirect(url_for("index"))  # ログイン画面にリダイレクト


@app.route("/register")
def register_form():
    return render_template("register.html")


@app.route("/register_exe", methods=["POST"])
def register_exe():
    user_name = request.form.get("username")
    tell = request.form.get("tell")
    mail = request.form.get("mail")
    password = request.form.get("password")

    if mail == "":
        error = "メールアドレスが未入力です。"
        return render_template(
            "register.html", error=error, mail=mail, password=password
        )
    if password == "":
        error = "パスワードが未入力です。"
        return render_template("register.html", error=error)

    count = db.insert_user(user_name, tell, mail, password)

    if count == 1:
        msg = "登録が完了しました。"
        return redirect(url_for("index", msg=msg))
    else:
        error = "登録に失敗しました。"
        return render_template("register.html", error=error)


@app.route("/book_register_form")
def book_register_form():
    return render_template("book_register_form.html")


@app.route("/book_register", methods=["POST"])
# 本の登録
def book_register():
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    publisher = request.form.get("publisher")

    db.insert_book(isbn, title, author, publisher)

    return render_template("book_register.html")


@app.route("/book_delete_form")
def book_delete_form():
    return render_template("book_delete_form.html")


@app.route("/book_delete", methods=["POST"])
# 本の削除
def book_delete():
    id = request.form.get("id")

    db.delete_book(id)

    return render_template("book_delete.html")


if __name__ == "__main__":
    app.run(debug=True)
