from random import shuffle
import csv
import os
import operator


def getUsers(type):#text=row[22]
    files=os.listdir('.')
    paths=[]
    stat=open(type+'.stats','w')
    if type=='voat':
        usrCol=0
        for f in files:
            if f.find('.voat.comment.csv')>-1:
                paths.append(f)
    
    if type=='4chan':
        usrCol=0
        for f in files:
            if f.find('.csv_20')>-1:
                paths.append(f)
        
    if type=='reddit':
        usrCol=0
        for f in files:
            if f.find('.reddit.comment.csv')>-1:
                paths.append(f)
    
    users=[]
    stat.write('medium,path,number of users,number of posts,max posts, median posts,upperQuartile,lowerQuartile,avg\n')
    
    for path in paths:
        statUser={}
        with open(path,'r', encoding="utf-8") as csvfile:   
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if len(row)>0:
                    if row[usrCol] not in statUser:
                        statUser[row[usrCol]]=0
                    statUser[row[usrCol]]=statUser[row[usrCol]]+1
                    users.append(row[usrCol])
        numPost=sum(statUser.values())
        numUsers=len(statUser)
        maxPost=sorted(statUser.items(),key=operator.itemgetter(1),reverse=True)[0][1]
        medianPost=sorted(statUser.items(),key=operator.itemgetter(1),reverse=True)[int(len(statUser)*0.5)][1]
        upperPost=sorted(statUser.items(),key=operator.itemgetter(1),reverse=True)[int(len(statUser)*0.25)][1]
        lowerPost=sorted(statUser.items(),key=operator.itemgetter(1),reverse=True)[int(len(statUser)*0.75)][1]
        stat.write(type+','+path+','+str(numUsers)+','+str(numPost)+','+str(maxPost)+','+str(medianPost)+','+str(upperPost)+','+str(lowerPost)+','+str(float(numPost)/float(numUsers))+'\n')
    return(set(users))
    

def testTrainSplit(users,type,n=10):
    splits=[]
    users=list(set(users))
    shuffle(users)
    shuffle(users)
    for i in range(0,n):
        splits.append([])
        
    for i in range(0,len(users)):
        splits[i%n].append(users[i])
    '''print(len(users))
    for i in splits:
        print(len(i))
    '''    
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
type='voat'
users=getUsers(type)
testTrainSplit(users,type)

type='4chan'
users=getUsers(type)
testTrainSplit(users,type)