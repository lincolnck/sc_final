from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from wrapper import wrapper
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
	return render_template('main.html')

@app.route('/averager')
def averager():
	return render_template("upload.html")

@app.route('/upload', methods=["POST"])
def upload():
	target = os.path.join(APP_ROOT, 'faces/')
	if not os.path.isdir(target):
			os.mkdir(target)
	else:
		print("Couldn't create upload directory: {}".format(target))
	for upload in request.files.getlist("file"):
		filename = upload.filename
		destination = "/".join([target, filename])
		upload.save(destination)
	return render_template("execute.html", image_name=filename)

@app.route('/execute', methods=["POST", "GET"])
def execute():
	file_path = 'faces/'
	average_face = wrapper(file_path)
	return render_template("success.html", image_name=average_face)
	
@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/acknowledgements')
def acknowledgements():
	return render_template('acknowledgements.html')

if __name__ == '__main__':
	app.run(debug=True)