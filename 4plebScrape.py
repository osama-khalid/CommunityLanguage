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
    media=2
    thread_num=r[page]['op']['thread_num']
    timestamp=r[page]['op']['timestamp']
    comment=r[page]['op']['comment']
    commentProcessed=r[page]['op']['comment_processed']
    if commentProcessed==None:
        commentProcessed=''
    board=r[page]['op']['board']['shortname']
    title=r[page]['op']['title']
    op=r[page]['op']['op']
    
    if r[page]['op']['media'] is not None:
        media=1
    else:
        media=0
    
    
    
    htp=0
    
    if comment ==None:
        comment=''
    if comment.find('http://')>-1 or comment.find('https://')>-1:
        htp=1
    quote=0
    if comment.find('>>')>-1:
        quote=1
    green=0
    if commentProcessed.find('class="greentext"')>-1:
        green=1
    arr=[board,thread_num,timestamp,title,op,comment,media,htp,quote,green]
    thread.append(arr)
    if 'posts' in r[page]:
        for p in r[page]['posts']:
            arr=[]
            thread_num=r[page]['posts'][p]['thread_num']
            timestamp=r[page]['posts'][p]['timestamp']
            comment=r[page]['posts'][p]['comment']
            commentProcessed=r[page]['posts'][p]['comment_processed']
            if commentProcessed==None:
                commentProcessed=""
            board=r[page]['posts'][p]['board']['shortname']
            title=r[page]['posts'][p]['title']
            op=r[page]['posts'][p]['op']
            
            media=2
            
            if r[page]['posts'][p]['media'] is not None:
                media=1
            else:
                media=0
            
            htp=0
            if comment == None:
                comment=''
            if comment.find('http://')>-1 or comment.find('https://')>-1:
                htp=1
            
            quote=0
            if comment.find('>>')>-1:
                quote=1
            green=0
            
            if commentProcessed.find('class="greentext"')>-1:
                green=1
            arr=[board,thread_num,timestamp,title,op,comment,media,htp,quote,green]
            thread.append(arr)
            
    
    return(thread)
csv_file=open(board+'_Dump.csv','w')
writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
writer.writerow(['board','thread','timeUTC','title','isOP','comment','hasMedia','hasURL','hasQuote','hasGreenText'])    
for p in page:
    thread=threadScrape(board,p)
    for row in thread:
        writer.writerow(row)
        
csv_file.close()        