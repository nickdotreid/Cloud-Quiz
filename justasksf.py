from flask import Flask, redirect, request, render_template, session, jsonify
from flaskext.sqlalchemy import SQLAlchemy
import re

from db_config import db_uri, secrect_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.secret_key = secrect_key
db = SQLAlchemy(app)

from models import *

@app.route("/",methods=['GET','POST'])
def index():
	return render_template('ask_question.html')