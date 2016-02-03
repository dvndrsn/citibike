from app import app
from flask import render_template
from config import STATIC_PATH

@app.route('/')
@app.route('/index')
def index():
	path = STATIC_PATH
	return render_template('index.html', path = path)