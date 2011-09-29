from justasksf import db

class Answer(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
	
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Answer %r>' % self.text
		
class BadWord(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(255))
	
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Bad Word %r>' % self.text
		
		
class Question(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(225))
	answers = db.relationship('Answer',backref='question',lazy="dynamic")
	
	def __init__(self, text):
		self.text = text
		
	def __repr__(self):
		return '<Question %r>' % self.text
	
		
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(255), nullable=True)
	name = db.Column(db.String(255), nullable=True)
	answers = db.relationship('Answer',backref='user',lazy="dynamic")
	
	def __init__(self,email=None,name=None):
		self.email = email
		self.name = name

	def __repr__(self):
		return '<User %r>' % self.email