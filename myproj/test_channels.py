import channels.layers
from asgiref.sync import async_to_sync

channel_layer = channels.layers.get_channel_layer()
print("Channel layer:", channel_layer)

print("Sending message to test_channel")
async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})

print("Receiving message from test_channel")
message = async_to_sync(channel_layer.receive)('test_channel')
print("Received message:", message)