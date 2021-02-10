from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as auth, login as dj_login, logout as dj_logout
from .models import Material, Invoice_List, School, order, Deputy, Payment
from django.utils import timezone
from .forms import IL, users1, invoicedetail, Payment_
from .utils import render_to_pdf
from django.http import HttpResponse

# Create your views here.
def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth(request, username=username, password=password)
		if user is not None:
			dj_login(request, user)
			return redirect('myapp:welcome')
	context = {}
	return render(request, 'login.html', context)

def logout(request):
	dj_logout(request)
	return redirect('myapp:login')

def welcome(request):
	return render(request, 'message.html')

def daily(request):
	form = users1()
	if request.method == 'POST':
		form = users1(request.POST)
		if form.is_valid():
			users = form.cleaned_data['users']
			date = form.cleaned_data['date']
			obj = Invoice_List.objects.filter(user=users, date=date)
			obj1 = len(obj)
			print(users, date)
			return render(request, 'daily.html',{'form':form,'obj':obj,'obj1':obj1})
	return render(request, 'daily.html',{'form':form})

def school_report(request):
	school = School.objects.all()
	if request.method == 'POST':
		if 'form6' in request.POST:
			school = request.POST["school"]
			schools = School.objects.get(school_name=school)
			schoo = Invoice_List.objects.filter(school=schools)
			obj1 = len(schoo)
			schoo = {'schoo':Invoice_List.objects.filter(school=schools)}
			schoo.update(schools=schools)
			schoo.update(obj1=obj1)
			pdf = render_to_pdf('school_data.html', schoo)
			return HttpResponse(pdf, content_type='application/pdf')
		else:
			school = request.POST["school"]
			if School.objects.filter(school_name=school):
				pass
			else:
				message3 = "Please Enter a Valid School Name."
				return render(request, 'message.html',{'message3':message3})
			schools = School.objects.get(school_name=school)
			schoo = Invoice_List.objects.filter(school=schools)
			obj1 = len(schoo)
			return render(request, 'school_report.html', {'schol':schoo,'obj1':obj1,'school':school})
	return render(request, 'school_report.html', {'school':school})

def check(request, *args, **kwargs):
	if request.method == 'POST':
		bill_no = request.POST.get('bill_new')
		if Invoice_List.objects.filter(bill_no=bill_no):
			pass
		else:
			message4 = "Please Enter a Valid Bill Number."
			return render(request, 'message.html',{'message4':message4,'bill_no':bill_no})
		order1 = {'order1':order.objects.filter(bill_no=bill_no)}
		check_bill = {'check_bill':Invoice_List.objects.get(bill_no=bill_no)}
		check_bill.update(order1)
		return render(request, 'check.html', check_bill)
	return render(request, 'check.html')

def billing(request):
	form = IL()
	material = Material.objects.all()
	if request.method == 'POST':
		if 'form' in request.POST:
			form = IL(request.POST)
			if form.is_valid():
				material = Material.objects.all()
				bill_no =request.POST["bill_no"]
				item = request.POST["material"]
				quantity = form.cleaned_data['quantity']
				order1 = order.objects.filter(user=request.user, bill_no=bill_no)
				order_qs = order.objects.filter(user=request.user, item=item, bill_no=bill_no)
				ac_price = Material.objects.get(material_name=item)
				act_price = ac_price.price
				price = int(quantity)* int(act_price)
				if order_qs.exists():
					order_qs = order.objects.get(user=request.user, item=item, bill_no=bill_no)
					quantity = int(quantity)
					order_qs.quantity += quantity
					order_qs.save()
					order_qs.price += quantity*act_price
					order_qs.save()
					order_qs = order.objects.filter(user=request.user, bill_no=bill_no)
					price = 0
					for odd in order_qs:
						price += odd.price

					ex_amount = price
					return render(request, 'billing.html',{'form':form,'order1':order1,'bill_new':bill_no,'material':material,'ex_amount':ex_amount})
				else:
					order_item = order.objects.create(user=request.user, bill_no=bill_no, item=item, quantity=quantity, price=price)
					order_qs = order.objects.filter(user=request.user, bill_no=bill_no)
					price = 0
					for odd in order_qs:
						price += odd.price

					ex_amount = price
					return render(request, 'billing.html',{'form':form,'order1':order1,'bill_new':bill_no,'material':material,'ex_amount':ex_amount})
				#added.description.add(order_item)
				print(item, quantity)
		elif 'form1' in request.POST:
			material = Material.objects.all()
			bill_no =request.POST["bill_no"]
			item = request.POST["material"]
			order1 = order.objects.filter(user=request.user, bill_no=bill_no)
			order_qs = order.objects.filter(user=request.user, item=item, bill_no=bill_no)
			if order_qs.exists():
				order_qs = order.objects.get(user=request.user, item=item, bill_no=bill_no)
				order_qs.delete()
				order_qs = order.objects.filter(user=request.user, bill_no=bill_no)
				price = 0
				for odd in order_qs:
					price += odd.price

				ex_amount = price
				return render(request, 'billing.html',{'form':form,'order1':order1,'bill_new':bill_no,'material':material,'ex_amount':ex_amount})
			else:
				print("Materal not found..!!!!")
				return render(request, 'billing.html',{'form':form,'order1':order1,'bill_new':bill_no,'material':material})
		elif 'form2' in request.POST:
			material = Material.objects.all()
			bill_no =request.POST["bill_new"]
			if Invoice_List.objects.filter(bill_no=bill_no):
				message = "This Bill Number is already in database. Please Generate a valid bill number."
				return render(request, 'message.html',{'bill_no':bill_no,'message':message})
			else:
				pass
			order1 = order.objects.filter(user=request.user, bill_no=bill_no)
			price = 0
			for odd in order1:
				price += odd.price

			ex_amount = price
			return render(request, 'billing.html',{'form':form,'order1':order1,'bill_new':bill_no,'material':material,'ex_amount':ex_amount})
	return render(request, 'billing.html',{'form':form,'material':material})

