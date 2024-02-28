# yourapp/management/commands/send_notification_update.py

from django.core.management.base import BaseCommand
from notifapi.consumers import send_notification_update_to_clients

class Command(BaseCommand):
    help = 'Send notification update to WebSocket clients'

    def handle(self, *args, **options):
        send_notification_update_to_clients()
