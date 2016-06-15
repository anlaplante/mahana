# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
import django_filters

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Category(models.Model):
    categoryid = models.AutoField(db_column='CategoryID', primary_key=True)
    categoryname = models.CharField('Name', db_column='CategoryName', unique=True, max_length=25)
    categorycode = models.CharField('Code', db_column='CategoryCode', unique=True, max_length=1)
    isactive = models.BooleanField('Is active', db_column='Active', default=True)
    
    def __str__(self):
        return self.categoryname

    class Meta:
        managed = False
        db_table = 'category'

class Subcategory(models.Model):
    subcategoryid = models.AutoField(db_column='SubCategoryID', primary_key=True)
    subcategoryname = models.CharField(db_column='SubCategoryName', unique=True, max_length=25)
    subcategorycode = models.CharField(db_column='SubCategoryCode', unique=True, max_length=1)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='CategoryID', verbose_name='Category')
    isactive = models.BooleanField('Is active', db_column='Active', default=True)
    
    def __str__(self):
        return self.subcategoryname

    class Meta:
        managed = False
        db_table = 'subcategory'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Supplier(models.Model):
    supplierid = models.AutoField(db_column='SupplierID', primary_key=True)
    suppliername = models.CharField(db_column='SupplierName', max_length=30, verbose_name = 'Name')
    supplieraddress = models.CharField(db_column='SupplierAddress', max_length=150, blank=True, null=True, verbose_name = 'Address')
    supplieremailaddress = models.CharField(db_column='SupplierEmailAddress', max_length=150, blank=True, null=True, verbose_name = 'Email address')
    supplierphonenumber = models.CharField(db_column='SupplierPhoneNumber', max_length=20, blank=True, null=True, verbose_name = 'Phone number')
    supplierphonenumber2 = models.CharField(db_column='SupplierPhoneNumber2', max_length=20, blank=True, null=True, verbose_name = 'Phone number')
    
    def __str__(self):
        return self.suppliername

    class Meta:
        managed = False
        db_table = 'supplier'


class Invoice(models.Model):
    invoiceid = models.AutoField(db_column='InvoiceID', primary_key=True)
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationID', verbose_name="Location name")
    invoicecode = models.CharField(db_column='InvoiceCode', unique=True, max_length=8)
    invoicedate = models.DateField(db_column='InvoiceDate', verbose_name='Invoice date')
    totalamount = models.IntegerField(db_column='TotalAmount', verbose_name="Payment")
    buypricetotal = models.IntegerField(db_column='BuyPriceTotal', verbose_name="Purchase")
    discount = models.IntegerField(db_column='Discount', verbose_name="Discount")
    ppnamount = models.IntegerField(db_column='PPN', verbose_name="PPN")
    ispaid = models.BooleanField(db_column='IsPaid', verbose_name = 'Is paid ?')
    deposit = models.IntegerField(db_column='Deposit')
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50, blank=True)
    customername = models.CharField(db_column='CustomerName', max_length=50, blank=True)
    isorder = models.BooleanField(db_column='IsOrder')
    invoicenote = models.CharField(db_column='InvoiceNote', max_length=300, blank=True)
    deliverydate = models.DateField(db_column='DeliveryDate', verbose_name='Delivery date', blank=True,null=True)
    isfinished = models.BooleanField(db_column='IsFinished', default=False)
    pickuplocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='PickUpLocation', verbose_name="Pickup location", related_name='pickup_location')

    class Meta:
        managed = False
        db_table = 'invoice'

class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = {'invoicedate': ['lt']}
        #fields = ['totalamount']

class InvoiceNd(models.Model):
    invoiceid = models.AutoField(db_column='InvoiceID', primary_key=True)
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationID', verbose_name="Location name")
    invoicecode = models.CharField(db_column='InvoiceCode', unique=True, max_length=15)
    invoicedate = models.DateField(db_column='InvoiceDate')
    totalamount = models.IntegerField(db_column='TotalAmount')
    buypricetotal = models.IntegerField(db_column='BuyPriceTotal')
    discount = models.IntegerField(db_column='Discount')
    ppnamount = models.IntegerField(db_column='PPN', verbose_name="PPN")
    ispaid = models.BooleanField(db_column='IsPaid', verbose_name = 'Is paid ?')
    deposit = models.IntegerField(db_column='Deposit')

    class Meta:
        managed = False
        db_table = 'invoice_nd'

