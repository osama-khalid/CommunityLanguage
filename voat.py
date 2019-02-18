import requests
import copy
import datetime


initdate=datetime.datetime(2015,1,1)

total=[]
board='news'
file=open(board+".voat",'w')
cutoff=datetime.datetime(2019,2,14)
while(initdate<cutoff):
    
    delta=datetime.timedelta(1)
    finaldate=initdate+delta
    smonth=str(initdate.month)
    sday=str(initdate.day)
    
    emonth=str(finaldate.month)
    eday=str(finaldate.day)
    if len(smonth)==1:
        smonth="0"+smonth
    if len(sday)==1:
        sday="0"+sday
        
    if len(emonth)==1:
        emonth="0"+emonth
    if len(eday)==1:
        eday="0"+eday

    i=0        
    if sday=="01":
        print(initdate)
    start=str(initdate.year)+'-'+smonth+'-'+sday
    end=str(finaldate.year)+'-'+emonth+'-'+eday
    prev=[]
    curr=[]
    while(1):
        
        
    
        
        prev=copy.deepcopy(curr)
        curr=[]
        url='https://searchvoat.co/?s='+board+'&o=1&p='+str(i)+'&df='+start+'&dt='+end+'&nsfw=off&o=on'
        
        page=str(requests.get(url).content)

        splits=page.split('<div class="entry">')
        for s in splits:
            try:
                curr.append(s.split('href="')[1].split('">')[0])
            except:
                pass
        if curr==prev:
            break
            
        if len(prev)>0:
            for p in prev:
                file.write(str(p)+'\n')
        i=i+1
        
    initdate=finaldate
    
    
    