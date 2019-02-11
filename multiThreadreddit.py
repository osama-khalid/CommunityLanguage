#https://api.pushshift.io/reddit/submission/search/?subreddit=pol&after=1506816000&before=1506902400&step=10000
import requests
import time
import threading

timeNow=1549636623
timeEnd=1356998400 #Jan 01 2013
board='pol'
def helper(subreddit,k,j):
    c=0
    d=0
    now = timeNow-k*2000
    #subreddit='politics'
    file=open(subreddit+"_"+str(k)+'.reddit','w')
    while now>timeEnd:
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
        
        now=int(now)-j*2000
        if len(pageJson['data'])>0:
            c=0
            for p in range(0,len(pageJson['data'])):
                file.write(pageJson['data'][p]['id']+','+subreddit+'\n')
                

    file.close()
            
t0 = threading.Thread(target=helper,args=(board,0,5)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=(board,1,5)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=(board,2,5)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=(board,3,5)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=(board,4,5)) 
t4.daemon =True
t4.start()



a=t0.join()
a=t1.join()
a=t2.join()
a=t3.join()
a=t4.join()
