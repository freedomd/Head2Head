from google.appengine.ext import db

class Survey(db.Model):
    user = db.UserProperty()
    categories = db.ListProperty()

class Category(db.Model):
    name = db.StringProperty()
    items = db.ListProperty()
    
class Item(db.Model):
    name = db.StringProperty()
    win = db.IntegerProperty(0)
    lose = db.IntegerProperty(0)
    rate = db.FloatProperty(0.0)