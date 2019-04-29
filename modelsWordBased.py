import os
files=[]


path=os.listdir('./')
for p in path:
    if p.find('.token.features')>-1:
        files.append(p)

import numpy as np
from sklearn.ensemble import RandomForestClassifier 
from sklearn import svm        
from sklearn import linear_model
from sklearn.cluster import KMeans 
import pickle
i=0
for i in range(0,3): 
    Test={}
    Train={}
    header=[]
    testFile=open('word.testSet.'+str(i),'w')
    trainFile=open('word.trainSet.'+str(i),'w')
    for p in files:
        fileSpec=p.split('.')
        
        
        if fileSpec[2]==str(i):     #Test
            dict=pickle.load(open(p,'rb'))
            
            for d in dict:
                if d not in Test:
                    Test[d]=dict[d]
                    
                    

        else:
            dict=pickle.load(open(p,'rb'))
            for d in dict:
                if d not in Train:
                    Train[d]=dict[d]
            
                header.extend(dict[d].keys())

    head=list(set(header))
    head.sort()

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
        temp=[]
        t='.'.join(r.split('.')[1:])
        Write=[]
        if t not in labelMap:
            labelMap[t]=j
            invLabelMap[j]=[t]
            j=j+1
        trainLabel.append(labelMap[t])
        Write.append(t)
        
        
        for s in head:
            if s not in Train[r]:
                temp.append(0)
                Write.append(str(0))
                
            else:
                temp.append(Train[r][s])
                Write.append(str(Train[r][s]))
                
        trainFile.write(','.join(Write)+'\n')
        trainSet.append(np.array(temp))            


        
    for r in Test:
        Write=[]
        t='.'.join(r.split('.')[1:])
        if t in labelMap:
            testLabel.append(labelMap[t])
            Write.append(t)
            temp=[]
            
            for s in head:
                if s not in Test[r]:
                    temp.append(0)
                    Write.append(str(0))
                else:
                    temp.append(Test[r][s])
                    Write.append(str(Test[r][s]))
                    
            testFile.write(','.join(Write)+'\n')
            testSet.append(np.array(temp))            
        
    rf.fit(trainSet, trainLabel)    
    predictions=rf.predict(testSet)                                                 
    accuracy = 1-sum(np.array(testLabel)^predictions)/len(predictions)          #<-XORs testLabel and Predicted Labels
    print(accuracy)

    testFile.close()
    trainFile.close()