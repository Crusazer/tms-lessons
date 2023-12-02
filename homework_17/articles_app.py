import dataclasses
import sqlite3

from flask import Flask



@dataclasses.dataclass
class Article:
    id: int
    title: str
    text: str
    author: str


def get_all_articles() -> list[Article]:
    connection = sqlite3.connect('article')
    cursor = connection.execute('SELECT * FROM article')
    return [Article(*article) for article in cursor.fetchall()]


def get_article(article_id: int) -> Article:
    connection = sqlite3.connect('article')
    cursor = connection.execute("SELECT * FROM article WHERE id = ?", (article_id,))
    if article := cursor.fetchone():
        return Article(*article)
    raise ValueError


def save_article(article: Article):
    connection = sqlite3.connect('article')
    connection.execute(f"UPDATE article SET title = ?, text = ?, author = ? WHERE id = ?",
                       (article.title, article.text, article.author, article.id))
    connection.commit()


app = Flask(__name__)


@app.route('/articles')
def articles():
    string = (f'<html>\n'
              f'    <head>\n'
              f'        <title>Articles APP</title>\n'
              f'    </head>\n'
              f'    <body>\n'
              f'        <h1 style="text-align: center;">All Articles</h1>\n'
              f'        <ul>\n')

    articles = get_all_articles()
    for i in articles:
        string += f"            <li>{i.title}</li>\n"

    string += (f"        </ul>\n"
               f"   </body>\n"
               f"</html>\n")
    print(string)
    return string


if __name__ == "__main__":
    app.run(port=8000, debug=True)
