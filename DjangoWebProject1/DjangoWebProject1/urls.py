"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from app import views
from django.contrib.auth import views as auth_views

from app.views import ProductList, ProductDetail, StockList, StockPerProduct
from app.views import InvoiceList, InvoiceDetail, TodayList

from rest_framework.urlpatterns import format_suffix_patterns
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^stock/$', StockList.as_view(), name='stock'),
    url(r'^stockproduct/$', StockPerProduct.as_view(), name='stockproduct'),
    url(r'^today/$', TodayList.as_view(), name='today'),
    #url(r'^about', views.product_list, name='about'),
    url(r'^product/$', ProductList.as_view(), name='product'),
    url(r'^product/(?P<productid>[0-9]+)/$', ProductDetail.as_view(), name='product_detail'),
    url(r'^invoice/$', InvoiceList.as_view(), name='invoice'),
    url(r'^invoice/(?P<invoiceid>[0-9]+)/$', InvoiceDetail.as_view(), name='invoice_detail'),
    url(r'^login/$',
        auth_views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        auth_views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^get_subcategory/(?P<category_id>[0-9]+)/$', views.get_subcategory),
    #url(r'^get_products/(?P<subcategory_id>[0-9]+)/$', views.get_products),
    url(r'^get_groups/$', views.group_list),
    url(r'^get_subgroups/$', views.subgroup_list),
    url(r'^get_products/$', views.product_list),
    url(r'^get_products2/$', views.get_products2),
    url(r'^get_stocks/$', views.stock_list),
    url(r'^get_stocks/(?P<stocklocation_id>[0-9]+)/$', views.stockperlocation_list),
    url(r'^get_stock_locations/$', views.stocklocation_list),
    url(r'^api/invoice/$', views.invoice_list),
    url(r'^api/invoiceN/$', views.invoiceN_list),
    url(r'^api/proforma/$', views.proforma_list),
    url(r'^api/proforma/(?P<pk>[0-9]+)/$', views.proforma_detail),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
