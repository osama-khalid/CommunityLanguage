#https://api.pushshift.io/reddit/submission/search/?subreddit=pol&after=1506816000&before=1506902400&step=10000
import requests
import time
import threading
def helper(subreddit,k):
    c=0
    d=0
    now = int(time.time())
    #subreddit='politics'
    file=open('reddit'+'.'+subreddit+'','w')
    while(1):
        d=d+1
        if d%10==0:
            print(d)
        while True:
            try:
                pageJson=requests.get('https://api.pushshift.io/reddit/submission/search/?subreddit='+subreddit+'&after='+str(int(now)-2000)+'&before='+str(now)+'&step=1000').json()
                break
            except:
                print("Wait")
                time.sleep(10)
        
        now=int(now)-2000
        if len(pageJson['data'])>0:
            for p in range(0,len(pageJson['data'])):
                file.write(pageJson['data'][p]['id']+','+subreddit+'\n')
                
        else:
            c=c+1
        if c==100:
            break
    file.close()
            
t0 = threading.Thread(target=helper,args=('askreddit',1)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=('KotakuInAction',1)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=('the_donald',1)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=('worldnews',1)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=('poltics',1)) 
t4.daemon =True
t4.start()



a=t0.join()
a=t1.join()
a=t2.join()
a=t3.join()
a=t4.join()
