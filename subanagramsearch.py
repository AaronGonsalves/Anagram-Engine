import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from myuser import MyAnagramDatabase
from addword import AddAnagram

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def ReorderingWord(unorderedWord):
    lexicographicalOrderedWord = ''.join(sorted(unorderedWord))
    return lexicographicalOrderedWord

def subanagramWordShuffle(getLexicographicalSubAnagramWord, subanagramWordSizeShuffle):
    splittingSubAnagramWordToLetter = tuple(getLexicographicalSubAnagramWord)
    lengthOfLexicographicalSubAnagramWord = len(splittingSubAnagramWordToLetter)
    createSubAnagramWordList = list(range(subanagramWordSizeShuffle))
    yield tuple(splittingSubAnagramWordToLetter[splitSubAnagramCounter] for splitSubAnagramCounter in createSubAnagramWordList)
    while True:
        for singleWordCounter in reversed(range(subanagramWordSizeShuffle)):
            if createSubAnagramWordList[singleWordCounter] != singleWordCounter + lengthOfLexicographicalSubAnagramWord - subanagramWordSizeShuffle:
                break
        else:
            return
        createSubAnagramWordList[singleWordCounter] = createSubAnagramWordList[singleWordCounter] + 1
        for singleWordCounterPlus in range(singleWordCounter+1, subanagramWordSizeShuffle):
            createSubAnagramWordList[singleWordCounterPlus] = createSubAnagramWordList[singleWordCounterPlus-1] + 1
        yield tuple(splittingSubAnagramWordToLetter[singleWordCounter] for singleWordCounter in createSubAnagramWordList)

class SubAnagramWord(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'
        template_values = {
            'subanagram_header_message' : 'Search Sub-anagram Word'
        }
        template = JINJA_ENVIRONMENT.get_template('subanagramsearch.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['content-Type'] = 'text/html'
        getUserName = users.get_current_user()

        if self.request.get('sub_search') == 'Search':
            getLexicographicalSubAnagramWord = self.request.get('sub_anagram_word_search')

            subAnagramWordStore = []
            sizeOfSubAnagramWord = len(getLexicographicalSubAnagramWord)
            sizeOfSubAnagramWordIncrement = sizeOfSubAnagramWord + 1

            for subAnagramWordSizeShuffle in range(sizeOfSubAnagramWordIncrement):
                if subAnagramWordSizeShuffle >= 3:
                    storeSubAnagramWord = list(map(''.join,(subanagramWordShuffle(getLexicographicalSubAnagramWord, subAnagramWordSizeShuffle))))
                    for takingSingleWord in storeSubAnagramWord:
                        reorderSubAnagramWord = ReorderingWord(takingSingleWord)
                        subAnagramWordKey = getUserName.user_id()+reorderSubAnagramWord
                        retriveAnagramWordKey = ndb.Key(MyAnagramDatabase, subAnagramWordKey)
                        retriveAnagramWord = retriveAnagramWordKey.get()
                        if retriveAnagramWord != None:
                            for singleword in retriveAnagramWord.anagramwordlist:
                                subAnagramWordStore.append(singleword)

            subAnagramWordStoreUnique = list(set(subAnagramWordStore))
            template_values = {
             'anagram_Word_List' : subAnagramWordStoreUnique,
             'sub_anagram_word_search_message' : 'Sub-anagram word list is empty'
            }
            template = JINJA_ENVIRONMENT.get_template('subanagramsearch.html')
            self.response.write(template.render(template_values))

        if self.request.get('button') == 'Back':
            self.redirect('/')
