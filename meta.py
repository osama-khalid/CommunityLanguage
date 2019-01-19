import requests
from bs4 import BeautifulSoup as BS

import threading


        
def helper(board,k):
    thread=[]
    i=0
    c=0

    while(1):
        i=i+1
        c=c+1
        if c%10==0:
            print(len(thread),i)
            
        url = "https://4archive.org/board/"+board+"/"+str(i)+"/"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r=requests.get(url,headers)
        page=str(r.content)
        
        if len(page)>40815:
            links=page.split('class="thread" id="')
            for l in links:
                if l[0]=='t':
                    t=l.split('">')[0].replace('t','')
                    thread.append('https://4archive.org/board/'+board+'/thread/'+t)
                
                
            thread=list(set(thread))   
        else:
            break
        
    file=open(board+'_thread','w')
    for i in thread:
        file.write(thread+'\n')
        
    file.close()    

t0 = threading.Thread(target=helper,args=('trv',1)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=('biz',1)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=('fit',1)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=('adv',1)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=('news',1)) 
t4.daemon =True
t4.start()

t5 = threading.Thread(target=helper,args=('diy',1)) 
t5.daemon =True
t5.start()

t6 = threading.Thread(target=helper,args=('mu',1)) 
t6.daemon =True
t6.start()

t7 = threading.Thread(target=helper,args=('lit',1)) 
t7.daemon =True
t7.start()

t8 = threading.Thread(target=helper,args=('ck',1)) 
t8.daemon =True
t8.start()

t9 = threading.Thread(target=helper,args=('p',1)) 
t9.daemon =True
t9.start()

t10 = threading.Thread(target=helper,args=('sci',1)) 
t10.daemon =True
t10.start()

t11 = threading.Thread(target=helper,args=('sp',1)) 
t11.daemon =True
t11.start()

t12 = threading.Thread(target=helper,args=('k',1)) 
t12.daemon =True
t12.start()

t13 = threading.Thread(target=helper,args=('tv',1)) 
t13.daemon =True
t13.start()

t14 = threading.Thread(target=helper,args=('co',1)) 
t14.daemon =True
t14.start()

t15 = threading.Thread(target=helper,args=('int',1)) 
t15.daemon =True
t15.start()

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
a=t11.join()
a=t12.join()
a=t13.join()
a=t14.join()
a=t15.join()