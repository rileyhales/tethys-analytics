from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from googleAnalytics import GAstats


@login_required()
def get_applist(request):
    from tools import applist
    apps = applist()
    return JsonResponse(apps)


def analytics(request):
    stats = GAstats(['ga:pagePath'])
    return JsonResponse(stats)