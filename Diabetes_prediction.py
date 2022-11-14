# -*- coding: utf-8 -*-
"""technolabs_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xGk88kpfs4dYHEAM5pC8E2qgu83-_YVw

**Problem Statement: Prediction of Diabetes using Machine Learning Algorithm**

**Import Important Dependencies**
"""

#importing libraries
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/drive/MyDrive/technolabs_assi/diabetes.csv')

"""**Data Preprocessing**"""

df.head()

df1 = df.drop('age',axis=1)
df1

df1.shape

#Handling Duplicates
df1.drop_duplicates()

df1.shape
#There are not duplicate values in dataset

df1.describe()

"""**Checking for Measures of Dispersion**"""

df1.std()
# Here std dev value for 'weight' is indicating that data is spread widely from it's mean

df1.var()

df1.skew()
# Values of skewness for all the features are != 0 so the data is not normally distributed

df1.kurt()

#Checking for Null values
df1.isnull().values.any()

df1.isnull().sum()

# unique values in diabetes coloumn. 1 corresponds to positive case and 0 to negative.
print(df1.diabetes.unique())

df1.info()

#We will first of all check all the missing value Percentage for each of the column
features_with_na = [features for features in df1.columns if df1[features].isnull().sum()>1]
# Print the % of missing values in each feature
for feature in features_with_na:
    print(feature, np.round(df1[feature].isnull().mean(),4),'%missing values')

"""**Weight column consists of 2318 missing values in the column**:

**Exploratory Data Analysis**

**1)Visualization**

**a)Univariate Analysis**
"""

df2 = df1.drop(['cholesterol','gluc','pressure','gender'],axis=1)
df2

"""**Checking for outliers using Boxplot**"""

#Plotting the boxplot & Histplot
for i in df2.columns:
    plt.figure()
    plt.tight_layout()
    sns.set(rc={"figure.figsize":(8, 5)})
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True)
    plt.gca().set(xlabel= i,ylabel='Frequency')
    sns.boxplot(df2[i], ax=ax_box , linewidth= 1.0)
    sns.histplot(df2[i], ax=ax_hist , bins = 10,kde=True)
    plt.show()

#Plotting the violinplot
for i in df2.columns:
    plt.figure()
    plt.tight_layout()
    sns.set(rc={"figure.figsize":(8, 5)})
    f, (ax_vio, ax_hist) = plt.subplots(2, sharex=True)
    plt.gca().set(xlabel= i,ylabel='Frequency')
    sns.violinplot(df2[i], ax=ax_vio , linewidth= 1.0)
    sns.histplot(df2[i], ax=ax_hist , bins = 10,kde=True)

#Checking the data whether balanced or imbalanced
# diabetes countplot
sns.countplot(x = 'diabetes',data = df2)
# diabetes = 1, no_diabetes = 0
# Following countplot indicates that the data consists of the people with diabetes is less than 30% as compared to no_diabetes. So our data is imbalanced data

"""**Bivariate Analysis**"""

# Scatter plot matrix 
from pandas.plotting import scatter_matrix
import pandas.plotting
scatter_matrix(df, figsize = (20, 20));

# Pairplot 
sns.pairplot(data = df2, hue = 'diabetes')
plt.show()

#Pearson Correlation 
plt.figure(figsize=(10, 12))
cor = df2.corr()
sns.heatmap(cor,annot=True, cmap = plt.cm.CMRmap_r)
plt.show()

#with the follwing function we can select highly correlated features 
#it will remove the features that is correlated with anything other feature
def correlation(df2, threshold):
    col_corr = set()   #set of all the names of correlated columns
    corr_matrix = df2.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (corr_matrix.iloc[i,j]) > threshold: #we interested in absolute coefficient values 
                colname = corr_matrix.columns[i]   #getting the name of column
                col_corr.add(colname)
    return col_corr

corr_features = correlation(df2, 0.7)
len(set(corr_features))

