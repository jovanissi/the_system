from django.shortcuts import render, redirect
from manager.models import user_profile, bank_accounts, transactions
from django.contrib import auth
from datetime import datetime
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from manager.forms import RegistrationForm
from django.core.files import File

def manager_login(request):
	secure = {}

	secure.update(csrf(request))
	return render(request, 'manager_login_screen.html', secure)  #this is kinda done

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)  #this is kinda done

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('manager_account')  #this is kinda done
	else:
		return HttpResponseRedirect('invalid')

def invalid_login(request):
	return render(request, 'invalid_login.html')  #this is kinda done

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('login2')  #this is kinda done


@login_required(login_url="login2")
def manager_account(request):
	data = {}
	data['user_deposits'] = transactions.objects.all()
	data['bank_account'] = bank_accounts.objects.all()
	return render(request, 'manager_account_screen.html', data) #this is kinda done


@login_required(login_url="login2")
def all_deposits(request):
	data = {}
	data['bank_account'] = bank_accounts.objects.all()
	x = request.POST['in_from_date']
	y = request.POST['in_to_date']
	data['shareholders_deposits'] = transactions.objects.filter(trans_date__range=[x, y], categories='Approved', depositor_type='shareholder', trans_type='in_trans')
	data['others_deposits'] = transactions.objects.filter(trans_date__range=[x, y], depositor_type='other', categories='Approved', trans_type='in_trans')
	data['sum_others_deposits'] = transactions.objects.filter(trans_date__range=[x, y], depositor_type='other', categories='Approved', trans_type='in_trans').aggregate(sum=Sum('money_in'))['sum']
	data['sum_shareholders_deposits'] = transactions.objects.filter(trans_date__range=[x, y], categories='Approved', depositor_type='shareholder', trans_type='in_trans').aggregate(sum=Sum('money_in'))['sum']
	data['sum_in_time_range'] = transactions.objects.filter(trans_date__range=[x, y], categories='Approved', trans_type='in_trans').aggregate(sum=Sum('money_in'))['sum']
	
	return render(request, 'Month_in.html', data) #this is kinda done


@login_required(login_url="login2")
def deposits_per_account(request):
	data = {}
	data['bank_account'] = bank_accounts.objects.all()
	x = request.POST['in_from_date']
	y = request.POST['in_to_date']
	acc_number = request.POST['account_number']
	data['bank_name'] = bank_accounts.objects.filter(account_number=acc_number)
	data['shareholders_deposits'] = transactions.objects.filter(trans_date__range=[x, y], categories='Approved', depositor_type='shareholder', trans_type='in_trans', account_number=acc_number)
	data['others_deposits'] = transactions.objects.filter(trans_date__range=[x, y], depositor_type='other', categories='Approved', trans_type='in_trans', account_number=acc_number)
	data['sum_others_deposits'] = transactions.objects.filter(trans_date__range=[x, y], depositor_type='other', categories='Approved', trans_type='in_trans', account_number=acc_number).aggregate(sum=Sum('money_in'))['sum']
	data['sum_shareholders_deposits'] = transactions.objects.filter(trans_date__range=[x, y], categories='Approved', depositor_type='shareholder', trans_type='in_trans', account_number=acc_number).aggregate(sum=Sum('money_in'))['sum']
	data['sum_in_time_range'] = transactions.objects.filter(trans_date__range=[x, y], categories='Approved', trans_type='in_trans', account_number=acc_number).aggregate(sum=Sum('money_in'))['sum']
	
	return render(request, 'Month_in_2.html', data) #this is kinda done


@login_required(login_url="login2")
def all_withdrawals(request):
	data = {}
	data['bank_account'] = bank_accounts.objects.all()
	x = request.POST['out_from_date']
	y = request.POST['out_to_date']
	data['withdrew'] = transactions.objects.filter(trans_date__range=[x, y], trans_type='out_trans', categories='Approved')
	data['sum_withdrew'] = transactions.objects.filter(trans_date__range=[x, y], trans_type='out_trans', categories='Approved').aggregate(sum=Sum('money_out'))['sum']

	return render(request, 'Month_out.html', data) #this is kinda done


@login_required(login_url="login2")
def withdrawals_per_account(request):
	data = {}
	data['bank_account'] = bank_accounts.objects.all()
	x = request.POST['out_from_date']
	y = request.POST['out_to_date']
	acc_number = request.POST['account_number']
	data['bank_name'] = bank_accounts.objects.filter(account_number=acc_number)
	data['withdrew'] = transactions.objects.filter(trans_date__range=[x, y], trans_type='out_trans', categories='Approved', account_number=acc_number)
	data['sum_withdrew'] = transactions.objects.filter(trans_date__range=[x, y], trans_type='out_trans', categories='Approved', account_number=acc_number).aggregate(sum=Sum('money_out'))['sum']

	return render(request, 'Month_out_2.html', data) #this is kinda done


