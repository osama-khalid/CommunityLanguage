#d[word.lower()] syllable
#https://docs.python.org/2/library/urllib.html#urllib.quote_plus        urlunqote

#from pycontractions import Contractions         #pip install
#https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python


import nltk         #pip install    
nltk.download('punkt')
nltk.download('words')
nltk.download('cmudict')
nltk.download('averaged_perceptron_tagger')
import contractions #pip install

from nltk.corpus import words             #check dictionary
from nltk import pos_tag as posTag
import re                           #elongation
from autocorrect import spell as spellCheck      #pip install     #check spelling
from nltk.tokenize import sent_tokenize #sentence tokenizer         https://www.nltk.org/api/nltk.tokenize.html also see
import csv                              #read file    
from datetime import datetime           #convert unix time to human time
from nltk.tokenize import RegexpTokenizer       #remove puncutations
from nltk import edit_distance as ed    #check word spelling correction distance
import urllib.request as urllib         #ud convert url to unicode
punctuations = RegexpTokenizer(r'\w+')
from nltk.corpus import cmudict
CMUdict = cmudict.dict()      #syllable

class preProcess(object):
    
    def __init__(self):
        self.ud=self.urbanLoad()
    
    def chanCleaner(self,post):          #clean 4archive posts
        return(post.replace('<marquee>[trigger warning]</marquee>','').replace('\\\n',' . ')[6:])

    def chanDate(self,D,split=1):    #standardizes 4chan date
        date_object=datetime.fromtimestamp(int(row[dateStamp]))
        return(str(date_object.year)+'-'+str((int(date_object.month)-1)//split))

    def voatCleaner(self,post):      #cleans voat posts
        return(html.unescape(post).replace('\n','. ').replace('&nbsp;','.'))    
    
    def redditCleaner(self,post):      #cleans voat posts
        return(post.replace('\n','. '))        
    
    def voatDate(self,D,split=1):    #standardizes voat date
        date_object=D.split(' ')[0].split('/')
        return(str(date_object[2])+'-'+str((int(date_object[0])-1)//split))
    
    def redditDate(self,D,split=1):    
        date_object=datetime.fromtimestamp(int(row[dateStamp]))
        return(str(date_object.year)+'-'+str((int(date_object.month)-1)//split))

    def urbanLoad(self,year=2019): #urban dictionary load in lowercase

        #load urban dictionary
        urbanFile=open('urbandictionary.'+str(year),'r',encoding='utf-8').read().split('\n')
        #urban dictionary:
        ud=[]
        for u in urbanFile:
            if len(u)>0:
                ud.append(urllib.unquote(u.lower()))
        return(ud)
        
        
    def reduceLengthening(self,text):           #Contracts all repetitions to at most 2
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", text)

    def reduceLengtheningSingle(self,text):    #Contracts all repetitions to 1
        pattern = re.compile(r"(.)\1{1,}")
        return pattern.sub(r"\1", text)
        
            
    def wordCheck(self,word):
        if word in words.words():         #if word in dictionary
            return(word)
        if word in self.ud:                      #if word in urbandictionary
            return(word)
        return(None)
    

    
    def wordNormalizer(self,word):#      Does not convert i;ve to I have
        word=word.lower()
        
        word1=reduceLengtheningSingle(word)
        
        word2=reduceLengthening(word)
        if word1==word:                     #No double letter
            return(wordCheck(word))
            
        if word==word2:                    #No contraction at all
            return(wordCheck(word))
        if wordCheck(word2) != None:       #word with double letter is in dictionary            
            return(wordCheck(word2))
        if wordCheck(word1) !=None:        #word with single letters is in dictionary          luuuuvvvv
            return(wordCheck(word1))
            
        if spellCheck(word1)==spellCheck(word2):                  #   finnnnnaaaallly
            return(spellCheck(word1))
        else:
            return(None)

    def deContraction(self,word): #Normalizes contractions (but doesn't work for all lower case)         #A better option would be pycontractions, but my current machine can't load the models
        return(contractions.fix(word))



    
    def sentenceTokenize(self,post):		#Returns list of sentences in Post and list of list of words
        sentences=[]
        word=[]
        rawSentences=sent_tokenize(post)
        for s in rawSentences:
            if len(s.strip('.').strip(' '))>0:
                sentences.append(s)
                if len(s)>0:
                    tokens = punctuations.tokenize(s)
                    if len(tokens)>0:
                        word.append(tokens)           #all words tokenized
        return([sentences,word])

    def wordTokenize(self,sentence): #Returns list of words in sentence
        tokens = punctuations.tokenize(sentence)
        if len(tokens)>0:
            return(tokens)
        else:
            return(None)        


    def wordTokenizeCons(self,sentence):    #Conservative word Tokenizer
        sentence=sentence.replace("'",'_')
        tempTokens = punctuations.tokenize(sentence)
        tokens=[]
        if len(tempTokens)>0:
            for t in tempTokens:
                deContract=self.deContraction(t.replace("_","'")).split(' ')
                for d in deContract:
                    tokens.append(d)
            return(tokens)
        
        
        else:
            return(None)        

        
    def postFlatten(self,board):
        s=""
        for p in board:
            s=s+" "+p
        return(s)

class featureCalc(object):

    def syllableCount(self,word):      #returns count of syllables in word using CMU's dictionary, or none if token isn't a word
        word=word.lower()
        if word in CMUdict:
            return(len(CMUdict[word][0]))
        else:
            return(-1)
        
    def isComplex(self,word):        #Is word Complex
        if syllableCount(word) >=3:
            return True
        elif syllableCount(word)<0:
            return(None)
        else:
            return(False)

    def shortWordCount(self,sentence):
        tokens=wordTokenize(sentence)
        cnt=0
        for t in tokens:
            if len(t)<4:
                cnt=cnt+1
        return(cnt)
    def specialCharFreq(self,sentence):
        specialChar=['~','@','#','$','%','!','^','&','*','(',')','-','_','=','<','+','>','<','[','{','}',']','/','\\','|']
        cnt=0
        for s in specialChar:
            cnt=cnt+sentence.count(s)
        return(cnt)
        
    def posNGram(self,sentence,n):      #tokenized sentence
        posDic={}
        if n%2==1:                                  #odd POS
            for i in range(n-n//2-1,len(sentence)-n//2):
                posTuple=[]
                POS=posTag(sentence[i-n//2:i+n//2+1])
                for p in POS:
                    posTuple.append(p[1])
                posTuple=tuple(posTuple)
                if posTuple not in posDic:
                    posDic[posTuple]=0
                posDic[posTuple]=posDic[posTuple]+1
            return(posDic)
            
        else:                                           #even POS
            for i in range(len(sentence)-n+1):
                posTuple=[]
                POS=posTag(sentence[i:i+n])
                for p in POS:
                    posTuple.append(p[1])
                posTuple=tuple(posTuple)
                if posTuple not in posDic:
                    posDic[posTuple]=0
                posDic[posTuple]=posDic[posTuple]+1
            return(posDic)
            
#4CHAN
flag='4chan'
user=-1
text=22
path="pol.csv_2015-1"
dateStamp=4


split=1         # OR 6 for 6 months


#VOAT
path="politics.comment.csv"

text=1
user=0
flag='voat'
dateStamp=2


c=0

cleaner=preProcess()
stater=featureCalc()
path="askreddit_4.comment.csv"

text=1
user=0
flag='reddit'
dateStamp=5
c=0

allPosts={}
#text=row[22]
with open(path,'r', encoding="utf-8") as csvfile:   
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:    
        #print(datetime.fromtimestamp(int(row[dateStamp])))
        c=c+1
        #if c <100:
        content=""
        
        if flag=='4chan':
            content=cleaner.chanCleaner(row[text])          #post
            datekey=cleaner.chanDate(row[dateStamp],split)
        if flag=='voat':
            content=cleaner.voatCleaner(row[text])
            datekey=cleaner.voatDate(row[dateStamp],split)
        if flag=='reddit':
            content=cleaner.redditCleaner(row[text])
            datekey=cleaner.redditDate(row[dateStamp],split)
        
        if datekey not in allPosts:
            allPosts[datekey]=[]
        allPosts[datekey].append(content)
        print(datekey)
        
        
        
        #else:
        #break
       





#X='luuuuuvvv'









