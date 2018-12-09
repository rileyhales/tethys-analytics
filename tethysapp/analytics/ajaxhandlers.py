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
