from django.shortcuts import render, redirect
from django.contrib import auth
from manager.models import user_profile, bank_accounts, transactions
from .backends import CustomUserAuth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import contenttypes
from django.views.decorators.csrf import csrf_protect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from manager.forms import RegistrationForm



@login_required(login_url="login1")
def user_account(request):

	data = {}
	data['user'] = request.user
	first_name = request.user.first_name
	last_name = request.user.last_name
	email = request.user.email
	data['umwirondoro'] = user_profile.objects.filter(Name=first_name, Surname=last_name, E_mail=email)
	
	return render(request, 'user_account_screen.html', data) #this is kinda done

@login_required(login_url="login1")
def bitsa(request):
	data = {}
	data['user'] = request.user
	data['umwirondoro'] = user_profile.objects.all()
	data['bank_account'] = bank_accounts.objects.all()

	return render(request, 'bitsa.html', data) #this is kinda done

@login_required(login_url="login1")
def ayasohotse(request):
	data = {}
	data['all_withdrawals'] = transactions.objects.filter(trans_type='out_trans', categories='Approved')
	data['sum_deposits'] = transactions.objects.filter(trans_type='in_trans', categories='Approved').aggregate(sum=Sum('money_in'))['sum']
	data['sum_withdrawals'] = transactions.objects.filter(trans_type='out_trans', categories='Approved').aggregate(sum=Sum('money_out'))['sum']
	data['balance'] = bank_accounts.objects.all().aggregate(sum=Sum('balance'))['sum']

	return render(request, 'ayasohotse.html', data) #this is kinda done

@login_required(login_url="login1")
def user_deposit(request):
	data = {}
	data['user'] = request.user
	x =  request.user.id
	data['user_deposits'] = transactions.objects.filter(reference=x, trans_type='in_trans', depositor_type='shareholder')
	data['sum_user_deposits'] = transactions.objects.filter(reference=x, categories='Approved', trans_type='in_trans', depositor_type='shareholder').aggregate(sum=Sum('money_in'))['sum']

	return render(request, 'nabikije.html', data) #this is kinda done

@login_required(login_url="login1")
def deposit_by_shareholder(request):
	if request.method == 'POST':
		date = request.POST['date']
		trans_type = request.POST['trans_type']
		depositor_type = request.POST['depositor_type']
		categories = request.POST['categories']
		depositor_names = request.POST['depositor_names']
		account_number = request.POST['account_number']
		account_name = bank_accounts.objects.get(account_number=account_number).account_name
		slip_number = request.POST['slip_number']
		deposited_amount = request.POST['deposited_amount']
		number_of_months = request.POST.getlist('number_of_months')
		comment = request.POST['comment']
		slip_picture = request.FILES['slip_picture']
		user_id = request.POST['user_id']
		transactions.objects.create(
			trans_date = date,
			trans_type = trans_type,
			depositor_type = depositor_type,
			categories = categories,
			depositor_name = depositor_names,
			account_number = account_number,
			account_name = account_name,
			slip_number = slip_number,
			money_in = deposited_amount,
			contribution_months = number_of_months,
			trans_comment = comment,
			transaction_proof = slip_picture,
			reference = user_id,
			)

		send_mail(
			'Deposit by %s'%depositor_names,
			'Deposited on %s'%date,
			'corenotifications2017@gmail.com',
			['nissijova@gmail.com'],
			fail_silently = False,
			)
	return HttpResponseRedirect('bitsa') #this is kinda done

def login(request):
	secure = {}

	secure.update(csrf(request))
	return render(request, 'login_screen.html', secure)


def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('user_account')
	else:
		return HttpResponseRedirect('invalid')

def invalid_login(request):
	return render(request, 'invalid.html')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('login1')

@login_required(login_url="login1")
def out_transaction(request, out_trans_id):
	data = {}
	data['withdraw'] = transactions.objects.get(pk=out_trans_id)
	return render(request, 'out_transaction.html', data)

@login_required(login_url="login1")
def user_transaction(request, user_trans_id):
	data = {}
	data['deposit'] = transactions.objects.get(pk=user_trans_id)
	return render(request, 'user_transaction.html', data)
