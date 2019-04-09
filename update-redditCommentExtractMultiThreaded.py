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
        if f.find(board)>-1 and f.find('.reddit')>-1:
            dbs.append(f)
    for d in dbs:
        content=open(d,'r').read().split('\n')
        for row in content:
            if len(row)>0:
                r=row.split(',')
                data.append((r[0],r[1]))
    return(data)	
board='politics'


post=merge(board)
print(len(post))
def helper(board,posts,k,j):
    C=0
    XX=0
    
    csv_file=open(board+'_'+str(k)+'.commentID.csv','w', encoding="utf-8")
    #writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
    
    for p in posts:
        if C%j==k:
            XX=XX+1
            if XX%50==0:
                print(XX)
            id=p[0]
            subreddit=p[1]
            url="https://api.pushshift.io/reddit/submission/comment_ids/"+p[0]
            while True:
                try:
                    pageJson=requests.get(url).json()		
                    break
                except:
                    print("Wait")
                    time.sleep(10)
                    
                    
            
            comments=pageJson['data']	
            
            for c in comments:
                csv_file.write(c+'\n')
            
            
        C=C+1
    
    

    csv_file.close()        	    

t0 = threading.Thread(target=helper,args=(board,post,0,6)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=(board,post,1,6)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=(board,post,2,6)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=(board,post,3,6)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=(board,post,4,6)) 
t4.daemon =True
t4.start()


t5 = threading.Thread(target=helper,args=(board,post,5,6)) 
t5.daemon =True
t5.start()


a=t0.join()
a=t1.join()
a=t2.join()
a=t3.join()
a=t4.join()	
a=t5.join()	
