from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "warmify_dashboard/index.html")


def reports(request):
    return render(request, "warmify_dashboard/reports.html")


def logs(request):
    return render(request, "warmify_dashboard/logs.html")


def settings(request):
    return render(request, "warmify_dashboard/settings.html")
