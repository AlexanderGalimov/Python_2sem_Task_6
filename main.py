import os

from PIL import Image, ImageEnhance
from flask import Flask, render_template, request, send_from_directory

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))

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
    print(request.files.getlist("file"))
    for file in request.files.getlist("file"):
        if file.filename == "":
            filename = "er.png"
            return render_template("complete.html", image_name=filename)

        print("{} is the file name".format(file.filename))
        filename = file.filename
        print("fi" + filename)
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        file.save(destination)

        try:
            b = request.form['brightness']
            brightness = float(b)
            change_brightness(destination, brightness)

            a = request.form['rotate']
            angle = int(a)
            rotate_image(destination, angle)

            left = request.form['left']
            upper = request.form['upper']
            right = request.form['right']
            lower = request.form['lower']
            left_parsed = int(left)
            upper_parsed = int(upper)
            right_parsed = int(right)
            lower_parsed = int(lower)
            crop_image(destination, left_parsed, upper_parsed, right_parsed, lower_parsed)


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


def rotate_image(filename, angle):
    img = Image.open(filename)
    rotated_img = img.rotate(angle)
    rotated_img.save(filename)


def crop_image(filename, left, upper, right, lower):
    img = Image.open(filename)
    im_crop = img.crop((left, upper, right, lower))
    im_crop.save(filename)


if __name__ == "__main__":
    app.run(port=4565, debug=False)
