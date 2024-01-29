from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import JsonResponse
import urllib.request
import json

class SimpleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Allow all connections
        await self.channel_layer.group_add(
            "public_room",
            self.channel_name
        )
        await self.accept()
        # Fetch data from the api
        

    async def disconnect(self, close_code):
        # Remove the channel from the public_room group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            "public_room",
            self.channel_name
        )
    

    async def send_notification_update(self, event):
        # Method for handling new notification updates sent by the signal
        # Send the new notification data to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "notification.update",
            "message": event["message"]
        }))

    async def receive(self, text_data):
        # Handle incoming messages (if any)
        pass

