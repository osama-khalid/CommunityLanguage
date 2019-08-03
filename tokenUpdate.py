##
##
##
##

##
## RENAME VARIABLE SPLIT
import pickle
#d[word.lower()] syllable
#https://docs.python.org/2/library/urllib.html#urllib.quote_plus        urlunqote
import collections
#from pycontractions import Contractions         #pip install
#https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
from LIWC import liwc
import textstat
import sklearn
import numpy as np
import nltk         #pip install
nltk.download('punkt')
nltk.download('words')
nltk.download('cmudict')
nltk.download('stopwords')
from nltk.corpus import stopwords
stopWords=set(stopwords.words('english'))
import threading
import os
import html
nltk.download('averaged_perceptron_tagger')
import contractions #pip install
from collections import Counter
from nltk.corpus import words             #check dictionary
from nltk import pos_tag as posTag
import emoji #pip install
import re                           #elongation
from autocorrect import spell    #pip install     #check spelling
from nltk.tokenize import sent_tokenize #sentence tokenizer         https://www.nltk.org/api/nltk.tokenize.html also see
import csv                              #read file
from datetime import datetime           #convert unix time to human time
from nltk.tokenize import RegexpTokenizer       #remove puncutations
from nltk import edit_distance as ed    #check word spelling correction distance
import urllib.request as urllib         #ud convert url to unicode
punctuations = RegexpTokenizer(r'\w+')
from nltk.corpus import cmudict
import math

CMUdict = cmudict.dict()      #syllable


