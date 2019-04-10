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
                
    print(len(data))
    return(data)	
board='politics'
allComments = merge(board)            
def helper(board,allComments,k,j):
    csv_file=open(board+'_'+str(k)+'.commentAll.csv','w', encoding="utf-8")
    writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
    for i in range(0,len(allComments)):
        cmt=[]
        c=0
        if i%j==k:
            cmt.append(allComments[i])
            c=c+1                                   
            if c%1000==0:
            
                while True:
                    try:
                        comment=requests.get("https://api.pushshift.io/reddit/comment/search?ids="+','.join(cmt)).json()
                        break
                    except:
                        print('wait')
                        time.sleep(10)
                for c in comment['data']:
                    author=c['author']
                    body=c['body']
                    image=0
                    html=0
                    if c['body'].find('http:')>-1 or c['body'].find('https:')>-1:
                        html=1
                    if c['body'].find('.jpg')>-1 or c['body'].find('.png')>-1:      
                        image=1
                    id=c['id']
                    utc=c['created_utc']
                    writer.writerow([author,body,html,image,id,utc,subreddit,op,p[0]])                        
                    
                cmt=[]
                c=0
                    
            
            
    csv_file.close()
    

t0 = threading.Thread(target=helper,args=(board,allComments,0,6)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=(board,allComments,1,6)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=(board,allComments,2,6)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=(board,allComments,3,6)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=(board,allComments,4,6)) 
t4.daemon =True
t4.start()    

t5 = threading.Thread(target=helper,args=(board,allComments,5,6)) 
t5.daemon =True
t5.start()    

a=t0.join()
a=t1.join()
a=t2.join()
a=t3.join()
a=t4.join() 
a=t5.join()