###*******************Catalog******************

###             Third project as part of the Udacity/Google - Full Stack Web Developer - Nanodegree
 
###Key things learnt:
1. ORM -> Flask_SQLAlchemy ,OAuth, Flask framework, HTML inheritance, Template Engine - Jinja2, Forms - WTF
2. Sessions, Flash Messaging, Routing in flask, Providing JSON API End Point, RESTFul API


###About Project:
1. A catalog app which can store Categories and its Items. Description for Items can be specified.
2. Categories can be added and deleted. Items can be added, edited and deleted.
3. A JSON RESTFull API Endpoint is provided.

###Development Environment :
1. The virtual machine used/provided is Ubuntu 14.04, 32 bits.
2. Database engine - SQLlite.
3. Python 2.7.3
4. Flask framework, ORM -> Flask_SQLAlchemy, Template Engine - Jinja2, Forms - WTF

###Steps for running the project:
1. **Clone** the repo of the current project using - `git clone https://github.com/jayarajsajjanar/catalog.git` 
2.  Use virtualenv and the requirements.txt provided to install necessary libraries and softwares.
3.  Need to have facebook login details for editing/deleting. (Oauth is provided for Facebook only)
2. `cd app` and then  `python db_create.py` to create the database and to instantiate minimally required objects.
3. `cd .` to return to parent directory. Hit `python run.py` to run the project. Visit `localhost:5000` on your browser.
4.  Have fun adding/deleting/editing categories and items.
5.  API endpoint is provided at `\all_items.json`

      