class preProcess(object):
    
    def __init__(self):
        '''
        loads urban dictionary and emoji list
        '''
        self.ud=self.urbanLoad()
        self.emojiList=self.emojiLoad()
        
        
    def chanCleaner(self,post):          #clean 4archive posts
        '''
        cleans 4chan posts by removing the initial disclaimer
        '''
        
        return(post.replace('<marquee>[trigger warning]</marquee>','').replace('\\\n',' . ')[6:])

    def chanDate(self,D,split=1):
        '''
        standardizes 4chan date to
        YYYY-S
        where S = split
        if split =1 S will range from 0 to 11
        if split =6, S will range from 0 to 1
        '''
        date_object=datetime.fromtimestamp(int(D))
        return(str(date_object.year)+'-'+str((int(date_object.month)-1)//split))

    def voatCleaner(self,post):      #cleans voat posts
        '''
        cleans Voat posts by fixing escaped html
        '''
        return(html.unescape(post).replace('\n','. ').replace('&nbsp;','.'))
    
    def redditCleaner(self,post):      #cleans voat posts
        '''
        cleans reddit posts by converting newline to ".".
        This makes it easier for the sentence tokenizer
        '''
        return(post.replace('\n','. '))
    
    def voatDate(self,D,split=1):
        '''
        standardizes voat date to
        YYYY-S
        where S = split
        if split =1 S will range from 0 to 11
        if split =6, S will range from 0 to 1
        '''
        date_object=D.split(' ')[0].split('/')
        return(str(date_object[2])+'-'+str((int(date_object[0])-1)//split))
    
    def redditDate(self,D,split=1):
        '''
        standardizes reddit date to
        YYYY-S
        where S = split
        if split =1 S will range from 0 to 11
        if split =6, S will range from 0 to 1
        '''
        date_object=datetime.fromtimestamp(int(D))
        return(str(date_object.year)+'-'+str((int(date_object.month)-1)//split))
    
    def emojiLoad(self):
        '''
        loads emoji list
        '''
        emojiList=[]
        emojis=emoji.UNICODE_EMOJI
        for e in emojis:
            emojiList.append(e)
            
        return(emojiList)
    
    
    def urbanLoad(self,year=2019):
        '''
        loads urban dictionary in lowercase
        '''
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


    def hasElongation(self,text):
        '''
        returns True if word has a letter with 3 or more repetitions
        e.g. helllo
        False otherwise
        '''
        text=text+" "
        c=1
        maxC=1
        for i in range(1,len(text)):
            if text[i]==text[i-1]:
                c=c+1
            else:
                if c>maxC:
                    maxC=c
                c=1
        if maxC>=3:
            return(True)
        else:
            
            return(False)
        
            
    def wordOOV(self,word):           #Also for OOV Words
        '''
        return False if word is not OOV
        true otherwise
        Dictionaries   = words.word for standard english
                            = urban dictionary
                            = emoji List
        '''
        if word in words.words():         #if word in dictionary
            return(False)
        if word in self.ud:                      #if word in urbandictionary
            return(False)
        if word in self.emojiList:
            return(False)
        return(True)
    

    def spellCheck(self,word):
        '''
        returns True if spelling error
        False if no spelling error
        Does not correct word,
        Use autocorrect.spell to correct spelling
        limitation of Autocorrect.spell: Will map every word onto a potential word
        
        There's some logic behind this that I have now forgotten.
        Oh Right! autocorrect.spell treats no spelling error and out of vocab words the same
        e.g.
        apple=apple
        yoeyeyeohfifess=yoeyeyeohfifess
        but
        appple=apple
        
        '''
        norvigWord=spell(word)          #Norvig's 21 line spell check https://impythonist.wordpress.com/2014/03/18/peter-norvigs-21-line-spelling-corrector-using-probability-theory/
        if norvigWord==word:
            if wordOOV(norvigWord)==False:      #Not OOV
                return(False)             #No Spell Error
            else:
                return(True)               #Spell Error
                
        return(True)                      #Spelling Error
        
                
            
            
    def wordNormalizer(self,word):#      Does not convert i;ve to I have
        '''
        if a word has a elongation, removes elongation
        returns a word if it has a elongation (and is in the dictionary)
        or doesn't have a elongation (Can spell check later on)
        returns None, if the word might have a elongation, but the elongation
        is not in the dictionary
        '''
        if self.hasElongation(word)==False:
            return(word)
        
        word=word.lower()
        
        word1=reduceLengtheningSingle(word)
        
        word2=reduceLengthening(word)
        if word1==word:                     #No double letter
            return(wordOOV(word))
            
        if wordOOV(word2) == False:       #word with double letter is in dictionary
            return(wordOOV(word2))
        if wordOOV(word1) ==False:        #word with single letters is in dictionary          luuuuvvvv
            return(wordOOV(word1))

        else:
            return(None)

    def deContraction(self,word):
        '''
        Normalizes contractions (but doesn't work for all lower case)
        A better option would be pycontractions, but my current machine can't load the models
        '''
        return(contractions.fix(word))



    
    def sentenceTokenize(self,post):
        '''
        Returns list of sentences in Post
        and list of list of words   #To reduce compute cost
        '''
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

    def wordTokenize(self,sentence):
        '''
        #Returns list of words in sentence
        '''
        sentence=sentence.replace("'",'_')
        tempTokens = punctuations.tokenize(sentence)
        tokens=[]
        if len(tempTokens)>0:
            tokens=' '.join(tempTokens).replace('_',"'").lower().split(' ')
            
            return(tokens)
        else:
            return(None)


    def wordTokenizeCons(self,sentence):
        '''
        Conservative word Tokenizer
        Fixes Contractions before tokenizing
        
        '''
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
        '''
        flattens a list of sentences into a single sentence
        
        '''
        s=""
        for p in board:
            s=s+" "+p
        return(s)
def config(type):

    if type=='4chan':
        user=0
        text=22
        dateStamp=4
        
        label=-1
    if type=='voat':
        
        text=1
        user=0
        dateStamp=2
        label=6

    if type=='reddit':
        text=1
        user=0
        
        dateStamp=5
        label=6
    return([text,user,dateStamp,label])
        

class wordPreProcess:
    def wordCount(self,post,cleaner):
        sentenceBreak=cleaner.sentenceTokenize(post.lower())        #?
        wordCollection=cleaner.wordTokenize(cleaner.postFlatten(cleaner.sentenceTokenize(post.lower())[0]))
        wC=dict(Counter(wordCollection))

        return(wC)
        #return({'_words':dict(Counter(wordCollection)),'_sentence':len(sentenceBreak[0]),'_post':1})
    

split=1         # OR 6 for 6 months

cleaner=preProcess()

files=[]
social=['voat','4chan','reddit']


files=os.listdir('./DataDump/')
        
k=0
j=4
import copy
def helper(k,j):
#print(apple)
    for J in range(0,len(files)):
        if J%j==k:
            featureList=[]            #FeaturesList
            p=files[J]
            wordCollection=[]
            #fileWrite=open('./tokens/'+p+'.token.features','wb')
            
            print(p)
            #pDocs={}            #Pseudo documents
            featureSet={}
            
            #print(J%j==k,J,j,k)
            
            file=p.split('.')
            type=file[-3]
            prefix=p
            KK=0
            conf=config(type)
            with open('./DataDump/'+p,'r', encoding="utf-8") as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    KK=KK+1
               
                    if type=='4chan':
                        content=cleaner.chanCleaner(row[conf[0]])          #post
                    if type=='voat':
                        content=cleaner.voatCleaner(row[conf[0]])
                    if type=='reddit':
                        content=cleaner.redditCleaner(row[conf[0]])

                
                    
                    wordCollection.append(wordPreProcess().wordCount(content,cleaner))
                    
                    
            wordSum={}            
            for item in wordCollection:
                for w in item:
                    if w not in wordSum:
                        wordSum[w]=0
                    wordSum[w]=wordSum[w]+item[w]
                    
            wordSumDeep=copy.deepcopy(wordSum)        
            totSum=sum(wordSum.values())
            
            for w in wordSumDeep:
                wordSumDeep[w]=float(wordSumDeep[w])/float(totSum)
            
            diction={}
            diction[prefix]=wordSumDeep
            #print(features)
            outfile=open('./tokenNew/'+prefix+'.token','wb')
            pickle.dump(diction,outfile)
            outfile.close()
        
t0 = threading.Thread(target=helper,args=(0,100))  
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=(1,100))  
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=(2,100))  
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=(3,100))  
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=(4,100))  
t4.daemon =True
t4.start()

t5 = threading.Thread(target=helper,args=(5,100))  
t5.daemon =True
t5.start()

t6 = threading.Thread(target=helper,args=(6,100))  
t6.daemon =True
t6.start()

t7 = threading.Thread(target=helper,args=(7,100))  
t7.daemon =True
t7.start()

t8 = threading.Thread(target=helper,args=(8,100))  
t8.daemon =True
t8.start()

t9 = threading.Thread(target=helper,args=(9,100))  
t9.daemon =True
t9.start()

t10 = threading.Thread(target=helper,args=(10,100))  
t10.daemon =True
t10.start()

t11 = threading.Thread(target=helper,args=(11,100))  
t11.daemon =True
t11.start()

t12 = threading.Thread(target=helper,args=(12,100))  
t12.daemon =True
t12.start()

t13 = threading.Thread(target=helper,args=(13,100))  
t13.daemon =True
t13.start()

t14 = threading.Thread(target=helper,args=(14,100))  
t14.daemon =True
t14.start()

t15 = threading.Thread(target=helper,args=(15,100))  
t15.daemon =True
t15.start()

t16 = threading.Thread(target=helper,args=(16,100))  
t16.daemon =True
t16.start()

t17 = threading.Thread(target=helper,args=(17,100))  
t17.daemon =True
t17.start()

t18 = threading.Thread(target=helper,args=(18,100))  
t18.daemon =True
t18.start()

t19 = threading.Thread(target=helper,args=(19,100))  
t19.daemon =True
t19.start()

t20 = threading.Thread(target=helper,args=(20,100))  
t20.daemon =True
t20.start()

t21 = threading.Thread(target=helper,args=(21,100))  
t21.daemon =True
t21.start()

t22 = threading.Thread(target=helper,args=(22,100))  
t22.daemon =True
t22.start()

t23 = threading.Thread(target=helper,args=(23,100))  
t23.daemon =True
t23.start()

t24 = threading.Thread(target=helper,args=(24,100))  
t24.daemon =True
t24.start()

t25 = threading.Thread(target=helper,args=(25,100))  
t25.daemon =True
t25.start()

t26 = threading.Thread(target=helper,args=(26,100))  
t26.daemon =True
t26.start()

t27 = threading.Thread(target=helper,args=(27,100))  
t27.daemon =True
t27.start()

t28 = threading.Thread(target=helper,args=(28,100))  
t28.daemon =True
t28.start()

t29 = threading.Thread(target=helper,args=(29,100))  
t29.daemon =True
t29.start()

t30 = threading.Thread(target=helper,args=(30,100))  
t30.daemon =True
t30.start()

t31 = threading.Thread(target=helper,args=(31,100))  
t31.daemon =True
t31.start()

t32 = threading.Thread(target=helper,args=(32,100))  
t32.daemon =True
t32.start()

t33 = threading.Thread(target=helper,args=(33,100))  
t33.daemon =True
t33.start()

t34 = threading.Thread(target=helper,args=(34,100))  
t34.daemon =True
t34.start()

t35 = threading.Thread(target=helper,args=(35,100))  
t35.daemon =True
t35.start()

t36 = threading.Thread(target=helper,args=(36,100))  
t36.daemon =True
t36.start()

t37 = threading.Thread(target=helper,args=(37,100))  
t37.daemon =True
t37.start()

t38 = threading.Thread(target=helper,args=(38,100))  
t38.daemon =True
t38.start()

t39 = threading.Thread(target=helper,args=(39,100))  
t39.daemon =True
t39.start()

t40 = threading.Thread(target=helper,args=(40,100))  
t40.daemon =True
t40.start()

t41 = threading.Thread(target=helper,args=(41,100))  
t41.daemon =True
t41.start()

t42 = threading.Thread(target=helper,args=(42,100))  
t42.daemon =True
t42.start()

t43 = threading.Thread(target=helper,args=(43,100))  
t43.daemon =True
t43.start()

t44 = threading.Thread(target=helper,args=(44,100))  
t44.daemon =True
t44.start()

t45 = threading.Thread(target=helper,args=(45,100))  
t45.daemon =True
t45.start()

t46 = threading.Thread(target=helper,args=(46,100))  
t46.daemon =True
t46.start()

t47 = threading.Thread(target=helper,args=(47,100))  
t47.daemon =True
t47.start()

t48 = threading.Thread(target=helper,args=(48,100))  
t48.daemon =True
t48.start()

t49 = threading.Thread(target=helper,args=(49,100))  
t49.daemon =True
t49.start()

t50 = threading.Thread(target=helper,args=(50,100))  
t50.daemon =True
t50.start()

t51 = threading.Thread(target=helper,args=(51,100))  
t51.daemon =True
t51.start()

t52 = threading.Thread(target=helper,args=(52,100))  
t52.daemon =True
t52.start()

t53 = threading.Thread(target=helper,args=(53,100))  
t53.daemon =True
t53.start()

t54 = threading.Thread(target=helper,args=(54,100))  
t54.daemon =True
t54.start()

t55 = threading.Thread(target=helper,args=(55,100))  
t55.daemon =True
t55.start()

t56 = threading.Thread(target=helper,args=(56,100))  
t56.daemon =True
t56.start()

t57 = threading.Thread(target=helper,args=(57,100))  
t57.daemon =True
t57.start()

t58 = threading.Thread(target=helper,args=(58,100))  
t58.daemon =True
t58.start()

t59 = threading.Thread(target=helper,args=(59,100))  
t59.daemon =True
t59.start()


t60 = threading.Thread(target=helper,args=(60,100))  
t60.daemon =True
t60.start()

t61 = threading.Thread(target=helper,args=(61,100))  
t61.daemon =True
t61.start()

t62 = threading.Thread(target=helper,args=(62,100))  
t62.daemon =True
t62.start()

t63 = threading.Thread(target=helper,args=(63,100))  
t63.daemon =True
t63.start()

t64 = threading.Thread(target=helper,args=(64,100))  
t64.daemon =True
t64.start()

t65 = threading.Thread(target=helper,args=(65,100))  
t65.daemon =True
t65.start()

t66 = threading.Thread(target=helper,args=(66,100))  
t66.daemon =True
t66.start()

t67 = threading.Thread(target=helper,args=(67,100))  
t67.daemon =True
t67.start()

t68 = threading.Thread(target=helper,args=(68,100))  
t68.daemon =True
t68.start()

t69 = threading.Thread(target=helper,args=(69,100))  
t69.daemon =True
t69.start()


t70 = threading.Thread(target=helper,args=(70,100))  
t70.daemon =True
t70.start()

t71 = threading.Thread(target=helper,args=(71,100))  
t71.daemon =True
t71.start()

t72 = threading.Thread(target=helper,args=(72,100))  
t72.daemon =True
t72.start()

t73 = threading.Thread(target=helper,args=(73,100))  
t73.daemon =True
t73.start()

t74 = threading.Thread(target=helper,args=(74,100))  
t74.daemon =True
t74.start()

t75 = threading.Thread(target=helper,args=(75,100))  
t75.daemon =True
t75.start()

t76 = threading.Thread(target=helper,args=(76,100))  
t76.daemon =True
t76.start()

t77 = threading.Thread(target=helper,args=(77,100))  
t77.daemon =True
t77.start()

t78 = threading.Thread(target=helper,args=(78,100))  
t78.daemon =True
t78.start()

t79 = threading.Thread(target=helper,args=(79,100))  
t79.daemon =True
t79.start()

t80 = threading.Thread(target=helper,args=(80,100))  
t80.daemon =True
t80.start()

t81 = threading.Thread(target=helper,args=(81,100))  
t81.daemon =True
t81.start()

t82 = threading.Thread(target=helper,args=(82,100))  
t82.daemon =True
t82.start()

t83 = threading.Thread(target=helper,args=(83,100))  
t83.daemon =True
t83.start()

t84 = threading.Thread(target=helper,args=(84,100))  
t84.daemon =True
t84.start()

t85 = threading.Thread(target=helper,args=(85,100))  
t85.daemon =True
t85.start()

t86 = threading.Thread(target=helper,args=(86,100))  
t86.daemon =True
t86.start()

t87 = threading.Thread(target=helper,args=(87,100))  
t87.daemon =True
t87.start()

t88 = threading.Thread(target=helper,args=(88,100))  
t88.daemon =True
t88.start()

t89 = threading.Thread(target=helper,args=(89,100))  
t89.daemon =True
t89.start()

t90 = threading.Thread(target=helper,args=(90,100))  
t90.daemon =True
t90.start()

t91 = threading.Thread(target=helper,args=(91,100))  
t91.daemon =True
t91.start()

t92 = threading.Thread(target=helper,args=(92,100))  
t92.daemon =True
t92.start()

t93 = threading.Thread(target=helper,args=(93,100))  
t93.daemon =True
t93.start()

t94 = threading.Thread(target=helper,args=(94,100))  
t94.daemon =True
t94.start()

t95 = threading.Thread(target=helper,args=(95,100))  
t95.daemon =True
t95.start()

t96 = threading.Thread(target=helper,args=(96,100))  
t96.daemon =True
t96.start()

t97 = threading.Thread(target=helper,args=(97,100))  
t97.daemon =True
t97.start()

t98 = threading.Thread(target=helper,args=(98,100))  
t98.daemon =True
t98.start()

t99 = threading.Thread(target=helper,args=(99,100))  
t99.daemon =True
t99.start()


a=t0.join()
a=t1.join()
a=t2.join()
a=t3.join()
a=t4.join()	
a=t5.join()	      

a=t6.join()
a=t7.join()
a=t8.join()
a=t9.join()
a=t10.join()

a=t11.join()
a=t12.join()
a=t13.join()
a=t14.join()	
a=t15.join()	      

a=t16.join()
a=t17.join()
a=t18.join()
a=t19.join()

a=t20.join()
a=t21.join()
a=t22.join()
a=t23.join()
a=t24.join()	
a=t25.join()	      

a=t26.join()
a=t27.join()
a=t28.join()
a=t29.join()

a=t30.join()
a=t31.join()
a=t32.join()
a=t33.join()
a=t34.join()	
a=t35.join()	      

a=t36.join()
a=t37.join()
a=t38.join()
a=t39.join()


a=t40.join()
a=t41.join()
a=t42.join()
a=t43.join()
a=t44.join()	
a=t45.join()	      

a=t46.join()
a=t47.join()
a=t48.join()
a=t49.join()


a=t50.join()
a=t51.join()
a=t52.join()
a=t53.join()
a=t54.join()	
a=t55.join()	      

a=t56.join()
a=t57.join()
a=t58.join()
a=t59.join()


a=t60.join()
a=t61.join()
a=t62.join()
a=t63.join()
a=t64.join()	
a=t65.join()	      

a=t66.join()
a=t67.join()
a=t68.join()
a=t69.join()

a=t70.join()
a=t71.join()
a=t72.join()
a=t73.join()
a=t74.join()	
a=t75.join()	      

a=t76.join()
a=t77.join()
a=t78.join()
a=t79.join()


a=t80.join()
a=t81.join()
a=t82.join()
a=t83.join()
a=t84.join()	
a=t85.join()	      

a=t86.join()
a=t87.join()
a=t88.join()
a=t89.join()


a=t90.join()
a=t91.join()
a=t92.join()
a=t93.join()
a=t94.join()	
a=t95.join()	      

a=t96.join()
a=t97.join()
a=t98.join()
a=t99.join()



        
