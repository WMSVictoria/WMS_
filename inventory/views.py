from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Inventory
from .forms import ItemForm, InventoryForm, ItemUpdateForm, InventoryUpdateForm

def inventory_list(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventory_items': inventory_items})

def add_stock(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/add_stock.html', {'form': form})

def item_detail(request, pk):
    item = Item.objects.get(pk=pk)
    return render(request, 'inventory/item_detail.html', {'item': item})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = ItemUpdateForm(instance=item)
    return render(request, 'inventory/item_update.html', {'form': form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/item_delete.html', {'item': item})

def inventory_update(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryUpdateForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryUpdateForm(instance=inventory)
    return render(request, 'inventory/inventory_update.html', {'form': form})

def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        inventory.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_delete.html', {'inventory': inventory})

def modify_stock(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'inventory/modify_stock.html', {'inventory_items': inventory_items})

def modify_item(request):
    items = Item.objects.all()
    return render(request, 'inventory/modify_item.html', {'items': items})

from django.shortcuts import render, redirect
from .models import Receiving, Inventory
from .forms import ReceivingForm

def receive_inventory(request):
    if request.method == 'POST':
        form = ReceivingForm(request.POST)
        if form.is_valid():
            receiving = form.save(commit=False)
            receiving.received_by = request.user
            receiving.save()

            # Create or update inventory entry
            inventory, created = Inventory.objects.get_or_create(
                item=receiving.item,
                location=receiving.putaway_location,
                section=receiving.putaway_section,
                defaults={'quantity': receiving.quantity_received}
            )

            if not created:
                # If the inventory entry already exists, update the quantity
                inventory.quantity += receiving.quantity_received
                inventory.save()

            return redirect('inventory_list')
    else:
        form = ReceivingForm()

    return render(request, 'inventory/receive_inventory.html', {'form': form})

from django.shortcuts import render, redirect
from .models import  Receiving


#def putaway_inventory(request):
    #if request.method == 'POST':
        #form = PutawayForm(request.POST)
        #if form.is_valid():
           # form.save()
            #return redirect('putaway_inventory')
    #else:
        #form = PutawayForm()
    #received_items = Receiving.objects.all()  # List of all received items
    #return render(request, 'inventory/putaway_inventory.html', {'form': form, 'received_items': received_items})

from django.shortcuts import render, redirect
from .models import Supplier
from .forms import SupplierForm

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_supplier')
    else:
        form = SupplierForm()
    return render(request, 'inventory/add_supplier.html', {'form': form})

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/edit_supplier.html', {'form': form, 'supplier': supplier})

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'inventory/delete_supplier.html', {'supplier': supplier})

from django.shortcuts import render, redirect
from .models import InternalTransfer
from .forms import InternalTransferForm

def internal_transfer(request):
    if request.method == 'POST':
        form = InternalTransferForm(request.POST, location=request.POST.get('location'))
        if form.is_valid():
            transfer = form.save(commit=False)
            # Update inventory quantities
            try:
                source_inventory = Inventory.objects.get(
                    item=transfer.item,
                    location=transfer.location,
                    section=transfer.source_section
                )
                destination_inventory, created = Inventory.objects.get_or_create(
                    item=transfer.item,
                    location=transfer.location,
                    section=transfer.destination_section,
                    defaults={'quantity': 0}
                )
                
                if source_inventory.quantity >= transfer.quantity:
                    source_inventory.quantity -= transfer.quantity
                    source_inventory.save()
                    
                    destination_inventory.quantity += transfer.quantity
                    destination_inventory.save()
                    
                    transfer.save()
                    return redirect('internal_transfer')
                else:
                    form.add_error(None, "Not enough inventory in the source section.")
            except Inventory.DoesNotExist:
                form.add_error(None, "Inventory record does not exist.")
    else:
        form = InternalTransferForm()

    return render(request, 'inventory/internal_transfer.html', {'form': form})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import InternalTransfer
from .forms import InternalTransferForm

def internal_transfer_list(request):
    transfers = InternalTransfer.objects.all()
    return render(request, 'inventory/internal_transfer_list.html', {'transfers': transfers})

def internal_transfer_update(request, pk):
    transfer = get_object_or_404(InternalTransfer, pk=pk)
    if request.method == 'POST':
        form = InternalTransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return redirect('internal_transfer_list')
    else:
        form = InternalTransferForm(instance=transfer)
    return render(request, 'inventory/internal_transfer_form.html', {'form': form})

def internal_transfer_delete(request, pk):
    transfer = get_object_or_404(InternalTransfer, pk=pk)
    if request.method == 'POST':
        transfer.delete()
        return redirect('internal_transfer_list')
    return render(request, 'inventory/internal_transfer_confirm_delete.html', {'transfer': transfer})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, ShippingDetail
from .forms import OrderForm, OrderItemForm, ShippingDetailForm

from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Ensure 'order_list' is the correct URL name for listing orders
    else:
        form = OrderForm()
    return render(request, 'inventory/create_order.html', {'form': form})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'inventory/order_detail.html', {'order': order})

def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'inventory/update_order.html', {'form': form})

def pick_order(request):
    orders = Order.objects.filter(status='Processing')
    return render(request, 'inventory/pick_order.html', {'orders': orders})

def ship_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = ShippingDetailForm(request.POST)
        if form.is_valid():
            shipping_detail = form.save(commit=False)
            shipping_detail.order = order
            shipping_detail.save()
            order.status = 'Shipped'
            order.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = ShippingDetailForm()
    return render(request, 'inventory/ship_order.html', {'form': form, 'order': order})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, ShippingDetail, Customer
from .forms import OrderForm, OrderItemForm, ShippingDetailForm, CustomerForm

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'inventory/create_customer.html', {'form': form})

def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'inventory/update_customer.html', {'form': form})

def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'inventory/delete_customer.html', {'customer': customer})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})

from django.shortcuts import render
from .models import Order

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'inventory/order_list.html', {'orders': orders})

from django.shortcuts import get_object_or_404

# Existing imports...

def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'inventory/delete_order.html', {'order': order})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm

def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form})

def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})


# inventory/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import  Order, Customer




# def shipping_create(request, order_id=None):
#     order = get_object_or_404(Order, pk=order_id) if order_id else None

#     if request.method == 'POST':
#         form = ShippingForm(request.POST, order=order)
#         if form.is_valid():
#             shipping = form.save(commit=False)
#             shipping.order = order
#             shipping.save()
#             return redirect('shipping_list')
#     else:
#         form = ShippingForm(order=order)

#     return render(request, 'inventory/shipping_form.html', {'form': form})





# def shipping_update(request, pk):
#     shipping = get_object_or_404(Shipping, pk=pk)
#     if request.method == 'POST':
#         form = ShippingForm(request.POST, instance=shipping)
#         if form.is_valid():
#             form.save()
#             return redirect('shipping_list')
#     else:
#         form = ShippingForm(instance=shipping, order=shipping.order, customer=shipping.customer)
    
#     return render(request, 'inventory/shipping_form.html', {'form': form})

from django.shortcuts import render
#from .models import Shipping

# def shipping_list(request):
#     shippings = Shipping.objects.all()
#     return render(request, 'inventory/shipping_list.html', {'shippings': shippings})


# from django.http import JsonResponse
# from .models import Order

# def get_customer_address(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#     customer = order.customer
#     response_data = {
#         'customer_name': customer.name,
#         'shipping_address': customer.address,
#     }
#     return JsonResponse(response_data)


