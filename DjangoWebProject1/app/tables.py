import django_tables2 as tables
from .models import Stock, StockLocation, Product, Invoice
from django_tables2.utils import A
from django.contrib.humanize.templatetags.humanize import intcomma

class ColumnWithThousandsSeparator(tables.Column):
    def render(self,value):
        return intcomma(value)

class ProductTable(tables.Table):
    reference = tables.Column(orderable=False)
    subcategoryid = tables.Column(orderable=False, attrs={"td": {"class": "text-center"}})
    #productid = tables.Column(visible=False)
    productname = tables.Column(orderable=False)
    #categoryid = tables.Column(orderable=False, attrs={"td": {"class": "text-center"}})
    #size = tables.Column(visible=False)
    #buyingprice = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    #weight = tables.Column(visible=False)
    saleprice = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    #cubicsize = tables.Column(visible=False)
    #isactive = tables.Column(visible=False)
    #stocklimit = tables.Column(visible=False)
    #isordered = tables.BooleanColumn(orderable=False, attrs={"td": {"class": "text-center"}})
    info = tables.LinkColumn('product_detail', text='details', args=[A('pk')], orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}})

    class Meta:
        #model = Product
        attrs = {"class": "table table-center"}
        order_by = ('reference')
        exclude = ("salepricenotax", )
        empty_text = "You must select a category"

class InvoiceTable(tables.Table):
    invoiceid = tables.Column(visible=False)
    invoicecode = tables.Column(orderable=False)
    #invoicedate = tables.DateColumn(format='d/m/Y', orderable=False)
    totalamount = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    ppnamount = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    #discount = tables.Column(orderable=False, attrs={"td": {"class": "text-right"}})
    buypricetotal = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    #retailequivalent = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    info = tables.LinkColumn('invoice_detail', text='details', args=[A('pk')], orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}})
    
    class Meta:
        model = Invoice
        exclude = {'invoicedate', 'discount', 'deposit', 'emailaddress', 'customername', 'paid'}
        attrs = {"class": "table table-center"}
        localize = ('totalamount','buypricetotal', 'ppnamount')
        order_by = ('-invoicecode')

class ProductInvoiceTable(tables.Table):
    productinvoiceid = tables.Column(visible=False)
    productid = tables.Column(verbose_name='Product name', orderable=False)
    #invoiceid = tables.Column(orderable=False)
    quantity = tables.Column(orderable=False, attrs={"td": {"class": "text-center"}})
    buyingprice = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-center"}})
    saleprice = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-center"}})
    
    class Meta:
        attrs = {"class": "table table-center"}
        order_by = ('productinvoiceid')

  
class StockLocationTable(tables.Table):
    productid = tables.Column(visible=False)
    reference = tables.Column(orderable=False)
    productname = tables.Column(verbose_name='Product name', orderable=False)
    quantity = tables.Column(orderable=False, attrs={"td": {"class": "text-center"}})
        
    class Meta:
        attrs = {"class": "table table-center"}
        order_by = ('productid')

class StockLocationProductTable(tables.Table):
    productid = tables.Column(visible=False)
    stocklocationid = tables.Column(verbose_name='Location name', orderable=False)
    quantity = tables.Column(orderable=False, attrs={"td": {"class": "text-center"}})
        
    class Meta:
        attrs = {"class": "table table-center table-bordered"}
        order_by = ('stocklocationid')
class ProductSupplierTable(tables.Table):
    productid = tables.Column(visible=False)
    supplierid = tables.Column(orderable=False)
    supplierreference = tables.Column(orderable=False)
    supplierprice = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-center"}})
        
    class Meta:
        attrs = {"class": "table table-center table-bordered"}
        order_by = ('supplierid')

class TodayTable(tables.Table):
    invoicedate = tables.DateColumn(format='d/m/Y', orderable=False)
    retail = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    business = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    total = ColumnWithThousandsSeparator(orderable=False, attrs={"td": {"class": "text-right"}})
    
    class Meta:
        #model = Invoice
        #exclude = {'invoicecode', 'invoiceid', 'totalamount', 'buypricetotal', 'ppnamount', 'discount', 'deposit', 'emailaddress', 'customername', 'paid'}
        attrs = {"class": "table table-center"}
        order_by = ('invoicedate')


"""
Table stock par produit
    Table dynamique avec pour colonnes les points de stockages 
"""
class StockTable(tables.Table):
    productstockid = tables.Column(visible=False)
    productid = tables.Column(orderable=False)
    
    class Meta:
        attrs = {"class": "table table-center"}

def define_table(StockLocation):
    attrs = dict((r.sl_name, tables.Column()) for r in StockLocation)
    attrs['Meta'] = type('Meta', (), dict(attrs={"class":"table table-center", "orderable":"False"}) )
    klass = type('DynamicTable', (StockTable,), attrs)
    return klass

