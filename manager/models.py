from django.db import models
from datetime import datetime


class user_profile(models.Model):
	Name = models.CharField(max_length=50, blank=False)
	Surname = models.CharField(max_length=50, blank=False)
	Occupied_post = models.CharField(max_length=20, blank=False)
	Birth_date = models.DateField(blank=False)
	National_ID = models.CharField(max_length=50, blank=False)
	E_mail = models.CharField(max_length=50, blank=True)
	Phone = models.CharField(max_length=50, blank=False)
	Username = models.CharField(max_length=50, blank=False)
	Password = models.CharField(max_length=100, blank=False)
	User_picture = models.FileField(upload_to='uploads/User_profile_pictures')

	def __str__(self):
		return self.Name


class bank_accounts(models.Model):
	account_name = models.CharField(max_length=70, blank=False)
	account_number = models.CharField(max_length=50, blank=False)
	bank_name = models.CharField(max_length=70, blank=False)
	date_of_opening = models.DateField(default=datetime.now, blank=False)
	proof_of_creation = models.FileField(upload_to='uploads/Accounts_proofs', default='null')
	balance = models.CharField(max_length=70, default=0)

	def __str__(self):
		return self.account_name


class transactions(models.Model):
	trans_date = models.DateField(default=datetime.now, blank=True)
	account_name = models.CharField(max_length=30, blank=True)
	account_number = models.CharField(max_length=30, blank=True)
	in_trans = 'in_trans'
	out_trans = 'out_trans'
	trans_choices = {
	(in_trans, 'in_trans'),
	(out_trans, 'out_trans'),
	}
	trans_type = models.CharField(max_length=20, blank=True, choices=trans_choices)
	shareholder = 'shareholder'
	other = 'other'
	depositor_type_choices = {
	(shareholder, 'shareholder'),
	(other, 'other'),
	}
	depositor_type = models.CharField(max_length=30, blank=True, choices=depositor_type_choices)
	depositor_name = models.CharField(max_length=50, blank=True)
	contribution_months = models.CharField(max_length=200, blank=True)
	reference = models.IntegerField(default=0, blank=True)
	Approved = 'Approved'
	Unapproved = 'Unapproved'
	Pending = 'Pending'
	category_choices = {
	(Approved, 'Approved'),
	(Unapproved, 'Unapproved'),
	(Pending, 'Pending'),
	}
	categories = models.CharField(max_length=30, blank=True, choices=category_choices, default="Pending")
	Cash = 'Cash'
	Cheque = 'Cheque'
	classification_choices = {
	(Cash, 'Cash'),
	(Cheque, 'Cheque'),
	}
	classifications = models.CharField(max_length=30, blank=True, choices=classification_choices, default="Cash")
	cheque_number = models.CharField(max_length=50, blank=True, default='null')
	cheque_bank = models.CharField(max_length=80, blank=True, default='null')
	slip_number = models.CharField(max_length=50, default='null', blank=True)
	trans_comment = models.TextField(blank=True)
	money_in = models.IntegerField(default=0, blank=True)
	money_out = models.IntegerField(default=0, blank=True)
	transaction_proof = models.FileField(upload_to='uploads/transaction proofs', default='null', blank=True)
	

	def __str__(self):
		return self.slip_number