"""**Handling Missing Values**"""

df2['weight'] = df2['weight'].fillna(df2['weight'].median())

"""**For Handling missing values of weight I have chosen median imputation. Because Weight column consists of to many outliers, if we use the mean imputation the outliers of column will be affected**"""

df2

"""**Feature Engineering**

**Label Encoding for categorical features in the dataset such as cholesterol,gender,glucose, pressure**
"""

df_numeric = df2[['id', 'smoke', 'alco', 'active', 'age1', 'height','weight','diabetes']]
df_categorical = df1[['cholesterol', 'gluc', 'pressure', 'gender' ]]

df_categorical.head()

df1.columns

from sklearn.preprocessing import LabelEncoder

diabetes_encoder = LabelEncoder()

le = LabelEncoder()

# apply "le.fit_transform"
df_encoded = df_categorical.apply(le.fit_transform)
print(df_encoded)

data = pd.concat([df_numeric,df_encoded],axis=1)
data



data.columns

data.isnull().sum()
# No missing values remainig in the dataset

y = data['diabetes'].astype(int)
#Seperate object from input features
X = data.drop('diabetes',axis=1)

"""**As data consits of diabetes with positive = 1 is very less than diabetes with negative =0 in proportion. So the data is imbalanced which may create the problem of correct prediction of diabetes and which may give faulty prediction. So we need to perform oversampling to make data balanced.**"""

from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler()
X_os, y_os = ros.fit_resample(X,y)

X_os.shape, y_os.shape

"""**Outelier Treatment**"""

!pip install feature-engine

from feature_engine.outliers import Winsorizer

IQR = data.quantile(0.75) - data.quantile(0.25)
lower_limit = data.quantile(0.25) - (IQR * 1.5)
upper_limit = data.quantile(0.75) + (IQR * 1.5)

for i in data:
    winsor = Winsorizer(capping_method='iqr',
                            tail='both',
                            fold=1.5,
                            variables=[i])
    data[i] = winsor.fit_transform(data[[i]])

import seaborn as sns
for feature in data:
    sns.boxplot(data[feature])
    plt.show()

"""**Now data is free of Outliers**"""





"""**Split the dataframe into X and y**"""

X

y

"""**Apply Feature Scaling**"""

# Apply Standard Scaler
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X)
SSX = scaler.transform(X)

"""**Train Test Split**"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(SSX, y, test_size=0.2, random_state = 7)

X_train.shape, y_train.shape

X_test.shape, y_test.shape

X_train

y_train

# Creating a CSV file
data.to_csv("diabetes_cleaned1", index=False, encoding = "utf-8")

import pickle
pickle.dump(scaler, open('scaling1.pkl', 'wb'))

"""**Build the Classifcation Algorithm**

> Indented block

**1)Logistic Regression**
"""

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(solver='liblinear',multi_class='ovr')
lr.fit(X_train, y_train)

"""**2)KNearestneighbourClassifier(KNN)**"""

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

"""**3)Naive-Bayes Classifier**"""

from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(X_train, y_train)

"""**4)Support Vector Machine**"""

from sklearn.svm import SVC
sv = SVC()
sv.fit(X_train, y_train)

"""**5)DecisionTree**"""

from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

"""**6)Random Forest**"""

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

"""**Making Prediction**

**a) Making Prediction by Logistic Regression**
"""

lr_pred = lr.predict(X_test)
lr_pred

lr_pred.shape

"""**b) Making Prediction by KNN**"""

knn_pred = knn.predict(X_test)

knn_pred.shape

"""**c) Making Prediction by NB**


"""

nb_pred = nb.predict(X_test)

nb_pred.shape

"""**d) Making Prediction by SVM**"""

svm_pred = sv.predict(X_test)

svm_pred.shape

"""**Making Prediction by DT**"""

dt_pred = dt.predict(X_test)

dt_pred.shape

"""****Making Prediction by RF**"""

rf_pred = rf.predict(X_test)

rf_pred.shape

"""**Model Evaluation**

