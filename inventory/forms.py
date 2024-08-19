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


# from django import forms
# from .models import Shipping, Order, Customer

# from django import forms
# from .models import Shipping, Order

# from django import forms
# from .models import Shipping, Order

# from django import forms
# from .models import Shipping, Order, Customer

# from django import forms
# from .models import Shipping, Order, Customer

# class ShippingForm(forms.ModelForm):
#     class Meta:
#         model = Shipping
#         fields = ['order', 'shipping_address', 'shipping_status']
#         widgets = {
#             'order': forms.Select(),
#             'shipping_address': forms.TextInput(attrs={'readonly': 'readonly'}),
#         }

#     def __init__(self, *args, **kwargs):
#         order = kwargs.pop('order', None)
#         super().__init__(*args, **kwargs)

#         # Populate the order dropdown with all orders
#         self.fields['order'].queryset = Order.objects.all()

#         # If an order is provided, prepopulate the shipping address field
#         if order:
#             self.fields['order'].initial = order
#             customer_name = order.customer.name
#             # Check if a customer with this name exists in the Customer model
#             try:
#                 customer = Customer.objects.get(name=customer_name)
#                 self.fields['shipping_address'].initial = customer.address
#             except Customer.DoesNotExist:
#                 self.fields['shipping_address'].initial = "Customer not found in database"
            
#             self.fields['shipping_address'].widget.attrs['readonly'] = True  # Make address field read-only






