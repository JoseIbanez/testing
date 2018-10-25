#from flask import current_app
from google.appengine.ext import ndb



class Measure(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    probe = ndb.StringProperty()
    date  = ndb.DateTimeProperty(auto_now_add=True)
    temp  = ndb.IntegerProperty()
    name  = ndb.StringProperty()
    value = ndb.StringProperty()

    @classmethod
    def fetch(cls, id):
        return cls.query(Measure.probe == id ).fetch(1)

    @classmethod
    def create(cls):
        m = Measure(probe="siguenza",
                    temp=10000)
        m.put()
        return m

    @classmethod
    def update(cls, id, name, value):

        m = cls.query(Measure.probe == id ).fetch(1)

        
        if not m:
            item = Measure(probe=id, name=name, value=value)
        else:
            item = m[0]
            item.name = name
            item.value = value

        item.put()
        return item


        