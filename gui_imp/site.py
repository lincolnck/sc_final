# Software Carpentry Final Project
# Lincoln Kartchner
# site.py
'''
This script takes care of creating the server
side functionality of the averger website.
It is built off of the Flask framework.

Sources:
    1. https://flask-doc.readthedocs.io/en/latest/
'''
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from averager import main
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    """ home() returns the homepage """
    return render_template("home.html")


@app.route('/averager')
def averager():
    """ averager() returns the upload page
    when the averager link is clicked
    """
    return render_template("upload.html")


@app.route('/upload', methods=["POST"])
def upload():
    """ upload takes care of the image
    uploading process. It will create a
    directory to place the images uploaded if one
    does not already exist. Then it will
    interact with upload.html found in ./templates
    to allow the user to upload images and save
    them to the directory. If no images are
    uploaded it will reload the upload page
    with an error message.

    **Parameters**
    None

    **Returns**
    execute.html: html template page
    images: list
        list of images names in 'static/faces/'
    """
    target = os.path.join(APP_ROOT, 'static/faces/')
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    for upload in request.files.getlist("file"):
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        try:
            upload.save(destination)
        except IsADirectoryError:
            return render_template("noimages.html")
    images = os.listdir(os.path.join(APP_ROOT, 'static/faces/'))
    images = ['faces/' + file for file in images]
    return render_template("execute.html", images=images)


@app.route('/upload/<filename>')
def send_image(images):
    """ send_images sends the filename of the
    image files uploaded to be used in the
    execute.html page where the uploaded images
    are displayed.

    **Parameters**
    images: list
        the images list created and returned
        by upload()

    **Returns**
    The filename of the images requested by
    execute.html for display.
    """
    return send_from_directory("static/faces", images)


@app.route('/execute', methods=["POST", "GET"])
def execute():
    """ execute() calls the averager script main()
    to be executed on the images found in the filepath

    **Parameters**
    None

    **Returns**
    success.html and output image path if no
    errors were encountered in executing the averager
    script.

    failure.html if errors were encountered in executing
    the averager script.
    """
    file_path = 'static/faces/'
    output_impath = 'average_face.png'
    try:
        average_face = main(file_path)
        return render_template("success.html", output_image=output_impath)
    except Exception:
        return render_template("failure.html")


@app.route('/execute/<output_impath>')
def output_image(output_impath):
    """ output_image sends the filename of the
    output image to be used in the
    success.html page where the output image
    is displayed.

    **Parameters**
    images: str
        the filepath of the output image

    **Returns**
    The filename of the output image
    requested by success.html for display.
    """
    return send_from_directory("static/outputimage", output_impath)


@app.route('/about')
def about():
    """about() returns the about.html page"""
    return render_template('about.html')


@app.route('/acknowledgements')
def acknowledgements():
    """acknolwedgements() returns the
    acknowledgements.html page"""
    return render_template('acknowledgements.html')


@app.after_request
def add_header(response):
    """add_header() takes care of clearing the cache.
    This is important because after the averager
    script saves the output image, it is displayed by
    success.html which is then cached by the browser.

    If the browser cache is not cleared, then
    the new output image will not be displayed on the
    success.html page.
    """
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=False)
