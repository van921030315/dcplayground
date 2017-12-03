from django.conf.urls import url
from mocktrade.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'update_price_all', update_price_all),
    url(r'gethistoryprice$', get_price_history),
    url(r'gethistoryprice_week', get_price_history_week),
    url(r'getpredictionprice', get_price_prediction),
    url(r'^dashboard/', dashboard, name="dashboard"),
    url(r'^index/', index),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/', register, name="register"),
    url(r'^trade/', trade, name="trade"),
    url(r'^addusd/', add_usd, name="addusd"),
    url(r'^addcurrency/', buy_currency, name="addcurrency"),
    url(r'^sellcurrency/', sell_currency, name="sellcurrency"),
    url(r'^viewtransactions/', view_transactions, name="viewtransactions"),
    url(r'^vieworders/', view_orders, name="vieworders"),
    url(r'^postbuyorder/', post_buy_order, name="postbuyorder"),
    url(r'^postsellorder/', post_sell_order, name="postsellorder"),
    url(r'^viewcreatebuyorderpage/', view_create_buy_order_page, name="viewcreatebuyorderpage"),
    url(r'^viewcreatesellorderpage/', view_create_sell_order_page, name="viewcreatesellorderpage"),
    url(r'^cancelorder/', cancel_order, name="cancelorder"),
    url(r'^leaderboard/', view_leaderboard, name="leaderboard"),
    url(r'^investments/', view_investments, name="investments"),
    url(r'^getuserinvestments/', get_user_investments, name="getuserinvestments"),
    url(r'^export/',export_to_csv , name="export"),
    url(r'^manualpredictions/',view_manual_predictions, name="manualpredictions"),
    url(r'^calculatepredictions/',calculate_predictions, name="calculatepredictions"),
    url(r'^news/$', get_news, name="gnews"),
    url(r'^.*$', index),
]
