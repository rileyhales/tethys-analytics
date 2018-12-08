from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tools import applist, generate_app_urls, check_portal_analytics
from model import lonlat_list

check_portal_analytics()
lonlat_list()

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    context = {
        'urls': generate_app_urls(request, applist()),
    }

    return render(request, 'analytics/home.html', context)


@login_required()
def config(request):
    """
    Controller for the configuration instructions page
    """

    context = {
        'urls': generate_app_urls(request, applist()),
    }

    return render(request, 'analytics/config.html', context)


@login_required()
def app_template(request, name):
    """
    Controller for the page that shows app specific data. This controller:
    0. Clears data that would have been put into divs during previous renders
    1. figures out what page you're on
    2. Filters out the appropriate GA data for that page
    3. puts that data into the raw_stats div
    4. gets the urls for the navigation links on the left column like every page needs to
    """
    # set the name and url maps for the page which are passed to the context
    apps = applist()    # a dictionary from tools.py of the form {'full app name': 'app package name'}
    for app in apps:
        if apps[app] == name:   # if the full app name corresponds to the package name from the urls
            name = app          # change the name from package to full name.

    context = {
        'urls': generate_app_urls(request, applist()),
        'name': name,
    }

    return render(request, 'analytics/app_stats_template.html', context)
