from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    context = {}

    return render(request, 'analytics/home.html', context)

@login_required()
def config(request):
    """
    Controller for the configuration instructions page
    """

    context = {}

    return render(request, 'analytics/config.html', context)