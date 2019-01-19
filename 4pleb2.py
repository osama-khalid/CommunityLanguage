#http://archive.4plebs.org/_/api/chan/thread/?board=adv&num=16627902
#http://archive.4plebs.org/_/api/chan/index/?board=adv&page=1
import json
import requests
import time as time
allPage=[]
i=0
board='pol'
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
file=open('4pleb'+'_'+board+'json','w')
for f in allPage:
    file.write(f+'\n')
    
file.close()    