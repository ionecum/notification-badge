from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
import os, json

def process_json(request):
    file_path = os.path.join(settings.BASE_DIR, "static/notifications_filtered.json")
    with open(file_path, 'r', encoding='utf-8') as file:
        #json.load can't be used, because there are multiple objects in the json
        #json_data = json.load(file)
        json_data = [json.loads(line) for line in file]
    
    # Convert the JSON data to JSON format (essentially making a copy here)
    json_response = json.dumps(json_data)

    return HttpResponse(json_response, content_type='application/json; charset=utf-8')


def show_results(request):
    return render(request, "notifapi/demo.html")


class SimpleWebSocketTestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'notifapi/simple_ws_test.html')

