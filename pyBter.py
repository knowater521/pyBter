import httplib
import urllib
import json
import hashlib
import hmac
import time
import requests
import os

V1_PRIVATE = ['getfunds', 'placeorder', 'cancelorder', 'cancelorders',
              'getorder', 'orderlist', 'mytrades']
V2_PRIVATE = ['balances', 'depositeAddress', 'depositsWithdrawals', 'buy',
              'sell', 'cancelOrder', 'cancelOrders', 'cancelAllOrders',
              'getOrder', 'openOrders', 'tradeHistory', 'withdraw']

class pyBter(object):
    __api_key = ''
    __api_secret = ''
    __nonce_v = 1
    __wait_for_nonce = False
    __prefer_version = 2

    def __init__(self, api_key, api_secret, wait_for_nonce=False,
                 prefer_version=2):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__wait_for_nonce = wait_for_nonce
        self.__prefer_version = prefer_version

    def __nonce(self):
        if self.__wait_for_nonce:
            time.sleep(1)
        self.__nonce_v = str(time.time()).split('.')[0]

    def __signature(self, params):
        return hmac.new( self.__api_secret, params,
                        digestmod=hashlib.sha512).hexdigest()

    def __api_1_call(self, method, params):
        self.__nonce()
        _url = None
        _r = None
        if method in V1_PRIVATE:
            params['nonce'] = str(self.__nonce_v)
            params = urllib.urlencode(params)
            headers = {"Content-Type": "application/x-www-form-urlencoded",
                       "Key": self.__api_key,
                       "Sign": self.__signature(params)}
            _url = os.path.join("https://api.bter.com/api/1/private/", method)
            _r = requests.post(_url, data=params, headers=headers)
        else:
            params = urllib.urlencode(params)
            _url = os.path.join("http://data.bter.com/api/1/", method)
            _r = requests.get(_url, params=params)
        data = json.loads(_r.text)
        return data

    def __api_2_call(self, method, params):
        self.__nonce()
        _url = None
        _r = None
        if method in V2_PRIVATE:
            params['nonce'] = str(self.__nonce_v)
            params = urllib.urlencode(params)
            headers = {"Content-Type": "application/x-www-form-urlencoded",
                       "Key": self.__api_key,
                       "Sign": self.__signature(params)}
            _url = os.path.join("https://api.bter.com/api2/1/private/", method)
            _r = requests.post(_url, data=params, headers=headers)
        else:
            params = urllib.urlencode(params)
            _url = os.path.join("https://api.bter.com/api2/1/", method)
            _r = requests.get(_url, params=params)
        data = json.loads(_r.text)
        return data

    '''
    Following method is refer to API version 1
    '''
    def getfunds(self):
        return self.__api_1_call('getfunds', {})

    def placeorder(self, pair, type_, rate, amount):
        return self.__api_1_call('placeorder', {'pair': pair, 'type': type_,
                                                'rate': rate, 'amount': amount})

    def cancelorder(self, order_id, pair):
        return self.__api_1_call('cancelorder', {'order_id': order_id,
                                                 'pair': pair})

    def cancelorders(self, order_json):
        return self.__api_1_call('cancelorders', {'order_json': order_json})

    def getorder(self, order_id, pair):
        return self.__api_1_call('getorder', {'order_id':order_id, 'pair':pair})

    def orderlist(self):
        return self.__api_1_call('orderlist', {})

    def mytrades(self, pair, order_id):
        return self.__api_1_call('mytrades', {'pair':pair, 'order_id':order_id})

    '''
    Following method is refer to API version 2
    '''
    def pairs(self, prefer_version = None):
        if prefer_version:
            if 2 == prefer_version:
                return self.__api_2_call('pairs', {})
            if 1 == prefer_version:
                return self.__api_1_call('pairs', {})
        else:
            if 2 == self.__prefer_version:
                return self.__api_2_call('pairs', {})
            if 1 == self.__prefer_version:
                return self.__api_1_call('pairs', {})
        return None

    def marketinfo(self, prefer_version=None):
        if prefer_version:
            if 2 == prefer_version:
                return self.__api_2_call('marketinfo', {})
            if 1 == prefer_version:
                return self.__api_1_call('marketinfo', {})
        else:
            if 2 == self.__prefer_version:
                return self.__api_2_call('marketinfo', {})
            if 1 == self.__prefer_version:
                return self.__api_1_call('marketinfo', {})
        return None

    def marketlist(self, prefer_version=None):
        if prefer_version:
            if 2 == prefer_version:
                return self.__api_2_call('marketlist', {})
            if 1 == prefer_version:
                return self.__api_1_call('marketlist', {})
        else:
            if 2 == self.__prefer_version:
                return self.__api_2_call('marketlist', {})
            if 1 == self.__prefer_version:
                return self.__api_1_call('marketlist', {})
        return None

    def tickers(self, prefer_version=None):
        if prefer_version:
            if 2 == prefer_version:
                return self.__api_2_call('tickers', {})
            if 1 == prefer_version:
                return self.__api_1_call('tickers', {})
        else:
            if 2 == self.__prefer_version:
                return self.__api_2_call('tickers', {})
            if 1 == self.__prefer_version:
                return self.__api_1_call('tickers', {})
        return None

    def ticker(self, curr_a, curr_b, prefer_version=None):
        if prefer_version:
            if 2 == prefer_version:
                return self.__api_2_call(
                    os.path.join('ticker/', '_'.join((curr_a, curr_b))), {})
            if 1 == prefer_version:
                return self.__api_1_call(
                    os.path.join('ticker/', '_'.join((curr_a, curr_b))), {})
        else:
            if 2 == self.__prefer_version:
                return self.__api_2_call(
                    os.path.join('ticker/', '_'.join((curr_a, curr_b))), {})
            if 1 == self.__prefer_version:
                return self.__api_1_call(
                    os.path.join('ticker/', '_'.join((curr_a, curr_b))), {})
        return None

    def orderBooks(self):
        return self.__api_2_call('orderBooks', {})

    def orderBook(self, curr_a, curr_b):
        return self.__api_2_call(os.path.join('orderBook/',
                                              '_'.join((curr_a, curr_b))), {})

    def tradeHistory(self, curr_a, curr_b, tid=None):
        if tid:
            return self.__api_2_call('tradeHistory/{0}/{1}'.format(
                '_'.join((curr_a, curr_b)), str(tid)), {})
        else:
            return self.__api_2_call(
                os.path.join('tradeHistory/', '_'.join((curr_a, curr_b))), {})

    def balances(self):
        return self.__api_2_call('balances', {})

    def depositeAddress(self, currency):
        return self.__api_2_call('depositeAddress', {'currency': currency})

    def depositsWithdrawals(self, start=None, end=None):
        params = None
        if start and end:
            params = {'start':start, 'end':end}
        elif end is None and start:
            params = {'start':start}
        elif start is None and end:
            params = {'end':end}
        else:
            params = {}
        return self.__api_2_call('depositsWithdrawals', params)

    def buy(self, currencyPair, rate, amount):
        return self.__api_2_call('buy', {'currencyPair': currencyPair,
                                         'rate': rate,
                                         'amount': amount})

    def sell(self, currencyPair, rate, amount):
        return self.__api_2_call('sell', {'currencyPair': currencyPair,
                                         'rate': rate,
                                         'amount': amount})

    def cancelOrder(self, orderNumber, currencyPair):
        return self.__api_2_call('cancelOrder', {'orderNumber': orderNumber,
                                         'currencyPair': currencyPair})

    def cancelOrders(self, orders):
        return self.__api_2_call('cancelOrders', orders)

    def cancelAllOrders(self, type_, currencyPair):
        return self.__api_2_call('cancelAllOrders', {'type': type_,
                                         'currencyPair': currencyPair})

    def getOrder(self, orderNumber, currencyPair):
        return self.__api_2_call('getOrder', {'orderNumber': orderNumber,
                                         'currencyPair': currencyPair})

    def openOrders(self):
        return self.__api_2_call('openOrders', {})

    def tradeHistory(self, orderNumber, currencyPair):
        return self.__api_2_call('tradeHistory', {'orderNumber': orderNumber,
                                         'currencyPair': currencyPair})

    def withdraw(self, currency, amount, address):
        return self.__api_2_call('withdraw', {'currency': currency,
                                         'amount': amount, 'address':address})
