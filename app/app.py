from flask import Flask, render_template
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/')
app = Flask(__name__, template_folder = tmpl_dir)

@app.route('/')
@app.route('/login')
def login():
	return render_template('main.html')

if  __name__ == '__main__':
	app.run(debug=True)