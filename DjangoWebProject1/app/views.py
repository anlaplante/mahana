import sys

from django_tables2   import RequestConfig
from django.core import serializers
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.db import connection, IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.views.generic import ListView, DetailView
from app.forms import RangeDateForm, CategoryForm, ProductSearchForm, StockLocationForm, CategoryAndLocationForm, DayForm
from datetime import datetime, date
from django.utils import timezone
import calendar

from app.serializers import CategorySerializer, SubcategorySerializer, ProductSerializer, StockSerializer, StockLocationSerializer, InvoiceSerializer
from app.serializers import ProductInvoiceSerializer, ProductOrderSerializer, ProformaSerializer, ProductProformaSerializer
from app.serializers import ProductInvoiceNdSerializer, InvoiceNdSerializer

from app.models import Product, ProductFilter, ProductInvoice, Stock, StockLocation, InvoiceNd, ProductInvoiceNd
from app.models import Invoice, InvoiceFilter, Subcategory, Category, SupplierProduct, Proforma, ProductProforma

from app.tables import TodayTable, InvoiceTable, ProductInvoiceTable, StockTable, define_table, StockLocationTable, ProductTable, StockLocationProductTable, ProductSupplierTable
from django_tables2 import SingleTableView

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.db.models import Sum
from app.utils import *

import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'RangeDateForm' :RangeDateForm,
        })
    )

class TodayList(SingleTableView):
    model = Invoice
    table_class = TodayTable

    def get_context_data(self, **kwargs):
        context = super(TodayList, self).get_context_data(**kwargs)
        if 'stocklocationid' in self.request.GET and self.request.GET['stocklocationid']:
            stocklocationid = self.request.GET['stocklocationid']
        else:
            stocklocationid = ""
        context["form"] = StockLocationForm(initial={'stocklocationid': stocklocationid})
        return context

    def get_table_data(self, **kwargs):
        if 'stocklocationid' in self.request.GET and self.request.GET['stocklocationid']:
            stocklocationid = self.request.GET['stocklocationid']
        else:
            stocklocationid = StockLocation.objects.all()[0].stocklocationid
        retail = '25'
        query_text = "SELECT invoicedate, SUM(CASE WHEN discount <= " + retail + " THEN totalamount ELSE 0 END) AS retail, SUM(CASE WHEN discount > " + retail + " THEN totalamount ELSE 0 END) AS business, SUM(totalamount) as total"
        query_text += " FROM invoice WHERE invoicedate >= '" + firstDayCurrentmonth().strftime("%Y-%m-%d") + "' AND invoicedate <= '" + lastDayCurrentmonth().strftime("%Y-%m-%d")
        query_text +=  "' AND stocklocationid = " + str(stocklocationid) + " GROUP BY invoicedate ORDER BY invoicedate DESC"
        cursor = connection.cursor()
        cursor.execute(query_text)
        data = dictfetchall(cursor)
        return data

class ProductList(SingleTableView):
    model = Product
    table_class = ProductTable

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        
        if 'categoryid' in self.request.GET and self.request.GET['categoryid']:
            categoryid = self.request.GET['categoryid']
        else:
            categoryid = ""
        if 'subcategoryid' in self.request.GET and self.request.GET['subcategoryid']:
            subcategoryid = self.request.GET['subcategoryid']
        else:
            subcategoryid = ""

        context["form"] = CategoryForm(initial={'categoryid': categoryid, 'subcategoryid': subcategoryid})
        #context["formlocation"] = StockLocationForm()
        return context

    def get_table_data(self, **kwargs):
        if 'categoryid' in self.request.GET and self.request.GET['categoryid']:
            data = Product.objects.filter(categoryid=self.request.GET['categoryid'])
        else:
            data = []
        if 'subcategoryid' in self.request.GET and self.request.GET['subcategoryid']:
            data = data.filter(subcategoryid=self.request.GET['subcategoryid'])

        return data

class ProductDetail(SingleTableView):
    model = Stock
    table_class = StockLocationProductTable
    template_name = 'app/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['product'] = Product.objects.get(productid=self.kwargs['productid'])
        #context['table_prov'] = ProductSupplierTable(SupplierProduct.objects.filter(productid=self.kwargs['productid']), prefix="1-")
        return context

    def get_table_data(self, **kwargs):
        data = SupplierProduct.objects.filter(productid=self.kwargs['productid'])
        return data


