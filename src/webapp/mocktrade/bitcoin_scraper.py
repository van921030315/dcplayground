#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


# This is a blockchain currency scrapper that utilize the coinbase
# API
class Fetcher(object):

	__DEFAULT_BASE_URL = 'https://api.coinbase.com/v2/prices/'
	__DEFAULT_TIMEOUT = 120
	__SPOT_PRICE = 'spot'
	__SELL_PRICE = 'sell'
	__BUY_PRICE = 'buy'
	__HISTORY_BASE_URL = 'https://min-api.cryptocompare.com/data/pricehistorical?tsyms=USD&fsym='
	__HISTORY_BASE_URL_MIN = 'https://min-api.cryptocompare.com/data/histominute?tsym=USD&fsym='
	__HISTORY_BASE_URL_HOUR = 'https://min-api.cryptocompare.com/data/histohour?tsym=USD&fsym='
	__HISTORY_BASE_URL_DAY = 'https://min-api.cryptocompare.com/data/histoday?tsym=USD&fsym='

	def is_json(self, myjson):
		try:
			json_object = json.loads(myjson)
		except ValueError, e:
			return False, ""
		return True, json_object

	def __init__(self, base_url=__DEFAULT_BASE_URL, request_timeout=__DEFAULT_TIMEOUT, his_url = __HISTORY_BASE_URL,
				 hist_min_url = __HISTORY_BASE_URL_MIN, hist_hour_url = __HISTORY_BASE_URL_HOUR, hist_day_url =
				 __HISTORY_BASE_URL_DAY):
		self.base_url = base_url
		self.request_timeout = request_timeout
		self.his_url = his_url
		self.hist_min_url = hist_min_url
		self.hist_hour_url = hist_day_url
		self.hist_day_url = hist_day_url

	# @ parameter: type is the blockchain type
	def generateURL(self, blockchain, currency, price_type):

		url =  self.base_url+blockchain+'-'+currency+'/'+price_type  #e.g.
		return  url

	def generateHistURL(self, blockchain, timestamp = 10, rate = 'minute'):
		if rate == 'minute':
			url = self.hist_min_url+blockchain
			url += '&limit='+timestamp
		if rate == 'hour':
			url = self.hist_hour_url+blockchain
			url += '&limit=' + timestamp
		if rate == 'day':
			url = self.hist_day_url + blockchain
			url += '&limit=' + timestamp
		#print url
		return url

	# timestamp is the gap between current time and previous time
	def getPrice(self, blockchain, currency = 'USD', price_type = "", timestamp = False):
		prices = {}
		if price_type == "":
			url_buy = self.generateURL(blockchain, currency, self.__BUY_PRICE)
			url_sell = self.generateURL(blockchain, currency, self.__SELL_PRICE)
			url_spot = self.generateURL(blockchain, currency, self.__SPOT_PRICE)
			response = requests.get(url_buy)
			ok, res = self.is_json(response.text)
			if ok:
				prices['BUY'] = float(res['data']['amount'])
			response = requests.get(url_sell)
			ok, res = self.is_json(response.text)
			if ok:
				prices['SELL'] = float(res['data']['amount'])
			response = requests.get(url_spot)
			ok, res = self.is_json(response.text)
			if ok:
				prices['SPOT'] = float(res['data']['amount'])

		else:
			url = self.generateURL(blockchain, currency, price_type)
			response = requests.get(url)
			ok, res = self.is_json(response.text)
			if ok:
				prices[price_type] = float(res['data']['amount'])

		return prices

	def getPrePrice(self, blockchain, currency = 'USD', rate = "minute"):
		if rate == 'minute':
			prices = {}
			prices[blockchain] = []
			url = self.generateHistURL(blockchain, '9')
			response = requests.get(url)

			ok, res = self.is_json(response.text)
			if ok:
				if res['Response'] == 'Success':
					for i in range(len(res['Data'])):
						prices[blockchain] = [res['Data'][i]['close']] + prices[blockchain]
		if rate == 'hour':
			prices = {}
			prices[blockchain] = []
			url = self.generateHistURL(blockchain, '71', rate='hour')
			response = requests.get(url)
			ok, res = self.is_json(response.text)
			if ok:
				if res['Response'] == 'Success':
					for i in range(len(res['Data'])):
						prices[blockchain] = [res['Data'][i]['close']] + prices[blockchain]

		if rate == 'day':
			prices = {}
			prices[blockchain] = []
			url = self.generateHistURL(blockchain, '29', rate='day')
			response = requests.get(url)
			ok, res = self.is_json(response.text)
			if ok:
				if res['Response'] == 'Success':
					for i in range(len(res['Data'])):
						prices[blockchain] = [res['Data'][i]['close']] + prices[blockchain]

		if rate == 'year':
			prices = {}
			prices[blockchain] = []
			url = self.generateHistURL(blockchain, '365', rate='day')
			response = requests.get(url)
			ok, res = self.is_json(response.text)
			if ok:
				if res['Response'] == 'Success':
					for i in range(len(res['Data'])):
						if i%3 == 0:
							prices[blockchain] = [res['Data'][i]['close']] + prices[blockchain]

		return prices


