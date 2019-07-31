import csv
import os
import random
from datetime import datetime           #convert unix time to human time
files = os.listdir('.')
'''
def config(type):

    if type=='4chan':
        user=0
        text=22
        dateStamp=4
      
'''
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
    

chanFiles = []

for f in files:
    if f.find('.csv_20') > -1:
        chanFiles.append(f)
        
#for f in chanFiles:

f=chanFiles[0]
helper(f)
def helper(f):
    files={}
    with open('./'+f,'r', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        prefix = f.split('.')[0]+'.4chan'
        for row in readCSV: 
            if len(row)>0:
                rand=random.random()*100
                if rand<=33.333333:
                    midfix=0
                elif rand>66.66667:
                    midfix=2
                else:
                    midfix=1
                
                fileName=prefix+'.'+str(midfix)
                datekey=getDate(row[4],'4chan',1)
                #
                
                fileName=fileName+'.'+datekey
                if os.path.isfile(fileName) == False and fileName not in files:
                    csvfile=open(fileName,'w', encoding="utf-8")
                    files[fileName]=csv.writer(csvfile,delimiter=',', lineterminator='\n')
                    print(fileName)
                    
                elif os.path.isfile(fileName) == True and fileName not in files:
                    csvfile=open(fileName,'a', encoding="utf-8")
                    files[fileName]=csv.writer(csvfile,delimiter=',', lineterminator='\n')
                    print(fileName+'\t'+'append')
                
                
                files[fileName].writerow(row)
                
                