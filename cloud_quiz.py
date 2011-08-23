from flask import Flask, request, render_template
from flaskext.sqlalchemy import SQLAlchemy
import re

from db_config import db_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
	return render_template('index.html')
	
@app.route('/question',methods=['GET','POST'])
def get_tweets():
	return render_template('index.html')
	
@app.route('/view')
def render_cloud():
	return render_template('index.html')