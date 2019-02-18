import requests
import copy
import datetime


def voatScrape(link):
    thread=link.split('/')[-1]
    subvoat=link.split('/')[-2]
    #thread='3036816'
    i=0
    while (1):
        url="https://voat.co/comments/"+thread+"/null/siblings/"+str(i)+"/Top"
        i=i+8
        page=str(requests.get(url).content)
        users=page.split('username="')
        for p in range(1,len(users)):
            author=users[p].split('">')[0]
            body=users[p].split('<textarea')[1].split('">')[1].split('</textarea')[0]
            utc=users[p].split('time title="')[1].split('"')[0]
            id=users[p].split('id="commentContent-')[1].split('">')[0]
            
            bdy=users[p].split('commentContent-')[1].split('</div>')[0]
            url=0
            img=0
            
            img=len(body.split('.jpg'))-1
            img=img+len(body.split('.png'))-1
            img=img+len(body.split('.jpeg'))-1
            
            
            url=len(body.split('https:'))-1
            url=url+len(body.split('http:'))-1
            
            url=url-img
            
            #if url>0:
            #    url=1
            #if img>0:
            #    img=1
            #if body.find('http:')>-1 or body.find('https:')>-1:
            #    url=1
            #if bdy.find('.jpg')>-1 or bdy.find('.png')>-1:      
            #    img=1
            body=body.replace('&#xA;','\n')
            body=body.replace('&#xD;','\r')
            body=body.replace('&#x27',"'")
            #body=body.replace('&#xA8;',"")
            #print(thread,author,body,img,url,id,utc,subvoat)
            if body.find('&#x')>-1:
                print(body[body.find('&#x')-5:].split(' ')[1])
                
            
            
        #print(len(page))
        #print()
        if len(page)<100:
            break
        
voatScrape('https://voat.co/v/news/3036816')    
#author body, url,image,id,utc,subreddit,op    