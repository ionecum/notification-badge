from django.db import models
from django.contrib.auth.models import User

class NotifyManager(models.Manager):
    def addNotification(self, type_relationship, person_from, person_to, redirect_to, message):
        """
        Add a new notification.

        Args:
            type_relationship (int): The type of relationship.
            person_from (User): The sender of the notification.
            person_to (User): The receiver of the notification.
            redirect_to (str): The URL to redirect to.
            message (str): The message of the notification.

        Returns:
            Notification: The created or existing notification object, or None if there was an error.
        """
        try:
            notification, created = self.get_or_create(
                sender=person_from,
                receiver=person_to,
                type=type_relationship,
                redirect_url=redirect_to,
                message=message
            )
            if not created and not notification.is_read:
                """ 
                if A and B is the same than
                if A:
                    if B:
                """
                notification.save()
            return notification
        except Exception as e:
            print(f"Error adding notification: {e}")
            return None


class NotifyModel(models.Model):
    class Meta:
        db_table = 'notifications'
    
    BLOCK = 0 # will be used only in activity log
    FAVORITE = 1
    TEASE = 2
    UPVOTE = 3
    DOWNVOTE = 4 # will be used only in activity log
    VISIT = 5
    MESSAGE = 6

    TYPE_CHOICES = [
        (BLOCK, 'Blocked'),
        (FAVORITE, 'Favorites'),
        (TEASE, 'Teased'),
        (UPVOTE, 'Upvoted'),
        (DOWNVOTE, 'Downvoted'),
        (VISIT, 'Visited'),
        (MESSAGE, 'Message'),
    ]

    """
    Blank values for Django field types such as DateTimeField or ForeignKey will be stored as NULL in the DB. blank determines whether the field will be required in forms.
    """
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    is_read = models.BooleanField(null=False, default=False)
    redirect_url = models.CharField(max_length=120, null=True)
    message = models.CharField(max_length=250, null=True)

    objects = NotifyManager()
