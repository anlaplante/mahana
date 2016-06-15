from django.contrib import admin
from django.forms import ModelForm, Form
from django.forms.models import ModelChoiceField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Category, Subcategory, Product
from .models import Supplier, SupplierProduct, Employee
from .models import Invoice, ProductInvoice
from .models import StockLocation, Stock
#from .models import Continent, Country, Location

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryname', 'categorycode')

admin.site.register(Category, CategoryAdmin)

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['categorycode']

class SupplierInline(admin.TabularInline):
    model = SupplierProduct
    extra = 1

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    #form = ProductAdminForm
    inlines = (SupplierInline,StockInline,)
    list_display = ('productname','reference','subcategoryid','isactive')
    search_fields = ('productname', 'reference')
    list_filter = ('isactive','subcategoryid','subcategoryid__categoryid',)
    exclude = ('productid',)


admin.site.register(Product, ProductAdmin)

admin.site.register(Subcategory)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('suppliername', 'supplieremailaddress', 'supplierphonenumber', 'supplierphonenumber2')
admin.site.register(Supplier, SupplierAdmin)

admin.site.register(Stock)
admin.site.register(StockLocation)

class ProductInline(admin.TabularInline):
    model = ProductInvoice
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    #form = ProductAdminForm
    inlines = (ProductInline,)
    list_display = ('invoicecode','invoicedate','totalamount','buypricetotal','discount','ppnamount')

admin.site.register(Invoice, InvoiceAdmin)

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)