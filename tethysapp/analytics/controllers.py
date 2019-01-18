from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput

from .tools import applist, generate_app_urls, check_portal_analytics, supportedMetricsDimensions
from .model import lonlat_list

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
def requester(request):
    """
    Controller for the API requester page
    """

    metrics = []
    dimensions = []
    supported = supportedMetricsDimensions()
    for i in range(len(supported['metrics'])):
        name = supported['metrics'][i].replace('ga:', '').capitalize()
        newtuple = (name, supported['metrics'][i])
        metrics.append(newtuple)
    for i in range(len(supported['dimensions'])):
        name = supported['dimensions'][i].replace('ga:', '').capitalize()
        newtuple = (name, supported['dimensions'][i])
        dimensions.append(newtuple)

    metrics = SelectInput(
        display_text='Supported Metrics',
        name='metrics',
        multiple=True,
        original=False,
        options=metrics,
    )

    dimensions = SelectInput(
        display_text='Supported Dimensions',
        name='dimensions',
        multiple=True,
        original=False,
        options=dimensions,
    )

    context = {
        'urls': generate_app_urls(request, applist()),
        'metrics': metrics,
        'dimensions': dimensions,
    }

    return render(request, 'analytics/requester.html', context)


@login_required()
def app_template(request, name):
    """
    Controller for the page that shows app specific data.
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
