"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit, Layout, Field

from app.models import Product, Category, Subcategory, StockLocation

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class DayForm(forms.Form):
    selectdate = forms.DateField(label='Date', required = False)
    
    def __init__(self, *args, **kwargs):
        super(DayForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-date'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))
        
class RangeDateForm(forms.Form):
    startdate = forms.DateField(label='Start date', required = False)
    enddate = forms.DateField(label='End date', required = False)

    def __init__(self, *args, **kwargs):
        super(RangeDateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-daterange'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))
        #self.helper.layout = Layout(
        #    Field('startdate', data_name="whatever")
        #)

class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-category'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Product
        fields = ('categoryid','subcategoryid')

class ProductSearchForm(forms.Form):
    categoryid = forms.ModelChoiceField(queryset=Category.objects.all())
    subcategoryid = forms.ModelChoiceField(queryset=Subcategory.objects.none())
    productname = forms.ModelChoiceField(queryset=Product.objects.none())

    def __init__(self, *args, **kwargs):
        super(ProductSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'product-filter'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submitcat', 'Submit'))

    class Meta:
        model = Product
        fields = ('categoryid','subcategoryid', 'productname')

class StockLocationForm(forms.Form):
    stocklocationid = forms.ModelChoiceField(queryset=StockLocation.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super(StockLocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'location-filter'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submitloc', 'Submit'))

    class Meta:
        model = Product
        fields = ('stocklocationid')

class CategoryAndLocationForm(forms.ModelForm):
    stocklocationid = forms.ModelChoiceField(queryset=StockLocation.objects.all(), empty_label="Global")

    def __init__(self, *args, **kwargs):
        super(CategoryAndLocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-catandloc'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Product
        fields = ('stocklocationid','categoryid','subcategoryid')