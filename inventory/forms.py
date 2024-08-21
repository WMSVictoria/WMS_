from django import forms
from .models import Item, Inventory, Supplier

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'sku', 'description']

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item', 'quantity', 'location', 'section']

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'sku', 'description']

class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['quantity', 'location', 'section']

from django import forms
from .models import Receiving

from django import forms
from django.contrib.auth.models import User, Group
from .models import Receiving

from django import forms
from .models import Receiving

class ReceivingForm(forms.ModelForm):
    class Meta:
        model = Receiving
        fields = ['item', 'quantity_received', 'supplier', 'putaway_section', 'putaway_location']


from django import forms
#from .models import Putaway, Receiving

# class PutawayForm(forms.ModelForm):
#     class Meta:
#         model = Putaway
#         fields = ['received_item', 'location', 'section']
#         widgets = {
#             'received_item': forms.Select(),
#             'location': forms.Select(choices=Putaway._meta.get_field('location').choices),
#             'section': forms.Select(choices=Putaway._meta.get_field('section').choices),
#         }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'telephone', 'address', 'website']

from django import forms
from .models import InternalTransfer, Section

class InternalTransferForm(forms.ModelForm):
    class Meta:
        model = InternalTransfer
        fields = ['item', 'quantity', 'location', 'source_section', 'destination_section']
        widgets = {
            'item': forms.Select(),
            'location': forms.Select(choices=InternalTransfer._meta.get_field('location').choices),
            'source_section': forms.Select(),
            'destination_section': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        location = kwargs.pop('location', None)
        super().__init__(*args, **kwargs)
        if location:
            # Filter sections based on the current location
            self.fields['source_section'].queryset = Section.objects.filter(location=location)
            self.fields['destination_section'].queryset = Section.objects.filter(location=location)


from django import forms
from .models import Order, OrderItem, ShippingDetail, Customer

from django import forms
from .models import Order, Item, Customer

from django import forms
from .models import Order, Item, Customer

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'item', 'quantity', 'location', 'section', 'status']
        widgets = {
            'customer': forms.Select(),
            'item': forms.Select(),
            'location': forms.Select(choices=Order.LOCATION_CHOICES),
            'section': forms.Select(choices=Order.SECTION_CHOICES),
            'status': forms.Select(),
        }




class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

class ShippingDetailForm(forms.ModelForm):
    class Meta:
        model = ShippingDetail
        fields = ['shipping_label']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'telephone', 'address', 'website']


# forms.py

from django import forms

# forms.py

from django import forms
from .models import Order, InternalTransfer, Inventory

class AdHocReportForm(forms.Form):
    DATE_CHOICES = [
        ('all', 'All Time'),
        ('custom', 'Custom Range'),
    ]

    report_type = forms.ChoiceField(
        choices=[('orders', 'Orders'), ('transfers', 'Transfers'), ('inventory', 'Inventory')],
        required=True
    )
    date_range = forms.ChoiceField(choices=DATE_CHOICES, required=True)
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget)
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget)
    location = forms.ChoiceField(choices=[(loc, loc) for loc in ['Melbourne', 'Kilmore', 'Stawell', 'Shepparton', 'Hamilton']], required=False)
    item = forms.ModelChoiceField(queryset=Inventory.objects.values_list('item', flat=True).distinct(), required=False)
    section = forms.ChoiceField(choices=[(sec, sec) for sec in ['Section I', 'Section II', 'Section III', 'Section IV', 'Section V']], required=False)
    customer = forms.ModelChoiceField(queryset=Order.objects.values_list('customer', flat=True).distinct(), required=False)





