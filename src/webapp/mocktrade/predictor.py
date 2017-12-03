# from sklearn import linear_model
# import matplotlib.pyplot as plt
import bitcoin_scraper as bs
dates = []
prices = []

from math import sqrt


# Calculate root mean squared error
def rmse_metric(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)


# Evaluate regression algorithm on training dataset
def evaluate_algorithm(dataset, algorithm):
    test_set = list()
    for row in dataset:
        row_copy = list(row)
        row_copy[-1] = None
        test_set.append(row_copy)
    predicted = algorithm(dataset, test_set)
    #print(predicted)
    actual = [row[-1] for row in dataset]
    rmse = rmse_metric(actual, predicted)
    return rmse


# Calculate the mean value of a list of numbers
def mean(values):
    return sum(values) / float(len(values))


# Calculate covariance between x and y
def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar


# Calculate the variance of a list of numbers
def variance(values, mean):
    return sum([(x - mean) ** 2 for x in values])


# Calculate coefficients
def coefficients(dates, prices):
    x = dates
    y = prices
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]


# Simple linear regression algorithm
def simple_linear_regression(dates, prices, x):
    predictions = list()
    b0, b1 = coefficients(dates, prices)
    for i in range(x):
        yhat = b0 + b1 *(len(dates)+i)
        predictions.append(yhat)
    return predictions


# Test simple linear regression


def predict_price(cp, currency, rate = 'hourly'):
    dates, prices = get_data(cp, currency, rate)

    #dates = np.reshape(dates, (len(dates), 1))  # converting to matrix of n X 1
    #prices = np.reshape(prices, (len(prices), 1))

    predictions = simple_linear_regression(dates, prices, 6)

    # linear_mod = linear_model.LinearRegression()  # defining the linear regression model
    # linear_mod.fit(dates, prices)  # fitting the data points in the model
    #
    # plt.scatter(dates, prices, color='black', label='Data')  # plotting the initial datapoints
    # plt.plot(dates, linear_mod.predict(dates), color='red',
    #          label='Linear model')  # plotting the line made by linear regression
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.title('Linear Regression')
    # plt.legend()
    # plt.show()

    return predictions

def get_data(cp, currency, rate):
    f = bs.Fetcher()
    if rate == 'hourly':
        prices = f.getPrePrice(cp, currency, 'hour')[cp]
        prices = list(reversed(prices))

    if rate == 'daily':
        prices = f.getPrePrice(cp, currency, 'day')[cp]
        prices = list(reversed(prices))

    dates = []
    for i in range(len(prices)):
        dates.append(i)
    return dates, prices


# predict the trend in next 6 time units
# def predict_price2( cp, currency, rate = 'hourly'):
#     dates, prices = get_data(cp, currency, rate)
#     x = range(len(dates), len(dates) + 6)
#
#     prediction = {}
#     dates = np.reshape(dates, (len(dates), 1))  # converting to matrix of n X 1
#     prices = np.reshape(prices, (len(prices), 1))
#     x = np.reshape(x, (len(x), 1))
#
#     ridge_mod = linear_model.Ridge (alpha = 1)
#     ridge_mod.fit(dates, prices)
#     linear_mod = linear_model.LinearRegression()  # defining the linear regression model
#     linear_mod.fit(dates, prices)  # fitting the data points in the model
#
#     prediction = list(linear_mod.predict(x).flatten())
#     prediction = prediction + list(ridge_mod.predict(x).flatten())
#     return prediction

#dates, prices = get_data('LTC', 'USD')
#predictions = predict_price('BTC', 'USD', 'daily' )
# print predictions