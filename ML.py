# =========================================================================
# Dartmouth College, LING48, Spring 2021
# Thomas Rogers (Thomas.W.Rogers.23@dartmouth.edu) and Claire McKenna (Claire.L.McKenna.23@dartmouth.edu)
# Final Project: Linear Regression
#
# Based on code from: HW6 DistilBERT Classifier
#
#
# Summary: This file trains a linear regression model using ordinary least squares and outputs the results of the
# regression for both BTC and ETH)
#
# Inputs: Files: Sentiment score and price data, user input about coin preference and daily sentiment score
# Output: Statistical data and gives recommendations based on user input of the daily sentiment score
# =========================================================================
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# load in csv file
csvname = 'ResultsFinal.csv'
data = pd.read_csv(csvname)

# get x and y for regression
BTCPC = np.array(data['BTCPC'])
# https://stackoverflow.com/questions/11620914/removing-nan-values-from-an-array
BTCPC = BTCPC[np.logical_not(np.isnan(BTCPC))]
BTCSS = np.array(data['BTCSS'])
BTCSS = BTCSS[np.logical_not(np.isnan(BTCSS))]
BTC = plt.scatter(BTCSS, BTCPC)
# plt.show()

ETHPC = np.array(data['ETHPC'])
ETHPC = ETHPC[np.logical_not(np.isnan(ETHPC))]
ETHSS = np.array(data['ETHSS'])
ETHSS = ETHSS[np.logical_not(np.isnan(ETHSS))]

# create models
BTCModel = LinearRegression()
ETHModel = LinearRegression()

BTCModel.fit(BTCSS.reshape(-1, 1), BTCPC)
ETHModel.fit(ETHSS.reshape(-1, 1), ETHPC)

# print some statistical results
# https://stackoverflow.com/questions/27928275/find-p-value-significance-in-scikit-learn-linearregression
X2 = sm.add_constant(BTCSS)
est = sm.OLS(BTCPC, X2)
est2 = est.fit()
print(est2.summary())

# https://stackoverflow.com/questions/27928275/find-p-value-significance-in-scikit-learn-linearregression
X2 = sm.add_constant(ETHSS)
est = sm.OLS(ETHPC, X2)
est2 = est.fit()
print(est2.summary())

# calculate thresholds for buy and sell based on x intercept of regression line
BTCThreshold = (-BTCModel.intercept_) / BTCModel.coef_
ETHThreshold = (-ETHModel.intercept_) / ETHModel.coef_
print('\n')
print("BTC equation: price change = " + str(BTCModel.coef_[0]) + "*sentiment score + " + str(BTCModel.intercept_))
print("BTC Threshold:", BTCThreshold)
print('\n')
print("ETH equation: price change = " + str(ETHModel.coef_[0]) + "*sentiment score + " + str(ETHModel.intercept_))
print("Ethereum Threshold:", ETHThreshold)

print("\n")
# take user inputs for cointype and sentiment score
coin_type = input("What crypto currency are you interested in today? (Enter Bitcoin or Ethereum): \n")
sscore = input("What is today's sentiment score? \n")
sscore = float(sscore)

# check coin type
if coin_type == "bitcoin" or coin_type == "Bitcoin":
    # check if it falls above, below, or near threshold
    if sscore > (BTCThreshold + .005):
        print("We recommend you buy Bitcoin")
    elif sscore < (BTCThreshold - .005):
        print("We recommend you sell Bitcoin")
    else:
        print("We recommend you hold all Bitcoin")

if coin_type == "ethereum" or coin_type == "Ethereum":
    if sscore > (ETHThreshold + .005):
        print("We recommend you buy Ethereum")
    elif sscore < (ETHThreshold - .005):
        print("We recommend you sell Ethereum")
    else:
        print("We recommend you hold all Ethereum")
