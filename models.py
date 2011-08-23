from cloud_quiz import db

class Question(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(255))
	
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Question %r>' % self.text
		
class Term(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(255))
	
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Term %r>' % self.text