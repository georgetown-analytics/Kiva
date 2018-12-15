import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import f1_score, log_loss, roc_curve, precision_recall_curve, auc, make_scorer, recall_score, accuracy_score, precision_score, confusion_matrix

startTime = time.time()

df=pd.read_csv('data.csv')
y=df['fol'].sample(frac=0.1, random_state=1)
X=df.sample(frac=0.1, random_state=1).drop('fol',axis=1)
X=scale(X)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state=1)

seed=1

model = [
            'lr',
            'GBC'
        ]

clf = [
    LogisticRegression(random_state=seed, max_iter=1000),
    GradientBoostingClassifier(random_state=seed),
      ]

params = {
            model[0]: {'C':np.logspace(-4, 4, 5), 'solver':['liblinear','saga'], 'penalty': ['l1','l2'] },
            model[1]:{'learning_rate':[0.01,0.005], 'n_estimators':[10,200]}
         }
for name, estimator in zip(model,clf):
    print(name)
    clf = GridSearchCV(estimator, params[name], scoring='neg_log_loss', refit='True', n_jobs=-1, cv=5)
    clf.fit(X_train, y_train)
    print("best params: " + str(clf.best_params_))
    print("best scores: " + str(clf.best_score_))
    estimates = clf.predict_proba(X_test)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print("Accuracy: {:.4%}".format(acc))

endTime = time.time()
print('Took %s seconds to calculate.' % (endTime - startTime))
