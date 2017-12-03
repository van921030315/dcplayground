# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, time
from django.core import serializers
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Account, Prices
from .forms import SignUpForm
import bitcoin_scraper as bs
import predictor as pd
import feedparser
from xml.sax.saxutils import unescape,escape
from django.core.mail import send_mail
from .forms import *
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
import json
from .models import *
import datetime
import csv

f = bs.Fetcher()


def index(request):
    return render(request, "mocktrade/index.html")

@transaction.atomic
def register(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            account, create = Account.objects.get_or_create(user=request.user)
            account.usd = 1000000000
            account.save()
            return HttpResponseRedirect(reverse('index'))
            # new_user = form.save(commit=False)
            # new_user.set_password(form.cleaned_data['password1'])
            # new_user.is_active = False
            # new_user.save()

            # token = default_token_generator.make_token(new_user)
            # email_body = """
            #     Welcome to Grumblr! Please click the link below to verify your email and complete
            #     the registration of your account:

            #     http://%s%s
            #     """ % (request.get_host(), reverse('confirmemail', args=(new_user.username, token)))

            # send_mail(subject="Verify your email address",
            #           message=email_body,
            #           from_email="zhichao+j@andrew.cmu.edu",
            #           recipient_list=[new_user.email])

            # context['email'] = form.cleaned_data['email']
            # return render(request, 'registration/confirm.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@transaction.atomic
def confirm(request, username,token):
    user = get_object_or_404(User, username=username)
    # ipdb.set_trace()
    if not default_token_generator.check_token(user, token):
        return HttpResponse('Invalid confirmation page!')

    user.is_active = True
    user.save()

    # auth_user = authenticate(username = user.username, password = user.password)
    # login(request, auth_user)
    login(request, user)

    return redirect(reverse('home'))
# Create your views here.
@login_required
@transaction.atomic
def dashboard(request):
    account, create = Account.objects.get_or_create(user=request.user)
    return render(request, 'mocktrade/dashboard.html', {'account': account})

@login_required
@transaction.atomic
def view_investments(request):
    account, create = Account.objects.get_or_create(user=request.user)
    context = {}
    context['account']=account
    now = datetime.datetime.now()
    context['now']=now
    return render(request, 'mocktrade/investments.html', context)

# Create your views here.
@login_required
@transaction.atomic
def view_leaderboard(request):

    account, create = Account.objects.get_or_create(user=request.user)
    f = bs.Fetcher()
    context={}
    prices = {}
    prices['BTC'] = f.getPrice('BTC', 'USD', 'spot')['spot']
    prices['ETH'] = f.getPrice('ETH', 'USD', 'spot')['spot']
    prices['LTC'] = f.getPrice('LTC', 'USD', 'spot')['spot']
    context['account']=account
    for account in Account.objects.all():
        account.total_balance =(account.usd+account.btc* prices['BTC']+
                                account.eth* prices['ETH']+
                                account.ltc*prices['LTC'])
        account.save()
    now = datetime.datetime.now()
    user_accounts_sorted = Account.objects.order_by('-total_balance')
    context['user_accounts']= user_accounts_sorted
    context['now']=now
    return render(request, 'mocktrade/leaderboard.html', context)

#For displaying the trading page, follows same logic as dashboard
@login_required
@transaction.atomic
def trade(request):
    account, create = Account.objects.get_or_create(user=request.user)
    return render(request, 'mocktrade/trade.html', {'account': account})

#Adds USD to balance
@login_required
@transaction.atomic
def add_usd(request):
     context= {}
     account = Account.objects.get(user=request.user)
     context['account']= account
     if request.method == 'GET':
        return redirect(reverse('trade'))
     form = AddUSDForm(request.POST)
     context['form'] = form
     if not form.is_valid():
        context['add_errors'] = "True"
        return render (request, 'mocktrade/trade.html' , context)
     initial_balance = float(account.usd)
     initial_balance = float(initial_balance) + float(form.cleaned_data['usd_amount'])
     account.usd = initial_balance
     new_transaction = Transaction(user=request.user,amount =float(form.cleaned_data['usd_amount']),
                                   currency_type="USD", price_on_purchase =float(form.cleaned_data['usd_amount']), transaction_type='Add USD')
     new_transaction.save()
     account.save()
     return render(request, 'mocktrade/trade.html', context)

@login_required
@transaction.atomic
def try_to_sell (request, sell_order, buy_order):
    if sell_order.max_currency_quantity_units <= buy_order.max_currency_quantity_units:
        if sell_order.max_currency_quantity_units >= buy_order.min_currency_quantity_units:
            return make_order_transaction(request, sell_order,buy_order,sell_order.max_currency_quantity_units)
    if buy_order.max_currency_quantity_units <= sell_order.max_currency_quantity_units:
        if buy_order.max_currency_quantity_units >= sell_order.min_currency_quantity_units:
            return make_order_transaction(request, sell_order,buy_order,buy_order.max_currency_quantity_units)
    if buy_order.min_currency_quantity_units <= sell_order.max_currency_quantity_units:
        if buy_order.min_currency_quantity_units >= sell_order.min_currency_quantity_units:
            return make_order_transaction(request, sell_order,buy_order,buy_order.min_currency_quantity_units)
    if sell_order.min_currency_quantity_units <= buy_order.max_currency_quantity_units:
        if sell_order.min_currency_quantity_units >= buy_order.min_currency_quantity_units:
            return make_order_transaction(request, sell_order,buy_order,sell_order.min_currency_quantity_units)
    return "Not Sucess"


@login_required
@transaction.atomic
def make_order_transaction(request, sell_order, buy_order, quantity):
    currency = sell_order.currency_type
    price = buy_order.max_buy_price
    sell_account = Account.objects.get(user=sell_order.user)
    buy_account = Account.objects.get(user=buy_order.user)
    sell_account_curr = 0
    if currency == "BTC":
         if sell_account.btc < quantity:
              sell_order.status = "Cancelled, Insufficient BTC Balance"
              return "Not Success"
    if currency == "ETH":
         if sell_account.eth < quantity:
              sell_order.status = "Cancelled, Insufficient ETH Balance"
              return "Not Success"
    if currency == "LTC":
         if sell_account.ltc < quantity:
              sell_order.status = "Cancelled, Insufficient ETH Balance"
              return "Not Success"
    if  buy_account.usd < (quantity*price):
         buy_order.status = "Cancelled, Insufficient USD Balance"
         return "Not Success"
    sell_account.btc = sell_account.btc - quantity
    buy_account.btc = buy_account.btc + quantity
    buy_account.usd = buy_account.usd - quantity*price
    sell_account.usd =  sell_account.usd - quantity*price
    sell_account.save()
    buy_account.save()
    new_transaction = Transaction(user=sell_order.user,amount = quantity*price,
                               currency_type="USD", price_on_purchase =quantity*price, transaction_type='Order Get USD')
    new_transaction.save()
    new_transaction = Transaction(user=buy_order.user,amount = quantity*price,
                               currency_type="USD", price_on_purchase =quantity*price, transaction_type='Order Lose USD')
    new_transaction.save()
    new_transaction = Transaction(user=buy_order.user,amount = quantity,
                               currency_type=currency, price_on_purchase =price, transaction_type='Order Get '+currency)
    new_transaction.save()
    new_transaction = Transaction(user=sell_order.user,amount = quantity,
                               currency_type=currency, price_on_purchase =price, transaction_type='Order Sell '+currency)
    new_transaction.save()
    return "Success"

@login_required
@transaction.atomic
def match_orders(request):
    for sell_order in Order.objects.filter(type="SELL", status ="Pending"):
        for buy_order in Order.objects.filter(type="BUY", status ="Pending", currency_type = sell_order.currency_type).order_by('-max_currency_quantity_units').exclude(user=sell_order.user):
            if buy_order.max_buy_price >= sell_order.min_sell_price:
                if try_to_sell(request, sell_order, buy_order)== "Success":
                    buy_order.status = "Completed"
                    buy_order.save()
                    sell_order.status = "Completed"
                    sell_order.save()
                else:
                    break
    return

@login_required
@transaction.atomic
def view_create_buy_order_page(request):
     context= {}
     disable_outdated_orders(request)
     account = Account.objects.get(user=request.user)
     context['account']= account
     if request.method == 'GET':
        return render(request, 'mocktrade/createbuyorder.html', context)
     return render(request, 'mocktrade/createbuyorder.html', context)


@login_required
@transaction.atomic
def view_create_sell_order_page(request):
     context= {}
     disable_outdated_orders(request)
     account = Account.objects.get(user=request.user)
     context['account']= account
     if request.method == 'GET':
        return render(request, 'mocktrade/createsellorder.html', context)
     return render(request, 'mocktrade/createsellorder.html', context)

# Changes status of outdated Orders to Expired
@login_required
def disable_outdated_orders(request):
    context={}
    before_one_day = datetime.datetime.now() - datetime.timedelta(days=1)
    for order in Order.objects.filter(date_time__lt = before_one_day):
        if order.status == "Pending":
            order.status = "Expired"
            order.save()
    return

@login_required
@transaction.atomic
def post_buy_order(request):
     context= {}
     account = Account.objects.get(user=request.user)
     context['account']= account
     if request.method == 'GET':
        return render(request, 'mocktrade/createbuyorder.html', context)
     form = CreateBuyOrderForm(request.POST)
     context['form']=form
     if not form.is_valid():
        context['order_errors'] = "True"
        return render (request, 'mocktrade/createbuyorder.html' , context)
     new_order = Order(user=request.user, type = "BUY",
                       currency_type= form.cleaned_data['currency_type_order'],
                       min_currency_quantity_units=form.cleaned_data['min_currency_units'],
                       max_currency_quantity_units=form.cleaned_data['max_currency_units'],
                       max_buy_price = form.cleaned_data['max_buy_price'])
     disable_outdated_orders(request)
     return render(request, 'mocktrade/createbuyorder.html', context)

@login_required
@transaction.atomic
def post_sell_order(request):
     context= {}
     account = Account.objects.get(user=request.user)
     context['account']= account
     if request.method == 'GET':
        return render(request, 'mocktrade/createsellorder.html', context)
     form = CreateSellOrderForm(request.POST)
     context['form']=form
     if not form.is_valid():
        context['order_errors'] = "True"
        return render (request, 'mocktrade/createsellorder.html' , context)
     new_order = Order(user=request.user, type = "SELL",
                       currency_type= form.cleaned_data['currency_type_order'],
                       min_currency_quantity_units=form.cleaned_data['min_currency_units'],
                       max_currency_quantity_units=form.cleaned_data['max_currency_units'],
                       min_sell_price = form.cleaned_data['min_sell_price'])
     new_order.save()
     disable_outdated_orders(request)
     return render(request, 'mocktrade/createsellorder.html', context)


@login_required
@transaction.atomic
def view_orders(request):
     context= {}
     disable_outdated_orders(request)
     match_orders(request)
     account = Account.objects.get(user=request.user)
     context['account']= account
     user_orders = Order.objects.filter(user=request.user).order_by('-date_time')
     context['orders']=user_orders
     if request.method == 'GET':
        return render(request, 'mocktrade/vieworders.html', context)
     return render(request, 'mocktrade/vieworders.html', context)

@login_required
@transaction.atomic
def create_order(request):
     context= {}
     account = Account.objects.get(user=request.user)
     context['account']= account
     if request.method == 'GET':
        return render(request, 'mocktrade/createorder.html', context)
     return render(request, 'mocktrade/createorder.html', context)

#Cancels Order
@login_required
@transaction.atomic
def cancel_order(request):
     if request.method == 'GET':
        return redirect(reverse('vieworders'))
     disable_outdated_orders(request)
     form = CancelOrderForm(request.POST)
     if not form.is_valid():
          return redirect(reverse('vieworders'))
     order_to_be_cancelled = Order.objects.get(id = form.cleaned_data['cancel_order_id'])
     order_to_be_cancelled.status = "Cancelled"
     order_to_be_cancelled.save()
     return redirect(reverse('vieworders'))

#Adds currency to account. Allows user to buy digital currency.
@login_required
@transaction.atomic
def buy_currency(request):
     context= {}
     if request.method == 'GET':
        return redirect(reverse('trade'))
     form = BuyCurrencyForm(request.POST)
     context['form'] = form
     if not form.is_valid():
        context['buy_errors'] = "True"
        return render (request, 'mocktrade/trade.html' , context)
     account = Account.objects.get(user=request.user)
     context['account']= account
     currency =form.cleaned_data['currency_type_buy']
     currency_quantity = form.cleaned_data['buy_amount']
     # Get buy Price particular cryptocurrency
     currency_price = f.getPrice(currency, 'USD', 'buy')['buy']
     buy_amount = currency_quantity * currency_price
     user_usd = account.usd
     if buy_amount > user_usd:
        context['buy_errors'] = "True"
        context['buy_errors_desc'] = "Insufficient Balance"
        return render (request, 'mocktrade/trade.html' , context)
     if currency == 'BTC':
         temp = account.btc
         account.btc = temp + currency_quantity
     elif currency == 'ETH':
         temp = account.eth
         account.eth = temp + currency_quantity
     elif currency == 'LTC':
         temp = account.ltc
         account.ltc = temp + currency_quantity
     user_usd = account.usd - buy_amount
     account.usd  = user_usd
     new_transaction = Transaction(user=request.user,amount = buy_amount, currency_type=currency,
                                   price_on_purchase =currency_price, transaction_type='Buy')
     new_transaction.save()
     account.save()
     return render(request, 'mocktrade/trade.html', context)




#Removes currency from account.  Allows user to sell digital currency.
@login_required
@transaction.atomic
def sell_currency(request):
     context= {}
     account = Account.objects.get(user=request.user)
     context['account']= account
     if request.method == 'GET':
        return redirect(reverse('trade'))
     form = SellCurrencyForm(request.POST)
     context['form'] = form
     if not form.is_valid():
        context['sell_errors'] = "True"
        return render (request, 'mocktrade/trade.html' , context)
     currency =form.cleaned_data['currency_type_sell']
      # Get sell Price of particular cryptocurrency
     currency_quantity = form.cleaned_data['sell_amount']
     currency_price = f.getPrice(currency, 'USD', 'sell')['sell']
     sell_amount = currency_quantity * currency_price
     user_usd = account.usd
     if currency == 'BTC':
         temp = account.btc
         if currency_quantity > temp:
             context['sell_errors'] = "True"
             context['sell_errors_desc'] = "Insufficient BTC Balance"
             return render (request, 'mocktrade/trade.html' , context)
         else:
            account.btc = temp - currency_quantity
     elif currency == 'ETH':
         temp = account.eth
         if currency_quantity > temp:
             context['sell_errors'] = "True"
             context['sell_errors_desc'] = "Insufficient ETH Balance"
             return render (request, 'mocktrade/trade.html' , context)
         else:
            account.eth = temp - currency_quantity
     elif currency == 'LTC':
         temp = account.ltc
         if currency_quantity > temp:
             context['sell_errors'] = "True"
             context['sell_errors_desc'] = "Insufficient LTC Balance"
             return render (request, 'mocktrade/trade.html' , context)
         else:
            account.ltc = temp - currency_quantity
     user_usd = account.usd + sell_amount
     account.usd  = user_usd
     new_transaction = Transaction(user=request.user,amount =sell_amount, currency_type=currency,
                                   price_on_purchase =currency_price, transaction_type='Sell')
     new_transaction.save()
     account.save()
     return redirect(reverse('trade'))

@login_required
def view_manual_predictions(request):
     context={}
     account = Account.objects.get(user=request.user)
     context['account']= account
     return render(request, 'mocktrade/manualpredictions.html', context)

@login_required
def calculate_predictions(request):
     context={}
     account, create = Account.objects.get_or_create(user=request.user)
     form = CalculatePredictionsForm(request.POST)
     context['form'] = form
     if not form.is_valid():
        context['errors'] = "True"
        context['errors_desc'] = "Unable to Calculate, Enter valid inputs"
        return render (request, 'mocktrade/manualpredictions.html' , context)

     result = {}
     percentage_btc = form.cleaned_data['percentage_btc']
     percentage_eth = form.cleaned_data['percentage_eth']
     percentage_ltc = form.cleaned_data['percentage_ltc']
     new_btc_value = account.btc + account.btc * percentage_btc * 0.01
     if new_btc_value < 0:
         new_btc_value = 0
     new_eth_value = account.eth + account.eth * percentage_eth * 0.01
     if new_eth_value < 0:
         new_eth_value = 0
     new_ltc_value = account.ltc + account.ltc * percentage_ltc * 0.01
     if new_ltc_value < 0:
         new_ltc_value = 0
     new_balance = account.usd + new_btc_value + new_eth_value + new_ltc_value
     context['new_balance']=new_balance
     context['new_btc_value']=new_btc_value
     context['new_eth_value']= new_eth_value
     context['new_ltc_value']=new_ltc_value
     context['percentage_btc']=percentage_btc
     context['percentage_eth']=percentage_eth
     context['percentage_ltc']=percentage_ltc
     account = Account.objects.get(user=request.user)
     context['account']= account
     return render(request, 'mocktrade/manualpredictionresults.html', context)

#View all transactions
@login_required
def view_transactions(request):
     context={}
     account = Account.objects.get(user=request.user)
     context['account']= account
     user_transactions = Transaction.objects.filter(user=request.user).order_by('-date_time')
     context['transactions']=user_transactions
     return render(request, 'mocktrade/transactions.html', context)


def update_price_all(request):
    if request.POST:

        f = bs.Fetcher()
        if 'currency' in request.POST:
            currency = request.POST['currency']
        else:
            currency = 'USD'
        prices = {}
        prices['BTC'] = f.getPrice('BTC', currency, 'spot')['spot']
        prices['ETH'] = f.getPrice('ETH', currency, 'spot')['spot']
        prices['LTC'] = f.getPrice('LTC', currency, 'spot')['spot']

        price = Prices.objects.filter(date = date.today())

        if len(price) == 0:
            btcprice = Prices()
            btcprice.type = "BTC"
            btcprice.price = prices['BTC']
            btcprice.save()

            ethprice = Prices()
            ethprice.type = "ETH"
            ethprice.price = prices['ETH']
            ethprice.save()

            ltcprice = Prices()
            ltcprice.type = "LTC"
            ltcprice.price = prices['LTC']
            ltcprice.save()


        response_text = json.dumps(prices)
        return HttpResponse(response_text, content_type="application/json")

@login_required
@transaction.atomic
def get_price_history(request):
    if request.POST or request.GET:
        f = bs.Fetcher()
        if 'currency' in request.POST:
            currency = request.POST['currency']
        else:
            currency = 'USD'

        acc = Account.objects.get(user=request.user)
        prices = {}
        prices['BTC'] = f.getPrePrice('BTC')['BTC']
        prices['ETH'] = f.getPrePrice('ETH')['ETH']
        prices['LTC'] = f.getPrePrice('LTC')['LTC']
        prices['BAL'] = []

        for i in range(len(prices['BTC'])):

            b_p = float(prices['BTC'][i])
            l_p = float(prices['LTC'][i])
            e_p = float(prices['ETH'][i])
            bal = acc.btc * b_p + acc.ltc * l_p + acc.eth * e_p + acc.usd
            prices['BAL'] += [bal]

        response_text = json.dumps(prices)
        return HttpResponse(response_text, content_type="application/json")

@login_required
@transaction.atomic
def get_price_history_week(request):
    #print(request.body)
    #print ("History price called , getting weekly data")
    if request.POST:

        if 'currency' in request.POST:
            currency = request.POST['currency']
        else:
            currency = 'USD'
        acc = Account.objects.get(user=request.user)
        prices = {}
        prices['BTC'] = f.getPrePrice('BTC', 'USD', request.POST['rate'])['BTC']
        prices['ETH'] = f.getPrePrice('ETH', 'USD', request.POST['rate'])['ETH']
        prices['LTC'] = f.getPrePrice('LTC', 'USD', request.POST['rate'])['LTC']
        prices['BAL'] = []

        for i in range(len(prices['BTC'])):

            b_p = float(prices['BTC'][i])
            l_p = float(prices['LTC'][i])
            e_p = float(prices['ETH'][i])
            bal = acc.btc * b_p + acc.ltc * l_p + acc.eth * e_p + acc.usd
            prices['BAL'] += [bal]

        response_text = json.dumps(prices)
        return HttpResponse(response_text, content_type="application/json")

@login_required
@transaction.atomic
def get_price_prediction(request):
    if request.POST:
        rate = request.POST['rate']
        predictions = {}
        predictions['BTC'] = pd.predict_price('BTC', 'USD', rate)
        predictions['ETH'] = pd.predict_price('ETH', 'USD', rate)
        predictions['LTC'] = pd.predict_price('LTC', 'USD', rate)

        response_text = json.dumps(predictions)
        return HttpResponse(response_text, content_type="application/json")


@login_required
@transaction.atomic
def get_user_investments(request):
     account = Account.objects.get(user=request.user)
     context ={}
     prices={}
     prices['BTC'] = f.getPrice('BTC', 'USD', 'spot')['spot']
     prices['ETH'] = f.getPrice('ETH', 'USD', 'spot')['spot']
     prices['LTC'] = f.getPrice('LTC', 'USD', 'spot')['spot']
     context['account']=account
     for account in Account.objects.all():
        account.total_balance =(account.usd+account.btc* prices['BTC']+
                                account.eth* prices['ETH']+
                                account.ltc*prices['LTC'])
        account.save()
     context['account']= account
     investments={}
     investments['USD']=account.usd
     investments['ETH']=account.eth* prices['ETH']
     investments['BTC']= account.btc*prices['BTC']
     investments['LTC']= account.ltc*prices['LTC']
     response_text = json.dumps(investments)
     return HttpResponse(response_text, content_type="application/json")

@login_required
@transaction.atomic
def export_to_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    # Resources: https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Index', 'Transaction Id', 'Buy/Sell', 'Currency Type', 'Currency Units',
                     'Currency Price per Unit on Purchase', 'Date and Time' ])
    index =1
    for transaction in Transaction.objects.filter(user=request.user):
        writer.writerow([index, transaction.id, transaction.transaction_type,
                         transaction.currency_type,transaction.amount, transaction.price_on_purchase,
                          transaction.date_time])
        print transaction.transaction_type
        index=index+1
    return response

