from django.contrib import admin
from .models import Material,Invoice_List,School,Deputy, Payment, order

class cash_(admin.ModelAdmin):
	list_display = ('cheque_no','bill','recieved_from','on_account_of','mode_of_payment','user')

class material_(admin.ModelAdmin):
	list_display = ('material_name','price')

class MembershipInline(admin.TabularInline):
	model = Invoice_List.description.through

class order_(admin.ModelAdmin):
	list_display = ('item','quantity','price','user','bill_no')
	inlines = [
        MembershipInline,
    ]

class invoice_list(admin.ModelAdmin):
	list_display = ('bill_no','get_desc','inclusive_amount','payment_recieved', 'user','date')
	inlines = [
        MembershipInline,
    ]
	exclude = ['description']


admin.site.register(Material,material_)
admin.site.register(Invoice_List, invoice_list)
admin.site.register(School)
admin.site.register(Deputy)
admin.site.register(Payment, cash_)
admin.site.register(order, order_)