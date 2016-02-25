from app import app
from models import *
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/categories_all')
def Categories():
	return "All Categories"