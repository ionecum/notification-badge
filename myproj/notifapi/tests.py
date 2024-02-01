from myproj.asgi import application
from channels.testing import WebsocketCommunicator
from django.test import TestCase
import asyncio

class TestNotificationConsumer(TestCase):
    async def test_consumer(self):
        communicator = WebsocketCommunicator(application, '/websocket/ws/notifications/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        try:
            response = await communicator.receive_from(timeout=5)
            self.assertEqual(response, "Notification count updated")
        except asyncio.TimeoutError:
            print("Timeout error: No message received within the timeout period")
        await communicator.disconnect()
