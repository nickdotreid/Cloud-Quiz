from cloud_quiz import db

class Answer(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
	term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
	
	def __init__(self,question,term):
		self.question = question
		self.term = term
		
	def __repr(self):
		return '<Answer %r>' % self.id

class Question(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(255))
	
	answers = db.relationship('Answer',backref='question',lazy="dynamic")
	
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Question %r>' % self.text
		
class Term(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(255))
	
	answers = db.relationship('Answer',backref='term',lazy="dynamic")
	
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Term %r>' % self.text