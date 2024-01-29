from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import NotifyModel as Notification

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification_update",
                "message": instance.message
            }
        )