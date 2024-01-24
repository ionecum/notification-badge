from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class NotifyManager(models.Manager):
    def addNotification(self, typerel, person_from, person_to, redirect_to, msg):
        # created specify if the object is created or not
        (notification, created) = NotifyModel.objects.get_or_create(
            sender_id=person_from,
            receiver_id=person_to,
            type=typerel,
            redirect_url=redirect_to,
            message=msg
        )
        if created is False: # object exists
            if notification.is_read is False:
                # if the notification already exists, update the date
                notification.created_at = datetime.now()
                notification.save()
        return notification


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
        (BLOCK, 'blocked'),
        (FAVORITE, 'favorites'),
        (TEASE, 'teased'),
        (UPVOTE, 'upvoted'),
        (DOWNVOTE, 'downvoted'),
        (VISIT, 'visited'),
        (MESSAGE, 'message'),
    ]

    """
    Blank values for Django field types such as DateTimeField or ForeignKey will be stored as NULL in the DB. blank determines whether the field will be required in forms.
    """
    sender_id = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE, null=True)
    receiver_id = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)
    type = models.PositiveSmallIntegerField()
    is_read = models.BooleanField(null=False, default=False)
    redirect_url = models.CharField(max_length=120, null=True)
    message = models.CharField(max_length=250, null=True)

    objects = NotifyManager()
