#d[word.lower()] syllable
#https://docs.python.org/2/library/urllib.html#urllib.quote_plus        urlunqote
    
#from pycontractions import Contractions         #pip install
#https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python

from LIWC import liwc
import operator
import sklearn
import numpy as np
import nltk         #pip install    
nltk.download('punkt')
nltk.download('words')
nltk.download('cmudict')

import os
import html
import copy
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
import collections
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
    
    def wordUB(self,word):
        if word not in words.words() and word in self.ud:
            return(True)
        else:
            return(False)
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
            if self.wordOOV(norvigWord)==False:      #Not OOV
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
            for t in tempTokens:
                
                tokens.append(t.replace("_","'"))
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
            
class charAggr:
    '''
    Character Level Feature Calculations
    '''
    def __init__(self,post,cleaner):
        specialChar=self._specialChar(post)
        totChar=self._totChar(post)
        whiteSpace=self._whiteSpace(post)
        digits=self._digits(post)
        tabs=self._tabs(post)
        upper=self._upper(post)
        alphabet=self._alphabet(post)
        lines=self._lines(post)
        punctuations=self._punctuations(post)
        charWord=self._charWord(post,cleaner)
        self.stats={'specialChar':specialChar,'totChar':totChar,'whiteSpace':whiteSpace,'digits':digits,'tabs':tabs,'upper':upper,'alphabet':alphabet,'lines':lines,'punctuations':punctuations,'charWord':charWord}
        
    def _totChar(self,post):
        return(len(post))
    
    def _specialChar(self,post):
        specialChar=['~','@','#','$','%','!','^','&','*','(',')','-','_','=','<','+','>','<','[','{','}',']','/','\\','|']
        cnt=0
        for s in specialChar:
            cnt=cnt+post.count(s)
        return(cnt)
    
    def _whiteSpace(self,post):
        totChar=len(post)
        totNoSpace=len(post.replace(' ',''))
        totSpace=totChar-totNoSpace
        return(totSpace)
    def _digits(self,post):
        totChar=len(post)
        NoDigit=post
        for i in range(0,10):
            NoDigit=NoDigit.replace(str(i),'')
            
        totNoDigit=len(NoDigit)
        totDigit=totChar-totNoDigit
        return(totDigit)
    
    def _tabs(self,post):
        totChar=len(post)
        NoTab=post.replace('\t','')
        TabLen=totChar-len(NoTab)
        return(TabLen)
    
    def _upper(self,post):
        '''
        No. of upper case/char
        '''
        totChar=len(post)
        NoUpper=post
        for i in range(65,91):#ASCII A to Z
            NoUpper=NoUpper.replace(chr(i),'')
        
        
            
        totNoUpper=len(NoUpper)
        Upper=totChar-totNoUpper
        
        return(Upper)
    
    def _alphabet(self,post):
        '''
        No. Alphabets/char
        '''
        
        
        return(self._upper(post.upper()))
    
    
    def _lines(self,post):
        totChar=len(post)
        NoLine=len(post.replace('\n',''))
        return(totChar-NoLine)
        
        
    def _punctuations(self,post):
        punctuations=['.',',',';',':','!','?',"'",'"','-']
        
        NoPunc=post
        for item in punctuations:
            NoPunc=NoPunc.replace(item,'')
        return(len(post)-len(NoPunc))
    def _charWord(self,post,cleaner):
        return(len(''.join(cleaner.wordTokenize(post))))

class wordPreProcess:
    def wordCount(self,post,cleaner):
        sentenceBreak=cleaner.sentenceTokenize(post.lower())        #?
        wordCollection=cleaner.wordTokenize(cleaner.postFlatten(cleaner.sentenceTokenize(post.lower())[0]))
        wC=dict(Counter(wordCollection))
        wC['_sentence']=len(sentenceBreak[0])
        wC['_post']=1
        return(wC)
        #return({'_words':dict(Counter(wordCollection)),'_sentence':len(sentenceBreak[0]),'_post':1})
    
class LIWCPreProcess:
    def liwcCount(self,post,cleaner):
        words=' '.join(cleaner.wordTokenize(post))
        
        
        return(liwc().getLIWCCount(words))
