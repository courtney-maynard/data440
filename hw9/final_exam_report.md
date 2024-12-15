<h1 align = "center">HW 9/Final Exam - Email Classification</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">December 16th, 2024</h3>

## Questions
### Q1: Create Two Datasets, Testing and Training
Choose a topic to classify your emails on, but only choose one topic. 
- The training dataset should consist of 20 text documents of email messages that are relevant to the topic and 20 text documents of email messages that are non-relevant to the topic.
- The testing dataset should consist of five relevant and five non-relevant text documents of email messages.

**A: What topic did you decide to classify on?**

I decided to classify emails sent to all William and Mary students from school administrators. After looking through my emails, I determined that I receive many emails to my school account that either come from third parties or are notifications(blackboard, W&M spirit shop, etc.), where the main content is images, hyperlinks, or formatted HTML. Thus, I decided to choose emails that were mostly plain text, with some possibilities of links. Interestingly, all of the emails I found that were 100% plain text were email blasts to all students from school administrators, like Ginger Ambler or President Rowe, or other relevant authority figures like the mayor of Williamsburg or the police chief. Their content spanned from notifications about events such as convocation to emails about campus safety. For all of my other emails, I took a variety of emails that I receive that aren't spam but aren't emails that I open daily. Some examples are LinkedIn recap emails and compilations of daily New York Times articles. I removed email signatures from all emails in the training and testing sets. Since the content of these different types of emails was very different, I expected my classifier to perform well. 

### Q2: Naive Bayes Classifier
Use the example code to train and test your Naive Bayes classifier, using your email document dataset.
- Create a table to report the classification results for the email messages in the Testing dataset, including what the classifier reported vs the actual classification
  
#### Code:
I used the Naive Bayes Classifier from the colab notebook, with the basic classifier implementation, and then wrote my own functions as below:

```python
## ADDITIONAL IMPORTS
import os
import prettytable
from prettytable import PrettyTable

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

```

```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 data440 % python3 homework8classifier.py
+--------------------+-----------------------+--------------------------+---------+
|     Email File     | Actual Classification | Predicted Classification | Correct |
+--------------------+-----------------------+--------------------------+---------+
|  relevant_test_5   |        relevant       |       nonrelevant        |    0    |
| nonrelevant_test_5 |      nonrelevant      |       nonrelevant        |    1    |
| nonrelevant_test_4 |      nonrelevant      |       nonrelevant        |    1    |
|  relevant_test_4   |        relevant       |       nonrelevant        |    0    |
|  relevant_test_3   |        relevant       |         relevant         |    1    |
| nonrelevant_test_3 |      nonrelevant      |       nonrelevant        |    1    |
| nonrelevant_test_2 |      nonrelevant      |       nonrelevant        |    1    |
|  relevant_test_2   |        relevant       |       nonrelevant        |    0    |
| nonrelevant_test_1 |      nonrelevant      |       nonrelevant        |    1    |
|  relevant_test_1   |        relevant       |         relevant         |    1    |
|      Total:        |                       |                          |    7    |
+--------------------+-----------------------+--------------------------+---------+
accuracy:  0.7
```

#### Commentary:

Commentary goes here

**A: For those emails that the classifier got wrong, what factors might have caused the classifier to be incorrect? Look at the text of the email to determine.**


### Q3: Confusion Matrix
Draw a confusion matrix for the classification results, created using a table in Markdown not using another program or a screenshot of an image.

|  |  | **Actual** |  |
|--|--|--|--|
|  |  | **Relevant** | **Non-Relevant** |
| **Predicted** | **Relevant** | 2 (True Positive)  | 0 (False Positive)|
|  | **Non-Relevant** | 3 (False Negative) | 5 (True Negative) |



**A: Based on the results in the confusion matrix, how well did the classifier perform?**

The classifier performed moderately, with a 70% accuracy, but it performed better in classifying non-relevant emails as non-relevant than relevant emails as relevant. The true negatives, of which there were five, indicate that the classifier accurately deduced that all five non-relevant emails were non-relevant. However, the true positives, two, indicating that the classifier only correctly deduced two out of the five relevant emails, incorrectly classifying the rest of the relevant emails as non-relevant. This is not what we want from an email classifier in this case, because we failed to sort three relevant emails. There are no false positives, meaning that the classifier did not mistake any non-relevant emails to be relevant.

**B: Would you prefer an email classifier to have more false positives or more false negatives? Why?**

I would prefer the classifier to have more False Positives in this case than False Negatives, because we are trying to decipher which emails belong to the 'positive' group, the relevant emails, and the rest are all miscellaneous spam. False positives would mean that non-relevant emails, like a spam email, would be classified as relevant. Though this could be irritating as you are seeing spam emails that you don't want to, it's better than the alternative, false negatives, which would lead to missing important/relevant emails that are incorrectly classified as spam.

### Q4: Extra Credit
Report the precision and recall scores of your classification results and include the formulas used to compute the values.

_Precision: True Positives/(True Positives + False Positives)_

The precision of the classifier is: 2/(2+0) = 1.0

_Recall: True Positives/(True Positives + False Negatives)_

The recall of the classifier is: 2/(2+3) = 0.4


### Resources:
I found this post on StackOverflow about the pretty-printing tables: https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
