from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.manager_login, name='login'),
    url(r'^login2', views.manager_login, name= 'login'),
    url(r'^auth', views.auth_view, name = 'Auth'),
    url(r'^invalid', views.invalid_login, name = 'invalid'),
    url(r'^logout', views.logout, name = 'login'),
	url(r'^all_deposits', views.all_deposits, name='month_in'),
	url(r'^all_withdrawals', views.all_withdrawals, name='month_out'),
	url(r'^balance', views.balance, name='balance'),
	url(r'^deposit$', views.kwinjiza, name='kwinjiza'),
	url(r'^others_deposit', views.entering_others_deposits, name= 'kwinjiza'),
    url(r'^withdraw$', views.withdraw, name='withdraw'),
    url(r'^ayasohotse', views.withdrawing, name='withdrawing'),
    url(r'^0(?P<submission_id>\d+)$', views.validation, name='validation'),
    url(r'^manager_account', views.manager_account, name='manager_account'),
    url(r'^validate$', views.validate, name='valid'),
    url(r'^not_valid$', views.not_valid, name='invalid'),
    url(r'^sign_up_screen', views.sign_up_screen, name='sign_up_screen'),
    url(r'^register', views.register, name='register'),
    url(r'^account_created', views.account_created, name='account_created'),
    url(r'^new_bank_account$', views.new_bank_account, name='new_bank_account'),
    url(r'^bank_account$', views.bank_account, name='new_bank_account'),
    url(r'^bank_account_created',views.bank_account_created, name='bank_account_created'),
    url(r'^account-0(?P<bank_id>\d+)', views.specific_bank_account, name='specific_bank_account'),
    url(r'^deposits-per-account', views.deposits_per_account, name='month_in_2'),
    url(r'^withdrawals-per-account', views.withdrawals_per_account, name='month_out_2'),
    url(r'^specific-balance', views.specific_balance, name='specific_balance'),
    url(r'^in-transaction-0(?P<in_trans_id>\d+)', views.in_transaction, name='in_transaction'),
    url(r'^out-transaction-0(?P<out_trans_id>\d+)', views.out_transaction, name='out_transaction'),
    url(r'^user-transaction-0(?P<user_trans_id>\d+)', views.user_transaction, name='user_transaction'),
]

if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)