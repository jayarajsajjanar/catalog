#!flask/bin/python

from flask import Flask

from flask import render_template

from flask import Flask, abort, request, session
from flask import redirect, url_for, flash, jsonify


from uuid import uuid4
import requests
import requests.auth
import urllib

from flask_oauth import OAuth

from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required

from flask_restful import reqparse, abort, Api, Resource

from forms import form_add_categ, form_add_item, form_edit_item

from models import Items
from models import Cat
from models import db

from functools import wraps

app = Flask(__name__)


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'





oauth = OAuth()

# As of now. Only facebook authorisation is being provided.
facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com\
/dialog/oauth',
                            consumer_key="1121519951201568",
                            consumer_secret='1c404c42182566f62f75234dc27004dc',
                            request_token_params={'scope': ('email, ')}
                            )


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')


@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next'),
                                               _external=True))


# The query object is converted into a list. For easy accessibility.
items_py = []
for items_iter in Items.query.all():
    items_py.append(
        (str(items_iter.id),
         str(items_iter.Naming),
         str(items_iter.Description),
         str(items_iter.Cat.name)))
categs = []
for categs_iter in Cat.query.all():
    categs.append((str(categs_iter.id), str(categs_iter.name)))

@app.route('/')
@app.route('/index')
def index():
    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))
    return render_template('index.html',
                           title='index',
                           Items=items_py,
                           categs=categs)

# Other views extend this below view.
# Must send the below data structures into the views that extend "layout".


@app.route('/layout.html')
def layout():
    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))
    return render_template('layout.html',
                           title='layout',
                           Items=items_py,
                           categs=categs)

# This is a global temporary variable to be used in login_required decorator.
sess = False


@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    global sess
    session['logged_in'] = True
    # Update 'sess' value so that it can be used in login_required decorator.
    sess = session['logged_in']
    session['facebook_token'] = (resp['access_token'], '')

    # Below code extracts information from 'me' object!!!!!
    # me = facebook.get('/me')
    #  return 'Logged in as id=%s name=%s' % (me.data['id'], me.data['name'])
    return render_template('index.html',
                           title='index',
                           Items=items_py,
                           categs=categs)


# This is a decorator function. Insert '@login_required' before the
# functions that need authorisation.


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if sess is False:
            message = 'Need to Login to access that page!!!'
            # Flash displays a message only on first subsequent request.
            flash(message)
            return render_template('index.html',
                                   title='index',
                                   Items=items_py,
                                   categs=categs)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/logout")
def logout():
    pop_login_session()
    global sess
    sess = False
    return "logged out!!!"


def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)


# For development and debugging purposes.
@app.route('/categories_all')
@login_required
def Categories():

    return render_template('categories_all.html',
                           title='Categories_all',
                           Items=items_py,
                           categs=categs)

# This view is called when particular "Category" is clicked. To display
# items in a category.


@app.route('/all_items_in_categ.html')
def all_items_in_Categories():
    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))
    which_categ = request.args.get('i')

    return render_template('all_items_in_categ.html',
                           title='All_Items_In_Categories',
                           Items=items_py,
                           categs=categs,
                           categ=which_categ)
    # return ii


@app.route('/add_categ.html', methods=['GET', 'POST'])
@login_required
def add_categ():

    form = form_add_categ()
    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))
    if form.validate_on_submit():
        new_categ = str(form.categ_name.data)
        c1 = Cat(new_categ)
        db.session.add(c1)
        db.session.commit()
        # print ('New Category Added = {}').format(new_categ)
        message = 'Category addedddd:' + c1.name
        # Flash displays a message only on first subsequent request.
        flash(message)
        return render_template('categ_added.html',
                               title='Categ_added',
                               Items=items_py,
                               categs=categs)
        # return  render_template('index.html',user=new_categ)
    return render_template('add_categ.html',
                           title='Add Categories',
                           form=form,
                           Items=items_py,
                           categs=categs)


