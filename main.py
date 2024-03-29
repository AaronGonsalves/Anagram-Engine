import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from myuser import MyAnagramDatabase
from addword import AddAnagram
from subanagramsearch import SubAnagramWord
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

anagramUniqueWordCount = ''
anagramWordListCount = ''

def ReorderingWord(unorderedWord):
    lexicographicalOrderedWord = ''.join(sorted(unorderedWord))
    return lexicographicalOrderedWord

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'
        global anagramUniqueWordCount
        global anagramWordListCount
        welcome = 'Welcome'
        url_string = ''
        myuser = ''
        url = ''

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id(), username=user.email(),
                                anagramwordlistcount=0, anagramuniquewordcount=0)
                myuser.put()

            anagramUniqueWordCount = myuser.anagramuniquewordcount
            anagramWordListCount = myuser.anagramwordlistcount

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'

        template_values = {
         'url' : url,
         'url_string' : url_string,
         'user' : user,
         'welcome' : welcome,
         'myuser' : myuser,
         'uniqueanagramwordcurrentdata' : anagramUniqueWordCount,
         'anagramwordlistcurrentdata' : anagramWordListCount
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        welcome = 'Welcome'
        getUserName = users.get_current_user()
        url = users.create_login_url(self.request.uri)
        self.response.headers['content-Type'] = 'text/html'

        if self.request.get('search') == 'Search':

            getLexicographicalWord = self.request.get('anagram_word_search')
            lexicographicalOrderedAnagramWord = ReorderingWord(getLexicographicalWord)

            keyName = getUserName.user_id()+lexicographicalOrderedAnagramWord

            retriveAnagramWordKey = ndb.Key(MyAnagramDatabase, keyName)
            retriveAnagramWord = retriveAnagramWordKey.get()

            if retriveAnagramWord == None:
                template_values = {
                 'url' : url,
                 'user' : getUserName,
                 'welcome' : welcome,
                 'uniqueanagramwordcurrentdata' : anagramUniqueWordCount,
                 'anagramwordlistcurrentdata' : anagramWordListCount,
                 'anagram_Word_List_message' : 'Anagram word list is empty'
                }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))

            else:
                template_values = {
                 'url' : url,
                 'user' : getUserName,
                 'welcome' : welcome,
                 'uniqueanagramwordcurrentdata' : anagramUniqueWordCount,
                 'anagramwordlistcurrentdata' : anagramWordListCount,
                 'anagram_Word_List' : retriveAnagramWord.anagramwordlist,
                 'anagram_Word_Count' : len(retriveAnagramWord.anagramwordlist)
                }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/addword', AddAnagram),
    ('/subanagramsearch',SubAnagramWord)
    ], debug=True)