@login_required
def get_news(request):
    d = feedparser.parse('http://feed.informer.com/digests/I2GGLAVR70/feeder.rss')
    context = {}
    news = {}
    contexts = {}
    parsed_text = []
    count = True
    #print d['feed']['title']
    #print len(d.entries)
    contexts['content'] = []
    for j in range(0,len(d.entries)-1):
        content = {}
        if (len(d.entries[j]['summary'])>2700 or len(d.entries[j]['summary'])<300):
            continue
        text = (unescape(d.entries[j]['summary']))
        for i in range(0,99):
            text = text.replace("&#82"+str(i)," ")
            text = text.replace("<br />"," ")
            text = text.replace("[ 0;]","")
            text = text.replace("7;s","'s")
            text = text.replace("(+)","")
        content['1']=unescape(d.entries[j]['title'])
        content['3']=text
        content['2']=unescape(d.entries[j]['link'])
        contexts['content'].append(content)

        #print context['title']
        # for i in range(0,len(context)-2,1):
            # if (context[i]=='<') and (context[i+1] == 'p') and (context[i+2] == '>'):
            #     count = True
            # if (context[i] == '/') and (context[i+1] == 'p') and (context[i + 2] == '>'):
            #     count = False
            # print i
            # if(count):
            #     a = context[i]
            #     #print a
            #     parsed_text.append(a+'\n')


    #print context['title']
    #parsed_text = json.dump(parsed_text)
    contexts['test']= 'test'
    return render(request, 'mocktrade/news.html',contexts)
    #return  render(request, 'mocktrade/news.html')


