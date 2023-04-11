#!/usr/bin/env python
# coding: utf-8

# In[3]:


# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 13:23:52 2021

@author: Nick88stam
"""

import numpy as np
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from matplotlib import pyplot as plt
import csv

scores=np.zeros(5)
mean=np.zeros(5)
l=[0.1, 1, 10, 100, 200]

y=np.zeros(150)
x=np.zeros((150,13))
i=0

with open('train.csv','r') as csvfile:
    reader=csv.reader(csvfile)
    next(reader)
    for row in reader:
        y[i]=row[0]
        for j in range(0,13):
            x[i][j]=row[j+1]
        i=i+1

for k in range(0,5):
    model=Ridge(alpha=l[k], fit_intercept=False)

    cv=KFold(n_splits=10)

    scores=cross_val_score(model, x, y, scoring='neg_root_mean_squared_error', cv=cv, n_jobs=-1)
    scores=np.absolute(scores)
    mean[k]=np.mean(scores)

with open('Predictions.csv',mode='w',newline='') as predictionfile: #writing predictions
    predictionwriter=csv.writer(predictionfile)
    for k in range(0,5):
        predictionwriter.writerow([mean[k]])


# In[ ]:




