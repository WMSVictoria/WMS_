from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Inventory
from .forms import ItemForm, InventoryForm, ItemUpdateForm, InventoryUpdateForm

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Inventory
from django.core.paginator import Paginator

@login_required
def inventory_list(request):
    # Fetch inventory items
    inventory_items = Inventory.objects.all()

    # Pagination setup
    paginator = Paginator(inventory_items, 25)  # Show 25 inventory items per page
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)

    # Determine if the user is in the warehouse_managers or warehouse_staff group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    # Pass the paginated items and user group information to the template
    context = {
        'page_obj': page_obj,
        'is_manager': is_manager,
        'is_staff': is_staff,
    }

    return render(request, 'inventory/inventory_list.html', context)


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
    return render(request, 'inventory/item_form.html', {'form': form})

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Inventory
from .forms import ReceivingForm

@login_required
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

    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    return render(request, 'inventory/receive_inventory.html', {
        'form': form,
        'is_manager': is_manager,
        'is_staff': is_staff,
    })

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

@login_required
def supplier_list(request):
    # Fetch all suppliers
    suppliers = Supplier.objects.all()
    
    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    # Pass suppliers and group info to the template
    context = {
        'suppliers': suppliers,
        'is_manager': is_manager,
        'is_staff': is_staff,
    }
    
    return render(request, 'inventory/supplier_list.html', context)

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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def internal_transfer_list(request):
    # Fetch all internal transfers
    transfers = InternalTransfer.objects.all()
    
    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_warehouse_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_warehouse_staff = request.user.groups.filter(name='warehouse_staff').exists()

    # Pass transfers and group info to the template
    context = {
        'transfers': transfers,
        'is_warehouse_manager': is_warehouse_manager,
        'is_warehouse_staff': is_warehouse_staff,
    }
    
    return render(request, 'inventory/internal_transfer_list.html', context)


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
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .models import Inventory

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Assuming 'item' is a field in your OrderForm that links to the Inventory model
            item = order.item  # Replace 'item' with the actual field name in your form

            # Check inventory quantity
            inventory_item = Inventory.objects.get(id=item.id)
            if inventory_item.quantity < 10:
                messages.error(request, 'The quantity is not enough to create this order.')
                return render(request, 'inventory/create_order.html', {'form': form})
            
            # Proceed to save the order if inventory is sufficient
            order.save()
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

@login_required
def customer_list(request):
    # Fetch all customers
    customers = Customer.objects.all()
    
    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    # Pass customers and group info to the template
    context = {
        'customers': customers,
        'is_manager': is_manager,
        'is_staff': is_staff,
    }
    
    return render(request, 'inventory/customer_list.html', context)

from django.shortcuts import render
from .models import Order

@login_required
def order_list(request):
    # Fetch all orders
    orders = Order.objects.all()
    
    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_warehouse_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_warehouse_staff = request.user.groups.filter(name='warehouse_staff').exists()

    # Pass orders and group info to the template
    context = {
        'orders': orders,
        'is_warehouse_manager': is_warehouse_manager,
        'is_warehouse_staff': is_warehouse_staff,
    }
    
    return render(request, 'inventory/order_list.html', context)

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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def item_list(request):
    # Fetch all items
    items = Item.objects.all()
    
    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    # Pass items and group info to the template
    context = {
        'items': items,
        'is_manager': is_manager,
        'is_staff': is_staff,
    }
    
    return render(request, 'inventory/item_list.html', context)


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

from django.shortcuts import render


