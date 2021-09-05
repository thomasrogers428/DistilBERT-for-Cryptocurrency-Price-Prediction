# =========================================================================
# Dartmouth College, LING48, Spring 2021
# Thomas Rogers (Thomas.W.Rogers.23@dartmouth.edu) and Claire McKenna (Claire.L.McKenna.23@dartmouth.edu)
# Final Project: ETH Fine-Tuned DistilBERT
#
# Based on code from: HW6 DistilBERT Classifier
#
#
# Summary: This program creates a DistilBERT which is fine-tuned on hand labelled reddit data with positive and
# negative sentiments given. It then processes a series of unseen reddit post titles and outputs the sentiments for
# each sentence. These sentiments are compiled and a sentiment score is given for each day based on the average
# sentiment for that given day.
#
# Inputs: Files: ETHTSV.tsv - labelled training data, ETH_posts.txt - unseen reddit post titles from Ethereum subreddit
# Output: Sentiment scores for each day seen in ETH_posts.txt
# =========================================================================
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import torch
import transformers as ppb
import warnings

warnings.filterwarnings('ignore')

df = pd.read_csv('ETHTSV.tsv', delimiter='\t', header=None)

batch_1 = df[:136]
batch_1[1].value_counts()

# For DistilBERT:
model_class, tokenizer_class, pretrained_weights = (
ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')


# Load pretrained model/tokenizer
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
model = model_class.from_pretrained(pretrained_weights)

tokenized = batch_1[0].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))

max_len = 0
for i in tokenized.values:
    if len(i) > max_len:
        max_len = len(i)

padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])

attention_mask = np.where(padded != 0, 1, 0)

input_ids = torch.tensor(padded)
attention_mask = torch.tensor(attention_mask)

with torch.no_grad():
    last_hidden_states = model(input_ids, attention_mask=attention_mask)

features = last_hidden_states[0][:, 0, :].numpy()

labels = batch_1[1]

train_features, test_features, train_labels, test_labels = train_test_split(features, labels)

parameters = {'C': np.linspace(0.0001, 100, 20)}
grid_search = GridSearchCV(LogisticRegression(), parameters)
grid_search.fit(train_features, train_labels)

print('best parameters: ', grid_search.best_params_)
print('best scrores: ', grid_search.best_score_)

lr_clf = LogisticRegression(C=5.263252631578947)
lr_clf.fit(train_features, train_labels)

lr_clf.score(test_features, test_labels)

from sklearn.dummy import DummyClassifier

clf = DummyClassifier()

scores = cross_val_score(clf, train_features, train_labels)
print("Dummy classifier score: %0.3f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

new_input_ids = torch.tensor(
    tokenizer.encode("Ethereum is the best crytpocurrency", add_special_tokens=True)).unsqueeze(0)
new_outputs = model(new_input_ids)
new_last_hidden_states = [new_outputs[0].detach().numpy()[0][0]]
score1 = lr_clf.predict_proba(new_last_hidden_states)
print("Score 1", score1)

new_input_ids = torch.tensor(tokenizer.encode("I am optimistic about ethereum", add_special_tokens=True)).unsqueeze(0)
new_outputs = model(new_input_ids)
new_last_hidden_states = [new_outputs[0].detach().numpy()[0][0]]
score2 = lr_clf.predict_proba(new_last_hidden_states)
print("Score 2", score2)

new_input_ids = torch.tensor(tokenizer.encode("Ethereum is worse then bitcoin", add_special_tokens=True)).unsqueeze(0)
new_outputs = model(new_input_ids)
new_last_hidden_states = [new_outputs[0].detach().numpy()[0][0]]
score3 = lr_clf.predict_proba(new_last_hidden_states)
print("Score 3", score3)

# open testings posts
posttxtETH = open('ETH_posts_1.txt', 'r')

# create lists to hold posts by day/all days of posts
all_days_ETH = []
day_posts_ETH = []
for line in posttxtETH:
    line = line.strip('\n')
    # check for new date
    if line.__contains__('END DAY'):
        # add day to main list and reinitialize
        all_days_ETH.append(day_posts_ETH)
        day_posts_ETH = []
    else:
        # add post to day
        day_posts_ETH.append(line)

# create list of scores
all_scores = []
print("Scores:")
for day in all_days_ETH:
    # initialize daily score to 0 for new day
    day_score = 0
    for post in day:
        # get sentiment output
        new_input_ids = torch.tensor(tokenizer.encode(post, add_special_tokens=True)).unsqueeze(0)
        new_outputs = model(new_input_ids)
        new_last_hidden_states = [new_outputs[0].detach().numpy()[0][0]]
        score = lr_clf.predict_proba(new_last_hidden_states)
        day_score += score[0][1]
    # if posts avalible, average score to get output
    if len(day) != 0:
        day_score = day_score / len(day)
    # add score to list
    all_scores.append(day_score)
    print(day_score)

