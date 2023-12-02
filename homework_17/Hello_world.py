from flask import Flask, request

app = Flask(__name__)


@app.route('/<string:name>')
def hello_world(name: str):
    return f"<h1>Hello, {name}!</h1>"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
