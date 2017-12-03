import bitcoin_scraper as bs




f = bs.Fetcher()


# test case for fetching cryptocurrency prices
prices = {}
prices['BTC'] = f.getPrePrice('BTC')['BTC']
prices['ETH'] = f.getPrePrice('ETH')['ETH']
prices['LTC'] = f.getPrePrice('LTC')['LTC']
prices['BAL'] = []
for i in range(len(prices['BTC'])):
 b_p = float(prices['BTC'][i])
 l_p = float(prices['LTC'][i])
 e_p = float(prices['ETH'][i])
 bal = 0.12 * b_p + 0.231 * l_p + 23 * e_p
 prices['BAL'] += [bal]
print prices['BAL']

print f.getPrePrice('BTC', 'USD', 'hour')
