import os
files=[]
import math
from nltk.corpus import stopwords
sp=stopwords.words('english')
sp

styleFile=os.listdir('./style/')
sFile=[]
for s in styleFile:
    s1=s.split('.')
    sFile.append('.'.join(s1[:-1]))

path=os.listdir('./unigrams/')
for p in path:
    if p.find('.token')>-1 and '.'.join(p.split('.')[:-1]) in sFile:
        files.append(p)
        

import numpy as np
from sklearn.ensemble import RandomForestClassifier 
from sklearn import svm        
from sklearn import linear_model
from sklearn.cluster import KMeans 
import pickle
from collections import Counter
i=0
for i in range(0,3): 
    Test={}
    Train={}
    header=[]

    for p in files:
        fileSpec=p.split('.')
        
        dict=pickle.load(open('./unigrams/'+p,'rb'))
        diction2=dict[list(dict.keys())[0]]
            
        if fileSpec[-3]==str(i):     #Test
            Test[p]=diction2
                    
                    

        else:
            Train[p]=diction2
            
            header.extend(diction2.keys())

    #head=list(set(header))
    head1=list(set(header))
    
    
    head=[]
    for h in head1:
        if h not in sp:
            head.append(h)
            
    
    head.sort()
    #print(len(head1))
    print(len(head))
    trainSet=[]
    trainLabel=[]

    testSet=[]
    testLabel=[]

    labelMap={}
    invLabelMap={}     
    j=0
    #rf = RandomForestClassifier(n_jobs=20, random_state=0)               #<--------------------Change Model
    rf=linear_model.LogisticRegression(C=1e5)				#Logistic Regression
    #rf=svm.SVC()		    
    IDFr={}
    IDFs={}

    IDFrList=[]
    IDFsList=[]
    #print(Train.keys())
    for r in Train:
        IDFrList.extend(list(Train[r].keys()))
        '''
        for s in Train[r]:
            if s not in IDFr:
                IDFr[s]=0
            IDFr[s]=IDFr[s]+1
        '''
    print('Train PreCounter')    
    for r in Test:
        
        IDFsList.extend(list(Test[r].keys()))
        
        

        '''    
        
        for s in Test[r]:
            if s not in IDFs:
                IDFs[s]=0
            IDFs[s]=IDFs[s]+1
        '''
    print('Test PreCounter')    
    IDFr=Counter(IDFrList)    
    print('Train Counter')    
    IDFs=Counter(IDFsList)    
    print('Test PreCounter')    
    for r in Train:
        #print(r)
        temp=[]
        t='.'.join(r.split('.')[:2])
        Write=[]
        #print(t)
        if t not in labelMap:
            labelMap[t]=j
            invLabelMap[j]=[t]
            j=j+1
        trainLabel.append(labelMap[t])
        
        
        
        for s in head:
            if s not in Train[r]:
                temp.append(0)
        
                
            else:
                temp.append(Train[r][s]*math.log(len(Train)/IDFr[s]))
        
                
        trainSet.append(np.array(temp))            

    print(labelMap)
    #print(Test.keys())
    for r in Test:
        Write=[]
        t='.'.join(r.split('.')[:2])
        #print(t)
        if t in labelMap:
            testLabel.append(labelMap[t])
            Write.append(t)
            temp=[]
            
            for s in head:
                if s not in Test[r]:
                    temp.append(0)
                    
                else:
                    temp.append(Test[r][s]*math.log(len(Test)/IDFs[s]))
                    
                    
            
            testSet.append(np.array(temp))            
    print(testLabel)    
    rf.fit(trainSet, trainLabel)    
    predictions=rf.predict(testSet)                                                 
    accuracy=0
    Cc=0
    Conf={}
    for X in range(0,len(testLabel)):
        if testLabel[X] not in Conf:
            Conf[testLabel[X]]={}
        if predictions[X] not in Conf[testLabel[X]]:
            Conf[testLabel[X]][predictions[X]]=0
        Conf[testLabel[X]][predictions[X]]=Conf[testLabel[X]][predictions[X]]+1
        Conf[testLabel[X]]
        if int(testLabel[X])==int(predictions[X]):
            accuracy=accuracy+1
        Cc=Cc+1 
    D={}

    for c in testLabel:
        
        if c not in D:
            D[c]=0
        D[c]=D[c]+1



    for d in D:
        print(invLabelMap[d],d,D[d])
    print(accuracy,float(Cc))
    for c in Conf:
        for d in Conf[c]:
            print(invLabelMap[c],'|\t',invLabelMap[d],Conf[c][d])

