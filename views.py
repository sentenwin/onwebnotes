import jinja2
import os
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail

from models import Notes

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class MainPage(BaseHandler):

    def get(self):
        notes = Notes.all()
        self.render_template('index.html', {'notes': notes, 'users': users})

class Home(BaseHandler):

    def get(self):
		user = users.get_current_user()
		notes = Notes.all().filter("author =", user.user_id())
		self.render_template('home.html', {'notes': notes, 'users': users})
		
		
class CreateNote(BaseHandler):

    def post(self):
	user = users.get_current_user()
	if user:
		n = Notes(author=user.user_id(),
				title=self.request.get('title'),
				text=self.request.get('text'),
				priority=self.request.get('priority'),
				status=self.request.get('status'))
		n.put()
		return webapp2.redirect('/home')
	else:
		return webapp2.redirect('/')

    def get(self):
        self.render_template('create.html', {'users': users})


class EditNote(BaseHandler):

    def post(self, note_id):
	user = users.get_current_user()
	if user:
		iden = int(note_id)
		note = db.get(db.Key.from_path('Notes', iden))
		note.author = user.user_id()
		note.title = self.request.get('title')
		note.text = self.request.get('text')
		note.priority = self.request.get('priority')
		note.status = self.request.get('status')
		note.date = datetime.now()
		note.put()
		return webapp2.redirect('/home')
	else:
		return webapp2.redirect('/')
		
    def get(self, note_id):
		iden = int(note_id)
		note = db.get(db.Key.from_path('Notes', iden))
		self.render_template('edit.html', {'note': note, 'users': users})

class ShareNote(BaseHandler):

    def post(self, note_id):
	user = users.get_current_user()
	if user:
		iden = int(note_id)
		note = db.get(db.Key.from_path('Notes', iden))
		
		message = mail.EmailMessage(sender=user.email(),
                            subject="Sharing notes with you")
		message.to = self.request.get('email')
		message.body = note.text
		message.send()
		return webapp2.redirect('/home')
	else:
		return webapp2.redirect('/')
		
    def get(self, note_id):
		iden = int(note_id)
		note = db.get(db.Key.from_path('Notes', iden))
		self.render_template('share.html', {'note': note, 'users': users})

class DeleteNote(BaseHandler):

    def get(self, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notes', iden))
        db.delete(note)
        return webapp2.redirect('/home')


