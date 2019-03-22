import random
import csv
import os

def getUsers(type):#text=row[22]
    files=os.listdir('.')
    paths=[]
    
    if type=='voat':
        usrCol=0
        for f in files:
            if f.find('.voat.comment.csv')>-1:
                paths.append(f)
    
    if type=='4chan':
        usrCol=0
        for f in files:
            if f.find('pol.csv_20')>-1:
                paths.append(f)
        
    if type=='reddit':
        usrCol=0
        for f in files:
            if f.find('.reddit.comment.csv')>-1:
                paths.append(f)
    
    users=[]
    for path in paths:
    
        with open(path,'r', encoding="utf-8") as csvfile:   
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if len(row)>0:
                    users.append(row[usrCol])

    return(set(users))
    

def testTrainSplit(users,type,n=10):
    splits=[]
    users=set(users)
    for i in range(0,n):
        splits.append([])
        
    for u in users:
        splits[random.randint(0,9)].append(u)
        
    #print(len(users))
    if type == 'reddit':
        file=open('reddit.split','w')
    if type == 'voat':
        file=open('voat.split','w')
    if type=='4chan':
        file=open('4chan.split','w')
    for s in splits:
        file.write('|'.join(s)+'\n')
    file.close()
    
'''
type='voat'
users=getUsers(type)
testTrainSplit(users,type)
'''
type='reddit'
users=getUsers(type)
testTrainSplit(users,type)