class wordFeatures:
    def __init__(self,wordDict):
        self._syllables=self._syllable(wordDict)
        self._syllableCount=self._syllables[0]
        self._syllableWords=self._syllables[1]
        self._shortWordCount=self._shortWord(wordDict)
        
        honore=self._honore(wordDict)
        sichel=self._sichel(wordDict)
        brunet=self._brunet(wordDict)
        fkGrade=self._fleschKincaidGrade(wordDict)
        fkReadability=self._fleschKincaidReadability(wordDict)
        hapaxDislegomena=self._hapaxDislegomena(wordDict)
        hapaxLegomena=self._hapaxLegomena(wordDict)
        gunningFog=self._gunningFog(wordDict)
        ARI=self._ARI(wordDict)
        DCR=self._DCR(wordDict)
        SMOG=self._SMOG(wordDict)
        simpson=self._simpson(wordDict)
        CLI=self._CLI(wordDict)
        yule=self._yule(wordDict)
        self.stats={'syllablePerWord':float(self._syllableCount)/float(self._syllableWords),'syllablePerSentence':float(self._syllableCount)/float(wordDict['_sentence']),'syllablePerPost':float(self._syllableCount)/float(wordDict['_post']),'shortPerWord':float(self._shortWordCount)/float(sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']),'shortPerSentence':float(self._shortWordCount)/float(wordDict['_sentence']),'shortPerPost':float(self._shortWordCount)/float(wordDict['_post']),'honore':honore,'sichel':sichel,'brunet':brunet,'fleschKincaidGrade':fkGrade,'fleschKincaidReadability':fkReadability,'hapaxDislegomenaFreq':hapaxDislegomena/float(sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']),'hapaxLegomenaFreq':hapaxLegomena/float(sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']),'gunningFog':gunningFog,'ARI':ARI,'DCR':DCR,'SMOG':SMOG,'simpson':simpson,'CLI':CLI,'yule':yule}
        
      
    def syllableCount(self,word):      #returns count of syllables in word using CMU's dictionary, or none if token isn't a word
        '''
        Counts the number of syllable in a given word
        '''
        if word==-1:
            return('syllabeCount')
        word=word.lower()
        if word in CMUdict:
            return[len([y for y in x if y[-1].isdigit()]) for x in CMUdict[word.lower()]][0]
            #return(len(CMUdict[word][0]))
        else:
            return(-1)
        
    def isComplex(self,word):        #Is word Complex
        '''
        Returns True if word is complex
        i.e. syllable count >3
        
        '''
        if word==-1:
            return('isComplex')
        if self.syllableCount(word) >=3:
            return True
        elif self.syllableCount(word)<0:
            return(None)
        else:
            return(False)
        
        
    def _syllable(self,wordDict):
        wordList=wordDict.keys()
        syllableCount={}
        for w in wordList:
            if w !='_post' and w!='_sentence':
                cnt=self.syllableCount(w)
                if cnt>-1:
                    syllableCount[w]=cnt
        for s in syllableCount:
            syllableCount[s]=syllableCount[s]*wordDict[s]
            
        return(sum(syllableCount.values()),sum(wordDict.values()))
    
    def _shortWord(self,wordDict):
        wordList=wordDict.keys()
        shortWordCount={}
        for w in wordList:
            if w!='_post' and w!='_sentence':
                if len(w)<4:
                    shortWordCount[w]=wordDict[w]
        return(sum(shortWordCount.values()))            
    
    
    def _honore(self,wordDict):
        singles=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                if wordDict[w]==1:
                    singles=singles+1
        try:
            R=100*math.log10(sum(wordDict.values())-wordDict['_post']-wordDict['_sentence'])/(1-(singles/(len(wordDict)-2)))
        except:
            R=0
        return(R)
    def _sichel(self,wordDict):
        doubles=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                if wordDict[w]==2:
                    doubles=doubles+1
        S=doubles/(len(wordDict)-2)
        return(S)
    '''
    Numerical OverFlow
    '''
    def _brunet(self,wordDict):
        intermed=(len(wordDict)-2)**-0.165
        W=(sum(wordDict.values())-wordDict['_post']-wordDict['_sentence'])**intermed
        return(W)
    
    def _yule(self,wordDict):
        wordDictNew=copy.deepcopy(wordDict)
        del wordDictNew['_sentence']
        del wordDictNew['_post']
        N=sum(wordDictNew.values())#no of words
        freqs=list(wordDictNew.values())
        Vi=dict(collections.Counter(freqs))       #Words Occuring i times
        M=0
        for v in Vi:
            M=M+(v**2)*Vi[v]
        K=1000*(M-N)/(N**2)
        return(K)
        
    def _fleschKincaidReadability(self,wordDict):        #Flesch Kincaid is negative?
        #https://www.verblio.com/blog/flesch-reading-ease is low scores = low readability
        totSyllable=self._syllableCount
        totWords=sum(wordDict.values())-wordDict['_post']-wordDict['_sentence']
        totSentences=wordDict['_sentence']
        FK=206.835-1.015*(totWords/totSentences)-84.6*(totSyllable/totWords)
        return(FK)
        
    def _fleschKincaidGrade(self,wordDict):        #Harder to be negative?
        #https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#cite_note-10
        totSyllable=self._syllableCount
        totWords=sum(wordDict.values())-wordDict['_post']-wordDict['_sentence']
        totSentences=wordDict['_sentence']
        FK=0.39*(totWords/totSentences)+11.8*(totSyllable/totWords)-15.59
        return(FK)
        
    def _hapaxDislegomena(self,wordDict):
        count=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                if wordDict[w]==2:
                    count=count+1
        return(count)
    
    def _hapaxLegomena(self,wordDict):
        count=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                if wordDict[w]==1:
                    count=count+1
        return(count)     
    def _gunningFog(self,wordDict):
        
        sentences=wordDict['_sentence']
        words=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        complexWords=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                
                if self.isComplex(w)==True:
                    complexWords=complexWords+wordDict[w]
                    
        gunningFog=0.4*((words/sentences)+100*(complexWords/words))
        return(gunningFog)
    def _ARI(self,wordDict):
        #Automated Readability Index
        char=0
        sentences=wordDict['_sentence']
        words=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                char=char+len(w)*wordDict[w]
        #print(char,words,sentences)        
        ARI=4.71*(float(char)/float(words))+0.5*(words/sentences)-21.43
        return(ARI)
        
    def _DCR(self,wordDict):
        '''
        DaleChallReadability
        '''
        sentences=wordDict['_sentence']
        words=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        complexWords=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                if self.isComplex(w)==True:
                    complexWords=complexWords+wordDict[w]
                    
        DCR=0.1579*(100*(complexWords/words))+0.0496*(words/sentences)
        return(DCR)
    def _SMOG(self,wordDict):
        sentences=wordDict['_sentence']
        words=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        complexWords=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                if self.isComplex(w)==True:
                    complexWords=complexWords+wordDict[w]
        smog=1.0430*math.sqrt(complexWords*(30/sentences))+3.1291
        return(smog)
    def _simpson(self,wordDict):
        words=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        denom=words*(words-1)
        numer=0
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                numer=numer+wordDict[w]*(wordDict[w]-1)
                
        D=1-(numer/denom)
        return(D)
    def _CLI(self,wordDict):
        char=0
        sentences=wordDict['_sentence']
        words=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        for w in wordDict:
            if w!='_post' and w!='_sentence':
                char=char+len(w)*wordDict[w]
        L=100*char/words
        S=100*sentences/words
        CLI=0.0588*L-0.296*S-15.8
        return(CLI)
    
class OOVs:    
    #What to do with Punctuations? "that's"
    def __init__(self,wordSum,cleaner):
        wordDict=copy.deepcopy(wordSum)
        self.cleaner=cleaner
        wordDict['_sentence']=0
        wordDict['_post']=0
        self.tf=sorted(wordDict.items(),key=operator.itemgetter(1),reverse=True)
        self.OOVlist=set(words.words()).union(set(cleaner.ud)).union(set(cleaner.emojiList))
        oov100=self.OOV100()
        oov500=self.OOV500()
        oov200=self.OOV200()
        oov1000=self.OOV1000()
        oov5000=self.OOV5000()
        self.stats={'oov100':oov100,'oov200':oov200,'oov500':oov500,'oov1000':oov1000,'oov5000':oov5000}
        
    def OOV100(self):
        oovs=0
        w=[]
        tf=self.tf[:100]
        for t in tf:
            w.append(t[0])
        oovs=len(w)-len(set(w).intersection(self.OOVlist))
        
        return(oovs)
        
    def OOV500(self):
        oovs=0
        w=[]
        tf=self.tf[:500]
        for t in tf:
            w.append(t[0])
        oovs=len(w)-len(set(w).intersection(self.OOVlist))
        
        return(oovs)
    def OOV200(self):
        tf=self.tf[:200]
        w=[]
        for t in tf:
            w.append(t[0])
        oovs=len(w)-len(set(w).intersection(self.OOVlist))
        
        return(oovs)      
    def OOV1000(self):
        tf=self.tf[:1000]
        w=[]
        for t in tf:
            w.append(t[0])
        oovs=len(w)-len(set(w).intersection(self.OOVlist))
        
        return(oovs)      
    def OOV5000(self):
        tf=self.tf[:5000]
        w=[]
        for t in tf:
            w.append(t[0])
        oovs=len(w)-len(set(w).intersection(self.OOVlist))
        
        return(oovs)              
    '''
    def UB100(self):
        ubs=0
        tf=self.tf[:100]
        w=[]
        for t in tf:
            w.append(t[0])
        ubs=len(w)-len(set(words.words()).intersection(set(w).intersection(self.cleaner.ud)))
        return(ubs)
    def UB500(self):
        ubs=0
        tf=self.tf[:500]
        w=[]
        for t in tf:
            w.append(t[0])
        ubs=len(w)-len(set(words.words()).intersection(set(w).intersection(self.cleaner.ud)))
        return(ubs)        
    def UB200(self):
        ubs=0
        tf=self.tf[:200]
        w=[]
        for t in tf:
            w.append(t[0])
        ubs=len(w)-len(set(words.words()).intersection(set(w).intersection(self.cleaner.ud)))
        return(ubs)        
    
    def OOVfreq(self,wordDict):
        oovFreq=0
        words=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        for w in wordDict:
            if w !='_sentence' and w!='_post':
                if self.cleaner.wordOOV(w)==True:
                    oovFreq=oovFreq+wordDict[w]
        return(oovFreq/float(words))
    '''            
class posAggr:
    
    def posNGram(self,sentence,n=2):      #tokenized sentence       #sentenceTokenize[1]
        '''
            No. POS NGrams          https://cs.nyu.edu/grishman/jet/guide/PennPOS.html
        '''
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
    
    def stats(self,post,cleaner):
        sentences=cleaner.sentenceTokenize(post)[1]
        trigram={}
        unigram={}
        for item in sentences:
            tempDictionary=self.posNGram(item)
            for t in tempDictionary:
                if t not in trigram:
                    trigram[t]=0
                trigram[t]=trigram[t]+tempDictionary[t]
                
            tempDictionary=self.posNGram(item,1)
            for t in tempDictionary:
                if t not in unigram:
                    unigram[t]=0
                unigram[t]=unigram[t]+tempDictionary[t]
        Uni=sum(unigram.values())
        Tri=sum(trigram.values())
        #sums={'unigram':Uni,'ngram':Tri}
        
        #return({**trigram,**unigram,**sums})
        
        sums={'unigram':Uni}
        return({**unigram,**sums})

'''
Slows down the calcuations a bit
'''
class neologism:        
    def __init__(self,wordDict,cleaner):
        self.cleaner=cleaner
        
        
        #spellError=self.spellingError(wordDict)
        spellError=0
        elongation=self.elongation(wordDict)
        
        
        wordCount=sum(wordDict.values())-wordDict['_sentence']-wordDict['_post']
        self.stats={'elongationCount':elongation,'wordCount':wordCount}
        
        
    
    def elongation(self,wordDict):
        elongCount=0
        for w in wordDict:
            if w!='_sentence' and w!='_post':
                if self.cleaner.hasElongation(w)==True:
                    elongCount=elongCount+wordDict[w]
        return(elongCount)
    
    
        
cleaner=preProcess()

class emojiCount:
    def count(self,post):
        emoji=len(str(post.encode('utf-8')).split('\\xf0'))-1
        return(emoji)
        
    
socialMedia=['voat','4chan','reddit']
files=['politics.reddit.2.2017-0']

import os

import pickle
def fileWrite(p):
    r=0
    P=p
    file=p.split('.')
    type=file[1]
    conf=config(type)
    #print(p)
    wordCollection=[]
    wordStat=[]
    posStat=[]
    charStat=[]
    liwcStat=[]
    neoStat=[]
    emojiStat=[]
    #with open('./'+type+'/'+p,'r', encoding="utf-8") as csvfile:
    with open('./DataDump/'+p,'r',encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        
        for row in readCSV:
            r=r+1
            if r%50==0:
            
                print(p,'\t',r)
            if type=='4chan':
                content=cleaner.chanCleaner(row[conf[0]])
            if type=='voat':
                content=cleaner.voatCleaner(row[conf[0]])
            if type=='reddit':
                content=cleaner.redditCleaner(row[conf[0]])
            
                #wordCollection.append(wordPreprocess(content))
            if cleaner.wordTokenize(content) is not None:                
                A=charAggr(content,cleaner)
                charStat.append(A.stats)
                emojiStat.append(emojiCount().count(content))
               
                wordCollection.append(wordPreProcess().wordCount(content,cleaner))
                
                posStat.append(posAggr().stats(content,cleaner))
                liwcStat.append(LIWCPreProcess().liwcCount(content,cleaner))

            #posAggr(content)
            #posStat.append(posAggr.stats)
            
    wordSum={}
    charFeat={}
    liwcFeat={}
    wordFeat={}
    OOVFeat={}
    posFeat={}
    #print('First Pass')
    

    for item in wordCollection:
        for w in item:
            if w not in wordSum:
                wordSum[w]=0
            wordSum[w]=wordSum[w]+item[w]
    wordSumNew=copy.deepcopy(wordSum)
    for item in charStat:
        for w in item:
            if w not in charFeat:
                charFeat[w]=0
            charFeat[w]=charFeat[w]+item[w]
            
    for item in liwcStat:
        for w in item:
            if w not in liwcFeat:
                liwcFeat[w]=0
            liwcFeat[w]=liwcFeat[w]+item[w]
            
    for item in posStat:
        for subitem in item:
            if subitem not in posFeat:
                posFeat[subitem]=0
            posFeat[subitem]=posFeat[subitem]+item[subitem]
    wordFeat=wordFeatures(wordSum).stats
    
    neoFeat=neologism(wordSum,cleaner).stats
    emojiFeat=sum(emojiStat)
    
    #
    OOVFeat=OOVs(wordSum,cleaner).stats
    #
    emojiPerSentence={'emojiPerSentence':float(emojiFeat)/float(wordSumNew['_sentence'])}
    #
    emojiPerPost={'emojiPerPost':float(emojiFeat)/float(wordSumNew['_post'])}
    #
    emojiPerWord={'emojiPerWord':float(emojiFeat)/float(sum(wordSumNew.values())-wordSumNew['_sentence']-wordSumNew['_post'])}
    #
    emojProp=float(emojiFeat)/charFeat['totChar']
    emojiProportion={'emojiProportion':emojProp}
    #
    liwcSentence=copy.deepcopy(liwcFeat)
    del liwcSentence['WC']

    for l in liwcSentence:
        liwcSentence[l]=float(liwcSentence[l])/wordSumNew['_sentence']
    #   
    liwcPost=copy.deepcopy(liwcFeat)
    del liwcPost['WC']
    for l in liwcPost:
        liwcPost[l]=float(liwcPost[l]/wordSumNew['_post'])
    #
    liwcWord=copy.deepcopy(liwcFeat)
    totWord=liwcWord['WC']
    
    del liwcWord['WC']
    for l in liwcWord:
        liwcWord[l]=liwcWord[l]/float(totWord)
    
    
    charPost=copy.deepcopy(charFeat)

    for c in charPost:
        charPost[c]=charPost[c]/wordSumNew['_post']
    
    charSentence=copy.deepcopy(charFeat)
    
    for c in charSentence:
        charSentence[c]=charSentence[c]/wordSumNew['_sentence']
        
    charWord=copy.deepcopy(charFeat)
    
    for c in charWord:
        charWord[c]=charWord[c]/float(sum(wordSumNew.values())-wordSumNew['_sentence']-wordSumNew['_post'])
        
    charProp=copy.deepcopy(charFeat)
    totChars=charProp['totChar']
    
    del charProp['totChar']
    
    for c in charProp:
        charProp[c]=charProp[c]/totChars
        
    #
    elongWord={'elongationProportion':neoFeat['elongationCount']/neoFeat['wordCount']}
    #
    elongSentence={'elongationPerSentence':neoFeat['elongationCount']/wordSumNew['_sentence']}
    #
    elongPost={'elongationPerPost':neoFeat['elongationCount']/wordSumNew['_post']}
   
    posWords=copy.deepcopy(posFeat)
    posUni=posWords['unigram']
    
    #posNgram=posWords['ngram']
    del posWords['unigram']
    #del posWords['ngram']
    
    for f in posWords:
        if len(f)>1:
            posWords[f]=posWords[f]/posNgram
            
        else:
            posWords[f]=posWords[f]/posUni
            
    posSentence=copy.deepcopy(posFeat)
    del posSentence['unigram']
    #del posSentence['ngram']
    
    for p in posSentence:
        posSentence[p]=posSentence[p]/wordSumNew['_sentence']
        
    
    
    
    posPost=copy.deepcopy(posFeat)
    
    del posPost['unigram']
    #del posPost['ngram']
    
    for p in posPost:
        posPost[p]=posPost[p]/wordSumNew['_post']
    
    
    
    posPost2={}
    for p in posPost:
        posPost2[p[0]+'_post']=posPost[p]
        
    posSentence2={}
    for p in posSentence:
        posSentence2[p[0]+'_sentence']=posSentence[p]
        
    posWords2={}
    for p in posWords:
        posWords2[p[0]+'_word']=posWords[p]
        
    liwcSentence2={}
    
    for l in liwcSentence:
        liwcSentence2[l+'_sentence']=liwcSentence[l]
        
    
    liwcWord2={}
    
    for l in liwcWord:
        liwcWord2[l+'_word']=liwcWord[l]
        
    liwcPost2={}
    
    for l in liwcPost:
        liwcPost2[l+'_post']=liwcPost[l]
            
    
    charProp2={}
    
    for l in charProp:
        charProp2[l+'_prop']=charProp[l]
            
    charWord2={}
    
    for l in charWord:
        charWord2[l+'_word']=charWord[l]    
        
    charSentence2={}
    
    for l in charSentence:
        charSentence2[l+'_sentence']=charSentence[l]        
        
    charPost2={}
    
    for l in charPost:
        charPost2[l+'_prop']=charPost[l]        
   
    features={**OOVFeat,**emojiProportion,**emojiPerWord,**emojiPerSentence,**emojiPerPost,**liwcWord2,**liwcSentence2,**liwcPost2,**charProp2,**charWord2,**charSentence2,**charPost2,**elongWord,**elongSentence,**elongPost,**posWords2,**posSentence2,**posPost2,**wordFeat}
    
    
    #specialChar
    
    
    output={P:features}
    outfile=open('./pickled/'+P+'.pickle','wb')
    pickle.dump(output,outfile)
    outfile.close()
    
#fileWrite('politics.reddit.0.2014-5')    


import threading

def helper(files,k,j):
    C=0
    for f in files:
        if C%j==k:
            print(f,k)
            fileWrite(f)
            
        C=C+1

files=os.listdir('./DataDump/')
t0 = threading.Thread(target=helper,args=(files,0,50))
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=(files,1,50))
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=(files,2,50))
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=(files,3,50))
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=(files,4,50))
t4.daemon =True
t4.start()

