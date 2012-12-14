from google.appengine.ext import db

class Category(db.Model):
    user = db.StringProperty()
    username = db.StringProperty()
    category = db.StringProperty()
    
class Item(db.Model):
    item = db.StringProperty()
    win = db.IntegerProperty(0)
    lose = db.IntegerProperty(0)
    rate = db.FloatProperty(0.0)