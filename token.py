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
            tokens=' '.join(tempTokens).replace('_',"'").split(' ')
            
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

cleaner=preProcess()


features=featureCalc()

def helper(k,j):
#print(apple)
    for J in range(0,len(files)):
        if J%j==k:
            featureList=[]            #FeaturesList
            p=files[J]
            fileWrite=open(p+'.features','wb')
            
            print(p)
            #pDocs={}            #Pseudo documents
            featureSet={}
            
            #print(J%j==k,J,j,k)
            
            file=p.split('.')
            type=file[1]
            KK=0
            conf=config(type)
            with open('./'+type+'/'+p,'r', encoding="utf-8") as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    KK=KK+1
                    if KK<10000:
                        if type=='4chan':
                            content=cleaner.chanCleaner(row[conf[0]])          #post
                        if type=='voat':
                            content=cleaner.voatCleaner(row[conf[0]])
                        if type=='reddit':
                            content=cleaner.redditCleaner(row[conf[0]])
    
                    
                    
                        
                        label=file[3]+'.'+type+'.'+row[conf[3]]
                        
                        featureSet[label]=featureSet[label]+' . '+content
                        
            features={}
            for l in featureSet:
                feat=cleaner.wordTokenize(featureSet[l])
                features[l]=collections.Counter(feat)
                
            pickle.dump(features,fileWrite)
            fileWrite.close()
            