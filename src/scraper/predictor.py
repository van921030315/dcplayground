import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import bitcoin_scraper as bs
dates = []
prices = []


def get_data(cp, currency, rate):
    f = bs.Fetcher()
    if rate == 'hourly':
        prices = f.getPrePrice(cp, currency, 'hour')[cp]
        prices = list(reversed(prices))
        dates = np.arange(len(prices))
    if rate == 'daily':
        prices = f.getPrePrice(cp, currency, 'day')[cp]
        prices = list(reversed(prices))
        dates = np.arange(len(prices))

    return dates, prices


# predict the trend in next 6 time units
def predict_price( cp, currency, rate = 'hourly'):
    dates, prices = get_data(cp, currency, rate)
    x = range(len(dates), len(dates) + 6)

    prediction = {}
    dates = np.reshape(dates, (len(dates), 1))  # converting to matrix of n X 1
    prices = np.reshape(prices, (len(prices), 1))
    x = np.reshape(x, (len(x), 1))

    ridge_mod = linear_model.Ridge (alpha = 1)
    ridge_mod.fit(dates, prices)
    linear_mod = linear_model.LinearRegression()  # defining the linear regression model
    linear_mod.fit(dates, prices)  # fitting the data points in the model

    prediction = list(linear_mod.predict(x).flatten())
    prediction = prediction + list(ridge_mod.predict(x).flatten())
    return prediction

#dates, prices = get_data('LTC', 'USD')
predictions = predict_price('LTC', 'USD', 'daily' )
print predictions