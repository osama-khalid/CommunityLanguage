import requests
import threading
     
def helper(k,x):
    thread=[]
    i=0
    c=0
    board='b'
    x=""
    y=""
    for i in range(k,k+50000):
        
        c=c+1
        
        if c%10==0:
            print(len(thread),i)
            
        url = "https://thebarchive.com/b/page/"+str(i)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        r=requests.get(url,headers=header)
        page=str(r.content)
        
        x=page

        links=page.split('data-thread-num')
        for l in links:
            if l[0]=='=':
                t=l.split('">')[0][2:]
                thread.append(t)
            
        y=page    
        thread=list(set(thread))   
        
        
    file=open(board+'_'+str(k)+'_barchive','w')
    for i in thread:
        file.write(i+'\n')
        
    file.close()    
#400000    
#helper(100000)    

t0 = threading.Thread(target=helper,args=(1,1)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=(50001,1)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=(100001,1)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=(150001,1)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=(200001,1)) 
t4.daemon =True
t4.start()


t6 = threading.Thread(target=helper,args=(250001,1)) 
t6.daemon =True
t6.start()

t7 = threading.Thread(target=helper,args=(300001,1)) 
t7.daemon =True
t7.start()

t8 = threading.Thread(target=helper,args=(350001,1)) 
t8.daemon =True
t8.start()

t9 = threading.Thread(target=helper,args=(400001,1)) 
t9.daemon =True
t9.start()

t10 = threading.Thread(target=helper,args=(450001)) 
t10.daemon =True
t10.start()

a=t0.join()
a=t1.join()
a=t2.join()
a=t3.join()
a=t4.join()
a=t5.join()
a=t6.join()
a=t7.join()
a=t8.join()
a=t9.join()

a=t10.join()