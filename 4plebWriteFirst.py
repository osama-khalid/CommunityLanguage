#http://archive.4plebs.org/_/api/chan/thread/?board=adv&num=16627902
#http://archive.4plebs.org/_/api/chan/index/?board=adv&page=1
import json
import threading
import requests
import time as time
def helper(board,k):
    allPage=[]
    file=open('4pleb'+'_'+board+'_json','w')
    i=0
    error=open(board+'.error','w')
    while(1):
        i=i+1
        if i%10==0:
            print(i)
        while True:
            try:
                r=requests.get("http://archive.4plebs.org/_/api/chan/index/?board="+board+"&page="+str(i))
                break
            except:
                print("Wait")
                time.sleep(60)
        if len(r.content)>5:
            try:
                page=r.json()
                for p in page:
                    
                    file.write(p+'\n')
            except:
                error.write(str(i)+','+board+'\n')
            
        else:
            break

    
        
        
    file.close()    
    
helper('pol',1)
