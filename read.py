import json
import csv
import time as time


def helper(path):
    #path='pol.csv'

    f1=open(path+'_2013-1','w',encoding='ISO-8859-1')
    f1=csv.writer(f1,delimiter=',', lineterminator='\n')
    f2=open(path+'_2013-2','w',encoding='ISO-8859-1')
    f2=csv.writer(f2,delimiter=',', lineterminator='\n')

    f3=open(path+'_2014-1','w',encoding='ISO-8859-1')
    f3=csv.writer(f3,delimiter=',', lineterminator='\n')

    f4=open(path+'_2014-2','w',encoding='ISO-8859-1')
    f4=csv.writer(f4,delimiter=',', lineterminator='\n')


    f5=open(path+'_2015-1','w',encoding='ISO-8859-1')
    f5=csv.writer(f5,delimiter=',', lineterminator='\n')
    f6=open(path+'_2015-2','w',encoding='ISO-8859-1')
    f6=csv.writer(f6,delimiter=',', lineterminator='\n')

    f7=open(path+'_2016-1','w',encoding='ISO-8859-1')
    f7=csv.writer(f7,delimiter=',', lineterminator='\n')
    f8=open(path+'_2016-2','w',encoding='ISO-8859-1')
    f8=csv.writer(f8,delimiter=',', lineterminator='\n')

    f9=open(path+'_2017-1','w',encoding='ISO-8859-1')
    f9=csv.writer(f9,delimiter=',', lineterminator='\n')
    f10=open(path+'_2017-2','w',encoding='ISO-8859-1')
    f10=csv.writer(f10,delimiter=',', lineterminator='\n')

    f11=open(path+'_2018-1','w',encoding='ISO-8859-1')
    f11=csv.writer(f11,delimiter=',', lineterminator='\n')
    f12=open(path+'_2018-2','w',encoding='ISO-8859-1')
    f12=csv.writer(f12,delimiter=',', lineterminator='\n')

    f13=open(path+'_2019-1','w',encoding='ISO-8859-1')
    f13=csv.writer(f13,delimiter=',', lineterminator='\n')





    x=0
    y=0
    with open(path,'r',encoding='ISO-8859-1') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:    
            #x=x+1
            
            #   print(row)
            #else:
            #    break
            if len(row)>28:
                x=x+1
                R=row[:22]+[' '.join(row[22:-5])]+row[-5:]
            if len(row)==28:
                R=row
            if len(row)>=28 and str(row[4]).isnumeric()==True:
                if int(row[4])>1356998400 and int(row[4])<=1372636800:
                    f1.writerow(R)
                    
                    
                if int(row[4])>1372636800 and int(row[4])<=1388534400:
                    f2.writerow(R)
                    
                if int(row[4])>1388534400 and int(row[4])<=1404172800:
                    f3.writerow(R)

                if int(row[4])>1404172800 and int(row[4])<=1420070400:
                    f4.writerow(R)
                
                if int(row[4])>1420070400 and int(row[4])<=1435708800:
                    f5.writerow(R)
                    
                if int(row[4])>1435708800 and int(row[4])<=1451606400:
                    f6.writerow(R)
                    
                if int(row[4])>1451606400 and int(row[4])<=1467331200:
                    f7.writerow(R)
                
                if int(row[4])>1467331200 and int(row[4])<=1483228800:
                    f8.writerow(R)
                    
                if int(row[4])>1483228800 and int(row[4])<=1498867200:
                    f9.writerow(R)
                    
                if int(row[4])>1498867200 and int(row[4])<=1514764800:
                    f10.writerow(R)

                if int(row[4])>1514764800 and int(row[4])<=1530403200:
                    f11.writerow(R)

                if int(row[4])>1530403200 and int(row[4])<=1546300800:
                    f12.writerow(R)

                if int(row[4])>1546300800:
                    f13.writerow(R)


helper('adv.csv')
helper('hr.csv')
helper('s4s.csv')
helper('trv.csv')
helper('f.csv')
helper('o.csv')
helper('sp.csv')
helper('tv.csv')
helper('tg.csv')
helper('x.csv')