**Train & test Score**
"""

# Train and Test Score for Logistic Regression
from sklearn.metrics import accuracy_score
print("Train Accuracy of Logistic Regression", lr.score(X_train, y_train)*100)
print("Accuracy (Test) score of Logistic Regression", lr.score(X_test, y_test)*100)
print("Accuacy (Test) score of Logistic Regression",accuracy_score(y_test, lr_pred)*100)

# Train and Test Score for NB
print("Train Accuracy of NB", nb.score(X_train, y_train)*100)
print("Accuracy (Test) score of NB", nb.score(X_test, y_test)*100)
print("Accuacy (Test) score of NB",accuracy_score(y_test, nb_pred)*100)

# Train and Test Score for SVM
print("Train Accuracy of SVM", sv.score(X_train, y_train)*100)
print("Accuracy (Test) score of SVM", sv.score(X_test, y_test)*100)
print("Accuacy (Test) score of svm",accuracy_score(y_test, svm_pred)*100)

# Train and Test Score for DT
print("Train Accuracy of DT", dt.score(X_train, y_train)*100)
print("Accuracy (Test) score of dt", dt.score(X_test, y_test)*100)
print("Accuacy (Test) score of dt",accuracy_score(y_test, dt_pred)*100)

# Train and Test Score for RF
print("Train Accuracy of RF", rf.score(X_train, y_train)*100)
print("Accuracy (Test) score of RF", rf.score(X_test, y_test)*100)
print("Accuacy (Test) score of RF",accuracy_score(y_test, rf_pred)*100)

"""**Confusion Matrix**

**For Logistic Regression**
"""

from sklearn.metrics import classification_report,confusion_matrix
cm = confusion_matrix(y_test, lr_pred)
cm

sns.heatmap(confusion_matrix(y_test, lr_pred),annot=True, fmt = "d")

TN = cm[0,0]
FP = cm[0,1]
FN = cm[1,0]
TP = cm[1,1]

TN, FP, FN, TP

#Making the confusion matrix of Logistic Regression 
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score,roc_auc_score, roc_curve
cm = confusion_matrix(y_test, lr_pred)

print('TN - True Negative {}'.format(cm[0,0]))
print('FP - False Positive {}'.format(cm[0,1]))
print('FN - False Negative {}'.format(cm[1,0]))
print('TP - True Positive {}'.format (cm[1,1]))
print('Accuracy Rate: {}'.format(np.divide(np.sum([cm[0,0],cm[1,1]]),np.sum(cm))*100))
print('Misclassification Rate: {}'.format(np.divide(np.sum([cm[0,1],cm[1,0]]),np.sum(cm))*100))

plt.clf()
plt.imshow(cm,interpolation='nearest',cmap=plt.cm.Wistia)
classNames = ['0','1']
plt.title('Confusion Matrix of Logistic Regression')
plt.ylabel('Actual(true) values')
plt.xlabel('Predicted values')
tick_marks = np.arange(len(classNames))
plt.xticks(tick_marks,classNames,rotation=45)
plt.yticks(tick_marks,classNames)
s = [['TN','FP'],['FN','TP']]
for i in range(2):
    for j in range(2):
      plt.text(j,i, str(s[i][j]+" = "+str(cm[i][j])))
plt.show()

pd.crosstab(y_test,lr_pred,margins=True)

"""**Classification Report**"""

print('Classifiaction Report of Logistic Regression: \n',classification_report(y_test,lr_pred,digits=4))

"""**Conclusion from Classification Report**

**1)Model identifies the diabetes is positive = 1 and  it is correct 80% of the time.**

**2)Model identifies the diabetes is negative = 0 and  it is correct 88% of the time.**

**3)Our model has a recall of 0.9487—in other words, it correctly identifies 94.87% of all negative diabetes patients**

