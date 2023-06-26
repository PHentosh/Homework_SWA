from flask import Flask

app = Flask(__name__)


@app.get('/')
def login_get():
    return "Not implemented yet"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8082, debug=True)