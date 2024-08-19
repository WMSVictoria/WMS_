from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),  # Ensure this matches the intended URL
    path('add/', views.add_stock, name='add_stock'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('add_item/', views.add_item, name='add_item'),
    path('item/<int:pk>/update/', views.item_update, name='item_update'),  # Update item
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),  # Delete item
    path('inventory/<int:pk>/update/', views.inventory_update, name='inventory_update'),  # Update inventory
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),  # Delete inventory
    path('modify_stock/', views.modify_stock, name='modify_stock'),  # Add this line
    path('modify_item/', views.modify_item, name='modify_item'),  # Add this line
    path('receive/', views.receive_inventory, name='receive_inventory'),
    #path('putaway/', views.putaway_inventory, name='putaway_inventory'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('supplier_list/', views.supplier_list, name='supplier_list'),
    path('suppliers/edit/<int:pk>/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),
    path('internal_transfer/', views.internal_transfer, name='internal_transfer'),
    path('create_order/', views.create_order, name='create_order'),  # Create order
    path('order/<int:pk>/', views.order_detail, name='order_detail'),  # Order detail
    path('order/<int:pk>/update/', views.update_order, name='update_order'),  # Update order
    path('pick_order/', views.pick_order, name='pick_order'),  # Pick order
    path('order/<int:pk>/ship/', views.ship_order, name='ship_order'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('customer/<int:pk>/update/', views.update_customer, name='update_customer'),
    path('customer/<int:pk>/delete/', views.delete_customer, name='delete_customer'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('order_list/', views.order_list, name='order_list'),
    path('order/<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('items/delete/<int:pk>/', views.delete_item, name='delete_item'),
    #path('shipping/create/', views.shipping_create, name='shipping_create'),
    #path('shipping/update/<int:pk>/', views.shipping_update, name='shipping_update'),
    #path('shipping/', views.shipping_list, name='shipping_list'),
    #path('get_customer_address/<int:order_id>/', views.get_customer_address, name='get_customer_address'),
    path('internal_transfers/', views.internal_transfer_list, name='internal_transfer_list'),
    path('internal_transfers/<int:pk>/update/', views.internal_transfer_update, name='internal_transfer_update'),
    path('internal_transfers/<int:pk>/delete/', views.internal_transfer_delete, name='internal_transfer_delete'),
]
