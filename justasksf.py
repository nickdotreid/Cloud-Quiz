from flask import Flask, redirect, request, flash, render_template, session, jsonify
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
	
	if request.method == "POST" and 'text' in request.form:
		success = False
		if len(request.form['text']) > 0 and len(request.form['text']) < 550:
			question = UserQuestion(request.form['text'])
			if 'name' in request.form and len(request.form['name'])<255:
				question.name = request.form['name']
			flash('Question saved','success')
			db.session.add(question)
			db.session.commit()
			success = True
		return render_template('ask_question.html',question = request.form,success=success)
	return render_template('ask_question.html')