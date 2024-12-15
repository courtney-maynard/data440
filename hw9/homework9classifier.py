import sqlite3 as sqlite
import re
import os
import math

import prettytable
from prettytable import PrettyTable

# NAIVE BAYES CLASSIFIER ADAPTED FROM COLAB NOTEBOOK
class basic_classifier:

    def __init__(self,getfeatures,filename=None):
        # Counts of feature/category combinations
        self.fc={}
        # Counts of documents in each category
        self.cc={}
        self.getfeatures=getfeatures
        
    # Increase the count of a feature/category pair  
    def incf(self,f,cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat]+=1
    
    # Increase the count of a category  
    def incc(self,cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat]+=1  

    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # The number of items in a category
    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # The total number of items
    def totalcount(self):
        return sum(self.cc.values())

    # The list of all categories
    def categories(self):
        return self.cc.keys()

    def train(self,item,cat):
        features=self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f,cat)

        # Increment the count for this category
        self.incc(cat)

    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0

        # The total number of times this feature appeared in this 
        # category divided by the total number of items in this category
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # Calculate current probability
        basicprob=prf(f,cat)

        # Count the number of times this feature has appeared in
        # all categories
        totals=sum([self.fcount(f,c) for c in self.categories()])

        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp



class naivebayes(basic_classifier):   # change for basic_classifier

    def __init__(self,getfeatures):   
        basic_classifier.__init__(self,getfeatures)  # change for basic_classifier
        self.thresholds={}

    def docprob(self,item,cat):
        features=self.getfeatures(item)   

        # Multiply the probabilities of all the features together
        p=1
        for f in features: p*=self.weightedprob(f,cat,self.fprob)
        return p

    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t
        
    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=None):
        probs={}
        # Find the category with the highest probability
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max: 
                max=probs[cat]
                best=cat

        # Make sure the probability exceeds threshold*next best
        for cat in probs:
            if cat==best: continue
            if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best
    
def getwords(doc):
    splitter=re.compile('\W+')  # different than book
    #print (doc)
    # Split the words by non-alpha characters
    words=[s.lower() for s in splitter.split(doc) 
            if len(s)>2 and len(s)<20]
    
    # Return the unique set of words only
    uniq_words = dict([(w,1) for w in words])

    return uniq_words


## MY CODE FOR IMPLEMENTATION

'''
load_emails(folder):
    - loads in all of my email text files from my respective folders
    - uses the naming conventions i established for my files in order
    to properly set up email and label pairs
    
    returns three lists: the email file name, the email content, and the email labels
'''
def load_emails(folder):
    email_files = []
    text_emails = []
    email_labels = []
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            if filename.startswith('relevant'):
                label = 'relevant'
                #print(filename)
            elif filename.startswith('nonrelevant'):
                label = 'nonrelevant'
            
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as email_file:
                email_files.append(str(filename))
                text_emails.append(email_file.read())
                email_labels.append(label)
    return email_files, text_emails, email_labels

#load in all of my emails, training and testing, and set up labels
email_files, train_emails, train_labels = load_emails('training_emails')
#print(len(train_emails), len(train_labels))
email_files, test_emails, test_labels = load_emails('testingemails')

# create and train the naive bayes classifier
nbcl = naivebayes(getwords)

# pair together the email and label
for each_train_email, each_train_label in zip(train_emails, train_labels):
    # train the classifier with each labeled pair
    nbcl.train(each_train_email, each_train_label)

# setting up a table to print the results of classification
classifier_table = PrettyTable(['Email File', 'Actual Classification', 'Predicted Classification', 'Correct'])


# testing the classifier
correct = 0
# pair together the email name, email content, and label so it's easier to put all into the table and can be iterated over
for email_files, each_test_email, actual_label in zip(email_files, test_emails, test_labels):
    predicted_label = nbcl.classify(each_test_email, default='unknown')
    #print(f'snippet of email: {each_test_email[:50]}...')
    #print(f'actual classification: {actual_label}, predicted classification: {predicted_label}')

    if predicted_label == actual_label:
        # update correct count to calculate accuracy later
        correct += 1 
        # add correctly classified testing email to table
        classifier_table.add_row([email_files[:-4], actual_label, predicted_label, 1])
    else:
        # add incorrectly classified testing email to table
        classifier_table.add_row([email_files[:-4], actual_label, predicted_label, 0])
    

# evaluation of classifier: table and accuracy
classifier_table.add_row(['Total: ',' ', ' ', correct])
print(classifier_table)

accuracy = correct / len(test_emails)
print('accuracy: ', accuracy)