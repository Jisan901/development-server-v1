from flask import Flask
from app_main.db import Mongo
import json

app = Flask(__name__)

###
# production version control
###
production = False



with open('app_main/config.json','r') as c:
    params = json.load(c)['params']



if production == True:
    db_uri = params['databases']['cloud']
else:
    db_uri = params['databases']['local']

app.config['SECRET_KEY'] = params['secrets']
app.config['MONGODB_URI'] = db_uri
app.config['MONGO_APPLICATION_DATA'] = params['databases']['db_token']



db = Mongo(app)
users = db.column('users')
web_data = db.column('web_data')
admin_info = db.column('admin_info')
courses = db.column('courses')
course_req = db.column('course_req')
blogs = db.column('blogs')

from app_main import api
from app_main import routes
from app_main import admin
from app_main import s_routes
from app_main import authentication
from app_main import blog