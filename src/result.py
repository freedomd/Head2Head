import webapp2
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Category, Item

class ResultPage(webapp2.RequestHandler):
    def get(self):  
        user = users.get_current_user()
        
        if user:
            login = True
            url = users.create_logout_url(self.request.uri)
        else:
            login = False
            url = users.create_login_url(self.request.uri)
            self.redirect("/")
            return 
        
        creator = self.request.get('creator')
        category = self.request.get('category') 
        cats = Category.all()
        cats.filter('user =', creator) # get user category
        cats.filter('category =', category) # get category
        c = cats.get()
        
        if c == None:
            self.redirect("/")
            return
        
        items = Item.all()
        items.ancestor(c.key()) # get all the items of c
        items.order('-rate')
        
        template_values = {
            'user': user,
            'login': login, 
            'url': url,
            'items': items,
            'creator': creator,
            'creatorName': c.username,
            'category': category,
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/result.html')
        self.response.out.write(template.render(path, template_values))
    