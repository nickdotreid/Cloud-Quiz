from flask import Flask, redirect, request, flash, render_template, session, jsonify
from flaskext.sqlalchemy import SQLAlchemy
import re

from db_config import *

from createsend import CreateSend, Subscriber
CreateSend.api_key = campaign_monitor_api_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.secret_key = secrect_key
db = SQLAlchemy(app)

from models import *

@app.route("/",methods=['GET','POST'])
def index():
	if 'questions' not in session:
		start_session()
	questions = session['questions']
	start_session()
	return render_template('index.html',questions=questions)

@app.route("/topic_question",methods=['GET','POST'])
def topic_question():
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'topics[]' in request.form:
		session['questions']['topic']['success'] = True
	else:
		errors = {'topics[]':'Please select at least one interest'}
	if request.method == "POST" and 'ajax' in request.form:
		return render_template('topic_question.html',success=True,form=request.form,errors={})
	session['questions'] = session['questions'] # why do i have to do this?
	return redirect("/#topic_question")

@app.route("/ask_question",methods=['GET','POST'])
def ask_question():
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'text' in request.form:
		success = False
		errors = {}
		if len(request.form['text']) > 0 and len(request.form['text']) < 550:
			question = UserQuestion(request.form['text'])
			session['questions']['ask']['success'] = True
			session['questions']['ask']['form'] = request.form
			db.session.add(question)
			db.session.commit()
			success = True
		else:
			errors['text'] = 'Your question must be less than 500 characters'
	if request.method == "POST" and 'ajax' in request.form:
		return render_template('ask_question.html',success=True,form=request.form,errors={})
	session['questions'] = session['questions'] # why do i have to do this?
	return redirect("/#ask_question")
	
@app.route("/capture_email",methods=['GET','POST'])
def capture_email():
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'email' in request.form:
		success = False
		errors = {}
		if 'email' in request.form and len(request.form['email'])>0:
			sub = Subscriber()
			sub.add(campaign_monitor_list_id,request.form['email'],request.form['name'],[],True)
			session['questions']['email']['success'] = True
		else:
			errors['email'] = 'we need an email to keep in touch'
	if request.method == "POST" and 'ajax' in request.form:
		return render_template('email_question.html',success=True,form=request.form,errors={})
	session['questions'] = session['questions'] # why do i have to do this?
	return redirect("/#email_question")

@app.route("/register")
def redirect_to_register():
	return redirect("https://events.r20.constantcontact.com/register/eventReg?oeidk=a07e4q95wra4c76768d&oseq=")
	
def start_session():
	session['questions'] = {
		'topic':{'template':'topic_question.html'},
		'ask':{'template':'ask_question.html'},
		'email':{'template':'email_question.html'}
		}