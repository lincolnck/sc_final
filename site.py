from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('main.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/acknowledgements')
def acknowledgements():
	return render_template('acknowledgements.html')

@app.route('/application')
def application():
	print("hello")

if __name__ == '__main__':
	app.run(debug=True)