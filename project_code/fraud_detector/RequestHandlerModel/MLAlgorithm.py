# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 15:24:47 2020

@author: Bjarne
"""

"""
Dieses File ermöglicht das einfache austauschen von Modellen im Retrain-Prozess

"""
from sklearn.ensemble import RandomForestClassifier
#from sklearn.linear_model import LogisticRegression
#from sklearn.ensemble import GradientBoostingClassifier

Model = RandomForestClassifier
params = {'bootstrap': [True],
 'max_depth': [7,8],
 'max_features': ['auto'],
 'min_samples_leaf': [2,4,6],
 'min_samples_split': [80,100],
 'n_estimators': [80,100,120]}
