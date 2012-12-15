import webapp2
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
from category import *
from item import *
from vote import *
from result import *
from xmlHandler import *

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
            
        categories = Category.all()
        isEmpty = categories.get()
        template_values = {
            'user': user,
            'login': login,
            'categories': categories,
            'username': username,
            'url': url,
            'isEmpty': isEmpty,
            'message': self.request.get('message')
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, template_values))
        

app = webapp2.WSGIApplication([('/', HomePage), 
                               ('/category', CategoryPage),
                               ('/addCategory', AddCategory),
                               ('/manageCategory', ManageCategory),
                               ('/deleteCategory', DeleteCategory),
                               ('/modifyCategory', ModifyCategory),
                               ('/addItem', AddItem),
                               ('/deleteItem', DeleteItem),
                               ('/resetItem', ResetItem),
                               ('/vote',VotePage),
                               ('/result',ResultPage),
                               ('/export',Export),
                               ('/import',Import),
                              ], debug=True)
