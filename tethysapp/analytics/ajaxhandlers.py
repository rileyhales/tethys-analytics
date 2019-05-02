from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .googleAnalytics import GAstats
from .tools import applist

import ast


@login_required()
def get_applist(request):
    """
    controller for sending the list of apps to javascript using the applist from tools.py
    """
    return JsonResponse(applist())


@login_required()
def requester(request):
    """
    ajax controller for sending analytics results to the custom request composer page
    """
    import pprint
    body = ast.literal_eval(request.body.decode('UTF-8'))       # gets the list of selected metrics/dimensions

    selections = body['metrics']                # combines the metrics and dimensions into a single list
    dimensions = body['dimensions']
    for i in range(len(dimensions)):
        selections.append(dimensions[i])
    pprint.pprint(selections)

    results = GAstats(selections)               # gets the analytics data for those choices

    return JsonResponse(results)


@login_required()
def appstats(name):
    """
    controller for getting stats on the individual app pages.
    """
    data = {
        'users': 0,
        'sessions': 0,
        'avgSessionDuration': 0,
    }

    results = GAstats(['ga:users', 'ga:sessions', 'ga:avgSessionDuration', 'ga:pagePath'])
    results = results.get('reports', [])[0]['data']['rows']
    for i in range(len(results)):
        if '/apps/' + name in results[i]['dimensions'][0]:
            data['users'] += float(results[i]['metrics'][0]['values'][0])
            data['sessions'] += float(results[i]['metrics'][0]['values'][1])
            data['avgSessionDuration'] += float(results[i]['metrics'][0]['values'][2])/60

    print(data)

    return data


@login_required()
def apptchart(name):
    """
    A controller for getting the timeseries chart of an individual app's usage
    """

    import pprint
    timeusers = ['filler information to see if the highchart div gets read correctly']
    data = {}

    results = GAstats(['ga:users', 'ga:date', 'ga:pagePath'])
    results = results.get('reports', [])[0]['data']['rows']
    pprint.pprint(results)
    # for entry in results:
    #     timeusers.append([entry['dimensions'][0], entry['metrics'][0]['values'][0]])
    data['timeusers'] = timeusers

    return data


@login_required()
def app_page(request):
    """
    The controller that gets called when you open a stats view page for an app
    1. it takes the url of the page its on, divides it up, and takes the 2nd to last entry (which contains the name of
        the app). It then finds which app in the applist that corresponds to and keeps that value.
    2. Calls the functions for getting stats on various parts of the page
    3. Query analytics based on the specified list, filter the results based on the page path using the name from step
        1, fill the data dictionary, and return it as a json response.
    """
    url = ast.literal_eval(request.body.decode('UTF-8'))['url']
    substring = url.split('/')
    apps = applist()
    name = ''
    for app in apps:
        if substring[len(substring) - 2] in apps[app]:
            name = substring[len(substring) - 2]

    appstats(name)
    data.update(apptchart(name))

    return JsonResponse(data)
