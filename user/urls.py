from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^login1', views.login, name= 'login'),
	url(r'^auth', views.auth_view, name = 'Auth'),
	url(r'^invalid', views.invalid_login, name = 'invalid'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^user_account', views.user_account, name='user_account'),
	url(r'^deposit', views.bitsa, name='bitsa'),
	url(r'^withdrawals', views.ayasohotse, name='ayasohotse'),
	url(r'^user_deposit', views.user_deposit, name='ayasohotse'),
	url(r'^shareholder_deposit', views.deposit_by_shareholder, name='shareholder_deposit'),
	url(r'^out-transaction-0(?P<out_trans_id>\d+)', views.out_transaction, name='out_transaction'),
	url(r'^user-transaction-0(?P<user_trans_id>\d+)', views.user_transaction, name='user_transaction'),
]

if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)