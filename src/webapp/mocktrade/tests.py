from django.test import TestCase
from models import Account, Transaction
from django.contrib.auth.models import User

testuser1 = User(username = "test1", email="test1@test.com", password="helloworld")
testuser2 = User(username="test2", email="test2@test.com", password="helloworld")
class AccountTestCase(TestCase):
    def setUp(self):

        Account.objects.create(user=testuser1, usd=100.0, btc=0.2, ltc=0.0, eth=2.5)
        Account.objects.create(user=testuser2, usd=1000.0, btc=0.0, ltc=4.0, eth=4.5)

    def test_account_usd(self):
        test1 = Account.objects.get(user=testuser1)
        test2 = Account.objects.get(user=testuser2)
        self.assertEqual(test1.usd, 100.0)
        self.assertEqual(test2.usd, 1000.0)

    def test_account_btc(self):
        test1 = Account.objects.get(user=testuser1)
        test2 = Account.objects.get(user=testuser2)
        self.assertEqual(test1.btc, 0.2)
        self.assertEqual(test2.btc, 0.0)

    def test_account_eth(self):
        test1 = Account.objects.get(user=testuser1)
        test2 = Account.objects.get(user=testuser2)
        self.assertEqual(test1.eth, 2.5)
        self.assertEqual(test2.eth, 4.5)

    def test_account_ltc(self):
        test1 = Account.objects.get(user=testuser1)
        test2 = Account.objects.get(user=testuser2)
        self.assertEqual(test1.ltc, 0.0)
        self.assertEqual(test2.ltc, 4.0)

    def test_account_withdraw(self):
        test1 = Account.objects.get(user=testuser1)
        test2 = Account.objects.get(user=testuser2)
        test1.btc = test1.btc - 0.1
        self.assertEqual(test1.btc, 0.1)

    def test_account_deposit(self):
        test1 = Account.objects.get(user=testuser1)
        test2 = Account.objects.get(user=testuser2)
        test1.btc = test1.ltc + 0.8
        self.assertEqual(test1.ltc, 4.8)


class TransactionTestCase(TestCase):
    def setUp(self):
        Account.objects.create(user=testuser1, usd=100.0, btc=0.2, ltc=0.0, eth=2.5)
        Account.objects.create(user=testuser2, usd=1000.0, btc=0.0, ltc=4.0, eth=4.5)

    def test_transaction_addusd(self):
        trans1 = Transaction(user=testuser1, amount=100.0,
                             currency_type="USD", price_on_purchase=1.0,
                             transaction_type='Add USD')

        self.assertEqual(trans1.currency_type, 'USD')
        self.assertEqual(trans1.amount, 100.0)
        self.assertEqual(trans1.price_on_purchase, 1.0)

    def test_transaction_buybtc(self):
        trans1 = Transaction(user=testuser1, amount= 100.0,
                    currency_type="BTC", price_on_purchase=10213.0,
                    transaction_type='Buy')

        self.assertEqual(trans1.currency_type, 'BTC')
        self.assertEqual(trans1.amount, 100.0)
        self.assertEqual(trans1.price_on_purchase, 10213.0)
        self.assertEqual(trans1.transaction_type, 'Buy')

    def test_transaction_sellbtc(self):
        trans1 = Transaction(user=testuser1, amount= 100.0,
                    currency_type="BTC", price_on_purchase=10213.0,
                    transaction_type='Sell')

        self.assertEqual(trans1.currency_type, 'BTC')
        self.assertEqual(trans1.amount, 100.0)
        self.assertEqual(trans1.price_on_purchase, 10213.0)
        self.assertEqual(trans1.transaction_type, 'Sell')

    def test_transaction_buyltc(self):
        trans1 = Transaction(user=testuser1, amount= 12.0,
                    currency_type="LTC", price_on_purchase=93.2,
                    transaction_type='Buy')

        self.assertEqual(trans1.currency_type, 'LTC')
        self.assertEqual(trans1.amount, 12.0)
        self.assertEqual(trans1.price_on_purchase, 93.2)
        self.assertEqual(trans1.transaction_type, 'Buy')

    def test_transaction_sellltc(self):
        trans1 = Transaction(user=testuser1, amount= 12.0,
                    currency_type="LTC", price_on_purchase=93.2,
                    transaction_type='Buy')

        self.assertEqual(trans1.currency_type, 'LTC')
        self.assertEqual(trans1.amount, 12.0)
        self.assertEqual(trans1.price_on_purchase, 93.2)
        self.assertEqual(trans1.transaction_type, 'Buy')
