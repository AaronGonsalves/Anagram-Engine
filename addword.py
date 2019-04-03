import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from myuser import MyAnagramDatabase

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def ReorderingWord(unorderedWord):
    lexicographicalOrderedWord = ''.join(sorted(unorderedWord))
    return lexicographicalOrderedWord

class AddAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        keyid = user.user_id()
        myuser = myuser_key.get()

        template_values = {
         'myuser' : myuser
        }

        template = JINJA_ENVIRONMENT.get_template('addword.html')
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers['content-Type'] = 'text/html'

        if self.request.get('submit') == 'Submit':

            getUserName = users.get_current_user()

            getLexicographicalWord = self.request.get('anagram_word').lower()
            anagramWordLetterLength = len(getLexicographicalWord)
            lexicographicalOrderedAnagramWord = ReorderingWord(getLexicographicalWord)

            keyName = getUserName.user_id()+lexicographicalOrderedAnagramWord

            retriveAnagramkey = ndb.Key(MyAnagramDatabase, keyName)
            retriveAnagramWord = retriveAnagramkey.get()

            if retriveAnagramWord == None:

                storedatabase = MyAnagramDatabase(id=keyName, orderedword=lexicographicalOrderedAnagramWord,
                                                  lettercount = anagramWordLetterLength, useremailid = getUserName,
                                                  wordcount = 1)
                # storecountdatabase = MyUser(anagramuniquewordcount = 1)
                storedatabase.anagramwordlist.append(getLexicographicalWord)
                # storecountdatabase.put()
                storedatabase.put()

                template_values = {
                    'success' : 'Word added successfully to the system'
                }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))

            else:
                counterWordExist = 0
                for storedAnagramWord in retriveAnagramWord.anagramwordlist:
                    if storedAnagramWord == getLexicographicalWord:
                        counterWordExist = 1
                        break

                if counterWordExist == 1:
                    template_values = {
                        'error' : 'Word already exist in the system'
                    }
                    template = JINJA_ENVIRONMENT.get_template('main.html')
                    self.response.write(template.render(template_values))

                else:
                    retriveAnagramListLength = len(retriveAnagramWord.anagramwordlist)
                    retriveAnagramWord.wordcount = retriveAnagramListLength + 1

                    retriveAnagramWord.anagramwordlist.append(getLexicographicalWord)

                    retriveAnagramWord.put()

                    template_values = {
                        'success' : 'Word added successfully to the system'
                    }
                    template = JINJA_ENVIRONMENT.get_template('main.html')
                    self.response.write(template.render(template_values))

        if self.request.get('button') == 'Back':
            self.redirect('/')
