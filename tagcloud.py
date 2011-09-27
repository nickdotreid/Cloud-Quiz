from models import *

path_to_pytagcloud = "/Users/nickreid/Documents/sfhiv/JustAsk/lib/PyTagCloud/src"

def draw(question,size = (1000,600)):
	filename = "static/clouds/"+question.text+".png"
	tags = {}
	for answer in question.answers:
		if answer.text in tags:
			tags[answer.text] += 1
		else:
			tags[answer.text] = 1
	tags = format_tags(tags)
	
	import sys
	sys.path.append(path_to_pytagcloud)
	import pytagcloud
	
	pytagcloud.create_tag_image(tags,filename,size)
	
def format_tags(tags,color=(0,0,0)):
	new_tags = []
	for tag in tags:
		new_tags.append({
			'tag':tag,
			'size':tags[tag]*15,
			'color':color,
		})
	return new_tags