@login_required
def inventory_report(request):
    # Fetch all inventory records
    inventory_items = Inventory.objects.all()

    # Determine low stock items (for example, if the quantity is less than 10)
    low_stock_threshold = 10
    low_stock_items = inventory_items.filter(quantity__lt=low_stock_threshold)

    # Apply search filters
    item_name = request.GET.get('item', '')
    location = request.GET.get('location', '')
    section = request.GET.get('section', '')

    if item_name:
        inventory_items = inventory_items.filter(item__name__icontains=item_name)
    if location:
        inventory_items = inventory_items.filter(location__icontains=location)
    if section:
        inventory_items = inventory_items.filter(section__icontains=section)

    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    return render(request, 'inventory/inventory_report.html', {
        'inventory_items': inventory_items,
        'low_stock_items': low_stock_items,
        'low_stock_threshold': low_stock_threshold,
        'is_manager': is_manager,
        'is_staff': is_staff,
    })

from django.shortcuts import render
from django.db.models import Sum
from .models import Inventory, Order
from datetime import datetime, timedelta

@login_required
def inventory_turnover(request):
    # Define the period for analysis (e.g., the last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Calculate the total quantity sold for each item during the period
    items_sold = Order.objects.filter(date__range=[start_date, end_date]).values('item').annotate(total_sold=Sum('quantity'))

    # Calculate the average inventory for each item (assuming constant inventory levels for simplicity)
    inventory_levels = Inventory.objects.all()

    # Apply search filters
    item_name = request.GET.get('item', '')
    location = request.GET.get('location', '')
    section = request.GET.get('section', '')

    if item_name:
        inventory_levels = inventory_levels.filter(item__name__icontains=item_name)
    if location:
        inventory_levels = inventory_levels.filter(location__icontains=location)
    if section:
        inventory_levels = inventory_levels.filter(section__icontains=section)

    turnover_data = []
    for inventory_item in inventory_levels:
        item_sales = next((item['total_sold'] for item in items_sold if item['item'] == inventory_item.item.id), 0)
        average_inventory = inventory_item.quantity
        turnover_rate = item_sales / average_inventory if average_inventory > 0 else 0
        
        turnover_data.append({
            'item': inventory_item.item.name,
            'location': inventory_item.location,
            'section': inventory_item.section,
            'total_sold': item_sales,
            'average_inventory': average_inventory,
            'turnover_rate': turnover_rate,
        })

    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    return render(request, 'inventory/inventory_turnover.html', {
        'turnover_data': turnover_data,
        'start_date': start_date,
        'end_date': end_date,
        'is_manager': is_manager,
        'is_staff': is_staff,
    })

# views.py

from django.shortcuts import render
from .models import Order
from django import forms
from datetime import datetime

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

@login_required
def order_fulfillment_report(request):
    # Default date range (last 30 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})

    # Query orders within the selected date range
    orders = Order.objects.filter(date__range=[start_date, end_date])

    # Calculate the number of shipped and pending orders
    total_orders = orders.count()
    shipped_orders = orders.filter(status='Shipped').count()
    pending_orders = orders.filter(status='Pending').count()

    # Calculate fulfillment rate
    fulfillment_rate = (shipped_orders / total_orders * 100) if total_orders > 0 else 0

    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    return render(request, 'inventory/order_fulfillment_report.html', {
        'form': form,
        'total_orders': total_orders,
        'shipped_orders': shipped_orders,
        'pending_orders': pending_orders,
        'fulfillment_rate': fulfillment_rate,
        'start_date': start_date,
        'end_date': end_date,
        'is_manager': is_manager,
        'is_staff': is_staff,
    })

# views.py

from django.shortcuts import render
from .models import Receiving  # Assuming there's a Receiving model tracking received goods
from django import forms
from datetime import datetime, timedelta

# views.py

from django.shortcuts import render
from .models import Receiving  # Assuming there's a Receiving model tracking received goods
from django import forms
from datetime import datetime, timedelta

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

@login_required
def goods_received_report(request):
    # Default date range (last 30 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})

    # Query the received goods within the selected date range
    received_goods = Receiving.objects.filter(received_date__range=[start_date, end_date])

    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    return render(request, 'inventory/goods_received_report.html', {
        'form': form,
        'received_goods': received_goods,
        'start_date': start_date,
        'end_date': end_date,
        'is_manager': is_manager,
        'is_staff': is_staff,
    })

