# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


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
    categoryid = models.AutoField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField('Name', db_column='CategoryName', unique=True, max_length=25)  # Field name made lowercase.
    categorycode = models.CharField('Code', db_column='CategoryCode', unique=True, max_length=1)  # Field name made lowercase.
    
    def __str__(self):
        return self.categoryname

    class Meta:
        managed = False
        db_table = 'category'


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


class Invoice(models.Model):
    invoiceid = models.AutoField(db_column='InvoiceID', primary_key=True)  # Field name made lowercase.
    invoicecode = models.CharField(db_column='InvoiceCode', unique=True, max_length=20)  # Field name made lowercase.
    invoicedate = models.DateField(db_column='InvoiceDate')  # Field name made lowercase.
    totalamount = models.IntegerField(db_column='TotalAmount')  # Field name made lowercase.
    buypricetotal = models.IntegerField(db_column='BuyPriceTotal')  # Field name made lowercase.
    discount = models.IntegerField(db_column='Discount')  # Field name made lowercase.
    retailequivalent = models.IntegerField(db_column='RetailEquivalent')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceNd(models.Model):
    invoiceid = models.AutoField(db_column='InvoiceID', primary_key=True)  # Field name made lowercase.
    invoicecode = models.CharField(db_column='InvoiceCode', unique=True, max_length=15)  # Field name made lowercase.
    invoicedate = models.DateField(db_column='InvoiceDate')  # Field name made lowercase.
    totalamount = models.IntegerField(db_column='TotalAmount')  # Field name made lowercase.
    buypricetotal = models.IntegerField(db_column='BuyPriceTotal')  # Field name made lowercase.
    discount = models.IntegerField(db_column='Discount')  # Field name made lowercase.
    retailequivalent = models.IntegerField(db_column='RetailEquivalent')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice_nd'
"""
class LocationLink(models.Model):
    locationlinkid = models.AutoField(db_column='LocationLinkID', primary_key=True)  # Field name made lowercase.
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationId')  # Field name made lowercase.
    linkedlocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='LinkedLocationId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'location_link'
"""

class Orders(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    invoiceid = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='InvoiceID', unique=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50)  # Field name made lowercase.
    customername = models.CharField(db_column='CustomerName', max_length=50)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20)  # Field name made lowercase.
    deposit = models.IntegerField(db_column='Deposit')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orders'