t5 = threading.Thread(target=helper,args=(files,5,50))
t5.daemon =True
t5.start()

t6 = threading.Thread(target=helper,args=(files,6,50))
t6.daemon =True
t6.start()

t7 = threading.Thread(target=helper,args=(files,7,50))
t7.daemon =True
t7.start()

t8 = threading.Thread(target=helper,args=(files,8,50))
t8.daemon =True
t8.start()

t9 = threading.Thread(target=helper,args=(files,9,50))
t9.daemon =True
t9.start()

t10 = threading.Thread(target=helper,args=(files,10,50))
t10.daemon =True
t10.start()

t11 = threading.Thread(target=helper,args=(files,11,50))
t11.daemon =True
t11.start()

t12 = threading.Thread(target=helper,args=(files,12,50))
t12.daemon =True
t12.start()

t13 = threading.Thread(target=helper,args=(files,13,50))
t13.daemon =True
t13.start()

t14 = threading.Thread(target=helper,args=(files,14,50))
t14.daemon =True
t14.start()

t15 = threading.Thread(target=helper,args=(files,15,50))
t15.daemon =True
t15.start()

t16 = threading.Thread(target=helper,args=(files,16,50))
t16.daemon =True
t16.start()

t17 = threading.Thread(target=helper,args=(files,17,50))
t17.daemon =True
t17.start()

