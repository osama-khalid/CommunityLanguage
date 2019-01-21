#http://archive.4plebs.org/_/api/chan/thread/?board=adv&num=16627902

import json
import requests
import csv
import time as time
allPage=[]
i=0
board='pol'
page=['200546074','200541442']
def threadScrape(board,page):
    thread=[]
    r=requests.get("http://archive.4plebs.org/_/api/chan/thread/?board="+board+"&num="+str(page)).json()

    arr=[]
    thread_num=r[page]['op']['thread_num']
    timestamp=r[page]['op']['timestamp']
    comment=r[page]['op']['comment']
    board=r[page]['op']['board']['shortname']
    title=r[page]['op']['title']
    op=r[page]['op']['op']
    arr=[board,thread_num,timestamp,board,title,op,comment]
    thread.append(arr)
    if 'posts' in r[page]:
        for p in r[page]['posts']:
            arr=[]
            thread_num=r[page]['posts'][p]['thread_num']
            timestamp=r[page]['posts'][p]['timestamp']
            comment=r[page]['posts'][p]['comment']
            board=r[page]['posts'][p]['board']['shortname']
            title=r[page]['posts'][p]['title']
            op=r[page]['posts'][p]['op']
            arr=[board,thread_num,timestamp,board,title,op,comment]
            thread.append(arr)
            
    
    return(thread)
csv_file=open(board+'text.csv','w')
writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
    
for p in page:
    thread=threadScrape(board,p)
    for row in thread:
        writer.writerow(row)
        
        