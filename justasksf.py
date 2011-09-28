from flask import Flask, redirect, request, flash, render_template, session, jsonify, Blueprint
from flaskext.sqlalchemy import SQLAlchemy
import re

from db_config import *

from createsend import CreateSend, Subscriber
CreateSend.api_key = campaign_monitor_api_key

from twilio.rest import TwilioRestClient

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
	
@app.route("/sms",methods=['GET','POST'])
def twilio_connect():
	number = False
	message = False
	if request.method == "POST" and 'From' in request.form:
		number = request.form['From']
		message = 'Add your words about HIV.  Type "past", "present" or "future" followed by your words. ex "past mad sad bad".'
		if 'Body' in request.form and request.form['Body'] != '':
			words = request.form['Body'].split(' ')
			if len(words) > 1:
				question = False
				words.reverse()
				term = words.pop()
				if term == "past":
					question = get_question("words_past")
				if term == "present":
					question = get_question("words_present")
				if term == "future":
					question = get_question("words_future")
				if question:
					for word in words:
						answer = Answer(word)
						answer.question = question
						db.session.add(answer)
					db.session.commit()
					message = "Your words have been added to our cloud"
	if number and message:
		client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
		message = client.sms.messages.create(to=number,
		                                     from_="+14157023723",
		                                     body=message)
	return render_template('sms_form.html')
	
@app.route("/cloud")
def cloud_map():
	session['questions'] = [
	{'key':'words_past','title':'Past','template':'words_past_question.html'},
	{'key':'words_present','title':'Present','template':'words_present_question.html'},
	{'key':'words_future','title':'Future','template':'words_future_question.html'},
	]
	return render_template('cloud_map.html', questions=session['questions'])
	
@app.route("/tagmap",methods=['GET','POST'])
def get_cloud():
	answers = {}
	size = (800,800)
	question = False
	if request.method == "POST" and 'question' in request.form:
		if 'width' in request.form and 'height' in request.form:
			size = (int(request.form['width']),int(request.form['height']))
		question = get_question(request.form['question'])
	for answer in question.answers.all():
		if answer.text not in answers:
			answers[answer.text] = 1
		answers[answer.text] += 1
	if question:
		import tagcloud
		import sys
		sys.path.append(tagcloud.path_to_pytagcloud)
		import pytagcloud
	
		tags = tagcloud.format_tags(answers)
		cloud = pytagcloud.create_html_data(tags,size)
		return jsonify(words=cloud[0]['links'])
	return redirect("/")

@app.route("/words_question",methods=['GET','POST'])
def save_words():
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'question' in request.form and len(request.form['question'])>0 and 'answer' in request.form:
		question = get_question(request.form['question'])
		answers = request.form.getlist('answer')
		for value in answers:
			if len(value)>0:
				answer = Answer(value)
				answer.question = question
				db.session.add(answer)
				db.session.commit()
				save_answer(answer)
		if request.method == "POST" and 'ajax' in request.form:
			session_question = update_session_question(request.form['question'],{})
			return render_template(session_question['template'], success=True, form=request.form,errors={})
	update_session_question(request.form['question'],{'success':True})
	return redirect('/#words_question')

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
	else:
		errors = {'topics[]':'Please select at least one interest'}
	if request.method == "POST" and 'ajax' in request.form:
		return render_template('topic_question.html',success=True,form=request.form,errors={})
	update_session_question('topic',{'success':True})
	return redirect("/#topic_question")

@app.route("/ask_question",methods=['GET','POST'])
def ask_question():
	success = False
	errors = {}
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'text' in request.form:
		if len(request.form['text']) > 0 and len(request.form['text']) < 550:
			question = get_question("ask question")
			answer = Answer(request.form['text'])
			answer.question = question
			success = True
			if len(request.form['name'])>0 and session['email'] is not None:
				user = create_user(session['email'])
				if request.form['name'].upper() == user.name.upper():
					answer.user = user
				else:
					session['email'] = None
					session['name'] = request.form['name']
					user = User(None,request.form['name'])
					db.session.add(user)
					answer.user = user
			db.session.add(answer)
			db.session.commit()
			save_answer(answer)
			success = True
		else:
			errors['text'] = 'Your question must be less than 500 characters'
	if request.method == "POST" and 'ajax' in request.form:
		return render_template('ask_question.html',success=success,form=request.form,errors=errors)
	update_session_question('ask',{'success':success,'errors':errors})
	return redirect("/#ask_question")
	
@app.route("/capture_email",methods=['GET','POST'])
def capture_email():
	success = False
	errors = {}
	if request.method == "POST" and 'honeypot' in request.form and len(request.form['honeypot']) < 1 and 'email' in request.form:
		if 'email' in request.form and len(request.form['email'])>0:
			session['email'] = request.form['email']
			if len(request.form['name'])>0 and session['name'] is not None and request.form['name'].upper() == session['name'].upper():
				user = User.query.filter_by(name=session['name']).first()
				user.email = request.form('email')
			else:
				create_user(request.form['email'],request.form['name'])
			save_answer()
			sub = Subscriber()
			sub.add(campaign_monitor_list_id,request.form['email'],request.form['name'],[],True)
			success = True
		else:
			errors['email'] = 'we need an email to keep in touch'
	if request.method == "POST" and 'ajax' in request.form:
		return render_template('email_question.html',success=success,form=request.form,errors={})
	update_session_question('email',{'success':success,'errors':errors})
	return redirect("/#email_question")

@app.route("/register")
def redirect_to_register():
	return redirect("https://events.r20.constantcontact.com/register/eventReg?oeidk=a07e4q95wra4c76768d&oseq=")
	
def start_session():
	session['questions'] = [
		{'key':'ask','template':'ask_question.html'},
		{'key':'topic','template':'topic_question.html'},
		{'key':'email','template':'email_question.html'}
		]
	session['answers'] = []
	session['email'] = None
	session['name'] = None

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
	
def update_session_question(qslug,data):
	for question in session['questions']:
		if question['key'] == qslug:
			for key in data:
				question[key] = data
			session['questions'] = session['questions']
			return question