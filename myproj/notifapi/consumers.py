from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from django.core.serializers import serialize
from asgiref.sync import sync_to_async
import json
import logging

"""
LESSON TO TAKE HOME:
Asynchronous Context: When working with Django Channels or any asynchronous framework, be mindful of the context in which your code is executing. Synchronous database operations should be handled appropriately within asynchronous code.The sync_to_async utility provided by Django's django.db 
module allows to convert synchronous database operations into asynchronous ones, enabling smooth integration with asynchronous code.
"""
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Allow all connections
        await self.channel_layer.group_add("public_room", self.channel_name)
        await self.accept()
        await self.update_notification_count()

    
    async def update_notification_count(self, event=None):
        print("update_notification_count method called with event:", event)
        # you can't use a model directly from a consumer
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        notifications = await sync_to_async(list)(NotifyModel.objects.all().values('is_read'))
        messages = await sync_to_async(list)(NotifyModel.objects.all().values('message'))
        # Get the notification count asynchronously using a custom utility method
        notification_count = len(notifications)
        
        
        #print(f"Notification count is {notification_count}")
        # Extracting is_read values from notifications
        is_read_values = [notification['is_read'] for notification in notifications]
        messages_values = [notification['message'] for notification in messages]
        #print("Am I here?")
        print(f"Messages values are: {messages_values}")
        await self.send(text_data=json.dumps({
            "type": "notification.update",
            "count": notification_count,
            "is_read_values": is_read_values,
            "messages_values": messages_values
        }))

        
    async def disconnect(self, close_code):
        print("Consumer disconnected")
        # Remove the channel from the public_room group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            "public_room",
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages (if any)
        data = json.loads(text_data)
        if data['type'] == 'update.notification.count':
            await self.update_notification_count()
