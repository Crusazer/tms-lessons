""" This file contains main code for work with Flask. """
from flask import Flask, redirect, session, request
from flask_session import Session
from homework_18 import utilits
from homework_18 import db

# CONSTS
DATABASE_PATH = 'shop.db'

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def main_page():
    if session.get("is_authenticated"):
        session['current_page'] = '/'

    page = utilits.get_upper_string()
    page += f'<h3><a href="http://127.0.0.1:8080/products">Все товары</a></h3>'
    return page + utilits.get_main_page_string() + "</hr>"


@app.route("/products")
def all_products():
    if session.get("is_authenticated"):
        session['current_page'] = '/products'

    page = utilits.get_upper_string()
    page += '\n'.join([utilits.get_product_string(product) for product in db.load_products()])
    return page


@app.route("/product/<int:product_id>")
def send_page_product(product_id: int):
    if session.get("is_authenticated"):
        session['current_page'] = f"/product/{product_id}"

    product = db.load_product(product_id)
    return utilits.get_product_string(product)


@app.route("/category/<int:category_id>")
def products_from_category(category_id: int):
    if session.get("is_authenticated"):
        session['current_page'] = f"/category/{category_id}"

    page = utilits.get_upper_string()
    products = db.load_products_from_category(category_id)
    for product in products:
        page += utilits.get_product_string(product)
    return page


@app.route("/favorites")
def favorites():
    if not session.get("is_authenticated"):
        redirect('/auth')

    session['current_page'] = f"/favorites"
    page = utilits.get_upper_string()
    for product_id in session.get("favorite_products_id"):
        product = db.load_product(product_id)
        page += utilits.get_product_string(product)

    return page


'''---------REGISTRATION AND AUTHENTICATION----------------------------------'''


@app.route("/auth")
def authentication():
    return utilits.get_authentication_string()


@app.route("/registration")
def registration():
    return utilits.get_registration_string()


@app.route("/auth", methods=["POST"])
def authentication_user():
    username = request.form["username"]
    password = request.form["password"]

    # user is already sign in
    if session.get("is_authenticated"):
        return utilits.get_authentication_string("Вы уже вошли в аккаунт.")

    # user entered correct data
    user = db.load_user(username)
    if user and user.password == password:
        session["username"] = user.username
        session["password"] = user.password
        session["user_id"] = user.user_id
        session["favorite_products_id"] = db.load_favorites_user_products_id(user.user_id)
        session["is_authenticated"] = True
        return redirect("/")

    # user entered incorrect data
    return utilits.get_authentication_string("Вы ввели некорректный логин или пароль.", username, password)


@app.route("/registration", methods=["POST"])
def registration_user():
    username = request.form["username"]
    password = request.form["password"]

    # user is already sign in
    if session.get("is_authenticated"):
        return utilits.get_registration_string("Для регистрации нового аккаунта нужно выйти из текущего.")

    # user already exists
    if db.load_user(username):
        return utilits.get_registration_string("Пользователь с данным именем уже существует.")

    # user entered correct data
    db.create_user(username, password)
    user = db.load_user(username)
    session["username"] = user.username
    session["password"] = user.password
    session["user_id"] = user.user_id
    session['favorite_products_id'] = []
    session['current_page'] = '/registration'
    session["is_authenticated"] = True
    return utilits.get_registration_string("Поздравляем! регистрация пользователя прошла успешно.")


@app.route("/logout", methods=["POST"])
def logout_user():
    session["is_authenticated"] = False
    return redirect("/")


'''--------------------------------------------------------------------------'''


@app.route("/add_favorite/<int:product_id>", methods=["POST"])
def add_favorite_product(product_id: int):
    if not session.get("is_authenticated"):
        return redirect('/auth')

    # add product to favorite
    if product_id not in session['favorite_products_id']:
        session['favorite_products_id'].append(product_id)
        db.add_favorite_product(session["user_id"], product_id)
    # remove product from favorite
    else:
        session['favorite_products_id'].remove(product_id)
        db.delete_favorite_product(session["user_id"], product_id)

    return redirect(session.get("current_page"))


if __name__ == "__main__":
    app.run(port=8080, debug=True)