def new_billing(request):
	return render(request, 'new_billing.html')



def details(request):
	deputy = Deputy.objects.all()
	school = School.objects.all()
	form = invoicedetail()
	if request.method == 'POST':
		if 'form3' in request.POST:
			bill_new =request.POST["bill_no"]
			order1 = order.objects.filter(user=request.user, bill_no=bill_new)
			price = 0
			for odd in order1:
				price += odd.price

			ex_amount = price
			return render(request, 'details.html',{'form':form,'bill_new':bill_new, 'deputy':deputy, 'school':school,'order1':order1,'ex_amount':ex_amount})
		elif 'form4' in request.POST:
			form = invoicedetail(request.POST)
			if form.is_valid():
				bill_no =request.POST["bill_no"]
				school = request.POST["school"]
				schools = School.objects.get(school_name=school)
				deputy = request.POST["deputy"]
				deputys = Deputy.objects.get(deputy_name=deputy)
				income_tax = form.cleaned_data['income_tax']
				service_tax = form.cleaned_data['service_tax']
				pst_tax = form.cleaned_data['pst_tax']
				sale_tax = form.cleaned_data['sale_tax']
				payment_recieved = False
				order_qs = order.objects.filter(user=request.user, bill_no=bill_no)
				price = 0
				for odd in order_qs:
					price += odd.price

				ex_amount = price
				inclusive_amount = ex_amount + int(sale_tax) + int(pst_tax)+ int(service_tax) + int(income_tax)
				print(schools.id)
				added,cretaed = Invoice_List.objects.get_or_create(user=request.user, school=schools, deputy=deputys, bill_no=bill_no, PST_tax=pst_tax, service_tax=service_tax, income_tax=income_tax, ex_amount=ex_amount, sale_tax=sale_tax, inclusive_amount=inclusive_amount, payment_recieved=payment_recieved)
				added = Invoice_List.objects.get(user=request.user, bill_no=bill_no)
				#orderr = order.objects.all()
				#print(order_qs)
				#added.description.remove(*orderr)
				added.description.add(*order_qs)
				print(added.description)
				message2 = "Please Copy the Bill Number"
				return render(request, 'message.html',{'bill_no':bill_no,'message2':message2})
	return render(request, 'details.html',{'form':form, 'deputy':deputy, 'school': school})

def payment(request):
	form = Payment_()
	bill_no = Invoice_List.objects.filter(payment_recieved=False)
	if request.method == 'POST':
		form = Payment_(request.POST)
		if form.is_valid():
			bill_no =request.POST["bill_no"]
			if Invoice_List.objects.filter(bill_no=bill_no,payment_recieved=False):
				pass
			else:
				message5 = "Not a valid bill number."
				return render(request, 'message.html',{'bill_no':bill_no,'message5':message5})
			bill_no =Invoice_List.objects.get(bill_no=bill_no)
			recieved_from = form.cleaned_data['recieved_with_thanks_from']
			on_account_of = form.cleaned_data['on_account_of']
			mode_of_payment = form.cleaned_data['mode_of_payment']
			cheque_no = form.cleaned_data['cheque_no']
			phone_no = form.cleaned_data['phone_no']
			added = Invoice_List.objects.get(bill_no=str(bill_no))
			added.payment_recieved=True
			added.save()
			cash = Payment.objects.create(user=request.user, bill=bill_no, recieved_from=recieved_from, on_account_of=on_account_of, mode_of_payment=mode_of_payment, cheque_no=cheque_no, phone_no=phone_no)
			cash.save()
			message2 = "Succesfully added payment against the Bill."
			return render(request, 'message.html',{'message2':message2,'bill_no':bill_no})
	return render(request, 'payment.html',{'form':form,'bill_no':bill_no})

def print_bill(request):
	if request.method == 'POST':
		bill_no = request.POST.get('bill_no')
		order1 = {'order1':order.objects.filter(bill_no=bill_no)}
		check_bill = {'check_bill':Invoice_List.objects.get(bill_no=bill_no)}
		check_bill.update(order1)
		pdf = render_to_pdf('print_billing.html', check_bill)
		return HttpResponse(pdf, content_type='application/pdf')