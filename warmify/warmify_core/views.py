from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import IotDevice, Event
from .utils import get_schedule

def ping(request):
    return JsonResponse({'message': 'PONG'})

@csrf_exempt
@require_http_methods(['POST'])
def log_event(request):
    try:
        data = json.loads(request.body)

        if 'token' not in data or 'timestamp' not in data:
            return JsonResponse({'message': 'missing data'}, status=400) 

        token = data.get('token')
        timestamp = data.get('timestamp')
        device = IotDevice.objects.filter(token=token).first()

        if not device: 
            return JsonResponse({'message': 'invalid token'}, status=400)
        e = Event(timestamp=timestamp, device=device)
        e.save()
        return JsonResponse({'message': 'success'}, status=201)

    except Exception as e:
        print(e)
        return JsonResponse({'message': 'invalid payload'}, status=400)

@csrf_exempt
@require_http_methods(['GET'])
def schedule(request):
    token = request.META.get("HTTP_X_API_KEY") 
    device = IotDevice.objects.filter(token=token).first()
    if not token or not device:
        return JsonResponse({'message': 'invalid token'}, status=400)

    schedule = get_schedule(device.id)

    return JsonResponse({'data': schedule})

