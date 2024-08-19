from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from inventory.models import Inventory

class Command(BaseCommand):
    help = 'Check inventory levels and trigger replenishment'

    def handle(self, *args, **kwargs):
        items_below_threshold = Inventory.objects.filter(quantity__lte=models.F('replenishment_threshold'))
        
        if items_below_threshold.exists():
            # Prepare email content
            item_details = '\n'.join([f'Item: {item.item.name}, Quantity: {item.quantity}, Replenishment Threshold: {item.replenishment_threshold}' for item in items_below_threshold])
            subject = 'Inventory Replenishment Needed'
            message = f'The following items need replenishment:\n\n{item_details}\n\nPlease take the necessary action to order more stock.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.ADMIN_EMAIL]  # Assuming ADMIN_EMAIL is configured in settings

            # Send email
            send_mail(subject, message, from_email, recipient_list)
            
            self.stdout.write(self.style.SUCCESS('Replenishment email sent to admin.'))
        else:
            self.stdout.write(self.style.SUCCESS('No items need replenishment.'))
