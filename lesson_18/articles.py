import dataclasses
import sqlite3

from flask import Flask, abort

# CONSTS
DATABASE_PATH = 'article.db'

app = Flask(__name__)


@dataclasses.dataclass
class Article:
    id: int
    title: str
    text: str
    author: str
    like_count: int


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
        connection.execute(f"UPDATE article SET title = ?, text = ?, author = ? like_count = ? WHERE id = ?",
                           (article.title, article.text, article.author, article.id))
        connection.commit()


@app.route('/')
@app.route('/articles')
def articles():
    string = '\n'.join(
        f'<li><a href="http://127.0.0.1:8000/article/{i.id}">{i.title}</a></li>\n' for i in get_all_articles())

    return f"""<html>
                  <head>
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
                            
                            <from action="/like" method="post">
                        </body>
                    </html>
                '''
    except ValueError:
        abort(404, "Article not found")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
