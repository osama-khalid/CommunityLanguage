#d[word.lower()] syllable
#https://docs.python.org/2/library/urllib.html#urllib.quote_plus        urlunqote

import nltk         #pip install    
#nltk.download('punkt')
#nltk.download('words')
import html
from nltk.corpus import words             #check dictionary
import re                           #elongation
from autocorrect import spell as spell_check      #pip install     #check spelling
from nltk.tokenize import sent_tokenize #sentence tokenizer         https://www.nltk.org/api/nltk.tokenize.html also see
import csv                              #read file    
from datetime import datetime           #convert unix time to human time
from nltk.tokenize import RegexpTokenizer       #remove puncutations
from nltk import edit_distance as ed    #check word spelling correction distance
import urllib.request as urllib         #ud convert url to unicode
punctuations = RegexpTokenizer(r'\w+')
from nltk.corpus import cmudict
CMUdict = cmudict.dict()      #syllable

def channer(post):          #clean 4archive posts
    return(post.replace('<marquee>[trigger warning]</marquee>','').replace('\\\n',' . ')[6:])

def chandate(D,split=1):    #standardizes 4chan date
    date_object=datetime.fromtimestamp(int(row[dateStamp]))
    
    return(str(date_object.year)+'-'+str((int(date_object.month)-1)//split))

def voatter(post):      #cleans voat posts
    return(html.unescape(post).replace('\n','. ').replace('&nbsp;','.'))    
    
def voatdate(D,split=1):    #standardizes voat date
    date_object=D.split(' ')[0].split('/')
    return(str(date_object[2])+'-'+str((int(date_object[0])-1)//split))

def syllable_count(word):      #returns count of syllables in word using CMU's dictionary, or none if token isn't a word
    word=word.lower()
    if word in CMUdict:
        return(len(CMUdict[word][0]))
    else:
        return(None)
    


def urban_load(year=2019): #urban dictionary load in lowercase

    #load urban dictionary
    urbanFile=open('urbandictionary.'+str(year),'r',encoding='utf-8').read().split('\n')
    #urban dictionary:
    ud=[]
    for u in urbanFile:
        if len(u)>0:
            ud.append(urllib.unquote(u.lower()))
    return(ud)
    
ud=urban_load()
    
def reduce_lengthening(text):           #Contracts all repetitions to at most 2
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)

def reduce_lengthening_single(text):    #Contracts all repetitions to 1
    pattern = re.compile(r"(.)\1{1,}")
    return pattern.sub(r"\1", text)
    
        
def word_check(word):
    if word in words.words():         #if word in dictionary
        return(word)
    if word in ud:                      #if word in urbandictionary
        return(word)
    return(None)
        
def word_normalizer(word):
    word=word.lower()
    
    word1=reduce_lengthening_single(word)
    
    word2=reduce_lengthening(word)
    if word1==word:                     #No double letter
        return(word_check(word))
        
    if word==word2:                    #No contraction at all
        return(word_check(word))
    if word_check(word2) != None:       #word with double letter is in dictionary            
        return(word_check(word2))
    if word_check(word1) !=None:        #word with single letters is in dictionary          luuuuvvvv
        return(word_check(word1))
        
    if spell_check(word1)==spell_check(word2):                  #   finnnnnaaaallly
        return(spell_check(word1))
    else:
        return(None)
    
    



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
#text=row[22]
with open(path,'r', encoding="utf-8") as csvfile:   
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:    
        #print(datetime.fromtimestamp(int(row[dateStamp])))
        c=c+1
        if c <100:
            content=""
            
            if flag=='4chan':
                content=channer(row[text])
                datekey=chandate(row[dateStamp],split)
            if flag=='voat':
                content=voatter(row[text])
                datekey=voatdate(row[dateStamp],split)
            sentences=[]
            raw_sentences=sent_tokenize(content)
            
            for s in raw_sentences:
                if len(s.strip('.').strip(' '))>0:
                    sentences.append(s)
                    if len(s)>0:
                        tokens = punctuations.tokenize(s)
                        if len(tokens)>0:
                            print(tokens)           #all words tokenized
            print(content)                          #raw post
            print(sentences)                        #sentence tokenized
            
            
        else:
            break
       





#X='luuuuuvvv'









