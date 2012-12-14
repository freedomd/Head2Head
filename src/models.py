from google.appengine.ext import db

class Category(db.Model):
    user = db.StringProperty()
    username = db.StringProperty()
    category = db.StringProperty()
    
class Item(db.Model):
    item = db.StringProperty()
    win = db.IntegerProperty()
    lose = db.IntegerProperty()
    rate = db.IntegerProperty()
    category = db.StringProperty()
    user = db.StringProperty()