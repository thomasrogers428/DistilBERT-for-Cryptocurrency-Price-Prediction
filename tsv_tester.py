#=========================================================================
# Dartmouth College, LING48, Spring 2021
# Thomas Rogers (Thomas.W.Rogers.23@dartmouth.edu) and Claire McKenna (Claire.L.McKenna.23@dartmouth.edu)
# Final Project: Bitcoin Fine-Tuned DistilBERT
#
# Based on code from:
#
#
# Summary: This program takes in a text file of reddit title posts and labels which are divided by '---'. It parses
# each line individually and turns the file into a .tsv which can be processed by the DistilBERT.
#
# Inputs: Files: BTC.txt: labelled reddit data from bitcoin subreddit, ETH.txt: labelled reddit data from ethereum
# subreddit
# Output: BTCTSV.tsv: .tsv formatting of BTC.txt, ETHTSV.tsv: .tsv formatting of ETH.txt
# =========================================================================
import csv
import pandas as pd
BTC = open("BTC.txt", 'r')
ETH = open("ETH.txt", 'r')

# read all posts from text files
posts_BTC = []
scores_BTC = []
for row in BTC:
    string = str(row)
    splitstring = string.split("---")
    posts_BTC.append(splitstring[0])
    scores_BTC.append(splitstring[1].strip('\n'))

posts_ETH = []
scores_ETH = []
for row in ETH:
    string = str(row)
    splitstring = string.split("---")
    posts_ETH.append(splitstring[0])
    scores_ETH.append(splitstring[1].strip('\n'))

data_BTC = {'post': posts_BTC, 'score': scores_BTC}
df_BTC = pd.DataFrame(data_BTC)

data_ETH = {'post': posts_ETH, 'score': scores_ETH}
df_ETH = pd.DataFrame(data_ETH)

print(df_BTC)
print(df_ETH)


df_BTC.to_csv("BTCTSV.tsv", sep = "\t", index = False)
df_ETH.to_csv("ETHTSV.tsv", sep = "\t", index = False)