class InvoiceList(SingleTableView):
    model = Invoice
    table_class = InvoiceTable

    def get_context_data(self, **kwargs):
        context = super(InvoiceList, self).get_context_data(**kwargs)

        if 'selectdate' in self.request.GET and self.request.GET['selectdate']:
            selectdate = self.request.GET['selectdate']
        else:
            selectdate = date.today()
        context["form"] = DayForm(initial={'selectdate': selectdate})
        grandtotal = Invoice.objects.filter(invoicedate=selectdate).aggregate(Sum('totalamount'))
        context["sum_invoice"] = grandtotal
        return context

    def get_table_data(self):
        if 'selectdate' in self.request.GET and self.request.GET['selectdate']:
            selectdate = self.request.GET['selectdate']
        else:
            selectdate = date.today()

        data = Invoice.objects.filter(invoicedate=selectdate)
        return data

class InvoiceDetail(SingleTableView):
    model = ProductInvoice
    table_class = ProductInvoiceTable
    #context_object_name = 'invoice_detail'
    template_name = 'app/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetail, self).get_context_data(**kwargs)
        context['invoice'] = Invoice.objects.get(invoiceid=self.kwargs['invoiceid'])
        return context

    def get_table_data(self, **kwargs):
        data = ProductInvoice.objects.filter(invoiceid=self.kwargs['invoiceid'])
        return data

@method_decorator(login_required, name='dispatch')
class StockList(SingleTableView):
    model = Stock
    table_class = StockLocationTable

    def get_context_data(self, **kwargs):
        context = super(StockList, self).get_context_data(**kwargs)
        
        if 'categoryid' in self.request.GET and self.request.GET['categoryid']:
            categoryid = self.request.GET['categoryid']
        else:
            categoryid = ""
        if 'subcategoryid' in self.request.GET and self.request.GET['subcategoryid']:
            subcategoryid = self.request.GET['subcategoryid']
        else:
            subcategoryid = ""
        if 'stocklocationid' in self.request.GET and self.request.GET['stocklocationid']:
            stocklocationid = self.request.GET['stocklocationid']
        else:
            stocklocationid = ""
        context["form"] = CategoryAndLocationForm(initial={'stocklocationid': stocklocationid, 'categoryid': categoryid, 'subcategoryid': subcategoryid})
        #context["formlocation"] = StockLocationForm()
        return context

    def get_table_data(self):
        query_text = 'SELECT S.productid, reference, productname'
        if 'stocklocationid' in self.request.GET and self.request.GET['stocklocationid']:
            stocklocationid = self.request.GET['stocklocationid']
            query_text += ', SUM(CASE WHEN stocklocationid = ' + str(stocklocationid) + ' THEN quantity ELSE 0 END) AS quantity'
        else:
            query_text += ', SUM(quantity) AS quantity'

        query_text += ' FROM stock S INNER JOIN product P ON S.productid = P.productid '

        if 'subcategoryid' in self.request.GET and self.request.GET['subcategoryid']:
            subcategoryid = self.request.GET['subcategoryid']
            query_text += ' AND subcategoryid = ' + str(subcategoryid)
        else:
            if 'categoryid' in self.request.GET and self.request.GET['categoryid']:
                categoryid = self.request.GET['categoryid']
                query_text += ' AND categoryid = ' + str(categoryid)

        query_text += ' GROUP BY productid'
        cursor = connection.cursor()
        cursor.execute(query_text)
        data = dictfetchall(cursor)
        #table = define_table(StockLocation.objects.all())(data)
        return data

    def dispatch(self, *args, **kwargs):
        return super(StockList, self).dispatch(*args, **kwargs)

class StockPerProduct(SingleTableView):
    model = Stock
    template_name = "stock_per_product.html"

    def get_context_data(self, **kwargs):
        context = super(StockPerProduct, self).get_context_data(**kwargs)
        
        if 'categoryid' in self.request.GET and self.request.GET['categoryid']:
            categoryid = self.request.GET['categoryid']
        else:
            categoryid = ""
        if 'subcategoryid' in self.request.GET and self.request.GET['subcategoryid']:
            subcategoryid = self.request.GET['subcategoryid']
        else:
            subcategoryid = ""
        #context["form"] = CategoryForm(initial={'categoryid': categoryid, 'subcategoryid': subcategoryid})
        context["form"] = ProductSearchForm(initial={'categoryid': categoryid, 'subcategoryid': subcategoryid})
        return context

    def get_table(self):
        query_text = 'SELECT productid'
        for s in StockLocation.objects.all():
             query_text += ', SUM(CASE WHEN stocklocationid = ' + str(s.stocklocationid) + ' THEN quantity ELSE 0 END) AS ' + s.sl_name
        query_text += ' FROM stock GROUP BY productid'
        cursor = connection.cursor()
        cursor.execute(query_text)
        data = dictfetchall(cursor)
        table = define_table(StockLocation.objects.all())(data)
        return table

