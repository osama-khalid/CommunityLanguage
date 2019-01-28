import requests
import threading
     
def helper(k):
    thread=[]
    i=0
    c=0
    board='b'
    x=""
    y=""
    while(1):
        i=i+1
        c=c+1
        
        if c%10==0:
            print(len(thread),i)
            
        url = "https://thebarchive.com/b/page/"+str(i)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        r=requests.get(url,headers=header)
        page=str(r.content)
        print(r)
        x=page
        if len(page)>51225:
            links=page.split('data-thread-num')
            for l in links:
                if l[0]=='=':
                    t=l.split('">')[0][2:]
                    
                
            y=page    
            thread=list(set(thread))   
        else:
            break
        
    file=open(board+'_barchive','w')
    for i in thread:
        file.write(i+'\n')
        
    file.close()    
    
helper(1)    