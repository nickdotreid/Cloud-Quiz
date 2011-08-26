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
	if 'questions' not in session:
		session['questions'] = Question.query.all()
	if request.method == "POST" and 'question_id' in request.form and 'answer' in request.form:
		question = Question.query.filter_by(id=request.form['question_id']).first()
		if question is not None:
			term = Term.query.filter_by(text=request.form['answer']).first()
			if term is None:
				term = Term(request.form['answer'])
				db.session.add(term)
			answer = Answer(question,term)
			db.session.add(answer)
			db.session.commit()
	if len(session['questions'])>0:
		question = session['questions'].pop()
		session['questions'] = session['questions']
		return render_template('question.html',text=question.text,question_id=question.id)
	return render_template('index.html')
	
@app.route("/restart")
def reload_questions():
	session['questions'] = Question.query.all()
	return redirect('/')
	
@app.route("/skip")
def reload_questions():
	session['questions'] = []
	return redirect('/')

@app.route("/answers")
def get_answers():
	questions = []
	for question in Question.query.all():
		q = {'text':question.text,'terms':[]}
		for answer in question.answers:
			found = False
			for term in q['terms']:
				if term['text'] == answer.term.text:
					term['count'] += 1
					found = True
			if not found:
				q['terms'].append({'text':answer.term.text,'count':1})
		questions.append(q)
	return jsonify(questions = questions)