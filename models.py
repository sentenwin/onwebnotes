from google.appengine.ext import db



class Notes(db.Model):

	author = db.StringProperty()
	title = db.StringProperty()
	text = db.StringProperty(multiline=True)
	priority = db.StringProperty()
	status = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
