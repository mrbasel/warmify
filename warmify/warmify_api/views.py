from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from warmify_core.models import IotDevice, Event, Ping
from warmify_core.schedules import get_schedule
from warmify_core.tasks import check_heater_is_working, alert_empty_tank


@csrf_exempt
def health(request):
    return JsonResponse({"message": "PONG"})


@csrf_exempt
@require_http_methods(["POST"])
def log_event(request):
    try:
        data = json.loads(request.body)

        if "token" not in data or "timestamp" not in data:
            return JsonResponse({"message": "missing data"}, status=400)

        token = data.get("token")
        timestamp = data.get("timestamp")
        device = IotDevice.objects.filter(token=token).first()

        if not device:
            return JsonResponse({"message": "invalid token"}, status=400)
        e = Event(timestamp=timestamp, device=device)
        e.save()
        return JsonResponse({"message": "success"}, status=201)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "invalid payload"}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def ping(request):
    try:
        data = json.loads(request.body)
        if "token" not in data:
            return JsonResponse({"message": "missing token"}, status=401)

        token = data.get("token")
        filtered_devices = IotDevice.objects.filter(token=token)
        if len(filtered_devices) < 1:
            return JsonResponse({"message": "invalid token"}, status=400)
        device = filtered_devices[0]
        ping_event = Ping(device=device)
        if "controller_temperature" in data:
            ping_event.recorded_controller_temperature = data.get(
                "controller_temperature"
            )
        if "waterlevel" in data:
            ping_event.recorded_waterlevel = data.get("waterlevel")
            if ping_event.recorded_waterlevel == 0:
                alert_empty_tank.apply_async((device.id,))

        if "recorded_heater_temperature" in data:
            ping_event.recorded_heater_temperature = data.get(
                "recorded_heater_temperature"
            )

        if "is_on_heater" in data:
            ping_event.is_on_heater = data.get("is_on_heater")

        last_ping = Ping.get_last_ping(device.id)
        # Check if the heater turned on now
        if last_ping.is_on_heater == False and ping_event.is_on_heater == True:
            check_heater_is_working.apply_async((device.id,), countdown=30)

        ping_event.save()

        return JsonResponse({"message": "success"}, status=201)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "something went wrong.."}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_heater_status(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    device = IotDevice.objects.filter(token=token).first()
    if not token or not device:
        return JsonResponse({"message": "invalid token"}, status=400)

    current_datetime = datetime.now()
    schedule = get_schedule(device.id)
    should_turn_on_heater = False
    if schedule[current_datetime.hour]:
        should_turn_on_heater = True

    return JsonResponse({"status": should_turn_on_heater})