class Orders(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)
    invoiceid = models.OneToOneField(Invoice, models.DO_NOTHING, db_column='InvoiceID')
    deliverydate = models.DateField(db_column='DeliveryDate', verbose_name='Delivery date')
    finished = models.BooleanField('Is finished', db_column='Finished', default=False)
    pickuplocation = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='PickupLocation', verbose_name='Pickup location')

    class Meta:
        managed = False
        db_table = 'orders'


class Product(models.Model):
    productid = models.IntegerField(db_column='ProductID', primary_key=True)
    productname = models.CharField('Name', db_column='ProductName', max_length=30)
    reference = models.CharField('Reference', db_column='Reference', unique=True, max_length=5)
    picture = models.CharField(db_column='Picture', max_length=30, blank=True, null=True)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='CategoryID', verbose_name='Category')
    # subcategoryid = models.ForeignKey(Subcategory, models.DO_NOTHING, db_column='SubCategoryID', verbose_name='Sub Category')
    subcategoryid = ChainedForeignKey(Subcategory, chained_field='categoryid', chained_model_field='categoryid',  db_column='SubCategoryID', verbose_name='Sub Category')
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)
    buyingprice = models.IntegerField('Buying price', db_column='BuyingPrice')
    weight = models.DecimalField(db_column='Weight', max_digits=5, decimal_places=2, blank=True, null=True)
    saleprice = models.IntegerField('Sale price', db_column='SalePrice')
    salepricenotax = models.IntegerField(db_column='SalePriceNoTax')
    cubicsize = models.DecimalField('Cubic size', db_column='CubicSize', max_digits=5, decimal_places=2, blank=True, null=True)
    isactive = models.BooleanField('Is active', db_column='IsActive', default=True)
    stocklimit = models.IntegerField('Stock limit', db_column='StockLimit', default=0)
    isordered = models.BooleanField('Is ordered', db_column='IsOrdered', default=False)
    creationdate = models.DateField('Creation date', db_column='CreationDate', auto_now_add=True)
    suppliers = models.ManyToManyField(Supplier, through='SupplierProduct')
    
    def __str__(self):
        return self.productname

    class Meta:
        managed = False
        db_table = 'product'

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['subcategoryid','productname', 'saleprice']
        together = ['productname', 'saleprice']

class ProductInvoice(models.Model):
    productinvoiceid = models.AutoField(db_column='ProductInvoiceID', primary_key=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')
    invoiceid = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='InvoiceID', related_name='products')
    quantity = models.IntegerField(db_column='Quantity', verbose_name='Quantity')
    buyingprice = models.IntegerField(db_column='BuyingPrice', verbose_name='Buying price')
    saleprice = models.IntegerField(db_column='SalePrice', verbose_name='Sale price')
    isstock = models.BooleanField('Is stock', db_column='IsStock', default=False)
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationID', verbose_name="Location name",null=True)
    note = models.CharField('Note', db_column='Note', max_length=1000, blank=True)
    isordered = models.BooleanField('Is ordered', db_column='IsOrdered', default=False)
    isready = models.BooleanField('Is ready', db_column='IsReadyToPickUp', default=False)
    ispickedup = models.BooleanField('Is picked up', db_column='IsPickedUp', default=False)

    class Meta:
        managed = False
        db_table = 'product_invoice'


