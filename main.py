import webapp2
import os
import jinja2
from google.appengine.ext import db
import cgi

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

def blog_key(name = 'default'):
	return db.Key.from_path('blogs', name)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Posts(db.Model):
	title = db.StringProperty(required=True)
	newpost = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
	def get(self, title="", newpost="", error=""):
		newposts = db.GqlQuery("SELECT * FROM Posts "
			"ORDER BY created DESC limit 5;")
		# newposts = Posts.all().order('-created')
		self.render("blogpost.html", title=title, newpost=newpost, error=error, newposts=newposts)

class NewPost(Handler):
	def get(self, title="", newpost="", error=""):
		self.render("newpost.html", title=title, newpost=newpost, error=error)

	def post(self):
		title = self.request.get("title")
		newpost = self.request.get("newpost")

		if not title:
			error = "Please enter a title"
			self.get(title=title, newpost=newpost, error=error)

		elif not newpost:
			error = "Please enter a blog post" 
			self.get(title=title, newpost=newpost, error=error)

		else:
			a = Posts(title=title, newpost=newpost)
			a.put()
			self.get()

class ViewPostHandler(Handler):
    def get(self, id):
    	key = db.Key.from_path('Posts', int(id), parent = blog_key())
    	post = Posts.key
    	self.response.write(post)

app = webapp2.WSGIApplication([
	('/blog', MainPage),
	('/blog/newpost', NewPost),
	webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)