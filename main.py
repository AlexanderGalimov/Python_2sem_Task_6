import os

from PIL import Image, ImageEnhance
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
        des = "/".join([target, "temp.jpg"])
        print(des)
        file.save(des)

    change_brightness()

    return render_template("complete.html")


def change_brightness():
    img = Image.open("static/images/temp.jpg")
    enhancer = ImageEnhance.Brightness(img)
    # to reduce brightness by 50%, use factor 0.5
    img = enhancer.enhance(0.5)

    img.save("static/images/changed_image.jpg")


if __name__ == "__main__":
    app.run(port=4565, debug=False)
