import csv                              #read file    
from datetime import datetime           #convert unix time to human time
import os
def getDate(D,type,split=1):   
    '''
    standardizes 4chan date to 
    YYYY-S
    where S = split 
    if split =1 S will range from 0 to 11
    if split =6, S will range from 0 to 1
    '''
    if type=='4chan':
        date_object=datetime.fromtimestamp(int(D))
        return(str(date_object.year)+'-'+str((int(date_object.month)-1)//split))
        
    if type=='voat':
        date_object=D.split(' ')[0].split('/')
        return(str(date_object[2])+'-'+str((int(date_object[0])-1)//split))

    if type=='reddit':
        date_object=datetime.fromtimestamp(int(D))
        return(str(date_object.year)+'-'+str((int(date_object.month)-1)//split))        
    

def getFiles(type):
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
            if f.find('.csv_20')>-1:

                paths.append(f)
        
    if type=='reddit':
        usrCol=0
        for f in files:
            if f.find('.comment.csv')>-1:
                paths.append(f)
    return(paths)
    
def getUsers(type):
    file=open(type+'.split','r',encoding="utf-8").read().split('\n')
    users=[]
    for f in file:
        if len(f)>0:
            row=f.split('|')
            users.append(row)
            
    return(users)
    
def config(type):

    if type=='4chan':
        user=0
        text=22
        dateStamp=4
        paths=getFiles(type)

    if type=='voat':
        paths=getFiles(type)
        text=1
        user=0
        dateStamp=2


    if type=='reddit':
        text=1
        user=0
        paths=getFiles(type)
        dateStamp=5
    return([text,user,dateStamp,paths])
    

def helper(type):
    
    users=getUsers(type)
    conf=config(type)
    files={}
    print(conf)
    for p in conf[3]:
        print(p)
        with open(p,'r', encoding="utf-8") as csvfile:   
            readCSV = csv.reader(csvfile, delimiter=',')
            prefix=p.split('_')[0]
            for row in readCSV:  
                
                if len(row)>0:
                    for i in range(0,len(users)):
                        if row[0] in users[i]:
                            if len(row)>conf[2]:
                                    try:
                                        datekey=getDate(row[conf[2]],type,1)
                                        fileName=prefix+'.'+type+'.'+str(i)+'.'+datekey
                                        if os.path.isfile(fileName) == False:
                                            csfile=open(fileName,'w', encoding="utf-8")
                                            files[str(i)+'.'+datekey]=csv.writer(csfile,delimiter=',', lineterminator='\n')
                                            print(fileName)
                                        if type=='4chan':
                                            F=p.split('.')[0]
                                            row.append(F)
                                        
                                        files[str(i)+'.'+datekey].writerow(row)
                                        
                                    except:
                                        continue
                                
            
    for f in files:
        file=type+'.'+f
        
                
      
#helper('4chan')                    
helper('reddit')              
            