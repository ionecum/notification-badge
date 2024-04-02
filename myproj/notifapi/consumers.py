from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from channels.db import database_sync_to_async
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    """ def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_refresh_notification_count = False """
    
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
        return list(NotifyModel.objects.all().values('id','is_read','is_seen','message'))
    
    @database_sync_to_async
    def mark_all_db(self, kind):
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        notifications = NotifyModel.objects.all()
        for notification in notifications:
            if kind is "unseen":
                notification.is_seen = True
                #print(f"notificaiton {notification.id}  will be marked as seen")
            if kind is "seen": # debug only
                print(f"notificaiton {notification.id} supposed to be marked as unread")
                notification.is_seen = False # debug only
            if kind is "unread":
                print(f"notificaiton {notification.id}  will be marked as read")
            notification.save()
            print(f"notification is seen is {notification.is_seen}")


    async def mark_all_unseen(self):
        print("Mark all unseen was called!")
        await self.mark_all_db("seen")
        
    
    async def update_notification_count(self, event=None):
        notifications = await self.get_notifications()
        print(notifications)
        is_seen_values = [notification for notification in notifications if not notification['is_seen']]
        notification_count = len(is_seen_values)
        print(f"Unseen notification count is {notification_count}")
        is_read_values = [notification['is_read'] for notification in notifications]
        messages_values = [notification['message'] for notification in notifications]
        
        await self.send_notification_update(notification_count, is_seen_values, is_read_values, messages_values)
    
    
    async def send_notification_update(self, count, is_seen_values, is_read_values, messages_values):
        await self.send(
            text_data=json.dumps({
                "type": "notification.update",
                "count": count,
                "is_read_values": is_read_values,
                "is_seen_values": is_seen_values,
                "messages_values": messages_values
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
            message_type = data.get('type')
            print(f"message type is: {message_type}")
        except json.JSONDecodeError as e:
            await self.send_error_message("Error decoding JSON: {}".format(e))
        else:
            if message_type == 'mark.all.unseen':
                await self.mark_all_unseen()
            
            await self.update_notification_count()


    async def send_error_message(self, error_message):
        await self.send(text_data=json.dumps({
            "type": "error",
            "message": error_message
        }))
