##
##
##
##

##
## RENAME VARIABLE SPLIT

#d[word.lower()] syllable
#https://docs.python.org/2/library/urllib.html#urllib.quote_plus        urlunqote

#from pycontractions import Contractions         #pip install
#https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
from LIWC import liwc
import sklearn
import numpy as np
import nltk         #pip install    
nltk.download('punkt')
nltk.download('words')
nltk.download('cmudict')

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

class featureCalc:
    #Basic Features
    def __init__(self):
        self.luke=liwc()                        #loading LIWC (pronounced "Luke")
    def syllableCount(self,word):      #returns count of syllables in word using CMU's dictionary, or none if token isn't a word
        '''
        Counts the number of syllable in a given word
        '''
        word=word.lower()
        if word in CMUdict:
            return(len(CMUdict[word][0]))
        else:
            return(-1)
        
    def isComplex(self,word):        #Is word Complex
        '''
        Returns True if word is complex
        i.e. syllable count >3
        
        '''
        if syllableCount(word) >=3:
            return True
        elif syllableCount(word)<0:
            return(None)
        else:
            return(False)

    def shortWordCount(self,sentence):
        '''
        returns the number of short words in sentence
        
        '''
        
        tokens=cleaner.wordTokenize(sentence)
        cnt=0
        for t in tokens:
            if len(t)<4:
                cnt=cnt+1
        return(cnt)
        
        
        
    def specialCharFreq(self,sentence):
        '''
        Frequency of Special Characters
        '''
        specialChar=['~','@','#','$','%','!','^','&','*','(',')','-','_','=','<','+','>','<','[','{','}',']','/','\\','|']
        cnt=0
        for s in specialChar:
            cnt=cnt+sentence.count(s)
        return(cnt)
        
    def posNGram(self,sentence,n=3):      #tokenized sentence       #sentenceTokenize[1]
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
    #Composite Feature
    ''' SYLLABLES!'''
    def syllablePerWord(self,sentence):
        '''
        Breaks Sentence to Word
        Returns syllable/word
        
        '''
        wordlist=cleaner.wordTokenize(sentence)
        if wordlist != None:
            totWord=0
            totSyllable=0
            for w in wordlist:
                if self.syllableCount(w)>-1:
                    totSyllable+=self.syllableCount(w)
                    totWord+=1
                    
            return(float(totSyllable),float(totWord))           #Non-Normalized
        else:
            return(0,0)
    def syllablePerPost(self,post):
        '''
        Total Number of syllables per post
        '''
        syllyCount=self.syllablePerWord(post)
        return(syllyCount[0])
        
        
    def syllablePerSent(self,post):
        '''
        Average number of syllable per sentence
        
        Breaks posts to sentence:
        Counts total syllables and total words in Sentence
        returns Syllable Count. Sentence Count
        '''
        
        sentencelist=cleaner.sentenceTokenize(post)[0]
        totSentence=len(sentencelist)
        totSyllable=0
        for s in sentencelist:
            syllyWord=self.syllablePerWord(s)
            totSyllable=totSyllable+syllyWord[0]
            
        return(float(totSyllable)/float(totSentence))
        
    def avgSyllablePerWord(self,post):
        '''
        Average number of syllables per word
        '''
        
        
        syllyCount=self.syllablePerWord(post)
        return(syllyCount[0]/syllyCount[1])
        
    ''' SHORT WORDS'''
    
    def shortPerPost(self,post):
        '''
        Average number of short words per sentence
        '''
        sentenceList=cleaner.sentenceTokenize(post)[0]
        totSentence=len(sentenceList)
        totShorts=0
        for s in sentenceList:
            totShorts+=self.shortWordCount(s)
            
        return(float(totShorts)/float(totSentence))


    def totShortsPerPost(self,post):
        '''
        Total Number of shorts in the post
        '''
        return(self.shortWordCount(post))
        
    '''COMPLEX WORDS   '''
    

    ''' Characters'''
    
    def charPerSent(self,post):
        '''
        Average sentence length in characters
        '''
        sentences=cleaner.sentenceTokenize(post)
        l=0
        for s in sentences[0]:
            l=l+len(s)
        return(float(l)/float(len(sentences)))
        
    def whiteSpacePerChar(self,post):
        '''
        Total White Space/Total character
        '''
        totChar=len(post)
        totNoSpace=len(post.replace(' ',''))
        totSpace=totChar-totNoSpace
        
        return(float(totSpace)/float(totChar))
    
    def digitPerChar(self,post):
        '''
        total digits/character
        '''
        totChar=len(post)
        NoDigit=post
        for i in range(0,10):
            NoDigit=NoDigit.replace(str(i),'')
        totNoDigit=len(NoDigit)
        totDigit=totChar-totNoDigit
        return(float(totDigit)/float(totChar))
    
    def charLen(self,post):
        return(len(post))

    def tabsPerChar(self,post):
        '''
        tabs per character
        '''
        totChar=len(post)
        NoTab=post.replace('\t','')
        TabLen=totChar-len(NoTab)
        return(float(TabLen)/float(totChar))
        
    
    def upperPerChar(self,post):
        '''
        No. of upper case/char
        '''
        totChar=len(post)
        NoUpper=post
        for i in range(65,91):          #ASCII A to Z
            NoUpper=NoUpper.replace(chr(i),'')
            
        totNoUpper=len(NoUpper)
        Upper=totChar-totNoUpper
        
        return(float(Upper)/float(totChar))
        
        
    def alphaCount(self,post):
        '''
        No. Alphabets/char
        '''
        
        postNew=post.upper()
        return(self.upperPerChar(postNew))
    
    
    def liwcCounter(self,post):
        words=' '.join(cleaner.wordTokenize(post))
        return(self.luke.getLIWCCount(words))
    
        
    def nounPerSentence(self,post):
        '''
        Nouns Per Sentence
        '''
        sentenceList=cleaner.sentenceTokenize(post)[1]
        cnt=0
        for s in sentenceList:
            POS=self.posNGram(s,1)
            for p in POS:
                if p[0][0]=="N":
                    cnt=cnt+1
        return(float(cnt)/float(len(sentenceList)))
        
    def verbPerSentence(self,post):
        '''
        Verbs Pers Sentence
        '''
        sentenceList=cleaner.sentenceTokenize(post)[1]
        cnt=0
        for s in sentenceList:
            POS=self.posNGram(s,1)
            for p in POS:
                if p[0][0]=="V":
                    cnt=cnt+1
        return(float(cnt)/float(len(sentenceList)))
        
    def posPerSentence(self,post):
        '''
        Average POS Per Sentence
        '''
        sentenceList=cleaner.sentenceTokenize(post)[1]
        cnt=0
        for s in sentenceList:
            POS=self.posNGram(s,1)
            cnt=cnt+len(POS)
        return(float(cnt)/float(len(sentenceList)))
        
    def nounPerWord(self,post):
        word=cleaner.wordTokenize(post)
        POS=self.posNGram(word,1)
        cnt=0
        for w in POS:
            if w[0][0]=="N":
                cnt=cnt+1
        return(float(cnt)/float(len(word)))
    
    def verbPerWord(self,post):
        word=cleaner.wordTokenize(post)
        POS=self.posNGram(word,1)
        cnt=0
        for w in POS:
            if w[0][0]=="V":
                cnt=cnt+1
        return(float(cnt)/float(len(word)))
    def charWords(self,post):
        '''
        number of characters in words/number of total characters
        subtly different from 1-whitespace/char
        '''
        totChar=len(post)
        words=cleaner.wordTokenize(post)
        wordLen=0
        for w in words:
            wordLen=wordLen+len(w)
        
        return(float(wordLen)/float(totChar))
    def sentencePerPost(self,post):
        '''
        Total Sentence in post
        '''
        return(len(cleaner.sentenceTokenize(post)[1]))
        
    def linesPerPost(self,post):
        lineCount=len(post.split('\n'))
        return(lineCount)
  
    '''   Word Choice    '''
    def honore(self,post):
        words=cleaner.wordTokenize(post)
        unique=Counter(words)
        num=float(len(words))
        cnt=0
        for w in unique:
            if unique[w]==1:
                cnt=cnt+1
        denom=1-(float(cnt)/float(len(unique)))
        R=100*math.log10(num/denom)
        return(R)
     
    def sichel(self,post):
        words=cleaner.wordTokenize(post)
        unique=Counter(words)
        num=float(len(words))
        cnt=0
        for w in unique:
            if unique[w]==2:
                cnt=cnt+1
        
        S=float(cnt)/float(len(unique))
        return(S)
        
    def brunet(self,post):
        words=cleaner.wordTokenize(post)
        a=0.172
        W= len(words)** (len(set(words)) **a) 
        return(W)
    def fleschKincaid(self,post):
        #206.835 - 1.015(total Words/Total Sentences) -84.6(total Syllable/Total Words)    
        totSyllable=self.syllablePerPost(post)
        totWords=float(len(cleaner.wordTokenize(post)))
        totSentences=float(len(cleaner.sentenceTokenize(post)[0]))
        FK=206.835 - 1.015*(totWords/totSentences)-84.6*(totSyllable/totWords)
        return(FK)
        
    def hapaxLegomena(self,post):
        '''
        unnormalized
        '''
        words=cleaner.wordTokenize(post)
        unique=Counter(words)
        cnt=0
        for w in unique:
            if unique[w]==1:
                cnt=cnt+1
        
        return([cnt,len(words)])
    def hapaxDislogemna(self,post):
        '''
        unnormalized
        '''
        words=cleaner.wordTokenize(post)
        unique=Counter(words)
        cnt=0
        for w in unique:
            if unique[w]==2:
                cnt=cnt+1
        
        return([cnt,len(words)])
        
