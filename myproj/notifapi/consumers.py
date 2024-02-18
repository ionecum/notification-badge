from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from django.core.serializers import serialize
from asgiref.sync import sync_to_async
import json
import logging
logger = logging.getLogger(__name__)

"""
LESSON TO TAKE HOME:
Asynchronous Context: When working with Django Channels or any asynchronous framework, be mindful of the context in which your code is executing. Synchronous database operations should be handled appropriately within asynchronous code.The sync_to_async utility provided by Django's django.db 
module allows to convert synchronous database operations into asynchronous ones, enabling smooth integration with asynchronous code.
"""
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Allow all connections
        await self.accept()
        await self.update_notification_count()

    
    async def update_notification_count(self):
        """
        Using apps.get_model ensures that we are accessing the model without encountering import issues within the consumer. Importing a model directly within a consumer may result in circular imports, leading to potential issues within the Django Channels application.
        """
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        notification_count = await sync_to_async(NotifyModel.objects.all().count)()
        # Send the updated count to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "notification.update",
            "count": notification_count
    }))
        
    async def disconnect(self, close_code):
        print("Consumer disconnected")
        # Remove the channel from the public_room group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            "public_room",
            self.channel_name
        )
    
    """
    The following method is necessary because it is called by a signal
    """
    async def send_notification_update(self):
        # Method for handling new notification updates sent by the signal
        # Send the new notification data to the WebSocket client
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        notification_count = NotifyModel.objects.all().count()
        
        print(f"Notification count is {notification_count}")
        
        await self.send(text_data=json.dumps({
            "type": "notification.update",
            "count": notification_count
        }))

    async def receive(self, text_data):
        # Handle incoming messages (if any)
        print(f"Received event: {text_data}")
        data = json.loads(text_data)
        if data['type'] == 'update.notification.count':
            await self.update_notification_count(data)
    
