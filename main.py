import os

from flask import Flask, render_template, request

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("upload.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROUTE, "static/images/")
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        des = "/".join([target, filename])
        print(des)
        file.save(des)

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(port=4565, debug=False)
