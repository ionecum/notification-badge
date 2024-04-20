from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import NotifyModel as Notification
import asyncio

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:        
        channel_layer = get_channel_layer()
        group_name = None
        if instance.type == 2:
            group_name = 'tease_room'
        if instance.type == 5:
            group_name = 'visit_room'
        if instance.type == 6:
            group_name = 'message_room'
        else:
            group_name = 'public_room'

        try:
            async def send_notification():
                await channel_layer.group_send(
                    group_name,
                    {
                        "type": "update.notification.on.signal",
                        "notificationType": instance.type,
                        "message": instance.message
                    }
                )

            # Llama a la función asíncrona para enviar la notificación
            asyncio.run(send_notification())
            
        except Exception as e:
            # Maneja errores de manera más robusta
            print(f"Error in group_send: {e}")
