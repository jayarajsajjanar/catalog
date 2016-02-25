from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#Could not place this import statement at the top. 404 error occuring.
from models import *

@app.route('/categories_all')
def Categories():
	# db.create_all()
	# c1=Cat("hockey")
	# c1.name
	# i1=Items("Hockey Stick","Its made of wood, curved at the end. Rubber grip for better control",c1)
	# i2=Items("Hockey Ball","Usually white in color. Very hard.",c1)
	# c2=Cat("Football")
	# i3=Items("Ball","1 Feet diameter. Made of synthetic rubber.",c2)
	# i4=Items("Shoes","Made of rubber.",c2)
	# db.session.add(c1,c2)
	# db.session.add(i1,i2)
	# db.session.add(i3,i4)
	# db.session.commit()

	# items_py=[()]
	# for i in Items.query.all():
	# 	items_py.append((i.id,i.Naming,i.Description))

	return "Categories!!"

