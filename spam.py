# -*- coding: utf-8 -*-
"""Untitled19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1anXK7qpcgMZ3rKDSAlljb_6BfSudjwn4
"""

import numpy as np
import pandas as pd

df=pd.read_csv('spam_ham_dataset.csv')

df.sample(5)

df.info()

df.rename(columns={'label':'target'},inplace=True)

df.head()

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

df['target'] = encoder.fit_transform(df['target'])

df.head()

df.rename(columns={'label_num':'target-2'},inplace=True)

df.head()

df.drop(columns=['target-2'],inplace=True)

df.isnull().sum()

df['target'].value_counts()

import matplotlib.pyplot as plt

plt.pie(df['target'].value_counts(), labels=['ham', 'spam'], autopct="%0.2f", wedgeprops=dict(width=0.4))
plt.gca().add_artist(plt.Circle((0,0),0.3,color='white'))
plt.title('Distribution of ham and spam')
plt.show()

df['num_characters'] = df['text'].apply(len)

df['num_words'] = df['text'].apply(lambda x: len(x.split()))

df['num_sentences'] = df['text'].apply(lambda x: len(x.split('.')))

overall_stats = df[['num_characters', 'num_words', 'num_sentences']].describe()
spam_stats = df[df['target'] == 1][['num_characters', 'num_words', 'num_sentences']].describe()
non_spam_stats = df[df['target'] == 0][['num_characters', 'num_words', 'num_sentences']].describe()

print("Overall Stats:")
print(overall_stats)
print("\nSpam Stats:")
print(spam_stats)
print("\nNon-Spam Stats:")
print(non_spam_stats)

"""# **EDA**"""

import seaborn as sns

df.replace([np.inf, -np.inf], np.nan, inplace=True)

plt.figure(figsize=(12,6))
sns.histplot(df[df['target'] == 0]['num_characters'])
sns.histplot(df[df['target'] == 1]['num_characters'],color='red')

plt.figure(figsize=(12,6))
sns.histplot(df[df['target'] == 0]['num_words'])
sns.histplot(df[df['target'] == 1]['num_words'],color='red')

sns.pairplot(df,hue='target')

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

df['text'] = df['text'].str.replace('Subject: ', '')

import nltk
nltk.download('punkt')

nltk.download('stopwords')

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

def ttext(text):
    # Convert text to lowercase
    text = text.lower()

    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Initialize Porter Stemmer
    ps = PorterStemmer()

    # Initialize list to store processed tokens
    processed_tokens = []

    # Iterate through tokens
    for token in tokens:
        # Check if token is alphanumeric
        if token.isalnum():
            # Check if token is not a stopword and not punctuation
            if token not in stopwords.words('english') and token not in string.punctuation:
                # Stem the token and add to processed_tokens list
                processed_tokens.append(ps.stem(token))

    # Join processed tokens and return as a string
    return " ".join(processed_tokens)

df.head()

ttext("hi my name is niyath")

ttext("I'm gonna be home soon and i don't want to talk about this stuff anymore tonight")

df['ttext'] = df['text'].apply(ttext)

df.head()

## more analysis

# spamlist = []
# for msg in df[df['target'] == 1]['ttext'].tolist():
#     for word in msg.split():
#         spamlist.append(word)

# hamlist = []
# for msg in df[df['target'] == 0]['ttext'].tolist():
#     for word in msg.split():
#         hamlist.append(word)

# len(spamlist)

# counter = Counter(spamlist)

# # Convert counter to a DataFrame and get the 30 most common items
# df = pd.DataFrame(counter.most_common(30))

# # Plot using Seaborn
# sns.barplot(x=df[0], y=df[1])
# plt.xticks(rotation='vertical')
# plt.show()

# len(hamlist)

# from collections import Counter

# counter = Counter(spamlist)

# df = pd.DataFrame(counter.most_common(30))

# sns.barplot(x=df[0], y=df[1])
# plt.xticks(rotation='vertical')
# plt.show()

# counter = Counter(hamlist)

# df = pd.DataFrame(counter.most_common(30))

# sns.barplot(x=df[0], y=df[1])
# plt.xticks(rotation='vertical')
# plt.show()

"""# **Model Building**

"""

import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score

tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['ttext']).toarray()

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

df.head()

tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['ttext']).toarray()

y = df['target'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_split=0.2,
                    verbose=1)

y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
precision = precision_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Confusion Matrix:\n", conf_matrix)
print("Precision:", precision)

