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

	def is_json(self, myjson):
		try:
			json_object = json.loads(myjson)
		except ValueError, e:
			return False, ""
		return True, json_object

	def __init__(self, base_url=__DEFAULT_BASE_URL, request_timeout=__DEFAULT_TIMEOUT):
		self.base_url = base_url
		self.request_timeout = request_timeout

	# @ parameter: type is the blockchain type
	def generateURL(self, blockchain, currency, price_type):

		url =  self.base_url+blockchain+'-'+currency+'/'+price_type  #e.g.
		print url
		return  url

	def getPrice(self, blockchain, currency = 'USD', price_type = ""):
		prices = {}
		if price_type == "":
			url_buy = self.generateURL(blockchain, currency,self.__BUY_PRICE)
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


