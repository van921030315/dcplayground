from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

CATEGORIES = (
    ('BTC', 'BTC'),
    ('LTC', 'LTC'),
    ('ETH', 'ETH'),
)

ORDER_CATEGORIES =(
    ('BUY', 'BUY'),
    ('SELL', 'SELL'),
)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def clean_passwordrepeat(self):
        password1 = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data.get("passwordrepeat", "")
        if password1 and password2:  # If both passwords has value
            if password1 != password2:
                raise forms.ValidationError((u"Passwords didn't match."))
        else:
            raise forms.ValidationError((u"Passwords can't be blank."))
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return

class AddUSDForm(forms.Form):
    usd_amount = forms.FloatField(required=True, min_value=0)

    def clean(self):
        usd_amount = self.cleaned_data.get('usd_amount')
        if not usd_amount >= 0:
            raise forms.ValidationError("Amount should be positive")
        cleaned_data = super(AddUSDForm, self).clean()
        return cleaned_data

class BuyCurrencyForm(forms.Form):
    buy_amount = forms.FloatField(required=True, min_value=0)
    currency_type_buy = forms.ChoiceField(required=True,choices=CATEGORIES)

    def clean(self):
        cleaned_data = super(BuyCurrencyForm, self).clean()
        return cleaned_data



class SellCurrencyForm(forms.Form):
    currency_type_sell = forms.ChoiceField(required=True,choices=CATEGORIES)
    sell_amount = forms.FloatField(required=True, min_value=0)

    def clean(self):
        cleaned_data = super(SellCurrencyForm, self).clean()
        return cleaned_data


class CreateBuyOrderForm(forms.Form):
    currency_type_order = forms.ChoiceField(required=True,choices=CATEGORIES)
    min_currency_units = forms.FloatField(required=True, min_value=0)
    max_currency_units = forms.FloatField(required=True, min_value=0)
    max_buy_price = forms.FloatField(required=True, min_value=0)

    def clean(self):
        cleaned_data = super(CreateBuyOrderForm, self).clean()
        min_currency_units =  self.cleaned_data.get('min_currency_units')
        max_currency_units =  self.cleaned_data.get('max_currency_units')
        min_sell_price =   self.cleaned_data.get('min_sell_price')
        if not type(min_currency_units) is float:
               raise forms.ValidationError("Minimum Currency Units should be a number")
        if not type(max_currency_units) is float:
               raise forms.ValidationError("Maximum Currency Units should be a number")
        if float(min_currency_units) > float(max_currency_units):
            raise forms.ValidationError("Minimum currency units is greater than maximum currency units")
        return cleaned_data

class CreateSellOrderForm(forms.Form):
    currency_type_order = forms.ChoiceField(required=True,choices=CATEGORIES)
    min_currency_units = forms.FloatField(required=True, min_value=0)
    max_currency_units = forms.FloatField(required=True, min_value=0)
    min_sell_price = forms.FloatField(required=True, min_value=0)

    def clean(self):
        cleaned_data = super(CreateSellOrderForm, self).clean()
        min_currency_units =  self.cleaned_data.get('min_currency_units')
        max_currency_units =  self.cleaned_data.get('max_currency_units')
        min_sell_price =   self.cleaned_data.get('min_sell_price')
        if not type(min_currency_units) is float:
               raise forms.ValidationError("Minimim Currency Units should be a number")
        if not type(max_currency_units) is float:
               raise forms.ValidationError("Maximum Currency Units should be a number")
        if not type(min_sell_price) is float:
               raise forms.ValidationError("Minimum Selling Price should be a number")
        if float(min_currency_units) > float(max_currency_units):
            raise forms.ValidationError("Minimum currency units is greater than maximum currency units")
        return cleaned_data

class CancelOrderForm(forms.Form):
    cancel_order_id = forms.IntegerField(required=True, min_value=1)
    def clean(self):
        cleaned_data = super(CancelOrderForm, self).clean()
        return cleaned_data

class CalculatePredictionsForm(forms.Form):
    percentage_btc = forms.FloatField(required=True, min_value=-1000000, max_value=1000000)
    percentage_eth = forms.FloatField(required=True, min_value=-1000000, max_value=1000000)
    percentage_ltc = forms.FloatField(required=True, min_value=-1000000, max_value=1000000)
    def clean(self):
        cleaned_data = super(CalculatePredictionsForm, self).clean()
        return cleaned_data
