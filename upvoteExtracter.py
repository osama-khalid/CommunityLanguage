import requests
import csv
import threading
import time
import os
U='/r/travel/comments/9prow2/best_cities_in_europe_to_visit_during_december/e8426wl/'
#https://www.reddit.com/r/travel/comments/9qfj2e/is_there_a_train_that_goes_from_las_vegas_to_san/e8978fj.json
url='https://www.reddit.com/r/travel/comments/9qfj2e/is_there_a_train_that_goes_from_las_vegas_to_san/e8978fj.json'
url='https://www.reddit.com'+U[:-1]+'.json'
#rzTYibpnVGihJKYEeA3SMmeHyQE
board='travel'
csv_file=open(board+'_.power.csv','w', encoding="utf-8")
writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}
files=os.listdir('.')
for p in files:
    if p.find('comment')>-1:
        print(p)
        with open(p,'r', encoding="utf-8") as csvfile:   
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV: 
                if len(row)>8 and row[8]!="-1" and row[1]!='[removed]' and row[0]!='AutoModerator':
                    U=row[8]
                    url='https://www.reddit.com'+U[:-1]+'.json'
                    data=requests.get(url, headers=headers).json()        
                    #print(apple)
                    try:
                        writer.writerow([data[1]['data']['children'][0]['data']['body'],data[1]['data']['children'][0]['data']['ups'],data[1]['data']['children'][0]['data']['downs'],data[1]['data']['children'][0]['data']['id'],data[1]['data']['children'][0]['data']['author'],data[1]['data']['children'][0]['data']['created']])        
                    except:
                        print(row)

#data=requests.get(url, headers=headers).json()
#print(data[1]['data']['children'][0]['data']['body'],data[1]['data']['children'][0]['data']['ups'],data[1]['data']['children'][0]['data']['downs'],data[1]['data']['children'][0]['data']['id'],data[1]['data']['children'][0]['data']['author'])