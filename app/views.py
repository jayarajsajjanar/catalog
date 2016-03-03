from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',title='Home',user=user)

#Could not place this import statement at the top. 404 error occuring.
from models import Items
from models import Cat

@app.route('/categories_all')
def Categories():
	items_py=[()]
	for i in Items.query.all():
		items_py.append((i.id,i.Naming,i.Description))
	return render_template('categories_all.html',title='Categories_all',Items=items_py)