@app.route('/add_item.html', methods=['GET', 'POST'])
@login_required
def add_item():

    form = form_add_item()
    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))
    form.item_categ.choices = categs

    if form.validate_on_submit():
        item_name = str(form.item_name.data)
        item_desc = str(form.item_desc.data)
        item_categ = str(form.item_categ.data)

        for categ in Cat.query.all():
            if int(categ.id) == int(item_categ):
                categ_is = categ
                break
        i1 = Items(item_name, item_desc, categ_is)
        db.session.add(i1)
        db.session.commit()
        # print ('New Category Added = {}').format(new_categ)
        message = "Item Added:"+i1.Naming
        flash(message)
        return render_template('item_added.html',
                               title='Item_added',
                               Items=items_py,
                               categs=categs)

    return render_template('add_item.html',
                           title='Add Item',
                           form=form, Items=items_py, categs=categs)


@app.route('/delete_item.html', methods=['GET', 'POST'])
@login_required
def delete_item():
    which_item = request.args.get('i')
    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))
    for items_iter in Items.query.all():
        if int(items_iter.id) == int(which_item):
            item_is = items_iter
            deleted_item_name = items_iter.Naming
            break
    db.session.delete(item_is)
    db.session.commit()

    return render_template('delete_item.html',
                           title='Delete Item',
                           deleted_item_name=deleted_item_name,
                           Items=items_py,
                           categs=categs)

# If category is deleted then its associated items too are to be
# deleted.(cascading)


@app.route('/del_categ.html', methods=['GET', 'POST'])
@login_required
def delete_categ():
    which_categ = request.args.get('i')
    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))
    for categs_iter in Cat.query.all():
        if int(categs_iter.id) == int(which_categ):
            categ_is = categs_iter
            deleted_categ_name = categs_iter.name
            break
    db.session.delete(categ_is)
    db.session.commit()

    return render_template('delete_categ.html',
                           title='Delete Categ',
                           deleted_categ_name=deleted_categ_name,
                           Items=items_py,
                           categs=categs)


@app.route('/edit_item.html', methods=['GET', 'POST'])
@login_required
def edit_item():
    # importing a form.
    form = form_edit_item()

    items_py = []
    for items_iter in Items.query.all():
        items_py.append(
            (str(items_iter.id),
             str(items_iter.Naming),
             str(items_iter.Description),
             str(items_iter.Cat.name)))
    categs = []
    for categs_iter in Cat.query.all():
        categs.append((str(categs_iter.id), str(categs_iter.name)))

    which_item = request.args.get('i')

    for items_iter in Items.query.all():
        if int(items_iter.id) == int(which_item):
            item_is = items_iter
            edit_item_is = items_iter
            edit_item_id_is = items_iter.id
            break

    form.item_name.value = edit_item_is.Naming

    if form.validate_on_submit():
        item_name = str(form.item_name.data)
        item_desc = str(form.item_desc.data)

        ret = Items.query.filter_by(id=edit_item_id_is).first()
        ret.Naming = item_name
        ret.Description = item_desc

        db.session.commit()
        # print ('New Category Added = {}').format(new_categ)
        message = "Item Modified, New Item Name:"+item_name
        flash(message)
        return render_template('item_edited.html',
                               title='Item_Edited',
                               Items=items_py,
                               categs=categs)

    return render_template('edit_item.html',
                           title='Edit Item',
                           form=form,
                           edit_item_is=edit_item_is,
                           Items=items_py,
                           categs=categs,
                           Naming=edit_item_is.Naming,
                           Description=edit_item_is.Description)

# Deals with providing an API end point
# Below, a JOSN endpoint will be provided.

api = Api(app)

# Optional. Provides only Category information.
# class All_Categories(Resource):
#     def get(self):

#         all_categs=[{}]
#         for categs_iter in Cat.query.all():

#             return categs_iter.serialize

# At "/all_items.json", the entire catalog is displayed.


class All_Items(Resource):

    def get(self):

        ret = jsonify(
            all_categories=[categs_iter.serialize
                            for categs_iter
                            in Cat.query.all()])
        return ret


##
# Actually setup the Api resource routing here.
##
api.add_resource(All_Items, '/all_items.json')
# api.add_resource(All_Categories, '/all_categories.json')

# Needs to be '0.0.0.0' for it to be accessing on host when run on vagrant.
app.run(host='0.0.0.0', debug=True)