class ProductInvoiceNd(models.Model):
    productinvoiceid = models.AutoField(db_column='ProductInvoiceID', primary_key=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')
    invoiceid = models.ForeignKey(InvoiceNd, models.DO_NOTHING, db_column='InvoiceID', related_name='products')
    quantity = models.IntegerField(db_column='Quantity')
    buyingprice = models.IntegerField(db_column='BuyingPrice')
    saleprice = models.IntegerField(db_column='SalePrice')

    class Meta:
        managed = False
        db_table = 'product_invoice_nd'


class ProductOrder(models.Model):
    productorderid = models.AutoField(db_column='ProductOrderID', primary_key=True)
    #productinvoiceid = models.ForeignKey(ProductInvoice, models.DO_NOTHING, db_column='ProductInvoiceID', related_name='orderinfo')
    productinvoiceid = models.ForeignKey(ProductInvoice, models.DO_NOTHING, db_column='ProductInvoiceID')
    isstock = models.BooleanField(db_column='Stock', verbose_name = 'Is stock ?')
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationID')
    note = models.CharField(db_column='Note', max_length=1000)
    isorder = models.BooleanField(db_column='Order', verbose_name = 'Is order ?')
    isreadytopick = models.BooleanField(db_column='ReadyToPick')
    ispickedup = models.BooleanField(db_column='PickedUp', verbose_name = 'Already picked-up ?')

    class Meta:
        managed = False
        db_table = 'product_order'


class ProductProforma(models.Model):
    productproformaid = models.AutoField(db_column='ProductProformaID', primary_key=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')
    proformaid = models.ForeignKey('Proforma', models.DO_NOTHING, db_column='ProformaID', related_name='products')
    quantity = models.IntegerField(db_column='Quantity')
    buyingprice = models.IntegerField(db_column='BuyingPrice', verbose_name='Buying price')
    saleprice = models.IntegerField(db_column='SalePrice', verbose_name='Sale price')

    class Meta:
        managed = False
        db_table = 'product_proforma'


class Proforma(models.Model):
    proformaid = models.AutoField(db_column='ProformaID', primary_key=True)
    proformadate = models.DateField(db_column='ProformaDate')
    totalamount = models.IntegerField(db_column='TotalAmount')
    buypricetotal = models.IntegerField(db_column='BuyPriceTotal')
    discount = models.IntegerField(db_column='Discount')
    ppnamount = models.IntegerField(db_column='PPN', verbose_name="PPN")
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50, blank=True)
    customername = models.CharField(db_column='CustomerName', max_length=50, blank=True)
    proformanote = models.CharField(db_column='ProformaNote', max_length=300, blank=True)

    class Meta:
        managed = False
        db_table = 'proforma'

class SupplierProduct(models.Model):
    supplierproductid = models.AutoField(db_column='SupplierProductID', primary_key=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')
    supplierid = models.ForeignKey(Supplier, models.DO_NOTHING, db_column='SupplierID', verbose_name="Supplier name")
    supplierreference = models.CharField(db_column='SupplierReference', max_length=20, blank=True, null=True, verbose_name="Supplier reference")
    supplierprice = models.IntegerField(db_column='SupplierPrice', blank=True, null=True, verbose_name="Supplier price")

    class Meta:
        managed = False
        db_table = 'supplier_product'


class Stock(models.Model):
    productstockid = models.AutoField(db_column='ProductStockID', primary_key=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID', verbose_name="Product name")
    quantity = models.IntegerField(db_column='Quantity', verbose_name = 'Quantity')
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationID', verbose_name="Location name")

    class Meta:
        unique_together = ('productid', 'stocklocationid',)
        managed = False
        db_table = 'stock'

class StockLocation(models.Model):
    stocklocationid = models.AutoField(db_column='StockLocationID', primary_key=True)
    sl_code = models.CharField(db_column='SL_Code', max_length=3, verbose_name = 'Code')
    sl_name = models.CharField(db_column='SL_Name', max_length=30, verbose_name = 'Name')
    sl_address = models.CharField(db_column='SL_Address', max_length=150, verbose_name = 'Address')
    sl_sale = models.BooleanField(db_column='SL_Sale', verbose_name = 'Is store ?')
    invoiceprefix = models.CharField(db_column='InvoicePrefix', max_length=3, blank=True, verbose_name = 'Invoice prefix')
    lastinvoicenumber = models.IntegerField(db_column='LastInvoiceNumber', blank=True, verbose_name = 'Last invoice number')
    active = models.BooleanField(db_column='Active', verbose_name = 'Is Active ?')
    
    def __str__(self):
        return self.sl_name

    class Meta:
        managed = False
        db_table = 'stock_location'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey('StockLocation', models.DO_NOTHING, blank=True, null=True, db_column='StockLocationID', verbose_name='Store location')