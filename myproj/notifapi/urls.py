from notifapi.views import process_json, show_results
from django.urls import path
from . import views

urlpatterns = [
    path('api/process-json/', process_json, name="process_json"),
    path('', show_results, name="show_results"),
    path('ws/wstest/', views.SimpleWebSocketTestView.as_view(), name='simple_ws_test'),
]