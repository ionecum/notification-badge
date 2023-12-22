from notifapi.views import process_json, show_results
from django.urls import path

urlpatterns = [
    path('api/process-json/', process_json, name="process_json"),
    path('', show_results, name="show_results"),
]