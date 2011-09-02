from flask import Flask, redirect, request, flash, render_template, session, jsonify
from flaskext.sqlalchemy import SQLAlchemy
import re

from db_config import db_uri, secrect_key

from createsend import CreateSend, Subscriber
CreateSend.api_key = campaign_monitor_api_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.secret_key = secrect_key
db = SQLAlchemy(app)

from models import *

@app.route("/",methods=['GET','POST'])
def index():
	
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'text' in request.form:
		success = False
		errors = {}
		if len(request.form['text']) > 0 and len(request.form['text']) < 550:
			question = UserQuestion(request.form['text'])
			if 'name' in request.form and len(request.form['name'])<255:
				question.name = request.form['name']
			if 'optin' in request.form and 'email' in request.form and len(request.form['email'])>0:
				sub = Subscriber()
				sub.add(campaign_monitor_list_id,request.form['email'],request.form['name'],[],True)
			flash('Question saved','success')
			db.session.add(question)
			db.session.commit()
			success = True
		else:
			
			errors['text'] = 'Your question must be less than 500 characters'
		return render_template('ask_question.html',question = request.form,success=success,errors=errors)
	return render_template('ask_question.html',question = {"optin":True})
	
@app.route("/register")
def redirect_to_register():
	return redirect("https://events.r20.constantcontact.com/register/eventReg?oeidk=a07e4q95wra4c76768d&oseq=")