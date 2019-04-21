import os
files=[]


path=os.listdir('./')
for p in path:
    if p.find('.features')>-1:
        files.append(p)

import numpy as np
from sklearn.ensemble import RandomForestClassifier 
from sklearn import svm        
from sklearn import linear_model
from sklearn.cluster import KMeans 


for i in range(0,3): 
    Test=[]
    Train=[]
    header=""
    testFile=open('testSet.'+str(i),'w')
    trainFile=open('trainSet.'+str(i),'w')
    for p in files:
        fileSpec=p.split('.')
        if fileSpec[1]==str(i):     #Test
            file=open(p,'r').read().split('\n')
            header=file[0]
            for j in range(1,len(file)):
                Temp=[]
                if len(file[j])>0:
                    #row=file[j].split(',')
                    Test.append(file[j])
                    testFile.write(file[j]+'\n')
        else:
            file=open(p,'r').read().split('\n')
            header=file[0]
            for j in range(1,len(file)):
                Temp=[]
                if len(file[j])>0:
                    #row=file[j].split(',')
                    Train.append(file[j])
                    trainFile.write(file[j]+'\n')
    trainSet=[]
    trainLabel=[]

    testSet=[]
    testLabel=[]

    labelMap={}
    invLabelMap={}     
    j=0
    rf = RandomForestClassifier(n_jobs=20, random_state=0)               #<--------------------Change Model
    #rf=linear_model.LogisticRegression(C=1e5)				#Logistic Regression
    #rf=svm.SVC()		    
                    
    for r in Train:
        t=r.split(',')
        temp=[]
        for K in range(1,len(t)):
            t2=t[K]
            temp.append(float(t2))
        trainSet.append(np.array(temp))
        if t[0] not in labelMap:
            labelMap[t[0]]=j
            invLabelMap[j]=[t[0]]
            j=j+1
        trainLabel.append(labelMap[t[0]])
        
        
    for r in Test:
        t=r.split(',')
        temp=[]
        for K in range(1,len(t)):
            t2=t[K]
            temp.append(float(t2))
        
        if t[0] not in labelMap:
            labelMap[t[0]]=j
            invLabelMap[j]=[t[0]]
            j=j+1
        testSet.append(np.array(temp))
        testLabel.append(labelMap[t[0]])
    rf.fit(trainSet, trainLabel)    
    predictions=rf.predict(testSet)                                                 
    accuracy = 1-sum(np.array(testLabel)^predictions)/len(predictions)          #<-XORs testLabel and Predicted Labels
    print(accuracy)
    
    testFile.close()
    trainFile.close()