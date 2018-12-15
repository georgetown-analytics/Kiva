import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

df=pd.read_csv('data.csv')
y=df['fol']
X=df.drop('fol',axis=1)
print('Instances: ', len(X), ' Number of features: ', len(X.columns))

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state=1)

model=LogisticRegression().fit(X_train, y_train)

#Pickle
pickle.dump(model, open('kiva_predictor.pkl', 'wb'))
pickle.dump(model, open('../flask_app/kiva_predictor.pkl', 'wb'))

print('model dumped to pickle')
