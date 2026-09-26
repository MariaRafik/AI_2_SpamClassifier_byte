import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB      #for text analysis
from sklearn.metrics import accuracy_score, precision_score , recall_score, f1_score
import re      #clean punctuation

df=pd.read_csv('spam_ham_dataset.csv')

X=df['text']
y=df['label_num']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

vecto=TfidfVectorizer(stop_words='english')      #removes useless words
X_train_tfidf= vecto.fit_transform(X_train)     #learn vocab from training text and transform it to number matrix
X_test_tfidf=vecto.transform(X_test)           #transform test text to numbers using learned vocab

model=MultinomialNB()
model.fit(X_train_tfidf,y_train)

y_pred=model.predict(X_test_tfidf)
print('Model Evaluation Metrics')
print(f"Accuracy:{accuracy_score(y_test,y_pred)*100:.4f}% , Precision:{precision_score(y_test,y_pred)*100:.4f}%")
print(f"Recall:{recall_score(y_test,y_pred)*100:.4f}% , F1-Score:{f1_score(y_test,y_pred)*100:.4f}%\n")

feature_names=vecto.get_feature_names_out()   #full list of learned vocab
ham_log_probs= model.feature_log_prob_[0]     #prob of each word in safe email
spam_log_probs=model.feature_log_prob_[1]     #prob of each word in spam email

print('Phising Simulator Ready')
while True:
    user_in=input('\nEnter an email to scan or type EXIT to quit:')
    if user_in.lower()=='exit':
        break
    in_tfidf=vecto.transform([user_in])
    spam_score=model.predict_proba(in_tfidf)[0][1]*100
    trigger_words=[]
    clean_input=re.sub(r'[^\w\s]','',user_in.lower()).split()

    for word in clean_input:
        if word in feature_names:
            word_idx=np.where(feature_names==word)[0][0]
            if spam_log_probs[word_idx]>ham_log_probs[word_idx]:
                trigger_words.append(word)

    print(f"Spam Probability Score: {spam_score:.2f}%")

    if spam_score>50.0:
        print(f"Status: WARNING! Phising attempt detected")
        print(f"TRIGGER KEYWORDS: {', '.join(set(trigger_words))}")

    else:
        print('Status: Clean, No major threats detected')

