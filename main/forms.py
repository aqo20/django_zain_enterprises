from django import forms
import datetime
from .models import Material, School, Deputy, order, Invoice_List
from django.forms.models import ModelChoiceField
from django.conf import settings
from django.contrib.auth.models import User


GEEKS_CHOICES =( 
    ("Cash", "Cash"), 
    ("Cheque", "Cheque"), 
) 


class IL(forms.Form):
	quantity = forms.IntegerField()

class users1(forms.Form):
	users = forms.ModelChoiceField(queryset=User.objects.all())
	date = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}))

class invoicedetail(forms.Form):
	income_tax = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Putt a valid number between 0-100 in %'}))
	service_tax = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Putt a valid number between 0-100 in %'}))
	pst_tax = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Putt a valid number between 0-100 in %'}))
	sale_tax = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Putt a valid number between 0-100 in %'}))


class Payment_(forms.Form):
	recieved_with_thanks_from = forms.CharField()
	on_account_of = forms.CharField()
	mode_of_payment = forms.ChoiceField(choices = GEEKS_CHOICES)
	cheque_no = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Optional for Cash'}), required=False)
	phone_no = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Optional for Cash'}), required=False)
	