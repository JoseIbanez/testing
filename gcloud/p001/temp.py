#from flask import current_app
from google.appengine.ext import ndb



class Measure(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    probe = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    temp = ndb.IntegerProperty()

    @classmethod
    def query_probe(cls, key):
        #akey = ndb.Key(Measure.probe == "siguenza")
        #return cls.query(ancestor=akey).order(-cls.date)
        return cls.query(Measure.probe == "siguenza" )

    @classmethod
    def create(cls):
        m = Measure(probe="siguenza",
                    temp=10000)
        m.put()
        return m