from google.appengine.ext import ndb

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    anagramwordlistcount = ndb.IntegerProperty()
    anagramuniquewordcount = ndb.IntegerProperty()

class MyAnagramDatabase(ndb.Model):
    anagramwordlist = ndb.StringProperty(repeated=True)
    wordcount = ndb.IntegerProperty()
    lettercount = ndb.IntegerProperty()
    useremailid = ndb.UserProperty()
