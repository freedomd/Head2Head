import webapp2
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Category, Item
import xml.etree.ElementTree as xml
from xml.dom import minidom

class Export(webapp2.RequestHandler):
    def get(self):  
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 
        
        creator = self.request.get('creator')
        category = self.request.get('category') 
        #path = self.request.get('path')
        
        cats = Category.all()
        cats.filter('user =', creator) # get user category
        cats.filter('category =', category) # get category
        c = cats.get()
        
        if c == None:
            self.redirect("/")
            return
        
        items = Item.all()
        items.ancestor(c.key()) # get all the items of c
        
        self.response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        self.response.out.write('<CATEGORY>\n')
        self.response.out.write('\t<NAME>%s</NAME>\n' % category)
        #print '<CATEGORY>'
        #print '\t<NAME>%s</NAME>' % category
        
        for item in items.run():
            #print '\t<ITEM>'
            #print '\t\t<NAME>%s</NAME>' % item.item
            #print '\t</ITEM>'
            self.response.out.write('\t<ITEM>\n')
            self.response.out.write('\t\t<NAME>%s</NAME>\n' % item.item)
            self.response.out.write('\t</ITEM>\n')
        
        self.response.out.write('</CATEGORY>')
        #print '</CATEGORY>'
        
        '''
        CATEGORY = xml.Element('CATEGORY')
        NAME = xml.Element('NAME')
        NAME.text = category
        CATEGORY.append(NAME)
        '''
        
        '''
        for item in items.run():
            #Create child elements
            ITEM = xml.Element('ITEM')
            NAME = xml.Element('NAME')
            NAME.text = item.item
            ITEM.append(NAME)
            CATEGORY.append(ITEM)
        
        
        try:
            filename = category + ".xml"
            filepath = os.path.join(path, filename)
            out = open(filepath, 'w+') # open a file
            #Create an ElementTree object from the root element
            xml.ElementTree(CATEGORY).write(out)
            out.close()
        except Exception, e:
            message = 'Cannot open file %s' % filepath
            self.redirect("/?message=%s" % message)
            return 
        '''
        '''
        template_values = {
            'items': items,
            'category': category,
        }
        '''
        #path = os.path.join(os.path.dirname(__file__), 'templates/xml_template.xml')
        #self.response.out.write(template.render(path, template_values))
        #return template.render(path, template_values)


class Import(webapp2.RequestHandler):
    def post(self):  
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
            return 

        content = self.request.get('content')
        if content == None or content == "":
            self.redirect("/category")
            return 
        xmldoc = minidom.parseString(content)
        category = xmldoc.getElementsByTagName('CATEGORY')[0]
        categoryName = category.getElementsByTagName('NAME')[0].childNodes[0].nodeValue
        itemList = category.getElementsByTagName('ITEM')
        
        cats = Category.all()
        cats.filter("category =", str(categoryName))
        c = cats.get()
        
        if c == None: # category not exist
            newCat = Category() # create a new category
            newCat.category = categoryName
            newCat.user = user.email()
            newCat.username = user.nickname()
            newCat.put() # save
            for item in itemList:
                itemName = item.getElementsByTagName('NAME')[0].childNodes[0].nodeValue
                newItem = Item(item = itemName, win = 0, lose = 0, rate = 0, parent = newCat.key())
                newItem.put()
            importMessage = 'Import new category "%s" successfully.' % categoryName
            self.redirect("/category?importMessage=%s" % importMessage)
        else: # category exists
            items = Item.all()
            items.ancestor(c.key())
            
            oldItemNameList = []
            for item in items.run():
                oldItemNameList.append(item.item)
            
            newItemNameList = []
            for item in itemList:
                itemName = item.getElementsByTagName('NAME')[0].childNodes[0].nodeValue
                newItemNameList.append(itemName)
                if itemName not in oldItemNameList: # new item not exist
                    newItem = Item(item = itemName, win = 0, lose = 0, rate = 0, parent = c.key())
                    newItem.put()
            
            for item in items: # get old items
                if item.item not in newItemNameList: # old item not in new list, delete
                    item.delete()
                    
            importMessage = 'Import existed category "%s" successfully.' % categoryName
            self.redirect("/category?importMessage=%s" % importMessage)
        

    