from rest_framework import serializers
from app.models import Product, ProductFilter, ProductInvoice, Stock, StockLocation, ProductOrder, InvoiceNd, ProductInvoiceNd
from app.models import Invoice, InvoiceFilter, Subcategory, Category, SupplierProduct, ProductProforma, Proforma

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock

class StockLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLocation

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ('productorderid','note','isstock','stocklocationid','ispickedup')

class ProductInvoiceSerializer(serializers.ModelSerializer):
    #orderinfo = ProductOrderSerializer(many=True)

    class Meta:
        model = ProductInvoice
        #fields = ('productinvoiceid', 'productid', 'quantity', 'buyingprice', 'saleprice', 'orderinfo')
        fields = ('productinvoiceid', 'productid', 'quantity', 'buyingprice', 'saleprice', 'isstock', 'stocklocationid', 'note', 'ispickedup')

class InvoiceSerializer(serializers.ModelSerializer):
    products = ProductInvoiceSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ('invoiceid','stocklocationid', 'invoicecode','invoicedate','totalamount','buypricetotal','discount','ppnamount','ispaid','deposit','emailaddress','customername','invoicenote','isorder','deliverydate','products')
        #fields = ('invoiceid','stocklocationid', 'invoicecode','invoicedate','totalamount','buypricetotal','discount','ppnamount','products')
 
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        invoice = Invoice.objects.create(**validated_data)
        for product_data in products_data:
            #product_data.invoiceid = invoice.invoiceid
            ProductInvoice.objects.create(invoiceid=invoice, **product_data)
            #productinvoice = ProductInvoice.objects.create(**product_data)
            #order_info = validated_data.pop('orderinfo')
        return invoice

class ProductInvoiceNdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductInvoiceNd
        fields = ('productinvoiceid', 'productid', 'quantity', 'buyingprice', 'saleprice')

class InvoiceNdSerializer(serializers.ModelSerializer):
    products = ProductInvoiceNdSerializer(many=True)

    class Meta:
        model = InvoiceNd
        fields = ('invoiceid','stocklocationid', 'invoicecode','invoicedate','totalamount','buypricetotal','discount','ppnamount','ispaid','deposit', 'products')
         
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        invoice = InvoiceNd.objects.create(**validated_data)
        for product_data in products_data:
            ProductInvoiceNd.objects.create(invoiceid=invoice, **product_data)
        return invoice

class ProductProformaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductProforma
        fields = ('productproformaid', 'productid', 'quantity', 'buyingprice', 'saleprice')

class ProformaSerializer(serializers.ModelSerializer):
    products = ProductProformaSerializer(many=True)

    class Meta:
        model = Proforma
        fields = ('proformaid','proformadate','totalamount','buypricetotal','discount','ppnamount','emailaddress','customername','proformanote','products')
         
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        proforma = Proforma.objects.create(**validated_data)
        for product_data in products_data:
            ProductProforma.objects.create(proformaid=proforma, **product_data)
        return proforma