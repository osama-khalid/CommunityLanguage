#d[word.lower()] syllable
#https://docs.python.org/2/library/urllib.html#urllib.quote_plus        urlunqote

import nltk         #pip install    
#nltk.download('punkt')
#nltk.download('words')
from nltk.corpus import words             #check dictionary
import re                           #elongation
from autocorrect import spell as spell_check      #pip install     #check spelling
from nltk.tokenize import sent_tokenize #sentence tokenizer         https://www.nltk.org/api/nltk.tokenize.html also see
import csv                              #read file    
from datetime import datetime           #convert unix time to human time

from nltk import edit_distance as ed    #check word spelling correction distance
import urllib.request as urllib         #ud convert url to unicode

from nltk.corpus import cmudict
CMUdict = cmudict.dict()      #syllable
def syllable_count(word):
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
    
def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)

def reduce_lengthening_single(text):
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
    
    



        
        
user=-1
text=22
path="pol.csv_2015-1"
dateStamp=4
#date=row[4]
c=0
#text=row[22]
with open(path,'r', encoding="utf-8") as csvfile:   
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:    
        #print(datetime.fromtimestamp(int(row[dateStamp])))
        c=c+1
        if c <100000:
            X=sent_tokenize(row[text].replace('<marquee>[trigger warning]</marquee>','').replace('\\\n',' . ')[6:])    
            
            print(row[text])
            print(X)
        else:
            break
       





#X='luuuuuvvv'