"""
API
"""
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def group_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        groups = Category.objects.all()
        serializer = CategorySerializer(groups, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def subgroup_list(request):
    if request.method == 'GET':
        subgroups = Subcategory.objects.all()
        serializer = SubcategorySerializer(subgroups, many=True)
        return JSONResponse(serializer.data)
    else:
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JSONResponse(serializer.data)
    else:
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def stock_list(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return JSONResponse(serializer.data)
    else:
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def stockperlocation_list(request, stocklocation_id):

    if request.method == 'GET':
        stocks = Stock.objects.filter(stocklocationid=stocklocation_id)
        serializer = StockSerializer(stocks, many=True)
        return JSONResponse(serializer.data)
    else:
        return JSONResponse(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def stocklocation_list(request):
    if request.method == 'GET':
        stocklocations = StockLocation.objects.all()
        serializer = StockLocationSerializer(stocklocations, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def invoice_list(request):

    if request.method == 'GET':
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED, )
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def invoiceN_list(request):

    if request.method == 'GET':
        invoices = InvoiceNd.objects.all()
        serializer = InvoiceNdSerializer(invoices, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = InvoiceNdSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED, )
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['GET', 'POST'])
def proforma_list(request):

    if request.method == 'GET':
        proformas = Proforma.objects.all()
        serializer = ProformaSerializer(proformas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = ProformaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED, )
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def proforma_detail(request, pk):
    
    try:
        proforma = Proforma.objects.get(pk=pk)
    except Proforma.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        proforma.delete()
        return JSONResponse(status=status.HTTP_204_NO_CONTENT)




def get_subcategory(request, category_id):
    category = Category.objects.get(pk=category_id)
    """
    subcategories = Subcategory.objects.filter(categoryid=category)
    subcategory_dict = {}
    for subcategory in subcategories:
        subcategory_dict[subcategory.subcategoryid] = subcategory.subcategoryname
    return HttpResponse(json.dumps(subcategory_dict), content_type="application/json")
    """
    data = serializers.serialize('json', Subcategory.objects.filter(categoryid=category), fields=('subcategoryname'))
    return HttpResponse(data, content_type="application/json")

def get_products(request, subcategory_id):
    subcategory = Subcategory.objects.get(pk=subcategory_id)

    data = serializers.serialize('json', Product.objects.filter(subcategoryid=subcategory), fields=('productname'))
    return HttpResponse(data, content_type="application/json")

def get_products2(request):
    data = serializers.serialize('json', Product.objects.all(), fields=('productname'))
    return HttpResponse(data, content_type="application/json")

def get_groups(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Category")
    data = dictfetchall(cursor)
    return HttpResponse(data, content_type="application/json")

"""
def get_subgroups(request):
    data = serializers.serialize('json', Subcategory.objects.all())
    return HttpResponse(data, content_type="application/json")
"""
"""
OLD
"""

class InvoiceList2(ListView):
    model = Invoice
    context_object_name = 'invoice_list'

    def get_context_data(self, **kwargs):
        context = super(InvoiceList, self).get_context_data(**kwargs)
        context["form"] = RangeDateForm()
        invoice = InvoiceTable(Invoice.objects.all())
        RequestConfig(self.request).configure(invoice)
        context["invoice"] = invoice
        return context

    def get_queryset(self):
        invoice_list = Invoice.objects.all()

        if 'startdate' in self.request.GET and self.request.GET['startdate']:
            startdate = self.request.GET['startdate']
            invoice_list = invoice_list.filter(invoicedate__gt=startdate)
        if 'enddate' in self.request.GET and self.request.GET['enddate']:
            enddate = self.request.GET['enddate']
            invoice_list = invoice_list.filter(invoicedate__gt=enddate)
        return invoice_list

class ProductList2(ListView):
    model = Product
    context_object_name = 'product_list'

class ProductDetail2(DetailView):
    model = Product
    context_object_name = 'product_detail'