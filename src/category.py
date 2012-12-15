import webapp2
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Category, Item

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
            'isEmpty': isEmpty,
            'error': self.request.get('error'),
            'message': self.request.get('message'),
            'importMessage': self.request.get('importMessage')
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
            # check if exists
            c = Category.all()
            c.filter('user =', user.email()) # get user category
            c.filter('category =', category) # check
            if c.get() == None:# does not exist
                newCat = Category() # post a new category
                newCat.category = category
                newCat.user = user.email()
                newCat.username = user.nickname()
                newCat.put() # save 
            else:
                errorMessage = "Category %s already exists!" % category
                self.redirect("/category?error=%s" % errorMessage)
                return 

        self.redirect("/category")
        # return 
        
        
class ManageCategory(webapp2.RequestHandler):
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
        
        # get category information
        category = self.request.get('category')
        cs = Category.all()
        cs.filter('user =', user.email()) # get user category
        cs.filter('category =', category) # get category
        c = cs.get()
        if c != None: # this category
            items = Item.all()
            items.ancestor(c.key())
            isEmpty = items.get()
            
            template_values = {
                               'user': user,
                               'login': login, 
                               'url': url,
                               'isEmpty': isEmpty,
                               'category': category,
                               'items': items,
                               'error': self.request.get('error'),
                               'message': self.request.get('message')
            }
        
            path = os.path.join(os.path.dirname(__file__), 'templates/manage_category.html')
            self.response.out.write(template.render(path, template_values))
        else:       
            self.redirect("/category")


class DeleteCategory(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 
        
        # get category information
        category = self.request.get('category') 
        if category != "":
            cs = Category.all()
            cs.filter('user =', user.email()) # get user category
            cs.filter('category =', category) # get category
            c = cs.get()
            if c != None:
                items = Item.all()
                items.ancestor(c.key())
                for item in items.run():
                    item.delete()
                c.delete()
        
        self.redirect("/category")
        # return 

class ModifyCategory(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 
        
        # get category information
        category = self.request.get('category') 
        newname = self.request.get(category)
        if newname != "" and newname != category:
            cs = Category.all()
            cs.filter('user =', user.email()) # get user category
            cs.filter('category =', category) # get category
            c = cs.get()
            if c != None:
                c.category = newname
                c.put()
                message = 'Modification of "%s" successfully saved.' % newname
                self.redirect("/category?message=%s" % message)
                return
                    
        self.redirect("/category")