# views.py

from django.shortcuts import render
from .models import InternalTransfer
from django import forms
from datetime import datetime, timedelta

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

@login_required
def transfer_history_report(request):
    # Default date range (last 30 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})

    # Query the internal transfers within the selected date range
    transfers = InternalTransfer.objects.filter(date__range=[start_date, end_date])

    # Check if the user is in 'warehouse_managers' or 'warehouse_staff' group
    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    return render(request, 'inventory/transfer_history_report.html', {
        'form': form,
        'transfers': transfers,
        'start_date': start_date,
        'end_date': end_date,
        'is_manager': is_manager,
        'is_staff': is_staff,
    })

# views.py

from django.shortcuts import render
from .models import Order, InternalTransfer, Inventory
from .forms import AdHocReportForm
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AdHocReportForm
from .models import Order, InternalTransfer, Inventory

@login_required
def ad_hoc_report(request):
    form = AdHocReportForm(request.POST or None)
    report_data = None

    if request.method == 'POST' and form.is_valid():
        report_type = form.cleaned_data['report_type']
        date_range = form.cleaned_data['date_range']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        location = form.cleaned_data['location']
        item = form.cleaned_data['item']
        section = form.cleaned_data['section']
        customer = form.cleaned_data['customer']

        if date_range == 'custom' and (start_date and end_date):
            date_filter = {'date__range': [start_date, end_date]}
        else:
            date_filter = {}

        if report_type == 'orders':
            report_data = Order.objects.filter(**date_filter)
            if location:
                report_data = report_data.filter(item__inventory__location=location)
            if item:
                report_data = report_data.filter(item=item)
            if section:
                report_data = report_data.filter(item__inventory__section=section)
            if customer:
                report_data = report_data.filter(customer=customer)
        elif report_type == 'transfers':
            report_data = InternalTransfer.objects.filter(**date_filter)
            if location:
                report_data = report_data.filter(location=location)
            if item:
                report_data = report_data.filter(item=item)
            if section:
                report_data = report_data.filter(source_section=section) | report_data.filter(destination_section=section)
        elif report_type == 'inventory':
            report_data = Inventory.objects.filter(**date_filter)
            if location:
                report_data = report_data.filter(location=location)
            if item:
                report_data = report_data.filter(item=item)
            if section:
                report_data = report_data.filter(section=section)

    is_manager = request.user.groups.filter(name='warehouse_managers').exists()
    is_staff = request.user.groups.filter(name='warehouse_staff').exists()

    return render(request, 'inventory/ad_hoc_report.html', {
        'form': form,
        'report_data': report_data,
        'is_manager': is_manager,
        'is_staff': is_staff,
    })


# views.py

from django.http import JsonResponse
from django.db.models import Sum
from .models import Inventory, Order, InternalTransfer
from django.utils.timezone import now

def inventory_levels(request):
    # Aggregate data for current inventory levels
    data = Inventory.objects.values('location', 'section').annotate(total_quantity=Sum('quantity')).order_by('location', 'section')
    inventory_data = {
        'labels': [f"{item['location']} - {item['section']}" for item in data],
        'data': [item['total_quantity'] for item in data]
    }
    return JsonResponse(inventory_data)

def order_backlog(request):
    # Count the number of orders that are pending
    backlog_count = Order.objects.filter(status='Pending').count()
    return JsonResponse({'count': backlog_count})

def transfer_volume(request):
    # Aggregate data for transfer volumes
    start_date = request.GET.get('start_date', now().date())
    end_date = request.GET.get('end_date', now().date())
    transfers = InternalTransfer.objects.filter(date__range=[start_date, end_date]).values('date').annotate(total_quantity=Sum('quantity')).order_by('date')
    transfer_data = {
        'labels': [item['date'].strftime('%b %Y') for item in transfers],
        'data': [item['total_quantity'] for item in transfers]
    }
    return JsonResponse(transfer_data)