def testTrain(i,data):
    testSet=[]
    trainSet=[]
    for j in range(0,len(data)-1):
        row=data[j].split('|')
        if i==j:
        
            testSet=testSet+row
        else:
            
            trainSet=trainSet+row
    return(testSet,trainSet)
    
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
        

split=1         # OR 6 for 6 months




cleaner=preProcess()


features=featureCalc()
files=[]
social=['voat','4chan','reddit']
for s in social:
    if os.path.isdir('./'+s) == True:
        path=os.listdir('./'+s)
        for p in path:
            files.append(p)


from sklearn.ensemble import RandomForestClassifier 

for i in range(0,3):        #Cross Validation          <----------------------
    #i=0
    featTest=[]
    featTrain=[]
    fTest=open('test.'+str(i),'w')
    fTrain=open('train.'+str(i),'w')
    for p in files:
        print(p)
        #pDocs={}            #Pseudo documents    
        test={}
        train={}
        
        
        file=p.split('.')
        type=file[0]
        conf=config(type)
        with open('./'+type+'/'+p,'r', encoding="utf-8") as csvfile:   
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
            
                if type=='4chan':
                    content=cleaner.chanCleaner(row[conf[0]])          #post
                if type=='voat':
                    content=cleaner.voatCleaner(row[conf[0]])
                if type=='reddit':
                    content=cleaner.redditCleaner(row[conf[0]])

            
                if file[1]==str(i):
                    
                    label=type+'.'+row[conf[3]]
                    
                    if label not in test:
                        test[label]={}
                    pDoc=file[2]+'.'+row[conf[3]]+'.'+type
                    if pDoc not in test[label]:
                        test[label][pDoc]=""
                        
                    test[label][pDoc]=test[label][pDoc]+' . '+content
                    
                else:
                    label=type+'.'+row[conf[3]]
                    
                    if label not in train:
                        train[label]={}
                    pDoc=file[2]+'.'+row[conf[3]]+'.'+type
                    if pDoc not in train[label]:
                        train[label][pDoc]=""
                        
                    train[label][pDoc]=train[label][pDoc]+' . '+content
                    
        for t in test:
            for l in test[t]:
                content=test[t][l]
                label=l.split('.')
                featTest.append([label[1]+'.'+label[2],features.upperPerChar(content),features.verbPerSentence(content)])           #<--------------------Add Features

        for t in train:
            for l in train[t]:
                content=train[t][l]
                label=l.split('.')
                featTrain.append([label[1]+'.'+label[2],features.upperPerChar(content),features.verbPerSentence(content)])           #<--------------------Add Features

    from sklearn.ensemble import RandomForestRegressor
    trainSet=[]
    trainLabel=[]

    testSet=[]
    testLabel=[]

    labelMap={}
    invLabelMap={}
    
    rf = RandomForestClassifier(n_jobs=20, random_state=0)               #<--------------------Change Model
    j=0
    for t in featTrain:
        temp=[]
        for p in t:
            temp.append(str(p))
        fTrain.write(','.join(temp)+'\n')
        
        trainSet.append(np.array(t[1:]))
        if t[0] not in labelMap:
            labelMap[t[0]]=j
            invLabelMap[j]=[t[0]]
            j=j+1
        trainLabel.append(labelMap[t[0]])
        
        
    for t in featTest:
        temp=[]
        for p in t:
            temp.append(str(p))
        fTest.write(','.join(temp)+'\n')
        if t[0] not in labelMap:
            labelMap[t[0]]=j
            invLabelMap[j]=[t[0]]
            j=j+1
        testSet.append(np.array(t[1:]))
        testLabel.append(labelMap[t[0]])
    fTest.close()
    fTrain.close()
    rf.fit(trainSet, trainLabel)    
    predictions=rf.predict(testSet)                                                 
    accuracy = 1-sum(np.array(testLabel)^predictions)/len(predictions)          #<-XORs testLabel and Predicted Labels
    print(accuracy)