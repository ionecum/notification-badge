from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.load_profile, name='load-profile'),
]