class Product(models.Model):
    productid = models.IntegerField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=30)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', unique=True, max_length=5)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=30, null=True)  # Field name made lowercase.
    subcategoryid = models.ForeignKey('Subcategory', models.DO_NOTHING, db_column='SubCategoryID')  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    buyingprice = models.IntegerField(db_column='BuyingPrice')  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    saleprice = models.IntegerField(db_column='SalePrice')  # Field name made lowercase.
    salepricenotax = models.IntegerField(db_column='SalePriceNoTax')  # Field name made lowercase.
    cubicsize = models.DecimalField(db_column='CubicSize', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField(db_column='Active')  # Field name made lowercase.
    ordered = models.IntegerField(db_column='Ordered')  # Field name made lowercase.
    
    def __str__(self):
        return self.productname

    class Meta:
        managed = False
        db_table = 'product'


class ProductInvoice(models.Model):
    productinvoiceid = models.AutoField(db_column='ProductInvoiceID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    invoiceid = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='InvoiceID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    buyingprice = models.IntegerField(db_column='BuyingPrice')  # Field name made lowercase.
    saleprice = models.IntegerField(db_column='SalePrice')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_invoice'


class ProductInvoiceNd(models.Model):
    productinvoiceid = models.AutoField(db_column='ProductInvoiceID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    invoiceid = models.ForeignKey(InvoiceNd, models.DO_NOTHING, db_column='InvoiceID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    buyingprice = models.IntegerField(db_column='BuyingPrice')  # Field name made lowercase.
    saleprice = models.IntegerField(db_column='SalePrice')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_invoice_nd'


class ProductOrder(models.Model):
    productorderid = models.AutoField(db_column='ProductOrderID', primary_key=True)  # Field name made lowercase.
    productinvoiceid = models.ForeignKey(ProductInvoice, models.DO_NOTHING, db_column='ProductInvoiceID')  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock')  # Field name made lowercase.
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationID')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=1000)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    readytopick = models.IntegerField(db_column='ReadyToPick')  # Field name made lowercase.
    pickedup = models.IntegerField(db_column='PickedUp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_order'


class ProductProforma(models.Model):
    productproformaid = models.AutoField(db_column='ProductProformaID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    proformaid = models.ForeignKey('Proforma', models.DO_NOTHING, db_column='ProformaID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_proforma'


class Proforma(models.Model):
    proformaid = models.AutoField(db_column='ProformaID', primary_key=True)  # Field name made lowercase.
    proformacode = models.CharField(db_column='ProformaCode', unique=True, max_length=15)  # Field name made lowercase.
    proformadate = models.DateField(db_column='ProformaDate')  # Field name made lowercase.
    totalamount = models.IntegerField(db_column='TotalAmount')  # Field name made lowercase.
    buypricetotal = models.IntegerField(db_column='BuyPriceTotal')  # Field name made lowercase.
    discount = models.IntegerField(db_column='Discount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proforma'


class Provider(models.Model):
    providerid = models.AutoField(db_column='ProviderID', primary_key=True)  # Field name made lowercase.
    providername = models.CharField(db_column='ProviderName', max_length=30)  # Field name made lowercase.
    provideraddress = models.CharField(db_column='ProviderAddress', max_length=150, blank=True, null=True)  # Field name made lowercase.
    providerphonenumber = models.CharField(db_column='ProviderPhoneNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.providername

    class Meta:
        managed = False
        db_table = 'provider'


class ProviderProduct(models.Model):
    providerproductid = models.AutoField(db_column='ProviderProductID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    providerid = models.ForeignKey(Provider, models.DO_NOTHING, db_column='ProviderID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'provider_product'

class Stock(models.Model):
    productstockid = models.AutoField(db_column='ProductStockID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    stocklocationid = models.ForeignKey('StockLocation', models.DO_NOTHING, db_column='StockLocationID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock'


class StockLocation(models.Model):
    stocklocationid = models.AutoField(db_column='StockLocationID', primary_key=True)  # Field name made lowercase.
    sl_code = models.CharField(db_column='SL_Code', max_length=3)  # Field name made lowercase.
    sl_name = models.CharField(db_column='SL_Name', max_length=30)  # Field name made lowercase.
    sl_address = models.CharField(db_column='SL_Address', max_length=150)  # Field name made lowercase.
    sl_sale = models.IntegerField(db_column='SL_Sale')  # Field name made lowercase.
    invoiceprefix = models.CharField(db_column='InvoicePrefix', max_length=3)  # Field name made lowercase.
    lastinvoicenumber = models.IntegerField(db_column='LastInvoiceNumber')  # Field name made lowercase.
    active = models.IntegerField(db_column='Active')  # Field name made lowercase.
    
    def __str__(self):
        return self.sl_name

    class Meta:
        managed = False
        db_table = 'stock_location'


class Subcategory(models.Model):
    subcategoryid = models.AutoField(db_column='SubCategoryID', primary_key=True)  # Field name made lowercase.
    subcategoryname = models.CharField(db_column='SubCategoryName', unique=True, max_length=25)  # Field name made lowercase.
    subcategorycode = models.CharField(db_column='SubCategoryCode', unique=True, max_length=1)  # Field name made lowercase.
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='CategoryID')  # Field name made lowercase.
    
    def __str__(self):
        return self.subcategoryname

    class Meta:
        managed = False
        db_table = 'subcategory'

class Publication(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    class Meta:
        ordering = ('title',)

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    def __str__(self):              # __unicode__ on Python 2
        return self.headline

    class Meta:
        ordering = ('headline',)