import csv
import os
from random import shuffle

forum='reddit'
mainFile=forum+'.split'

#If mainSplit File exists
#if os.path.isfile(mainFile) == False:
    
    
#else:    

#Gets all relevant files
def getFile(subforum):
    forumFile=[]
    file=os.listdir('.')
    for f in file:
        if f.find('.comment.csv') > -1 and f.find(subforum) > -1:
            forumFile.append(f)
            
    return(forumFile)
    
#extracts users from each file    
def getUsers(fileList):
    users=[]
    userCol = 0         #Reddit User IDs
    for f in fileList:
        print(f)
        with open(f,'r',encoding='utf-8') as csvfile:
            readCSV = csv.reader(csvfile,delimiter = ',')
            for row in readCSV:
                if len(row)>0:
                    users.append(row[userCol])
                    
    return(list(set(users)))
        

def splitWrite(users,n=3):      #Three Folds by default
    shuffle(users)
    if os.path.isfile(mainFile) == False:
        file=open(mainFile,'w',encoding = 'utf-8')
        
        splits = []
        for i in range(0,n):
            splits.append([])
            
        for i in range(0,len(users)):
            splits[i%n].append(users[i])
        for s in splits:
            file.write('|'.join(s)+'\n')    
        file.close()
    else:
        file = open(mainFile,'r',encoding = 'utf-8').read().split('\n')
        priorSplit = []
        
        
        
        for f in file:
            row=f.split('|')
            if len(row)>0:
                priorSplit.extend(row)
            
        
        distinctUsers=list(set(priorSplit)^set(users))        
                
        splits = []
        for i in range(0,n):
            splits.append([])
            
        for i in range(0,len(distinctUsers)):
            splits[i%n].append(distinctUsers[i])
        
        file2=open(mainFile,'w',encoding = 'utf-8')
        for i in range(0,len(file)):
            if len(file[i]) > 0:
                templist=[]
                row=file[i].split('|')
                templist.extend(row)
                templist.extend(splits[i])
                file2.write('|'.join(templist)+'\n')
            
            
        file2.close()
       
#files = getFile('television')
files = getFile('politics')
users = getUsers(files)
splitWrite(users)