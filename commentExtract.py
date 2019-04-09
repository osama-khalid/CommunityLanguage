import requests
import csv
import os
import threading
import time
def merge(board):
    data=[]
    Files=os.listdir(".")
    dbs=[]
    
    for f in Files:
        if f.find(board)>-1 and f.find('.commentID')>-1:
            dbs.append(f)
    for d in dbs:
        content=open(d,'r').read().split('\n')
        for row in content:
            if len(row)>0:
                data.append(row)
    return(data)	
board='politics'
allComments = merge(board)            
print()
for i in range(0,len(allComments),1000):
    while True:
        try:
            comment=requests.get("https://api.pushshift.io/reddit/comment/search?ids="+','.join(allComments[i:i+1000])).json()
            break
        except:
            print('wait')
            time.sleep(10)