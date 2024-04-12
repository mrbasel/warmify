from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, "warmify_dashboard/index.html")


@login_required
def reports(request):
    return render(request, "warmify_dashboard/reports.html")


@login_required
def logs(request):
    return render(request, "warmify_dashboard/logs.html")


@login_required
def settings(request):
    return render(request, "warmify_dashboard/settings.html")
