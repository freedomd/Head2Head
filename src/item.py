import webapp2
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Category, Item

class AddItem(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 
        
        # get category information
        category = self.request.get('category') 
        item = self.request.get('newItem')
        if item != "":
            cs = Category.all()
            cs.filter('user =', user.email()) # get user category
            cs.filter('category =', category) # get category
            c = cs.get()
            if c != None:
                items = Item.all()
                items.filter('item =', item)
                items.ancestor(c.key())
                if items.get() == None:
                    newItem = Item(item = item, win = 0, lose = 0, rate = 0, parent = c.key()) # post a new item
                    newItem.put() # save 
                else:
                    errorMessage = "Item %s already exists!" % item
                    self.redirect("/manageCategory?category=%s&error=%s" % (category, errorMessage))
                    return 
        
        self.redirect("/manageCategory?category=%s" % category)

class DeleteItem(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 
        
        # get category information
        category = self.request.get('category') 
        item = self.request.get('item')
        if item != "":
            cs = Category.all()
            cs.filter('user =', user.email()) # get user category
            cs.filter('category =', category) # get category
            c = cs.get()
            if c != None:
                items = Item.all()
                items.filter('item =', item)
                items.ancestor(c.key())
                i = items.get()
                if i == None:
                    self.redirect("/manageCategory?category=%s" % category)
                    return
                else:
                    i.delete()
        
        self.redirect("/manageCategory?category=%s" % category)
        # return 