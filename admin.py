from flask import Flask, redirect, Blueprint
from flaskext.sqlalchemy import SQLAlchemy

from db_config import *

from createsend import CreateSend, Subscriber
CreateSend.api_key = campaign_monitor_api_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.secret_key = secrect_key
db = SQLAlchemy(app)

from models import *
from flaskext import admin

admin_blueprint = admin.create_admin_blueprint((Question, Answer, User), db.session)
app.register_blueprint(admin_blueprint, url_prefix='/admin')

@app.route("/")
def index():
	return redirect("/admin")