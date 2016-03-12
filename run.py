#!flask/bin/python

from app import app 

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#Needs to be '0.0.0.0' for it to be accessing on host when run on vagrant.
app.run(host='0.0.0.0',debug=True)

































