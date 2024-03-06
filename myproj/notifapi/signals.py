from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import NotifyModel as Notification
import asyncio

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    
    if created:
        print(f"A new notification was created {instance.message}")
        channel_layer = get_channel_layer()
        print(channel_layer)
        try:
            async_to_sync(channel_layer.group_send)(
                'public_room',
                {
                    "type":"update_notification_count",
                    "message":instance.message
                }
            )
            """ 
            async def send_notification():
                await channel_layer.send("public_room", {
                    # OJO, update_notification_count nunca es llamada
                    # ese es el verdadero problema. Solo es llamada después
                    # de refrescar con F5
                    "type": "update_notification_count",
                    "message": instance.message
                }) """

            # Call the async function to send the notification
            #async_to_sync(send_notification)()
            
        except Exception as e:
            print(f"Error in group_send: {e}")

