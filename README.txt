=========================================================================
Dartmouth College, LING48, Spring 2021
Thomas Rogers (Thomas.W.Rogers.23@dartmouth.edu) and Claire McKenna (Claire.L.McKenna.23@dartmouth.edu)
Final Project: README - Summary of Code
=========================================================================

The first file to run is Reddit_Final. This will output BTC_train.txt and ETH_train.txt. These files were then edited
to contain only the post tiles with clear sentiment and were scored accordingly. The edited files with scores are named
BTC.txt and ETH.txt. These files are then passed into tsv_tester which makes both files into .tsv form so that they can
but used by the BERT. tsv_tester creates the two files BTCTSV and ETHTSV which will be passed into BTC_BERT and ETH_BERT.
ByDate will scrape reddit for post titles for each date and will create two text files, ETH_posts_1.txt and BTC_posts_1.txt.
BTC_BERT and ETH_BERT can now be run and produce all the sentiment scores for each data. The sentiment scores were then
inputted into a .csv file, ResultsFinal with the price change for the given coin for each day. ML then reads the data from
ResultsFinal and creates a linear regression model for all processed sentiment scores and price changes. This file will
ask for user input and will give buy/sell/hold recommendations given a days sentiment score.

