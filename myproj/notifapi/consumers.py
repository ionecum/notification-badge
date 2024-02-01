from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from django.core.serializers import serialize
import json
import logging
logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect method called") 
        # Allow all connections
        await self.accept()
        await self.channel_layer.group_send(
            "public_room",
            {
                "type": "update_notification_count",
                "event": "notification.update"
            }
        )
    
    async def update_notification_count(self, event):
        print("update_notification_count called")  # Check if method is called
        await self.send(text_data="Notification count updated")
        notification_count = apps.NotifyModel.objects.all().count()
        
        print(f"Notification count is {notification_count}")
        # Send the updated count to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "notification.update",
            "event": "notification.update",
            "count": notification_count
    }))
        
    async def disconnect(self, close_code):
        print("Consumer disconnected")
        # Remove the channel from the public_room group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            "public_room",
            self.channel_name
        )
    

    async def send_notification_update(self, event):
        # Method for handling new notification updates sent by the signal
        # Send the new notification data to the WebSocket client
        notification_count = apps.NotifyModel.objects.all().count()
        
        print(f"Notification count is {notification_count}")
        
        await self.send(text_data=json.dumps({
            "type": "notification.update",
            "event": "notification.update",
            "count": notification_count
        }))

    async def receive(self, text_data):
        # Handle incoming messages (if any)
        print(f"Received event: {text_data}")
        data = json.loads(text_data)
        if data['type'] == 'update.notification.count':
            await self.update_notification_count(data)
    