t18 = threading.Thread(target=helper,args=(files,18,50))
t18.daemon =True
t18.start()

t19 = threading.Thread(target=helper,args=(files,19,50))
t19.daemon =True
t19.start()

t20 = threading.Thread(target=helper,args=(files,20,50))
t20.daemon =True
t20.start()

t21 = threading.Thread(target=helper,args=(files,21,50))
t21.daemon =True
t21.start()

t22 = threading.Thread(target=helper,args=(files,22,50))
t22.daemon =True
t22.start()

t23 = threading.Thread(target=helper,args=(files,23,50))
t23.daemon =True
t23.start()

t24 = threading.Thread(target=helper,args=(files,24,50))
t24.daemon =True
t24.start()

t25 = threading.Thread(target=helper,args=(files,25,50))
t25.daemon =True
t25.start()

t26 = threading.Thread(target=helper,args=(files,26,50))
t26.daemon =True
t26.start()

t27 = threading.Thread(target=helper,args=(files,27,50))
t27.daemon =True
t27.start()

t28 = threading.Thread(target=helper,args=(files,28,50))
t28.daemon =True
t28.start()

t29 = threading.Thread(target=helper,args=(files,29,50))
t29.daemon =True
t29.start()

t30 = threading.Thread(target=helper,args=(files,30,50))
t30.daemon =True
t30.start()

