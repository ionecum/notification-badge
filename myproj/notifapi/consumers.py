from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from channels.db import database_sync_to_async
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Websocket consumer for handling notifications.
    """
    async def connect(self):
        await self.channel_layer.group_add("public_room", self.channel_name)
        await self.accept()
        await self.update_notification_count()

    """
    Unique source to update notifications from database
    """
    @database_sync_to_async
    def get_notifications(self):
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        return list(NotifyModel.objects.all().values('is_read', 'message'))
    

    async def update_notification_count(self, event=None):
        notifications = await self.get_notifications()
        print(notifications)
        notification_count = len(notifications)
        is_read_values = [notification['is_read'] for notification in notifications]
        messages_values = [notification['message'] for notification in notifications]

        await self.send_notification_update(notification_count, is_read_values, messages_values)
    
    
    async def send_notification_update(self, count, is_read_values, messages_values):
        await self.send(
            text_data=json.dumps({
                "type": "notification.update",
                "count": count,
                "is_read_values": is_read_values,
            })
        )
        
    async def disconnect(self, close_code):
        # Remove the channel from the public_room group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            "public_room",
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
            await self.send_error_message("Error decoding JSON: {}".format(e))
        else:
            await self.update_notification_count()


    async def send_error_message(self, error_message):
        await self.send(text_data=json.dumps({
            "type": "error",
            "message": error_message
        }))
