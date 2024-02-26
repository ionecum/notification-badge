from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import NotifyModel as Notification


@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    try:
        if created:
            print(f"A new notification was created {instance.message}")
            channel_layer = get_channel_layer()
            database_sync_to_async(channel_layer.group_send)(
                "public_room",
                {
                    "type": "update_notification_count",
                    "message": instance.message
                }
            )
    except Exception as e:
        print(f"Error in group_send: {e}")

