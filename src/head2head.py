import webapp2
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template

class HomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            login = True
            username = user.nickname()
            url = users.create_logout_url(self.request.uri)
        else:
            login = False
            username = ""
            url = users.create_login_url(self.request.uri)
            
        categories = None
        template_values = {
            'login': login,
            'categories': categories,
            'username': username,
            'url': url
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, template_values))
        

app = webapp2.WSGIApplication([('/', HomePage), 
                               #('/login', LoginHandler),
                               #('/logout', LogoutHandler),
                               #('/register', RegisterHandler),
                              ], debug=True)