t31 = threading.Thread(target=helper,args=(files,31,50))
t31.daemon =True
t31.start()

t32 = threading.Thread(target=helper,args=(files,32,50))
t32.daemon =True
t32.start()

t33 = threading.Thread(target=helper,args=(files,33,50))
t33.daemon =True
t33.start()

t34 = threading.Thread(target=helper,args=(files,34,50))
t34.daemon =True
t34.start()

t35 = threading.Thread(target=helper,args=(files,35,50))
t35.daemon =True
t35.start()

t36 = threading.Thread(target=helper,args=(files,36,50))
t36.daemon =True
t36.start()

t37 = threading.Thread(target=helper,args=(files,37,50))
t37.daemon =True
t37.start()

t38 = threading.Thread(target=helper,args=(files,38,50))
t38.daemon =True
t38.start()

t39 = threading.Thread(target=helper,args=(files,39,50))
t39.daemon =True
t39.start()

t40 = threading.Thread(target=helper,args=(files,40,50))
t40.daemon =True
t40.start()

t41 = threading.Thread(target=helper,args=(files,41,50))
t41.daemon =True
t41.start()

t42 = threading.Thread(target=helper,args=(files,42,50))
t42.daemon =True
t42.start()

t43 = threading.Thread(target=helper,args=(files,43,50))
t43.daemon =True
t43.start()

t44 = threading.Thread(target=helper,args=(files,44,50))
t44.daemon =True
t44.start()

t45 = threading.Thread(target=helper,args=(files,45,50))
t45.daemon =True
t45.start()

t46 = threading.Thread(target=helper,args=(files,46,50))
t46.daemon =True
t46.start()

t47 = threading.Thread(target=helper,args=(files,47,50))
t47.daemon =True
t47.start()

t48 = threading.Thread(target=helper,args=(files,48,50))
t48.daemon =True
t48.start()

t49 = threading.Thread(target=helper,args=(files,49,50))
t49.daemon =True
t49.start()


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
