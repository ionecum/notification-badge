from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProfileModel(models.Model):
    class Meta:
        db_table = 'profiles'
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    personal_ad = models.TextField(max_length=2000, blank=True)

