from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tools import applist, generate_app_urls


@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    apps = applist()
    urls = generate_app_urls(request, apps)

    context = {
        'urls': urls,
    }

    return render(request, 'analytics/home.html', context)


@login_required()
def config(request):
    """
    Controller for the configuration instructions page
    """

    apps = applist()
    urls = generate_app_urls(request, apps)

    context = {
        'urls': urls,
    }

    return render(request, 'analytics/config.html', context)


def app_template(request, name):
    """
    Controller for the page that shows app specific data. This controller:
    0. Clears data that would have been put into divs during previous renders
    1. figures out what page you're on
    2. Filters out the appropriate GA data for that page
    3. puts that data into the raw_stats div
    4. gets the urls for the navigation links on the left column like every page needs to
    """

    apps = applist()
    urls = generate_app_urls(request, apps)

    context = {
        'urls': urls,
    }

    return render(request, 'analytics/app_stats_template.html', context)
