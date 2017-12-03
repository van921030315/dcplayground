import bitcoin_scraper as bs
import time



if __name__ == '__main__':
    # api = bs.Fetcher()
    # print time.time()
    # print api.getPrice('BTC', 'USD', 'spot')['spot']
    # print api.generateHistURL('BTC', '10' )
    # api.getPrePrice('BTC')
     f = bs.Fetcher()
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