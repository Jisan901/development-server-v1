from flask import Flask
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


from app_main import routes