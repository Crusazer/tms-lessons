import dataclasses
import sqlite3

from flask import Flask, abort, request, redirect, session
from flask_session import Session

# CONSTS
DATABASE_PATH = 'article.db'

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@dataclasses.dataclass
class Article:
    id: int
    title: str
    text: str
    author: str
    like_count: int


@dataclasses.dataclass
class User:
    id: int
    username: str
    password: str


def get_all_articles() -> list[Article]:
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute('SELECT * FROM article')
        return [Article(*article) for article in cursor.fetchall()]


def get_article(article_id: int) -> Article:
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute("SELECT * FROM article WHERE id = ?", (article_id,))
        if article := cursor.fetchone():
            return Article(*article)
        raise ValueError(f"Object with id = {article_id} not exists!")


def save_article(article: Article):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(f"UPDATE article SET title = ?, text = ?, author = ?, like_count = ? WHERE id = ?",
                           (article.title, article.text, article.author, article.like_count, article.id))
        connection.commit()


def check_user(username: str, password: str):
    with sqlite3.connect(DATABASE_PATH) as connection:
        execute = connection.execute(f'SELECT * FROM user WHERE username = ?', (username,))
        if data_user := execute.fetchone():
            user = User(*data_user)
            return user.password == password


def save_user(username: str, password: str):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(f'''INSERT INTO user(username, password) VALUES (?, ?)''',
                           (username, password))


def get_user(username: str) -> User:
    with sqlite3.connect(DATABASE_PATH) as connection:
        execute = connection.execute(f'''SELECT * FROM user WHERE username = ?''', (username,))
        return User(*execute.fetchone())


def add_like(user_id: str, article_id: int):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(f'''INSERT INTO user_to_article VALUES(?,?)''', (user_id, article_id))


def remove_like(user_id: int, article_id: int):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(f'''DELETE FROM user_to_article WHERE user_id = ? AND article_id = ?''',
                           (user_id, article_id))


def check_like(user_id: int, article_id: int) -> bool:
    with sqlite3.connect(DATABASE_PATH) as connection:
        execute = connection.execute(f'''SELECT * FROM user_to_article WHERE user_id = ? AND article_id = ?''',
                                     (user_id, article_id))
        if execute.fetchone():
            return True
        else:
            return False


@app.route("/auth")
def page_auth():
    return f'''
                <html>
                    <head>
                        <title>Authenticate</title>
                    </head>
                        <body>
                            <h1 style="text-align: center;">Authenticate</h1>
                            <form action="/auth" method="post">
                                Login:    <input type="text" name="login"/><br>
                                Password: <input type="text" name="password"/><br>
                                <input type="submit" value="Sign in">
                                <a href="http://127.0.0.1:8000/registration">Registration page</a>                                
                            </form>
                        </body>
                </html>
            '''


@app.route('/')
@app.route('/articles')
def articles():
    string = '\n'.join(
        f'<li><a href="http://127.0.0.1:8000/article/{i.id}">{i.title}</a></li>\n' for i in get_all_articles())

    if session.get("is_authenticated", False):
        user = (f'Username: {session.get("username")}'
                f'<form action="/logout" method="post"> <input type="submit" value="Logout"></form>')
    else:
        user = (f'Username: Stranger'
                f'<form action="/auth" method="get"> <input type="submit" value="Log in"></form>')

    return f"""<html>
                  <head>
                      <p>
                        {user}                            
                      </p>
                      <title>Articles APP</title>
                  </head>
                  <body>
                      <h1 style="text-align: center;">All Articles</h1>
                      <ul>
                          {string}
                      </ul>
                  </body>
               </html>
            """


@app.route("/article/<int:id>")
def article_view(id: int):
    try:
        article = get_article(id)
        return f'''<html>
                        <head>
                            <title>Articles APP</title>
                        </head>
                        <body>
                            <a href="http://127.0.0.1:8000/articles">Go to home page</a>
                            <h1 style="text-align: center;">{article.title}</h1>
                            <h3>{article.author}</h3>
                            <ul>
                                {article.text}
                            </ul>
                            <p>
                                Likes: {article.like_count}
                            </p>                            
                            <form action="/article/like" method="post">
                                <input type="hidden" value="{article.id}" name="article_id"/>
                                <input type="submit" value="Like">
                            </form>    
                        </body>
                    </html>
                '''
    except ValueError:
        abort(404, "Article not found")


@app.route("/article/like", methods=["POST"])
def like_counter():
    if session.get("is_authenticated", False):
        try:
            article_id = int(request.form['article_id'])
            article = get_article(article_id)

            if check_like(session.get('user_id'), article_id):
                article.like_count -= 1
                remove_like(session.get('user_id'), article_id)
            else:
                article.like_count += 1
                add_like(session.get('user_id'), article_id)

            save_article(article)
            return redirect(f"/article/{article.id}")

        except ValueError:
            print("Articles not found!")
            abort(404, "Something went wrong!")
    else:
        return redirect("/auth")


@app.route("/logout", methods=["POST"])
def logout():
    session["is_authenticated"] = False
    return redirect("/articles")


@app.route("/auth", methods=["POST"])
def authenticate():
    login = request.form["login"]
    password = request.form["password"]

    if check_user(login, password):
        session["is_authenticated"] = True
        user = get_user(login)
        session["username"] = user.username
        session["password"] = password
        session["user_id"] = user.id
        return redirect('/articles')
    else:
        return f'''
                <html>
                    <head>
                        <title>Authenticate</title>
                    </head>
                        <body>
                            <h1 style="text-align: center;">Authenticate</h1>
                            <p>Invalid username or password!</p>
                            <form action="/auth" method="post">
                                Login:    <input type="text" name="login"/><br>
                                Password: <input type="text" name="password"/><br>
                                <input type="submit" value="Sign in">
                            </form>
                        </body>
                </html>
            '''


@app.route("/registration")
def registration_page():
    return f'''
                <html>
                    <head>
                        <title>Registration</title>
                    </head>
                        <body>
                            <h1 style="text-align: center;">Registration</h1>
                            <form action="/registration" method="post">
                                Login:    <input type="text" name="login"/><br>
                                Password: <input type="text" name="password"/><br>
                                <input type="submit" value="Registrate">
                            </form>
                        </body>
                </html>
            '''


@app.route("/registration", methods=['POST'])
def registration():
    username = request.form["login"]
    password = request.form["password"]
    save_user(username, password)
    user = get_user(username)
    session["username"] = user.username
    session["password"] = user.password
    session["user_id"] = user.id
    session["is_authenticated"] = True
    return f'''
                <html>
                    <head>
                        <title>Authenticate</title>
                    </head>
                        <body>
                            <h1 style="text-align: center;">Authenticate</h1>
                            <h2>
                                User {user.username} has benn successfully registered! 
                            </h2>                            
                            <a href="http://127.0.0.1:8000/articles">Main page</a>
                        </body>
                </html>
            '''


if __name__ == "__main__":
    app.run(port=8000, debug=True)