from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

svc = SVC(kernel='sigmoid', gamma=1.0)
knc = KNeighborsClassifier()
mnb = MultinomialNB()
dtc = DecisionTreeClassifier(max_depth=5)
lrc = LogisticRegression(solver='liblinear', penalty='l1')
rfc = RandomForestClassifier(n_estimators=50, random_state=2)
abc = AdaBoostClassifier(n_estimators=50, random_state=2)
bc = BaggingClassifier(n_estimators=50, random_state=2)
etc = ExtraTreesClassifier(n_estimators=50, random_state=2)
gbdt = GradientBoostingClassifier(n_estimators=50, random_state=2)
xgb = XGBClassifier(n_estimators=50, random_state=2)

clfs = {
    'SVC' : svc,
    'KN' : knc,
    'NB': mnb,
    'DT': dtc,
    'LR': lrc,
    'RF': rfc,
    'AdaBoost': abc,
    'BgC': bc,
    'ETC': etc,
    'GBDT':gbdt,
    'xgb':xgb
}

def train_classifier(clf,X_train,y_train,X_test,y_test):
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test,y_pred)
    precision = precision_score(y_test,y_pred)

    return accuracy,precision

train_classifier(svc,X_train,y_train,X_test,y_test)

accuracy_scores = []
precision_scores = []

for name, clf in clfs.items():
    # Train the classifier and obtain accuracy and precision scores
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    current_accuracy = accuracy_score(y_test, y_pred)
    current_precision = precision_score(y_test, y_pred)

    # Print the results
    print("For", name)
    print("Accuracy:", current_accuracy)
    print("Precision:", current_precision)

    # Append scores to lists
    accuracy_scores.append(current_accuracy)
    precision_scores.append(current_precision)

performance_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy':accuracy_scores,'Precision':precision_scores}).sort_values('Precision',ascending=False)

performance_df

performance_df1 = pd.melt(performance_df, id_vars = "Algorithm")

performance_df1

plt.figure(figsize=(10, 6))
sns.pointplot(x='Algorithm', y='value', hue='variable', data=performance_df1, dodge=True, markers=["o", "x"], linestyles=["-", "--"])
plt.ylim(0.5, 1.0)
plt.xticks(rotation='vertical')
plt.show()

sns.catplot(x = 'Algorithm', y='value',
               hue = 'variable',data=performance_df1, kind='bar',height=5)
plt.ylim(0.5,1.0)
plt.xticks(rotation='vertical')
plt.show()plt.figure(figsize=(10, 6))
sns.boxplot(x='Algorithm', y='value', hue='variable', data=performance_df1)
plt.ylim(0.5, 1.0)
plt.xticks(rotation='vertical')
plt.show()

custom_palette = ["#99ff99", "#ffff99"]

sns.catplot(x='Algorithm', y='value', hue='variable', data=performance_df1, kind='bar', height=5, palette=custom_palette)
plt.ylim(0.5, 1.0)
plt.xticks(rotation='vertical')
plt.show()

temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_max_ft_3000':accuracy_scores,'Precision_max_ft_3000':precision_scores}).sort_values('Precision_max_ft_3000',ascending=False)

temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_scaling':accuracy_scores,'Precision_scaling':precision_scores}).sort_values('Precision_scaling',ascending=False)

new_df = performance_df.merge(temp_df,on='Algorithm')
new_df_scaled = new_df.merge(temp_df,on='Algorithm')

temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_num_chars':accuracy_scores,'Precision_num_chars':precision_scores}).sort_values('Precision_num_chars',ascending=False)

new_df_scaled.merge(temp_df,on='Algorithm')

from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, precision_score

classifiers = {
    'svm': SVC(kernel='sigmoid', gamma=1.0, probability=True),
    'nb': MultinomialNB(),
    'et': ExtraTreesClassifier(n_estimators=50, random_state=2)
}

voting = VotingClassifier(estimators=list(classifiers.items()), voting='soft')

voting.fit(X_train, y_train)
y_pred = voting.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)

"""# **Stacking**"""

estimators=[('svm', svc), ('nb', mnb), ('et', etc)]
final_estimator=RandomForestClassifier()

from sklearn.ensemble import StackingClassifier

clf = StackingClassifier(estimators=estimators, final_estimator=final_estimator)

clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)

print("Accuracy",accuracy_score(y_test,y_pred))
print("Precision",precision_score(y_test,y_pred))

