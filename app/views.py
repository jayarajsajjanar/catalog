from flask import render_template
from app import app

from flask import Flask, abort, request,session,redirect,url_for,flash,jsonify
from uuid import uuid4
import requests
import requests.auth
import urllib

from flask_oauth import OAuth

from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,current_user,login_required 

oauth = OAuth()

#As of now. Only facebook authorisation is being provided.
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="1121519951201568",
    consumer_secret='1c404c42182566f62f75234dc27004dc',
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',next=request.args.get('next'), _external=True))

#Could not place this import statement at the top. 404 error occuring.
from models import Items
from models import Cat
from models import db    


#The query object is converted into a list. For easy accessibility. 
items_py=[]
for i in Items.query.all():
    items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
categs=[]
for i in Cat.query.all():
    categs.append((str(i.id),str(i.name)))

@app.route('/')
@app.route('/index')
def index():
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    return render_template('index.html',title='index',Items=items_py,categs=categs)

#Other views extend this view. 
#Must send the below data structures in the views that extend "layout".
@app.route('/layout.html')
def layout():
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    return render_template('layout.html',title='layout',Items=items_py,categs=categs)

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    
    #Below code extracts information from 'me' object!!!!!
    #me = facebook.get('/me')
    # return 'Logged in as id=%s name=%s' % (me.data['id'], me.data['name'])
    return render_template('index.html',title='index',Items=items_py,categs=categs)

@app.route("/logout")
def logout():
    pop_login_session()
    return "logged out!!!"

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)


#For development and debugging purposes. 
@app.route('/categories_all')
# @login_required
def Categories():

	return render_template('categories_all.html',title='Categories_all',Items=items_py,categs=categs)

#This view is called when particular "Category" is clicked. To display items in a category.
@app.route('/all_items_in_categ.html')
def all_items_in_Categories():
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    ii = request.args.get('i')

    return render_template('all_items_in_categ.html',title='All_Items_In_Categories',Items=items_py,categs=categs,ii=ii)
    # return ii


from .forms import form_add_categ,form_add_item,form_edit_item


@app.route('/add_categ.html', methods=['GET', 'POST'])
def add_categ():

    form = form_add_categ()
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    if form.validate_on_submit():
    	new_categ=str(form.categ_name.data)
    	c1=Cat(new_categ)
    	db.session.add(c1)
    	db.session.commit()
        # print ('New Category Added = {}').format(new_categ)
        message = 'Category addedddd:' + c1.name
        #Flash displays a message only on first subsequent request.
        flash(message)
        return render_template('categ_added.html',title='Categ_added',Items=items_py,categs=categs)
        # return  render_template('index.html',user=new_categ)
    return render_template('add_categ.html', 
                           title='Add Categories',
                           form=form,Items=items_py,categs=categs)

@app.route('/add_item.html', methods=['GET', 'POST'])
def add_item():

    form = form_add_item()
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    form.item_categ.choices = categs
    
    if form.validate_on_submit():
        item_name=str(form.item_name.data)
        item_desc=str(form.item_desc.data)
        item_categ=str(form.item_categ.data)
        
        for c in Cat.query.all():
            if int(c.id) == int(item_categ):
                categ_is = c
                break
        i1=Items(item_name,item_desc,categ_is)
        db.session.add(i1)
        db.session.commit()
        # print ('New Category Added = {}').format(new_categ)
        message="Item Added:"+i1.Naming
        flash(message)
        return render_template('item_added.html',title='Item_added',Items=items_py,categs=categs)

    return render_template('add_item.html', 
                           title='Add Item',
                           form=form,Items=items_py,categs=categs)

@app.route('/delete_item.html', methods=['GET', 'POST'])
def delete_item():
    ii = request.args.get('i')
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    for i in Items.query.all():
        if int(i.id)==int(ii):
            item_is = i
            deleted_item_name = i.Naming
            break
    db.session.delete(item_is)
    db.session.commit()

    return render_template('delete_item.html',title='Delete Item',deleted_item_name=deleted_item_name,Items=items_py,categs=categs)

#If category is deleted then its associated items too are to be deleted.(cascading)
@app.route('/del_categ.html', methods=['GET', 'POST'])
def delete_categ():
    ii = request.args.get('i')
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    for i in Cat.query.all():
        if int(i.id)==int(ii):
            categ_is = i
            deleted_categ_name = i.name
            break
    db.session.delete(categ_is)
    db.session.commit()

    return render_template('delete_categ.html',title='Delete Categ',deleted_categ_name=deleted_categ_name,Items=items_py,categs=categs)

@app.route('/edit_item.html', methods=['GET', 'POST'])
def edit_item():
    #importing a form.
    form = form_edit_item()
    
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    
    ii = request.args.get('i')
    
    for i in Items.query.all():
        if int(i.id)==int(ii):
            item_is = i
            edit_item_is = i
            edit_item_id_is = i.id
            break
    
    form.item_name.value=edit_item_is.Naming
    aa=edit_item_is.Naming
    bb=edit_item_is.Description

    if form.validate_on_submit():
        item_name=str(form.item_name.data)
        item_desc=str(form.item_desc.data)

        ret=Items.query.filter_by(id=edit_item_id_is).first()
        ret.Naming=item_name
        ret.Description=item_desc

        db.session.commit()
        # print ('New Category Added = {}').format(new_categ)
        message="Item Modified, New Item Name:"+item_name
        flash(message)
        return render_template('item_edited.html',title='Item_Edited',Items=items_py,categs=categs)
        

    return render_template('edit_item.html', 
                           title='Edit Item',
                           form=form,edit_item_is=edit_item_is,Items=items_py,categs=categs,Naming=aa,Description=bb)

######Deals with providing an API end point
######Below JOSN endpoint will be provided.
from flask_restful import reqparse, abort, Api, Resource
api = Api(app)

######Optional. Provides only Category information.
# class All_Categories(Resource):
#     def get(self):
        
#         all_categs=[{}]
#         for i in Cat.query.all():
            
#             return i.serialize
        
#### At "/all_items.json", the entire catalog is displayed.
class All_Items(Resource):
    def get(self):
        
        ret=jsonify(all_categories=[i.serialize for i in Cat.query.all()])
        return ret
        

##
## Actually setup the Api resource routing here.
##
api.add_resource(All_Items, '/all_items.json')
# api.add_resource(All_Categories, '/all_categories.json')