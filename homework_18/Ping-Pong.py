from flask import Flask

app = Flask(__name__)


@app.route("/ping")
def ping():
    return f'''
<html>
<head>
    <title>Ping-Pong</title>
</head>
<body>
    <a href="http://127.0.0.1:8080/pong"">Pong</a>    
</body>
</html>
'''


@app.route("/pong")
def pong():
    return f'''
<html>
<head>
    <title>Ping-Pong</title>
</head>
<body>
    <a href="http://127.0.0.1:8080/ping">Ping</a>
</body>
</html>
'''


if __name__ == "__main__":
    app.run(port=8080, debug=True)
