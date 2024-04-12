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
        return list(NotifyModel.objects.all().order_by('-created_at').values('id','is_read','is_seen','message'))
    
    @database_sync_to_async
    def mark_all_db(self, kind):
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        notifications = NotifyModel.objects.all()
        for notification in notifications:
            if kind == "unseen":
                notification.is_seen = True
                #print(f"notificaiton {notification.id}  will be marked as seen")
            if kind == "unread":
                #print(f"notificaiton {notification.id}  will be marked as read")
                notification.is_read = True
            notification.save()
            #print(f"notification is seen is {notification.is_seen}")


    """
    This will mark just one notification as a read. The seen status is not supported in this case because
    it is not needed. 
    """
    @database_sync_to_async
    def mark_one_db(self, notification_id):
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        try:
            notification_to_set = NotifyModel.objects.get(pk=notification_id)
            notification_to_set.is_read = True
            notification_to_set.save()
        except NotifyModel.DoesNotExist:
            # debug only
            print("This notification does not exist")
            return False
        return True
        


    """ 
    Despite the confusing name, this method marks all the notification as seen, rather than unseen, which is
    correct. The incorrect name, it's because, at the beginning, this method was toggling the is_seen status
    for debugging purposes. 
    """
    async def mark_all_unseen(self):
        #print("Mark all unseen was called!")
        await self.mark_all_db("unseen")
        await self.update_notification_count()
        
    
    """
    This will mark all the notifications as read when the user click the link "Mark all as read"
    """
    async def mark_all_read(self):
        await self.mark_all_db("unread")
        await self.update_notification_count()
    

    async def mark_one_read(self, notification_id):
        print(f"Mark the notification id as read, the id is {notification_id}")
        await self.mark_one_db(notification_id)
        await self.update_notification_count()
        

    async def update_notification_count(self, event=None):
        notifications = await self.get_notifications()
        #print(notifications)
        # get notifications where is_seen is set to false
        unseen_values = [notification for notification in notifications if not notification['is_seen']]
        notification_count = len(unseen_values)        
        await self.send_notification_update(notification_count, notifications)
    
    
    async def send_notification_update(self, count, notifications):
        notifications_data = [{
            "id": notification['id'],
            "is_read": notification['is_read'],
            "message": notification['message']
        } for notification in notifications]

        await self.send(
            text_data=json.dumps({
                "type": "notification.update",
                "count": count,
                "notifications": notifications_data
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
            if message_type == 'mark.one.read':
                await self.mark_one_read(data.get('id'))
            if message_type == 'mark.all.read':
                await self.mark_all_read()
            
            await self.update_notification_count()


    async def send_error_message(self, error_message):
        await self.send(text_data=json.dumps({
            "type": "error",
            "message": error_message
        }))