@login_required(login_url="login2")
def balance(request):
	data = {}
	data['bank_account'] = bank_accounts.objects.all()
	data['shareholders_deposits'] = transactions.objects.filter(depositor_type='shareholder', categories='Approved', trans_type='in_trans')
	data['others_deposits'] = transactions.objects.filter(depositor_type='other', categories='Approved', trans_type='in_trans')
	data['withdrew'] = transactions.objects.filter(trans_type='out_trans', categories='Approved')
	data['sum_shareholder_deposits'] = transactions.objects.filter(trans_type='in_trans', depositor_type='shareholder', categories='Approved').aggregate(sum=Sum('money_in'))['sum']
	data['sum_others_deposits'] = transactions.objects.filter(trans_type='in_trans', depositor_type='other', categories='Approved').aggregate(sum=Sum('money_in'))['sum']
	data['sum_withdrawals'] = transactions.objects.filter(trans_type='out_trans', categories='Approved').aggregate(sum=Sum('money_out'))['sum']
	data['sum_deposits'] = transactions.objects.filter(trans_type='in_trans', categories='Approved').aggregate(sum=Sum('money_in'))['sum']
	data['balance'] = bank_accounts.objects.all().aggregate(sum=Sum('balance'))['sum']
	
	return render(request, 'Balance.html', data) #this is kinda done


@login_required(login_url="login2")
def specific_balance(request):
	data = {}
	acc_number = request.POST['account_number']
	data['bank_name'] = bank_accounts.objects.filter(account_number=acc_number)
	data['bank_account'] = bank_accounts.objects.all()
	data['shareholders_deposits'] = transactions.objects.filter(depositor_type='shareholder', categories='Approved', trans_type='in_trans', account_number=acc_number)
	data['others_deposits'] = transactions.objects.filter(depositor_type='other', categories='Approved', trans_type='in_trans', account_number=acc_number)
	data['withdrew'] = transactions.objects.filter(trans_type='out_trans', categories='Approved', account_number=acc_number)
	data['sum_shareholder_deposits'] = transactions.objects.filter(trans_type='in_trans', depositor_type='shareholder', categories='Approved', account_number=acc_number).aggregate(sum=Sum('money_in'))['sum']
	data['sum_others_deposits'] = transactions.objects.filter(trans_type='in_trans', depositor_type='other', categories='Approved', account_number=acc_number).aggregate(sum=Sum('money_in'))['sum']
	data['sum_withdrawals'] = transactions.objects.filter(trans_type='out_trans', categories='Approved', account_number=acc_number).aggregate(sum=Sum('money_out'))['sum']
	data['sum_deposits'] = transactions.objects.filter(trans_type='in_trans', categories='Approved', account_number=acc_number).aggregate(sum=Sum('money_in'))['sum']
	data['balance'] = bank_accounts.objects.filter(account_number=acc_number).aggregate(sum=Sum('balance'))['sum']
	
	return render(request, 'specific_balance.html', data) #this is kinda done

@login_required(login_url="login2")
def kwinjiza(request):
	data = {}
	data['bank_account'] = bank_accounts.objects.all()
	return render(request, 'Kwinjiza.html', data) #this is kinda done

@login_required(login_url="login2")
def entering_others_deposits(request):
	date = request.POST['date']
	trans_type = request.POST['trans_type']
	depositor_type = request.POST['depositor_type']
	categories = request.POST['categories']
	classifications = request.POST['classifications']
	names = request.POST['names']
	cheque_number = request.POST['cheque_number']
	cheque_bank = request.POST['cheque_bank']
	account_number = request.POST['account_number']
	account_name = bank_accounts.objects.get(account_number=account_number).account_name
	slip_number = request.POST['slip_number']
	deposited_amount = request.POST['deposited_amount']
	comment = request.POST['comment']
	slip_picture = request.FILES['slip_picture']
	transactions.objects.create(
		trans_date = date,
		trans_type = trans_type,
		depositor_type = depositor_type,
		categories = categories,
		classifications = classifications,
		depositor_name = names,
		cheque_number = cheque_number,
		cheque_bank = cheque_bank,
		account_number = account_number,
		account_name = account_name,
		slip_number = slip_number,
		money_in = deposited_amount,
		trans_comment = comment,
		transaction_proof = slip_picture,
		)
	a = transactions.objects.filter(trans_type='out_trans', categories='Approved', account_number=account_number).aggregate(sum=Sum('money_out'))['sum']
	b = transactions.objects.filter(trans_type='in_trans', categories='Approved', account_number=account_number).aggregate(sum=Sum('money_in'))['sum']
	balance = b-a
	bank_accounts.objects.filter(account_number=account_number).update(balance=balance)
	return HttpResponseRedirect('manager_account')  #this is kinda done

@login_required(login_url="login2")
def withdraw(request):
	data = {}
	data['bank_account'] = bank_accounts.objects.all()

	return render(request, 'withdraw.html', data)

