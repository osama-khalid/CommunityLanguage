#http://archive.4plebs.org/_/api/chan/thread/?board=adv&num=16627902
#http://archive.4plebs.org/_/api/chan/index/?board=adv&page=1
import json
import threading
import requests
import time as time
def helper(board,k):
    allPage=[]
    i=0
    
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
            page=r.json()
            for p in page:
                allPage.append(p)
            
        else:
            break

    allPage=list(set(allPage))
    file=open('4pleb'+'_'+board+'_json','w')
    for f in allPage:
        file.write(f+'\n')
        
    file.close()    
    
t0 = threading.Thread(target=helper,args=('adv',1)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=('f',1)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=('hr',1)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=('o',1)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=('pol',1)) 
t4.daemon =True
t4.start()

t5 = threading.Thread(target=helper,args=('s4s',1)) 
t5.daemon =True
t5.start()

t6 = threading.Thread(target=helper,args=('sp',1)) 
t6.daemon =True
t6.start()

t7 = threading.Thread(target=helper,args=('tg',1)) 
t7.daemon =True
t7.start()

t8 = threading.Thread(target=helper,args=('trv',1)) 
t8.daemon =True
t8.start()

t9 = threading.Thread(target=helper,args=('tv',1)) 
t9.daemon =True
t9.start()

t10 = threading.Thread(target=helper,args=('x',1)) 
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