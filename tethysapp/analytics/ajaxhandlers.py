from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from googleAnalytics import GAstats
from tools import applist

import ast


@login_required()
def get_applist(request):
    apps = applist()
    return JsonResponse(apps)


def requester(request):
    body = ast.literal_eval(request.body)

    selections = []
    metrics = body['metrics']
    dimensions = body['dimensions']

    for i in range(len(metrics)):
        selections.append(metrics[i])
    for i in range(len(dimensions)):
        selections.append(dimensions[i])

    results = GAstats(selections)

    return JsonResponse(results)


def appstats(request):
    url = ast.literal_eval(request.body)['url']
    substring = url.split('/')
    apps = applist()

    for app in apps:
        if substring[len(substring) - 2] in apps[app]:
            name = substring[len(substring) - 2]

    data = {
        'users': 0,
        'users7': 0,
        'users28': 0,
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

    # results = GAstats(['ga:7dayUsers', 'ga:pagePath'])
    # results = results.get('reports', [])[0]['data']['rows']
    # for i in range(len(results)):
    #     if '/apps/analytics' in results[i]['dimensions'][0]:
    #         data['users7'] += float(results[i]['metrics'][0]['values'][0])
    #
    # results = GAstats(['ga:28dayUsers', 'ga:pagePath']).get('reports', [])[0]['data']['rows']
    # for i in range(len(results)):
    #     if '/apps/analytics' in results[i]['dimensions'][0]:
    #         data['users28'] += float(results[i]['metrics'][0]['values'][0])

    return JsonResponse(data)
