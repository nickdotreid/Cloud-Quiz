from justasksf import db

class Question(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Question %r>' % self.text
		
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(255), nullable=True)
	name = db.Column(db.String(255), nullable=True)
	questions = db.relationship('Question',backref='user',lazy="dynamic")
	
	def __init__(self,email=None,name=None):
		self.email = email
		self.name = name

	def __repr__(self):
		return '<User %r>' % self.email