""" This file contains main code for work with Flask. """
from flask import Flask, redirect, session, request
from flask_session import Session
from homework_18 import db
from jinja2 import Environment, FileSystemLoader

# CONSTS
DATABASE_PATH = 'shop.db'

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize jinja
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

# Jinja pages
main_page = env.get_template("main.html")
authorization_page = env.get_template("authorization.html")
registration_page = env.get_template("registration.html")
product_page = env.get_template("product.html")
products_page = env.get_template("products.html")
favorite_products = env.get_template("favorite_products.html")
category_page = env.get_template("category.html")


@app.route('/')
def send_main_page():
    last_page = '/'
    if session.get("is_authenticated"):
        last_page = session['current_page']
        session['current_page'] = '/'

    return main_page.render(products=db.load_product_order_by_categories(), title="Главная страница",
                            is_auth=session.get("is_authenticated", False), username=session.get("username", ""),
                            last_page=last_page)


@app.route("/products")
def send_all_products_page():
    favorite_products_id = []
    last_page = '/'
    if session.get("is_authenticated"):
        last_page = session['current_page']
        session['current_page'] = '/products'
        favorite_products_id = session.get('favorite_products_id')

    return products_page.render(products=db.load_products(), title="Все продукты",
                                is_auth=session.get("is_authenticated", False), username=session.get("username", ""),
                                favorites=favorite_products_id, last_page=last_page)


@app.route("/product/<int:product_id>")
def send_product_page(product_id: int):
    last_page = '/'
    if session.get("is_authenticated"):
        last_page = session['current_page']
        session['current_page'] = f"/product/{product_id}"

    product = db.load_product(product_id)
    sign = ''
    text_button = "Добавить в избранное"
    if session.get('is_authenticated') and product.id in session.get('favorite_products_id'):
        sign = '&#10027;'
        text_button = "Удалить из избранного"

    return product_page.render(product=product, text_button=text_button, sign=sign, title=product.name,
                               is_auth=session.get("is_authenticated", False), username=session.get("username", ""),
                               last_page=last_page)


@app.route("/category/<int:category_id>")
def products_from_category(category_id: int):
    favorite_products_id = []
    last_page = '/'

    if session.get("is_authenticated"):
        last_page = session['current_page']
        session['current_page'] = f"/category/{category_id}"
        favorite_products_id = session.get('favorite_products_id')

    products = db.load_products_from_category(category_id)

    return category_page.render(products=products, favorites=favorite_products_id,
                                title=db.load_category_name(products[0].category_id),
                                is_auth=session.get("is_authenticated", False), username=session.get("username", ""),
                                last_page=last_page)


@app.route("/favorites")
def favorites():
    if not session.get("is_authenticated"):
        redirect('/auth')

    last_page = '/'
    session['current_page'] = f"/favorites"
    products = []

    for product_id in session.get("favorite_products_id"):
        products.append(db.load_product(product_id))

    return favorite_products.render(products=products, title="Любимые товары",
                                    is_auth=session.get("is_authenticated", False),
                                    username=session.get("username", ""), last_page=last_page)


'''---------REGISTRATION AND AUTHENTICATION----------------------------------'''


@app.route("/auth")
def authentication():
    return authorization_page.render(additional_data="")


@app.route("/registration")
def registration():
    return registration_page.render(additional_data="")


@app.route("/auth", methods=["POST"])
def authentication_user():
    username = request.form["username"]
    password = request.form["password"]

    # user is already sign in
    if session.get("is_authenticated"):
        return authorization_page.render(additional_data="Вы уже вошли в аккаунт.")

    # user entered correct data
    user = db.load_user(username)
    if user and user.password == password:
        session["username"] = user.username
        session["password"] = user.password
        session["user_id"] = user.user_id
        session["favorite_products_id"] = db.load_favorites_user_products_id(user.user_id)
        session["is_authenticated"] = True
        session['current_page'] = f"/auth"
        return redirect("/")

    # user entered incorrect data
    return authorization_page.render(additional_data="Вы ввели некорректный логин или пароль.", username=username,
                                     password=password)


@app.route("/registration", methods=["POST"])
def registration_user():
    username = request.form["username"]
    password = request.form["password"]

    # user is already sign in
    if session.get("is_authenticated"):
        return registration_page.render(additional_data="Для регистрации нового аккаунта нужно выйти из текущего.",
                                        username=username, password=password)

    # user already exists
    if db.load_user(username):
        return registration_page.render(additional_data="Пользователь с данным именем уже существует.",
                                        username=username, password=password)

    # user entered correct data
    db.create_user(username, password)
    user = db.load_user(username)
    session["username"] = user.username
    session["password"] = user.password
    session["user_id"] = user.user_id
    session['favorite_products_id'] = []
    session['current_page'] = '/registration'
    session["is_authenticated"] = True
    return registration_page.render(additional_data="Поздравляем! регистрация пользователя прошла успешно.")


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
