from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="No description provided")

    def __str__(self):
        return self.name

class Inventory(models.Model):
    LOCATION_CHOICES = [
        ('Melbourne', 'Melbourne'),
        ('Kilmore', 'Kilmore'),
        ('Stawell', 'Stawell'),
        ('Shepparton', 'Shepparton'),
        ('Hamilton', 'Hamilton'),
    ]

    SECTION_CHOICES = [
        ('Section I', 'Section I'),
        ('Section II', 'Section II'),
        ('Section III', 'Section III'),
        ('Section IV', 'Section IV'),
        ('Section V', 'Section V'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='Section I')
    replenishment_threshold = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.item.name} - {self.location} - {self.section}"
    

from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(default='example@example.com')
    telephone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField()
    website = models.URLField(default='http://defaultwebsite.com')

    def __str__(self):
        return self.name

class Receiving(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity_received = models.PositiveIntegerField()
    received_by = models.CharField(max_length=255)
    received_date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    putaway_location = models.CharField(max_length=100, 
                                        choices=[('Melbourne', 'Melbourne'), 
                                                 ('Kilmore', 'Kilmore'), ('Stawell', 'Stawell'), 
                                                 ('Shepparton', 'Shepparton'), 
                                                 ('Hamilton', 'Hamilton')])
    putaway_section = models.CharField(
        max_length=255,
        choices=[
            ('Section I', 'Section I'),
            ('Section II', 'Section II'),
            ('Section III', 'Section III'),
            ('Section IV', 'Section IV'),
            ('Section V', 'Section V')
        ],
        null=True, blank=True
    )

    def __str__(self):
        return f"Received {self.item.name} on {self.received_date}"


from django.db import models

# class Putaway(models.Model):
#     received_item = models.ForeignKey(Receiving, on_delete=models.CASCADE)
#     location = models.CharField(max_length=50, choices=[
#         ('Melbourne', 'Melbourne'),
#         ('Kilmore', 'Kilmore'),
#         ('Stawell', 'Stawell'),
#         ('Shepparton', 'Shepparton'),
#         ('Hamilton', 'Hamilton')
#     ])
#     section = models.CharField(max_length=50, choices=[
#         ('Section I', 'Section I'),
#         ('Section II', 'Section II'),
#         ('Section III', 'Section III'),
#         ('Section IV', 'Section IV'),
#         ('Section V', 'Section V')
#     ])

#     def __str__(self):
#         return f'{self.received_item.item.name} - {self.location} - {self.section}'
    
from django.db import models

class Section(models.Model):
    LOCATION_CHOICES = [
        ('Melbourne', 'Melbourne'),
        ('Kilmore', 'Kilmore'),
        ('Stawell', 'Stawell'),
        ('Shepparton', 'Shepparton'),
        ('Hamilton', 'Hamilton'),
    ]
    SECTION_CHOICES = [
        ('Section I', 'Section I'),
        ('Section II', 'Section II'),
        ('Section III', 'Section III'),
        ('Section IV', 'Section IV'),
        ('Section V', 'Section V'),
    ]
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    section_name = models.CharField(max_length=50, choices=SECTION_CHOICES)

    def __str__(self):
        return f"{self.location} - {self.section_name}"


from django.db import models
from django.core.exceptions import ValidationError

class InternalTransfer(models.Model):
    LOCATION_CHOICES = [
        ('Melbourne', 'Melbourne'),
        ('Kilmore', 'Kilmore'),
        ('Stawell', 'Stawell'),
        ('Shepparton', 'Shepparton'),
        ('Hamilton', 'Hamilton'),
    ]

    SECTION_CHOICES = [
        ('Section I', 'Section I'),
        ('Section II', 'Section II'),
        ('Section III', 'Section III'),
        ('Section IV', 'Section IV'),
        ('Section V', 'Section V'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    source_section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='Select Section')
    destination_section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='Select Section')

    def clean(self):
        # Ensure that source and destination sections are within the same location
        if self.source_section == self.destination_section:
            raise ValidationError("Source and destination sections cannot be the same.")


from django.db import models
#from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    address = models.TextField(default='no adress added')
    website = models.URLField(default='https://www.example.com')

    def __str__(self):
        return self.name


from django.db import models
from datetime import date

from django.db import models
from django.utils.timezone import now

# class Order(models.Model):
#     default_item_id = 1  # Replace with a valid Item ID
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, default=default_item_id, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)
#     date = models.DateField(default=now)  # Automatically set to today's date
#     status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('shipped', 'Shipped')])

#     def save(self, *args, **kwargs):
#         # Update the inventory quantity when an order is made
#         inventory_item = Inventory.objects.get(item=self.item)
#         inventory_item.quantity -= self.quantity
#         inventory_item.save()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Order ID: {self.id} - Customer: {self.customer} - Item: {self.item} - Quantity: {self.quantity} - Date: {self.date}"

from django.core.exceptions import ValidationError

class Order(models.Model):
    LOCATION_CHOICES = [
        ('Melbourne', 'Melbourne'),
        ('Kilmore', 'Kilmore'),
        ('Stawell', 'Stawell'),
        ('Shepparton', 'Shepparton'),
        ('Hamilton', 'Hamilton'),
    ]

    SECTION_CHOICES = [
        ('Section I', 'Section I'),
        ('Section II', 'Section II'),
        ('Section III', 'Section III'),
        ('Section IV', 'Section IV'),
        ('Section V', 'Section V'),
    ]

    default_item_id = 1  # Replace with a valid Item ID
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, default=default_item_id, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateField(default=now)  # Automatically set to today's date
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('shipped', 'Shipped')])
    
    # New fields for Location and Section
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default="Select Location")
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, default="Select Section")

    def save(self, *args, **kwargs):
        # Update the inventory quantity when an order is made
        inventory_item = Inventory.objects.get(item=self.item, location=self.location, section=self.section)
        if inventory_item.quantity < 10:
            raise ValueError("Cannot place order: Not enough inventory in the specified location and section.")
        inventory_item.quantity -= self.quantity
        inventory_item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order ID: {self.id} - Customer: {self.customer} - Item: {self.item} - Quantity: {self.quantity} - Date: {self.date}"

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantity} of {self.item.name} in Order {self.order.id}"

class ShippingDetail(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    shipping_label = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Shipping details for Order {self.order.id}"
    
# from django.db import models
# from django.contrib.auth.models import User
# from .models import Order, Customer  # Import your Order and Customer models

# class Shipping(models.Model):
#     SHIPPING_STATUS_CHOICES = [
#         ('shipped', 'Shipped'),
#         ('delayed', 'Delayed'),
#     ]
    
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     shipping_address = models.CharField(max_length=255)
#     shipping_status = models.CharField(max_length=10, choices=SHIPPING_STATUS_CHOICES, default='shipped')
    
#     def __str__(self):
#         return f"Shipping for Order {self.order.id} - {self.shipping_status}"





