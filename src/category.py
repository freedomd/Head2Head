import webapp2
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Category

class CategoryPage(webapp2.RequestHandler):
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
        
        userCats = Category.all()
        userCats.filter('user =', user.email()) # get user category
        isEmpty = userCats.get()
        #print userCats.count(self)"
        
        
        template_values = {
            'user': user,
            'userCats': userCats,
            'login': login, 
            'url': url,
            'isEmpty': isEmpty
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/category.html')
        self.response.out.write(template.render(path, template_values))
        

class AddCategory(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 
        
        # get category information
        category = self.request.get('newCategory') 
        if category != "":
            newCat = Category() # post a new category
            newCat.category = category
            newCat.user = user.email()
            newCat.username = user.nickname()
            newCat.put() # save 
        
        self.redirect("/category")
        # return 
