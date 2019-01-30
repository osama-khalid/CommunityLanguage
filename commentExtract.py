import requests
import csv

board='askreddit'
file = open(board+'.reddit','r').read().split('\n')
csv_file=open(board+'_comment.csv','w')
writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
for f in file:
    row=f.split(',')
    id=row[0]
    subreddit=row[1]
    comments="https://api.pushshift.io/reddit/submission/comment_ids/"+row[0]
    pageJson=requests.get(comments).json()
    comments=pageJson['data']
    op=0
    comment=requests.get("https://api.pushshift.io/reddit/comment/search?ids="+','.join(comments)).json()
    for c in comment['data']:
        author=c['author']
        body=c['body']
        image=0
        html=0
        if c['body'].find('http:')>-1 or c['body'].find('https:')>-1:
            html=1
        if c['body'].find('.jpg')>-1 or c['body'].find('.png')>-1:      
            image=1
        id=c['id']
        utc=c['created_utc']
        writer.writerow([author,body,html,image,id,utc,subreddit,op])
            
csv_file.close()        