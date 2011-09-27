import tagcloud
from models import *

for question in Question.query.all():
	tagcloud.draw(question,(800,800))