**4)Our model has a recall of 0.6298—in other words, it correctly identifies 62.98% of all positive diabetes patients**

**ROC AUC Curve**
"""

#Area under Curve
auc = roc_auc_score(y_test,lr_pred)
print("ROC AUC SCORE of Logistic Regression is", auc)

fpr, tpr , thresholds = roc_curve(y_test, lr_pred)
plt.plot(fpr, tpr, color='orange', label = 'ROC')
plt.plot([0,1],[0,1], color = 'darkblue',linestyle = '--', label='ROC curve (area = %0.2f)' %auc)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characterstics Curve of Logistic Regression')
plt.legend()
plt.grid()
plt.show()

"""**The ROC curve shows the trade-off between sensitivity (or TPR) and specificity (1 – FPR). Logistic Regression Classifiers that give curves closer to the top-left corner indicate a better performance.**

**Confusion Matrix of SVM**
"""

from sklearn.metrics import classification_report,confusion_matrix
cm1 = confusion_matrix(y_test, svm_pred)
cm1

sns.heatmap(confusion_matrix(y_test, svm_pred),annot=True, fmt = "d")

TN = cm1[0,0]
FP = cm1[0,1]
FN = cm1[1,0]
TP = cm1[1,1]

TN, FP, FN, TP

print('Classifiaction Report of SVM: \n',classification_report(y_test,svm_pred,digits=4))

fpr, tpr , thresholds = roc_curve(y_test, svm_pred)
plt.plot(fpr, tpr, color='orange', label = 'ROC')
plt.plot([0,1],[0,1], color = 'darkblue',linestyle = '--', label='ROC curve (area = %0.2f)' %auc)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characterstics Curve of SVM')
plt.legend()
plt.grid()
plt.show()

import pickle
with open('model_pkl.pkl', 'wb') as files:
    pickle.dump(sv, files)

"""**Hyperparameter Optimization**"""

## Hyper Parameter Optimization

params={
 "learning_rate"    : [0.05, 0.10, 0.15, 0.20, 0.25, 0.30 ] ,
 "max_depth"        : [ 3, 4, 5, 6, 8, 10, 12, 15],
 "min_child_weight" : [ 1, 3, 5, 7 ],
 "gamma"            : [ 0.0, 0.1, 0.2 , 0.3, 0.4 ],
 "colsample_bytree" : [ 0.3, 0.4, 0.5 , 0.7 ]
    
}

## Hyperparameter optimization using RandomizedSearchCV
from sklearn.model_selection import RandomizedSearchCV
import xgboost

classifier=xgboost.XGBClassifier()

random_search=RandomizedSearchCV(classifier,param_distributions=params,n_iter=5,scoring='roc_auc',n_jobs=-1,cv=5,verbose=3)
random_search

from datetime import datetime
def timer(start_time=None):
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print('\n Time taken: %i hours %i minutes and %s seconds.' % (thour, tmin, round(tsec, 2)))

# Here we go
start_time = timer(None) # timing starts from this point for "start_time" variable
random_search.fit(X_train,y_train.ravel())
timer(start_time) # timing ends here for "start_time" variable

random_search.best_estimator_

classifier = xgboost.XGBClassifier(colsample_bytree=0.7, gamma=0.1, learning_rate=0.3, max_depth=5)

classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

cm_h = confusion_matrix(y_test, y_pred)
score = accuracy_score(y_test, y_pred)
print(cm_h)
print(score)

from sklearn.model_selection import cross_val_score
score = cross_val_score(classifier,X_train, y_train.ravel(),cv=10)
score

score.mean()

"""**After Hyperparameter Optimization using RandomizedSearchCV  the accuracy score is improved to 0.9773 and best_estimator is found to XGBClassifier**

**Out of 6 Classification algorithm SVM has given the good accuracy than others so SVM is used to build the ML model for predicting Diabetes of Patient**
"""
