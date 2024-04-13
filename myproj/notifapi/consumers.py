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
    Get a list of notifications from database. kind is a filter allowing to restrict the query
    to certain type of notification only, for example only visits. So, to get only notifications
    about visits, just pass 'VISIT' to it, to get only notifications about teases, just pass
    'TEASE' to it.
    """
    @database_sync_to_async
    def get_notifications(self,kind=None):
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        queryset = NotifyModel.objects.all().order_by('-created_at')
        if kind is not None:
            queryset = queryset.filter(type=getattr(NotifyModel, kind, None))
        
        return list(queryset.values('id','is_read','is_seen','message','type'))


    """
    This functions will mark all the notifications to read or seen, depending of the what
    parameter. Like the previous function, it also accept a kind to restrict the span of 
    the action to only one type of notification. For example, pass 'VISIT' to it if you
    want to mark all the notifications about visits as unread or unseen.
    """
    @database_sync_to_async
    def mark_all_db(self, what, kind=None):
        NotifyModel = apps.get_model('notifapi', 'NotifyModel')
        queryset = NotifyModel.objects.all()
        if kind is not None:
            queryset = queryset.filter(type=getattr(NotifyModel, kind, None))

        for notification in queryset:
            if what == "unseen":
                notification.is_seen = True
                #print(f"notificaiton {notification.id}  will be marked as seen")
            if what == "unread":
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
    Mark all the notifications as seen.
    """
    async def mark_all_seen(self):
        # pass an extra parameter, for example 'VISIT' to reduce the action to visits only
        await self.mark_all_db("unseen")
        await self.update_notification_count()
        
    
    """
    This will mark all the notifications as read when the user click the link "Mark all as read"
    """
    async def mark_all_read(self):
        # pass an extra parameter, for example 'VISIT' to reduce the action to visits only
        await self.mark_all_db("unread")
        await self.update_notification_list()
    

    async def mark_one_read(self, notification_id):
        print(f"Mark the notification id as read, the id is {notification_id}")
        await self.mark_one_db(notification_id)
        await self.update_notification_list()
        

    """
    This function only updates the list of notification without updating the unseen notifications counter.
    """
    async def update_notification_list(self, event=None):
        notifications = await self.get_notifications()
        notification_data = [{
            "id": notification['id'],
            "is_read": notification['is_read'],
            "message": notification['message']
        } for notification in notifications]
        
        await self.send(
            text_data=json.dumps({
                "type": "notification.update",
                "notifications": notification_data
            })
        )

    """
    This function updates the notification list and also updates the unseen counter.
    """
    async def update_notification_count(self, event=None):
        # pass 'VISIT' to delimit the notifications to visits only for example
        notifications = await self.get_notifications()
        #print(notifications)
        # get notifications where is_seen is set to false
        unseen_values = [notification for notification in notifications if not notification['is_seen']]
        notification_count = len(unseen_values)
        notification_data = [{
            "id": notification['id'],
            "is_read": notification['is_read'],
            "message": notification['message']
        } for notification in notifications]

        await self.send_notification_update(notification_count, notification_data)
    
    
    async def send_notification_update(self, count, notification_data):
        await self.send(
            text_data=json.dumps({
                "type": "notification.update",
                "count": count,
                "notifications": notification_data
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
            if message_type == 'mark.all.seen':
                await self.mark_all_seen()
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
