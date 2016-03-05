from flask import render_template
from app import app

from flask import Flask, abort, request,session,redirect,url_for,flash
from uuid import uuid4
import requests
import requests.auth
import urllib

from flask_oauth import OAuth

from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,current_user,login_required 

oauth = OAuth()

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

@app.route('/')
@app.route('/index')
def index():
    items_py=[]
    for i in Items.query.all():
        items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
       # items_py=[]
    # for i in Items.query.all():
    #     items_py.append(i)
    categs=[]
    for i in Cat.query.all():
        categs.append((str(i.id),str(i.name)))
    return render_template('index.html',title='index',Items=items_py,categs=categs)

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    # data = facebook.get('/me').data

    # if 'id' in data and 'name' in data:
    # 	user_id = data['id']
    # 	user_name = data['name']

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s' % (me.data['id'], me.data['name'])

    # return "facebook authorised!!! Hi "

    # return "facebook authorised!!! Hi %s" %user_id

@app.route("/logout")
def logout():
    pop_login_session()
    return "logged out!!!"

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

# CLIENT_ID = "1121519951201568" # Fill this in with your client ID
# CLIENT_SECRET = '1c404c42182566f62f75234dc27004dc' # Fill this in with your client secret
# REDIRECT_URI = "http://localhost:5000/facebook_callback"

# lm = LoginManager(app)
# lm.login_view = 'index'

# def base_headers():
#     return {"User-Agent": user_agent()}

# # @app.route('/')
# # @app.route('/index')
# # def index():
# #     user = {'nickname': 'Miguel'}  # fake user
# #     return render_template('index.html',title='Home',user=user)

#Could not place this import statement at the top. 404 error occuring.
from models import Items
from models import Cat
from models import db
# # from run import make_authorization_url

# @app.route('/')
# def homepage():
#     text = '<a href="%s">Authenticate with facebook</a>'
#     return text % make_authorization_url()
    

@app.route('/categories_all')
# @login_required
def Categories():
	items_py=[]
	for i in Items.query.all():
		items_py.append((str(i.id),str(i.Naming),str(i.Description),str(i.Cat.name)))
       # items_py=[]
    # for i in Items.query.all():
    #     items_py.append(i)
	categs=[]
	for i in Cat.query.all():
		categs.append((str(i.id),str(i.name)))
	return render_template('categories_all.html',title='Categories_all',Items=items_py,categs=categs)

from .forms import form_add_categ

# index view function suppressed for brevity

@app.route('/add_categ', methods=['GET', 'POST'])
def add_categ():
    form = form_add_categ()
    if form.validate_on_submit():
    	new_categ=str(form.categ_name.data)
    	c1=Cat(new_categ)
    	db.session.add(c1)
    	db.session.commit()
        # print ('New Category Added = {}').format(new_categ)
        flash('Category addedddd:',c1.name)
        return render_template('categ_added.html',title='Categ_added')
        # return  render_template('index.html',user=new_categ)
    return render_template('add_categ.html', 
                           title='Add Categories',
                           form=form)

# def make_authorization_url():
#     # Generate a random string for the state parameter
#     # Save it for use later to prevent xsrf attacks
#     state = str(uuid4())
#     # save_created_state(state)
#     params = {"client_id": CLIENT_ID,
#               "response_type": "code",
#               "state": state,
#               "redirect_uri": REDIRECT_URI,
#               "duration": "temporary",
#               "scope": "email"}
#     url = "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(params)
#     return url

# @app.route('/facebook_callback')
# def facebook_callback():
#     error = request.args.get('error', '')
#     if error:
#         return "Error: " + error
#     # state = request.args.get('state', '')
#     # if not is_valid_state(state):
#     #     # Uh-oh, this request wasn't started by us!
#     #     abort(403)
#     code = request.args.get('code')
#     # access_token = get_token(code)
#     # # Note: In most cases, you'll want to store the access token, in, say,
#     # # a session for use in other parts of your web app.
#     # return "Your facebook username is: %s" % get_username(access_token)
#     return '<a href="/logout">logged in !!</a> <br> <a href="http://localhost:5000/categories_all">all categorie !!s</a>'  

# def get_token(code):
#     # client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
#     # post_data = {"grant_type": "authorization_code",
#     #              "code": code,
#     #              "redirect_uri": REDIRECT_URI}
#     # #headers = base_headers()
#     # response = requests.post("https://ssl.facebook.com/api/v1/access_token",
#     #                          auth=client_auth,
#     #                          data=post_data)
#     # token_json = response.json()
#     # return token_json["access_token"]
#     return "inside get_token()"
    
# def get_username(access_token):
#     headers = base_headers()
#     headers.update({"Authorization": "bearer " + access_token})
#     response = requests.get("https://oauth.facebook.com/api/v1/me", headers=headers)
#     me_json = response.json()
#     return me_json['name']

# @app.route('/logout')
# def logout():
#     logout_user()
#     return "logged out!"