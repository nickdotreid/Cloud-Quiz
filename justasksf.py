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
	start_session()
	questions = session['questions']
	return render_template('index.html',questions=questions)
	
@app.route("/townhall")
def townhall_flyer():
	return render_template('townhall_flyer.html')

@app.route("/topic_question",methods=['GET','POST'])
def topic_question():
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'topic' in request.form:
		topic = request.form.getlist('topic')
		question = get_question("topic quesiton")
		for value in topic:
			answer = Answer(value)
			answer.question = question
			db.session.add(answer)
			db.session.commit()
			save_answer(answer)
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
			question = get_question("ask question")
			answer = Answer(request.form['text'])
			answer.question = question
			session['questions']['ask']['success'] = True
			session['questions']['ask']['form'] = request.form
			if len(request.form['name'])>0 and session['email'] is not None:
				user = create_user(session['email'])
				if request.form == user.name:
					answer.user = user
				else:
					session['email'] = None
			db.session.add(answer)
			db.session.commit()
			save_answer(answer)
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
			session['email'] = request.form['email']
			create_user(request.form['email'],request.form['name'])
			save_answer()
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
		'ask':{'template':'ask_question.html'},
		'topic':{'template':'topic_question.html'},
		'email':{'template':'email_question.html'}
		}
	session['answers'] = []
	session['email'] = None

def get_question(text):
	question = Question.query.filter_by(text=text).first()
	if question is not None:
		return question
	question = Question(text)
	db.session.add(question)
	db.session.commit()
	return question
	
def save_answer(answer=None):
	user = None
	if answer is not None:
		session['answers'].append(answer.id)
		session['answers'] = session['answers']
	if session['email'] is not None:
		user = create_user(session['email'])
	for answer_id in session['answers']:
		answer = Answer.query.filter_by(id=answer_id).first()
		if answer is not None and user is not None:
			user.answers.append(answer)
	db.session.commit()
		
def create_user(email = None,name = None):
	if email is not None and email != '' and User.query.filter_by(email=email).first() is not None:
		return User.query.filter_by(email=email).first()
	if name is not None and name != '' and User.query.filter_by(name=name).first() is not None:
		return User.query.filter_by(name=name).first()
	user = User(email,name)
	db.session.add(user)
	db.session.commit()
	return user