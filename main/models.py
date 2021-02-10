from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Material(models.Model):
	material_name = models.CharField(max_length=200)
	price = models.IntegerField()
	slug = models.SlugField()

	def __str__(self):
		return self.material_name

class order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	bill_no = models.IntegerField()
	item = models.CharField(max_length=100)
	quantity = models.IntegerField()
	price = models.IntegerField()

	def __str__(self):
		#return f"{self.quantity} of {self.item}"
		#return f"{self.quantity}"
		return "{0} {1}".format(self.item,self.quantity)

class School(models.Model):
	school_name = models.CharField(max_length=200)

	def __str__(self):
		return self.school_name
		
class Deputy(models.Model):
	deputy_name = models.CharField(max_length=200)

	def __str__(self):
		return self.deputy_name

class Invoice_List(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
	date = models.DateTimeField(auto_now_add=True)
	bill_no = models.IntegerField()
	deputy =  models.ForeignKey(Deputy, on_delete=models.CASCADE)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	description = models.ManyToManyField('order')
	ex_amount = models.IntegerField()
	sale_tax = models.IntegerField()
	income_tax = models.IntegerField()
	service_tax = models.IntegerField()
	PST_tax = models.IntegerField()
	inclusive_amount = models.IntegerField()
	payment_recieved = models.BooleanField()

	def __str__(self):
		return str(self.bill_no)

	def get_desc(self):
		return ",\n".join([p.item for p in self.description.all()])

class Payment(models.Model):
	class payment_choices(models.TextChoices):
		by_Cash = 'Cash', _('Cash')
		by_Cheque = 'Cheque', _('Cheque')

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
	bill = models.ForeignKey(Invoice_List, on_delete=models.CASCADE)
	date_cash = models.DateTimeField(auto_now_add=True)
	recieved_from = models.CharField(max_length=100)
	on_account_of = models.CharField(max_length=100) 
	mode_of_payment = models.CharField(max_length=10, choices=payment_choices.choices)
	cheque_no = models.IntegerField(blank=True, null=True)
	phone_no = models.IntegerField(blank=True, null=True)
