import webapp2
import os
import random
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Category, Item

class VotePage(webapp2.RequestHandler):
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
        itemList = []
        for item in items.run():
            itemList.append(item.item)
        
        if len(itemList) > 1:
            length = len(itemList)
            i = random.randint(0, length - 1)
            j = random.randint(0, length - 1)
            while i == j:
                j = random.randint(0, length - 1)

            choice1 = itemList[i]
            choice2 = itemList[j]
            error = None
        else:
            choice1 = None
            choice2 = None
            error = "Options not enough!"
        
        template_values = {
            'user': user,
            'login': login, 
            'url': url,
            'winner': None,
            'loser': None,
            'choice1': choice1, 
            'choice2': choice2,
            'creator': creator,
            'creatorName': c.username,
            'category': category,
            'error': error
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/vote.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):  
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
        
        # check winner
        winner = self.request.get('option')
        lastChoice1 = self.request.get('choice1')
        lastChoice2 = self.request.get('choice2')
        if winner == lastChoice1:
            loser = lastChoice2
        else:
            loser = lastChoice1
        
        items = Item.all()
        items.ancestor(c.key()) # get all the items of c
        itemList = []
        #w, l = None
        for item in items.run():
            itemList.append(item.item)
            
            # update winner and loser data
            if item.item == winner:
                item.win += 1
                item.rate = item.win * 100 / (item.win + item.lose)
                item.put()
                w = item
            if item.item == loser:
                item.lose += 1
                item.rate = item.win * 100 / (item.win + item.lose)
                item.put()
                l = item
                     
        if len(itemList) > 1:
            length = len(itemList)
            i = random.randint(0, length - 1)
            j = random.randint(0, length - 1)
            while i == j:
                j = random.randint(0, length - 1)

            choice1 = itemList[i]
            choice2 = itemList[j]
            error = None
        else:
            error = "Options not enough!"
        
        template_values = {
            'user': user,
            'login': login, 
            'url': url,
            'winner': w,
            'loser': l,
            'choice1': choice1, 
            'choice2': choice2,
            'creator': creator,
            'creatorName': c.username,
            'category': category,
            'error': error
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/vote.html')
        self.response.out.write(template.render(path, template_values))