@login_required(login_url="login2")
def withdrawing(request):
	if request.method == 'POST':
		date = request.POST['date']
		trans_type = request.POST['trans_type']
		categories = request.POST['categories']
		account_number = request.POST['account_number']
		account_name = bank_accounts.objects.get(account_number=account_number).account_name
		slip_number = request.POST['slip_number']
		reason = request.POST['reason']
		withdraw_slip_picture = request.FILES['withdraw_slip_picture']
		withdrew_amount = float(request.POST['withdrew_amount'])
		surplus = float(request.POST['surplus'])
		a = withdrew_amount + surplus
		transactions.objects.create(
			trans_date = date,
			trans_type = trans_type,
			categories = categories,
			account_number = account_number,
			account_name = account_name,
			money_out = a,
			slip_number = slip_number,
			trans_comment = reason,
			transaction_proof = withdraw_slip_picture,
			)
		a = transactions.objects.filter(trans_type='out_trans', categories='Approved', account_number=account_number).aggregate(sum=Sum('money_out'))['sum']
		b = transactions.objects.filter(trans_type='in_trans', categories='Approved', account_number=account_number).aggregate(sum=Sum('money_in'))['sum']
		balance = b-a
		bank_accounts.objects.filter(account_number=account_number).update(balance=balance)
	return HttpResponseRedirect('manager_account')  #this is kinda done

@login_required(login_url="login2")
def validation(request, submission_id):
	data = {}
	data['user_deposits'] = transactions.objects.get(pk=submission_id)
	
	return render(request, 'Validation.html', data) #this is kinda done


@login_required(login_url="login2")
def validate(request):
	data = {}
	data['user_deposits'] = transactions.objects.filter(trans_type='in_trans', depositor_type='shareholder')
	specific = request.POST['slip_pk']
	transactions.objects.filter(slip_number=specific, trans_type='in_trans', depositor_type='shareholder').update(categories = 'Approved')

	return render(request, 'manager_account_screen.html', data) #this is kinda done (not sure)

@login_required(login_url="login2")
def not_valid(request):
	data = {}
	data['user_deposits'] = transactions.objects.filter(trans_type='in_trans', depositor_type='shareholder')
	specific = request.POST['slip_pk']
	transactions.objects.filter(shareholder_deposit_slip_number = share).update(categories = 'Unapproved')

	return render(request, 'manager_account_screen.html', data) #this is kinda done

@login_required(login_url="login2")
def sign_up_screen(request):
	return render(request, 'sign_up_screen.html')  #this is kinda done


@login_required(login_url="login2")
def account_created(request):
	return render(request, 'acc_created.html')  #this is kinda done

@login_required(login_url="login2")
def register(request):
	name = request.POST['first_name']
	surname = request.POST['last_name']
	position = request.POST['post']
	birth_date = request.POST['birth_date']
	national_id = request.POST['NID']
	email = request.POST['email']
	phone = request.POST['phone']
	username = request.POST['username']
	password = request.POST['password2']
	picture = request.FILES['user_picture']
	user_profile.objects.create(
		Name = name,
		Surname = surname,
		Occupied_post = position,
		Birth_date = birth_date,
		National_ID = national_id,
		E_mail = email,
		Phone = phone,
		Username = username,
		Password = password,
		User_picture = picture,
		)
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('account_created')  #this is kinda done

	else:
		form = RegistrationForm()

		args = {'form': form}
		return render(request, 'sign_up_screen.html', args)

@login_required(login_url="login2")
def new_bank_account(request):
	return render(request, 'new_bank_account.html')  #this is kinda done

@login_required(login_url="login2")
def bank_account(request):
	account_name = request.POST['account_name']
	account_number = request.POST['account_number']
	bank_name = request.POST['bank_name']
	proof_of_creation = request.FILES['proof_of_creation']
	creation_date = request.POST['creation_date']
	bank_accounts.objects.create(
		account_name = account_name,
		account_number = account_number,
		bank_name = bank_name,
		proof_of_creation = proof_of_creation,
		date_of_opening = creation_date,
		)
	return HttpResponseRedirect('bank_account_created')  #this is kinda done

@login_required(login_url="login2")
def bank_account_created(request):
	return render(request, 'bank_account_created.html')  #this is kinda done

@login_required(login_url="login2")
def specific_bank_account(request, bank_id):
	data = {}
	data['bank_account'] = bank_accounts.objects.get(pk=bank_id)
	return render(request, 'specific_bank_account.html', data)  #this is kinda done


@login_required(login_url="login2")
def in_transaction(request, in_trans_id):
	data = {}
	data['deposit'] = transactions.objects.get(pk=in_trans_id)
	return render(request, 'in_transaction.html', data)

@login_required(login_url="login2")
def out_transaction(request, out_trans_id):
	data = {}
	data['withdraw'] = transactions.objects.get(pk=out_trans_id)
	return render(request, 'out_transaction.html', data)

@login_required(login_url="login2")
def user_transaction(request, user_trans_id):
	data = {}
	data['deposit'] = transactions.objects.get(pk=user_trans_id)
	return render(request, 'user_transaction.html', data)