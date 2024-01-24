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
        await self.accept()
        # Fetch data from the api
        url = 'http://127.0.0.1:8000/api/process-json/'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle incoming messages (if any)
        pass
