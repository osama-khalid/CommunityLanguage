import re
import requests
import csv
board='pol_thread'
file=open(board,'r').read().split('\n')
csv_file=open(board+'text.csv','w')
writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
x=0

for f in file:
    if len(f)>0:
    
    
        p=str(requests.get(f).content)
        blocks=p.split('<span class="nameBlock ">')
        flag=0
        for b in blocks:
            image=0
            if b.find('class="subject">')>-1:
                title=b.split('class="subject">')[1].split('<')[0]
                op=1
                
            
            if b.find('postMessage')>-1:
                if flag==0:
                    X=1
                    title=title
                    op=1
                    flag=1
                else:
                    title=""
                    op=0
                c=b.split('postMessage')
                if c[0].find("<img src")>-1:
                    image=1
                else:
                    image=0
                if c[1].find('class="quotelink">')>-1:
                    quote=1
                else:
                    quote=0
                if c[1].find('class="quote">') >-1:
                    green=1
                else:
                    green=0
                    
                
                    
                if b.find('postContainer')>-1:

                    
                    time=c[0].split('dateTime"')[1].split('<')[0].strip(" ").strip(">")
                    q=c
                    d=c[1].split('postContainer')[0].split('</blockquote>')[0].replace('<br>','<>\n').replace('undefined<','<').replace('&quot;','"')
                    x=d.find('>')
                    d=re.sub('<.*?>', '<>', d[x:])
                    X=d.replace('>undefined<','><').replace('><','').replace('&gt;','>').replace('<>','').replace('&#039;',"'").replace('>>>','>>').replace('undefined>','>')
                    r=X.rfind('undefined')
                    
                    if r>-1:
                        comment=X[:r+1]
                    else:
                        comment=X
                    if comment.find('http://') >-1 or comment.find('https://')>-1:
                        url=1
                    else:
                        url=0
                    writer.writerow([time,comment,quote,green,url,image,f.split('/')[-1],op,title])
                    
                    
                else:
                    time=c[0].split('dateTime"')[1].split('<')[0].strip(" ").strip(">")
                    d=c[1].split('thread-stats')
                    p=d
                    d=p[0].split('postContainer')[0].split('</blockquote>')[0].replace('<br>','<>\n').replace('undefined<','<').replace('&quot;','"')
                    
                    x=d.find('>')
                    
                    d=re.sub('<.*?>', '<>', d[x:])
                    
                    X=d.replace('>undefined<','><').replace('><','').replace('&gt;','>').replace('<>','').replace('&#039;',"'").replace('>>>','>>').replace('undefined>','>')
                    r=X.rfind('undefined')
                    
                    

                    if r>-1:
                        comment=X[:r+1]
                    else:
                        comment=X
                    if comment.find('http://') >-1 or comment.find('https://')>-1:
                        url=1
                    else:
                        url=0
                    writer.writerow([time,comment,quote,green,url,image,f.split('/')[-1],op,title])
                    
                