import os

from PIL import Image, ImageEnhance
from flask import Flask, render_template, request, send_from_directory

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'HEIC'}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("upload.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/upload/<filename>')
def send_image(filename):
    print(filename)
    return send_from_directory("static/images", filename)


@app.route('/upload', methods=['POST', 'GET'])
def upload():

    target = os.path.join(APP_ROUTE, 'static/images')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for file in request.files.getlist("file"):
        print(file)
        print("{} is the file name".format(file.filename))
        filename = file.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        file.save(destination)

        try:
            b = request.form['brightness']
            brightness = float(b)
            change_brightness(destination, brightness)
        except TypeError:
            print("error")
        except ValueError:
            print("error")

    return render_template("complete.html", image_name=filename)


def change_brightness(filename, koef):
    img = Image.open(filename)
    enhancer = ImageEnhance.Brightness(img)
    # to reduce brightness by 50%, use factor 0.5
    img = enhancer.enhance(koef)

    img.save(filename)


if __name__ == "__main__":
    app.run(port=4565, debug=False)
