import webapp2
from views import MainPage, CreateNote, DeleteNote, EditNote, Home, ShareNote

app = webapp2.WSGIApplication([
        ('/', MainPage), 
		('/home', Home), 
        ('/create', CreateNote), 
        ('/edit/([\d]+)', EditNote),
		('/share/([\d]+)', ShareNote),
        ('/delete/([\d]+)', DeleteNote)
        ],
        debug=True)
