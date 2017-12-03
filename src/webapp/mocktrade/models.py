# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.

#Contains fields for user account
class Account(models.Model):
    user = models.ForeignKey(User)
    btc = models.FloatField(default=0.0)
    eth = models.FloatField(default=0.0)
    ltc = models.FloatField(default=0.0)
    usd = models.FloatField(default=0.0)
    total_balance = models.FloatField(default=0.0)

class Transaction(models.Model):
    user = models.ForeignKey(User)
    amount = models.FloatField(default=0.0)
    currency_type = models.CharField(max_length=10)
    time = models.TimeField(auto_now_add=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    price_on_purchase = models.FloatField(default=0.0)
    transaction_type = models.CharField(max_length=10,blank=True)



# although we can get historical price from blockchain
# API, the price table is used for back up purpose,
# in case the external api is done
# to control the size of the database, the backup will
# be made twice a day.
class Prices(models.Model):
    type = models.CharField(max_length=10)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    price = models.FloatField()


class Order(models.Model):
    user = models.ForeignKey(User, related_name="user")
    type = models.CharField(max_length=10) #Buy, Sell
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    currency_type = models.CharField(max_length=10)
    min_currency_quantity_units = models.FloatField(blank=True, default=0.0)
    max_currency_quantity_units = models.FloatField(blank=True, default=0.0)
    status = models.CharField(max_length=50, default = "Pending") #Pending, Completed, Expired, Cancelled, Cancelled - Insufficient Balance
    min_sell_price = models.FloatField(blank=True, default=0.0)
    max_buy_price = models.FloatField(blank=True, default=0.0)
    completed_amount = models.FloatField(blank=True, default=0.0)
    completed_quantity_units = models.FloatField(blank=True, default=0.0)
    completed_price = models.FloatField(blank=True, default=0.0)
    order_completed_user = models.ForeignKey(User, related_name="order_completed_user", null=True, default=None)
