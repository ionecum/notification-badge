from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import NotifyModel as Notification
import asyncio

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        print(f"A new notification was created: {instance.message}")
        channel_layer = get_channel_layer()
        try:
            async def send_notification():
                await channel_layer.group_send(
                    'public_room',
                    {
                        "type": "update_notification_count",
                        "message": instance.message
                    }
                )

            # Llama a la función asíncrona para enviar la notificación
            asyncio.run(send_notification())
            
        except Exception as e:
            # Maneja errores de manera más robusta
            print(f"Error in group_send: {e}")
