from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from wrapper import wrapper
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/averager')
def averager():
    return render_template("upload.html")

@app.route('/upload', methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/faces/')
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        print(filename)
        destination = "/".join([target, filename])
        upload.save(destination)
    return render_template("execute.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/faces", filename)

@app.route('/execute', methods=["POST", "GET"])
def execute():
    file_path = 'static/faces/'
    average_face = wrapper(file_path)
    # output_impath = os.path.join(APP_ROOT, 'images/average_face.png')
    output_impath = 'average_face.png'
    print(APP_ROOT)
    return render_template("success.html", output_image = output_impath)

@app.route('/execute/<output_impath>')
def output_image(output_impath):
    return send_from_directory("static/images", output_impath)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/acknowledgements')
def acknowledgements():
    return render_template('acknowledgements.html')

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)