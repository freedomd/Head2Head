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
                    newItem = Item(item = item, win = 0, lose = 0, rate = 0, 
                                   category = c.category, user = user.email(), parent = c.key()) # post a new item
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

class ResetItem(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 
        
        # get category information
        category = self.request.get('category') 
        item = self.request.get('item')
        newname = self.request.get(item)
        if newname != "":
            cs = Category.all()
            cs.filter('user =', user.email()) # get user category
            cs.filter('category =', category) # get category
            c = cs.get()
            if c != None:
                items = Item.all()
                items.filter('item =', item)
                items.ancestor(c.key())
                i = items.get()
                if i != None:
                    # reset
                    i.item = newname
                    i.win = 0
                    i.lose = 0
                    i.rate = 0
                    i.put()
                    message = 'Reset "%s" successfully.' % newname
                    self.redirect("/manageCategory?category=%s&message=%s" % (category, message))
                    return
                    
        self.redirect("/manageCategory?category=%s" % category)
        # return 