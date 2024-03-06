from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from asgiref.sync import sync_to_async, async_to_sync
import json
from channels.layers import get_channel_layer
import asyncio


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
        """ Sends a notification to the client by converting the event data (a dictionary) to a JSON string and sending it as text data through the WebSocket connection. """
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
        await self.update_notification_count(data)


# this function is just for test, but it does not work
def send_notification_update_to_clients():
    channel_layer = get_channel_layer()
    notification_count = 10  # Example notification count
    is_read_values = [False, True, False]  # Example list of read statuses
    messages_values = ["New message 1", "New message 2", "New message 3"]  # Example list of messages

    async_to_sync(channel_layer.send)(
        "public_room",
        {
            "type": "send.notification.update",
            "count": notification_count,
            "is_read_values": is_read_values,
            "messages_values": messages_values
        }
    )